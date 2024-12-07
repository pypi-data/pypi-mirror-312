import io
import json
import logging
import os
import typing as t
import uuid
from pathlib import Path
from typing import Any

from botocore.client import BaseClient
from localstack.aws.api import (
    RequestContext,
    ServiceRequest,
)
from localstack.aws.api.dynamodbstreams import TableName
from localstack.aws.api.events import PutEventsRequestEntry, PutEventsResultEntryList
from localstack.aws.api.s3 import PutObjectRequest
from localstack.aws.api.sqs import Message
from localstack.aws.chain import HandlerChain
from localstack.aws.connect import InternalClientFactory
from localstack.aws.handlers.cors import ALLOWED_CORS_ORIGINS
from localstack.aws.handlers.service import ServiceRequestRouter
from localstack.config import is_in_docker
from localstack.extensions.patterns.webapp import WebAppExtension
from localstack.http import Response
from localstack.pro.core.services.iam.policy_engine.engine import IAMEnforcementEngine
from localstack.services.apigateway.next_gen.execute_api.context import RestApiInvocationContext
from localstack.services.apigateway.next_gen.execute_api.integrations.aws import (
    RestApiAwsProxyIntegration,
)
from localstack.services.dynamodb.models import RecordsMap
from localstack.services.dynamodb.provider import DynamoDBProvider, EventForwarder
from localstack.services.dynamodbstreams.dynamodbstreams_api import (
    _process_forwarded_records,
)
from localstack.services.events.models import FormattedEvent, Rule, TransformedEvent
from localstack.services.events.provider import LOG as EventsProviderLOG
from localstack.services.events.provider import (
    EventsProvider,
    extract_event_bus_name,
    extract_region_and_account_id,
)
from localstack.services.events.target import (
    TargetSender,
    transform_event_with_target_input_path,
)
from localstack.services.lambda_.api_utils import function_locators_from_arn
from localstack.services.lambda_.event_source_mapping.senders.lambda_sender import LambdaSender
from localstack.services.lambda_.invocation.lambda_service import LambdaService
from localstack.services.s3.notifications import S3EventNotificationContext
from localstack.services.s3.provider import S3Provider
from localstack.services.sns.models import SnsSubscription
from localstack.services.sns.publisher import (
    PublishDispatcher,
    SnsPublishContext,
)
from localstack.services.sqs.models import FifoQueue, StandardQueue
from localstack.utils.patch import Patch
from localstack.utils.strings import long_uid

from eventstudio.api.config import Config
from eventstudio.api.event_storage import EventStorageService
from eventstudio.api.event_streamer import EventStreamer
from eventstudio.api.logging_handler import EventStudioIAMCallback, EventStudioLogHandler
from eventstudio.api.types.errors import ErrorType, InputErrorModel
from eventstudio.api.types.events import InputEventModel
from eventstudio.api.types.services import ServiceName
from eventstudio.api.types.trace_context import TraceContext
from eventstudio.api.utils.tracing_utils import (
    extract_trace_context_from_context,
    get_trace_context,
    set_trace_context,
    submit_with_trace_context,
)
from eventstudio.api.utils.utils import (
    compile_regex_patterns,
    convert_raw_entry,
    load_apigateway_body,
    load_sqs_message_body,
    log_event_studio_error,
    pars_timestamp_ms,
)
from eventstudio.api.utils.xray_tracing_utils import (
    extract_aws_trace_header,
    extract_xray_trace_id_from_header_str,
    get_trace_context_from_esm_event,
)
from eventstudio.api.web import WebApp
from eventstudio.constants import INTERNAL_REQUEST_TRACE_HEADER

LOG = logging.getLogger(__name__)

IGNORE_EVENT_BRIDGE_DETAIL_TYPE_PATTERS = compile_regex_patterns([r"Parameter Store Change"])

IGNORE_BUCKET_PATTERNS = compile_regex_patterns([r"awslambda-.*-tasks"])

XRAY_TRACE_HEADER = "X-Amzn-Trace-Id"


class MyExtension(WebAppExtension):
    """IMPORTANT: always store copy of data from localstack not reference to avoid data corruption"""

    name = "eventstudio"

    def __init__(self):
        super().__init__(template_package_path=None)
        self.db_path = Config.DATABASE_PATH

        if not is_in_docker:
            ALLOWED_CORS_ORIGINS.append("http://127.0.0.1:3000")

        if is_in_docker:
            database_directory = Path("/var/lib/localstack/cache/extensions/eventstudio")
            if not database_directory.is_dir():
                database_directory.mkdir(parents=True)
            self.clear_db()  # make sure to clear db on startup if persistence is not enabled
            self.db_path = database_directory / Config.DATABASE_NAME

        self._event_streamer: EventStreamer = EventStreamer()
        self._event_storage_service: EventStorageService = EventStorageService(
            db_path=self.db_path, event_streamer=self._event_streamer
        )
        self._transformed_events: list[FormattedEvent | TransformedEvent] = []

    ############
    # APIGateway
    ############

    def _invoke_apigateway(self, fn, self_, context: RestApiInvocationContext, **kwargs) -> None:
        try:
            trace_context = get_trace_context()
            parent_id = trace_context.parent_id
            trace_id = trace_context.trace_id
            version = trace_context.version

            invocation_request = context.invocation_request.copy()
            api_name = context.deployment.rest_api.rest_api.get("name")
            invocation_request.pop("headers", None)  # TODO fix Json seralize headers
            body, body_type = load_apigateway_body(invocation_request.pop("body", None))
            if body_type == "BINARY":
                event_bytedata = body
                body = "<binary data>"
            else:
                event_bytedata = None

            input_event = InputEventModel(
                parent_id=parent_id,
                trace_id=trace_id,
                event_id=context.context_variables.get("requestId"),
                version=version,
                account_id=context.account_id,
                region=context.region,
                service=ServiceName.APIGATEWAY,
                operation_name="Input",
                is_replayable=True,
                event_data={
                    "body": body,
                    "request": invocation_request,
                },
                event_bytedata=event_bytedata,
                event_metadata={
                    "api_type": self_.name,
                    "api_name": api_name,
                    "deployment_id": context.deployment_id,
                    "stage_name": context.stage,
                    "request_type": "invocation",
                    "body_type": body_type,
                },
            )
            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            integration_request = context.integration_request.copy()
            integration_request.pop("headers", None)  # TODO fix Json seralize headers
            body, body_type = load_apigateway_body(integration_request.pop("body", None))
            if body_type == "BINARY":
                event_bytedata = body
                body = "<binary data>"
            else:
                event_bytedata = None

            input_event = InputEventModel(
                parent_id=span_id,
                trace_id=trace_id,
                event_id=context.context_variables.get("requestId"),
                version=version,
                account_id=context.account_id,
                region=context.region,
                service=ServiceName.APIGATEWAY,
                operation_name="Invoke",
                is_replayable=True,
                event_data={
                    "body": body,
                    "request": integration_request,
                },
                event_bytedata=event_bytedata,
                event_metadata={
                    "api_type": self_.name,
                    "api_name": api_name,
                    "deployment_id": context.deployment_id,
                    "stage_name": context.stage,
                    "request_type": "integration",
                    "body_type": body_type,
                },
            )
            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            # set new trace context for calling patched function
            new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
            set_trace_context(new_trace_context)

        except Exception as e:
            log_event_studio_error(
                logger=LOG, service=ServiceName.APIGATEWAY, operation="Invoke", error=str(e)
            )

        return fn(self_, context=context, **kwargs)

    ##########
    # DynamoDB
    ##########

    def _forward_request(
        self, fn, self_, context: RequestContext, service_request: ServiceRequest = None, **kwargs
    ) -> None:
        try:
            if context.service_operation.operation == "PutItem":
                trace_context = get_trace_context()
                parent_id = trace_context.parent_id
                trace_id = trace_context.trace_id
                version = trace_context.version

                input_event = InputEventModel(
                    parent_id=parent_id,
                    trace_id=trace_id,
                    event_id=context.request_id,
                    version=version,
                    account_id=context.account_id,
                    region=context.region,
                    service=ServiceName.DYNAMODB,
                    operation_name="PutItem",
                    is_replayable=True,
                    event_data={"item": context.service_request.get("Item")},
                    event_metadata={
                        "table_name": context.service_request.get("TableName"),
                        "operation": "PutItem",
                    },
                )
                span_id, trace_id = self._event_storage_service.add_event(
                    InputEventModel.model_validate(input_event)
                )

                # set new trace context for calling patched function
                new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
                set_trace_context(new_trace_context)

                # link xray trace id to new trace context # TODO necessary here?
                if xray_trace_header := extract_aws_trace_header(context.trace_context):
                    self._event_storage_service.store_xray_trace(
                        xray_trace_id=xray_trace_header.root, trace_context=new_trace_context
                    )

        except Exception as e:
            log_event_studio_error(
                logger=LOG, service=ServiceName.DYNAMODB, operation="PutItem", error=str(e)
            )

        return fn(self_, context=context, service_request=service_request, **kwargs)

    # Streams

    def _submit_records(
        self,
        fn,
        self_,
        account_id: str,
        region_name: str,
        records_map: RecordsMap,
    ):
        return submit_with_trace_context(
            self_.executor, self_._forward, account_id, region_name, records_map
        )

    def _patch_process_forwarded_event(
        self,
        fn,
        account_id: str,
        region_name: str,
        table_name: TableName,
        table_records: dict,
        kinesis,
        **kwargs,
    ) -> None:
        try:
            trace_context = get_trace_context()
            parent_id = trace_context.parent_id
            trace_id = trace_context.trace_id
            version = trace_context.version

            records = table_records["records"]
            stream_type = table_records["table_stream_type"]

            input_event = InputEventModel(
                parent_id=parent_id,
                trace_id=trace_id,
                event_id=records[0]["eventID"],
                version=version,
                account_id=account_id,
                region=region_name,
                service=ServiceName.DYNAMODB,
                operation_name="Forwarded Stream Records",
                is_replayable=False,
                event_data={"records": records},
                event_metadata={
                    "table_name": table_name,
                    "stream_type": stream_type.stream_view_type,
                },
            )
            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            # set new trace context for calling patched function
            new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
            set_trace_context(new_trace_context)

        except Exception as e:
            log_event_studio_error(
                logger=LOG,
                service=ServiceName.DYNAMODB,
                operation="Forwarded Stream Records",
                error=str(e),
            )

        return fn(
            account_id=account_id,
            region_name=region_name,
            table_name=table_name,
            table_records=table_records,
            kinesis=kinesis,
            **kwargs,
        )

    #############
    # EventBridge
    #############

    def _patch_process_entry(
        self,
        fn,
        self_,
        entry: PutEventsRequestEntry,
        processed_entries: PutEventsResultEntryList,
        failed_entry_count: dict[str, int],
        context: RequestContext,
        **kwargs,
    ) -> None:
        detail_type = entry.get("DetailType")
        if any(pattern.match(detail_type) for pattern in IGNORE_EVENT_BRIDGE_DETAIL_TYPE_PATTERS):
            # don't track specific writes
            return fn(self_, entry, processed_entries, failed_entry_count, context, **kwargs)

        trace_context = get_trace_context()
        parent_id = trace_context.parent_id
        trace_id = trace_context.trace_id
        version = trace_context.version

        entry_copy = entry.copy()
        event_bus_name_or_arn = entry_copy.get("EventBusName", "default")
        event_bus_name = extract_event_bus_name(event_bus_name_or_arn)
        region, account_id = extract_region_and_account_id(event_bus_name_or_arn, context)
        converted_entry = convert_raw_entry(entry_copy)
        input_event = InputEventModel(
            parent_id=parent_id,
            trace_id=trace_id,
            event_id=str(long_uid()),
            version=version,
            account_id=account_id,
            region=region,
            service=ServiceName.EVENTS,
            operation_name="Input",
            is_replayable=True,
            event_metadata={"event_bus_name": event_bus_name},
            event_data=converted_entry,
        )

        span_id, trace_id = self._event_storage_service.add_event(
            InputEventModel.model_validate(input_event)
        )

        # set new trace context for calling patched function
        new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
        set_trace_context(new_trace_context)

        fn(self_, entry, processed_entries, failed_entry_count, context, **kwargs)

        # internal step, restore trace context to input state
        input_trace_context = TraceContext(trace_id=trace_id, parent_id=parent_id, version=version)
        set_trace_context(input_trace_context)

    def _patch_proxy_capture_input_event(self, fn, self_, event: FormattedEvent, **kwargs) -> None:
        trace_context = get_trace_context()
        parent_id = trace_context.parent_id
        trace_id = trace_context.trace_id
        version = trace_context.version

        event_copy = event.copy()

        event_bus_name = event_copy.pop("event-bus-name")
        event_copy["detail_type"] = event_copy.pop(
            "detail-type", None
        )  # pydantic field alias for serialization does not work for validation

        input_event = InputEventModel(
            parent_id=parent_id,
            trace_id=trace_id,
            event_id=event_copy.pop("id"),
            version=version,
            account_id=event_copy.pop("account"),
            region=event_copy.pop("region"),
            service=ServiceName.EVENTS,
            operation_name="Converted",
            is_replayable=True,
            event_metadata={
                "event_bus_name": event_bus_name,
                "original_time": event_copy.pop("time"),
            },
            event_data=event_copy,
        )

        span_id, trace_id = self._event_storage_service.add_event(
            InputEventModel.model_validate(input_event)
        )

        # set new trace context for calling patched function
        new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
        set_trace_context(new_trace_context)

    def _patch_process_rules(
        self,
        fn,
        self_,
        rule: Rule,
        region: str,
        account_id: str,
        event_formatted: FormattedEvent,
        **kwargs,
    ) -> None:
        trace_context = get_trace_context()
        parent_id = trace_context.parent_id
        trace_id = trace_context.trace_id
        version = trace_context.version

        event_copy = event_formatted.copy()

        event_bus_name = event_copy.pop("event-bus-name")
        event_copy["detail_type"] = event_copy.pop(
            "detail-type", None
        )  # pydantic field alias for serialization does not work for validation

        input_event = InputEventModel(
            parent_id=parent_id,
            trace_id=trace_id,
            event_id=event_copy.pop("id"),
            version=version,
            account_id=event_copy.pop("account"),
            region=event_copy.pop("region"),
            service=ServiceName.EVENTS,
            operation_name="Match Rule",
            event_metadata={
                "event_bus_name": event_bus_name,
                "original_time": event_copy.pop("time"),
            },
            event_data=event_copy,
        )

        span_id, trace_id = self._event_storage_service.add_event(
            InputEventModel.model_validate(input_event)
        )

        # set new trace context for calling patched function
        new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
        set_trace_context(new_trace_context)

        fn(
            self_,
            rule,
            region,
            account_id,
            event_formatted,
            **kwargs,
        )

        # internal step, restore trace context to input state
        input_trace_context = TraceContext(trace_id=trace_id, parent_id=parent_id, version=version)
        set_trace_context(input_trace_context)

    def _process_event(self, fn, self_, event: FormattedEvent, **kwargs) -> None:
        trace_context = get_trace_context()
        parent_id = trace_context.parent_id
        trace_id = trace_context.trace_id
        version = trace_context.version

        event_copy = event.copy()

        event_bus_name = event_copy.pop("event-bus-name")
        event_copy["detail_type"] = event_copy.pop(
            "detail-type", None
        )  # pydantic field alias for serialization does not work for validation
        input_event = InputEventModel(
            parent_id=parent_id,
            trace_id=trace_id,
            event_id=event_copy.pop("id"),
            version=version,
            account_id=event_copy.pop("account"),
            region=event_copy.pop("region"),
            service=ServiceName.EVENTS,
            operation_name="Send to Target",
            event_metadata={
                "event_bus_name": event_bus_name,
                "replay_name": event_copy.get("replay-name", None),
                "original_time": event_copy.pop("time"),
            },
            event_data=event_copy,
        )
        span_id, trace_id = self._event_storage_service.add_event(
            InputEventModel.model_validate(input_event)
        )

        # capture input path transformation
        if input_path := self_.target.get("InputPath"):
            transformed_event = transform_event_with_target_input_path(input_path, event_copy)
            input_event = InputEventModel(
                parent_id=span_id,
                trace_id=trace_id,
                event_id=event_copy.pop("id"),
                version=version,
                account_id=event_copy.pop("account"),
                region=event_copy.pop("region"),
                service=ServiceName.EVENTS,
                operation_name="InputPathTransformation",
                event_metadata={
                    "event_bus_name": event_bus_name,
                    "replay_name": event_copy.get("replay-name", None),
                    "original_time": event_copy.pop("time"),
                },
                event_data=transformed_event,
            )
            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

        # capture input transformer transformation
        if input_transformer := self_.target.get("InputTransformer"):
            transformed_event = self_.transform_event_with_target_input_transformer(
                input_transformer, event_copy
            )
            input_event = InputEventModel(
                parent_id=span_id,
                trace_id=trace_id,
                event_id=event_copy.pop("id"),
                version=version,
                account_id=event_copy.pop("account"),
                region=event_copy.pop("region"),
                service=ServiceName.EVENTS,
                operation_name="InputTransformation",
                event_metadata={
                    "event_bus_name": event_bus_name,
                    "replay_name": event_copy.get("replay-name", None),
                    "original_time": event_copy.pop("time"),
                },
                event_data=transformed_event,
            )
            self._event_storage_service.add_event(InputEventModel.model_validate(input_event))

        # set new trace context for calling patched function
        new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
        set_trace_context(new_trace_context)

        fn(self_, event, **kwargs)

        # internal step, restore trace context to input state
        input_trace_context = TraceContext(trace_id=trace_id, parent_id=parent_id, version=version)
        set_trace_context(input_trace_context)

    ############
    # Lambda ESM
    ############

    # TODO step 1: capture message transformation
    # TODO step 2: capture filtering

    # step 3 invoke lambda - find event via event id
    def _send_events_to_lambda(self, fn, self_, events: list[dict] | dict, **kwargs) -> dict:
        # TODO deal with multiple events in batch
        try:
            trace_context = get_trace_context_from_esm_event(events[0], self._event_storage_service)
            parent_id = trace_context.parent_id
            trace_id = trace_context.trace_id
            version = trace_context.version

            function_name, _, account_id, region = function_locators_from_arn(self_.target_arn)
            payload = {"Records": events}

            input_event = InputEventModel(
                parent_id=parent_id,
                trace_id=trace_id,
                event_id=str(long_uid()),
                version=version,
                account_id=account_id,
                region=region,
                service=ServiceName.LAMBDA,
                operation_name="EventSourceMapping",
                is_replayable=True,
                event_data={"payload": payload},
                event_metadata={"function_name": function_name},
            )
            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            # set new trace context for calling patched function
            new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
            set_trace_context(new_trace_context)

        except Exception as e:
            log_event_studio_error(
                logger=LOG, service=ServiceName.LAMBDA, operation="EventSourceMapping", error=str(e)
            )

        return fn(self_, events=events, **kwargs)

    ########
    # Lambda
    ########

    def _invoke_lambda(
        self,
        fn,
        self_,
        region: str,
        account_id: str,
        request_id: str,
        payload: bytes | None,
        **kwargs,
    ) -> dict:
        try:
            trace_context = get_trace_context()
            parent_id = trace_context.parent_id
            trace_id = trace_context.trace_id
            version = trace_context.version

            parsed_payload = json.loads(payload)

            input_event = InputEventModel(
                parent_id=parent_id,
                trace_id=trace_id,
                event_id=request_id,
                version=version,
                account_id=account_id,
                region=region,
                service=ServiceName.LAMBDA,
                operation_name="Invoke",
                is_replayable=True,
                event_data={"payload": parsed_payload},
                event_metadata={"function_name": kwargs.get("function_name")},
            )
            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            # set new trace context for calling patched function
            new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
            set_trace_context(new_trace_context)

            # link xray trace id to new trace context
            if xray_trace_header := extract_aws_trace_header(kwargs["trace_context"]):
                self._event_storage_service.store_xray_trace(
                    xray_trace_id=xray_trace_header.root, trace_context=new_trace_context
                )

        except Exception as e:
            log_event_studio_error(
                logger=LOG, service=ServiceName.LAMBDA, operation="Invoke", error=str(e)
            )

        return fn(
            self_,
            payload=payload,
            region=region,
            account_id=account_id,
            request_id=request_id,
            **kwargs,
        )

    #####
    # SNS
    #####

    def _publish_to_topic(self, fn, self_, ctx: SnsPublishContext, topic_arn: str) -> dict:
        try:
            trace_context = get_trace_context()
            parent_id = trace_context.parent_id
            trace_id = trace_context.trace_id
            version = trace_context.version

            message = vars(ctx.message).copy()
            topic_attributes = ctx.topic_attributes.copy()
            topic_attributes.pop("sns_backend")

            try:
                message["message"] = json.loads(json.loads(message["message"]))
            except TypeError:
                try:
                    message["message"] = json.loads(message["message"])
                except json.JSONDecodeError:
                    pass
            except json.JSONDecodeError:
                pass

            input_event = InputEventModel(
                parent_id=parent_id,
                trace_id=trace_id,
                event_id=message["message_id"],
                version=version,
                account_id=ctx.store._account_id,
                region=ctx.store._region_name,
                service=ServiceName.SNS,
                operation_name="Publish",
                is_replayable=True,
                event_data={"message": message},
                event_metadata={"topic_arn": topic_attributes.get("arn")},
            )

            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            # set new trace context for calling patched function
            new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
            set_trace_context(new_trace_context)

        except Exception as e:
            log_event_studio_error(
                logger=LOG, service=ServiceName.SNS, operation="Publish", error=str(e)
            )

        return fn(self_, ctx=ctx, topic_arn=topic_arn)

    def _submit_sns_notification_with_context(
        self, fn, self_, notifier, ctx: SnsPublishContext, subscriber: SnsSubscription
    ):
        return submit_with_trace_context(self_.executor, notifier.publish, ctx, subscriber)

    #####
    # SQS
    #####

    def _put_message_sqs_queue(self, fn, self_, message: Message, **kwargs) -> dict:
        try:
            trace_context = get_trace_context()
            parent_id = trace_context.parent_id
            trace_id = trace_context.trace_id
            version = trace_context.version

            message_copy = message.copy()
            body, body_type = load_sqs_message_body(message_copy["Body"])
            parsed_timestamp = pars_timestamp_ms(list(message_copy["Attributes"].values())[1])
            input_event = InputEventModel(
                parent_id=parent_id,
                trace_id=trace_id,
                event_id=message_copy.pop("MessageId"),
                version=version,
                account_id=self_.account_id,
                region=self_.region,
                service=ServiceName.SQS,
                operation_name="Send",
                is_replayable=True,
                event_data={"body": body},
                event_metadata={
                    "queue_arn": self_.arn,
                    "body_type": body_type,
                    "original_time": parsed_timestamp,
                },
            )

            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            # set new trace context for calling patched function
            new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
            set_trace_context(new_trace_context)

        except Exception as e:
            log_event_studio_error(
                logger=LOG, service=ServiceName.SQS, operation="Send", error=str(e)
            )

        return fn(self_, message=message, **kwargs)

    ####
    # S3
    ####

    def _put_object_s3_bucket(
        self, fn, self_, context: RequestContext, request: PutObjectRequest, **kwargs
    ) -> dict:
        try:
            bucket_name = request.get("Bucket")
            if any(pattern.match(bucket_name) for pattern in IGNORE_BUCKET_PATTERNS):
                # don't track specific writes
                return fn(self_, context=context, request=request, **kwargs)

            trace_context = get_trace_context()
            parent_id = trace_context.parent_id
            trace_id = trace_context.trace_id
            version = trace_context.version

            original_body_content: bytes = request.get("Body").read()
            try:
                body_string = original_body_content.decode("utf-8")
                event_bytedata = None
                s3_data_type = "TEXT"
            except UnicodeDecodeError:
                body_string = "<binary data>"
                event_bytedata = original_body_content
                s3_data_type = "BINARY"

            input_event = InputEventModel(
                parent_id=parent_id,
                trace_id=trace_id,
                event_id=uuid.uuid4().hex,  # cannot extract id from request
                version=version,
                account_id=context.account_id,
                region=context.region,
                service=ServiceName.S3,
                operation_name="Put",
                is_replayable=True,
                event_data={"body": body_string},
                event_bytedata=event_bytedata,
                event_metadata={
                    "bucket": request["Bucket"],
                    "key": request["Key"],
                    "data_type": s3_data_type,
                },
            )

            span_id, trace_id = self._event_storage_service.add_event(
                InputEventModel.model_validate(input_event)
            )

            # set new trace context for calling patched function
            new_trace_context = TraceContext(trace_id=trace_id, parent_id=span_id)
            set_trace_context(new_trace_context)

            request["Body"] = io.BytesIO(original_body_content)

        except Exception as e:
            log_event_studio_error(
                logger=LOG, service=ServiceName.S3, operation="Put", error=str(e)
            )

        return fn(self_, context=context, request=request, **kwargs)

    def _submit_s3_notification_with_context(
        self, fn, self_, notifier, ctx: S3EventNotificationContext, config
    ):
        return submit_with_trace_context(self_._executor, notifier.notify, ctx, config)

    #########
    # Tracing
    #########
    def set_thread_local_trace_parameters_from_context(
        self, fn, _self, chain: HandlerChain, context: RequestContext, response: Response
    ):
        trace_context = extract_trace_context_from_context(context)

        if trace_context.parent_id is None:
            trace_context = self._get_trace_context_from_xray_trace_header(context)

        set_trace_context(trace_context)

        fn(_self, chain=chain, context=context, response=response)

    def _get_trace_context_from_xray_trace_header(
        self, context: RequestContext
    ) -> TraceContext | None:
        xray_header = next(
            (item[1] for item in context.request.headers if item[0] == XRAY_TRACE_HEADER), None
        )

        if not xray_header:
            return None

        try:
            if x_ray_trace_id := extract_xray_trace_id_from_header_str(xray_header):
                trace_id, parent_id = self._event_storage_service.get_trace_from_xray_trace(
                    x_ray_trace_id
                )
                if trace_id and parent_id:
                    return TraceContext(trace_id=trace_id, parent_id=parent_id)

        except (IndexError, AttributeError, TypeError):
            pass

        return None

    def _get_client_post_hook_with_trace_header(self, fn, self_, client: BaseClient, **kwargs):
        client.meta.events.register("before-call.*.*", handler=_handler_inject_trace_header)

        def _error_highlighting(exception, **kwargs):
            if exception is not None:
                trace_context = get_trace_context()
                parent_id = trace_context.parent_id
                if parent_id is not None:
                    error = InputErrorModel(
                        error_type=ErrorType.BOTO_ERROR,
                        error_text=str(exception),
                        span_id=parent_id,
                    )
                    self._event_storage_service.add_error(error)

        client.meta.events.register("after-call-error", handler=_error_highlighting)

        return fn(self_, client=client, **kwargs)

    ##########
    # Patching
    ##########

    def on_platform_ready(self):
        super().on_platform_ready()
        # APIGateway
        Patch.function(RestApiAwsProxyIntegration.invoke, self._invoke_apigateway).apply()

        # DynamoDB
        Patch.function(DynamoDBProvider.forward_request, self._forward_request).apply()
        Patch.function(EventForwarder._submit_records, self._submit_records).apply()
        Patch.function(_process_forwarded_records, self._patch_process_forwarded_event).apply()

        # EventBridge
        Patch.function(EventsProvider._process_entry, self._patch_process_entry).apply()
        Patch.function(
            EventsProvider._proxy_capture_input_event, self._patch_proxy_capture_input_event
        ).apply()
        Patch.function(EventsProvider._process_rules, self._patch_process_rules).apply()
        Patch.function(TargetSender.process_event, self._process_event).apply()

        # Lambda ESM
        Patch.function(LambdaSender.send_events, self._send_events_to_lambda).apply()

        # Lambda
        Patch.function(LambdaService.invoke, self._invoke_lambda).apply()

        # SNS
        Patch.function(PublishDispatcher.publish_to_topic, self._publish_to_topic).apply()
        Patch.function(PublishDispatcher.publish_batch_to_topic, self._publish_to_topic).apply()
        Patch.function(
            PublishDispatcher._submit_notification, self._submit_sns_notification_with_context
        ).apply()

        # SQS
        Patch.function(StandardQueue.put, self._put_message_sqs_queue).apply()
        Patch.function(FifoQueue.put, self._put_message_sqs_queue).apply()

        # S3
        Patch.function(S3Provider.put_object, self._put_object_s3_bucket).apply()
        # Patch.function(
        #     NotificationDispatcher._submit_notification, self._submit_s3_notification_with_context
        # ).apply()

        # tracing
        Patch.function(
            ServiceRequestRouter.__call__, self.set_thread_local_trace_parameters_from_context
        ).apply()
        Patch.function(
            InternalClientFactory._get_client_post_hook,
            self._get_client_post_hook_with_trace_header,
        ).apply()

        # LOG recording
        log_handler = EventStudioLogHandler(event_studio_service=self._event_storage_service)
        log_handler.setLevel(logging.INFO)
        EventsProviderLOG.addHandler(log_handler)

        # IAM error recording
        iam_callback = EventStudioIAMCallback(event_studio_service=self._event_storage_service)
        IAMEnforcementEngine.get().add_callback(iam_callback)

        LOG.info("Extension Loaded")

    def collect_routes(self, routes: list[t.Any]):
        routes.append(
            WebApp(
                event_storage_service=self._event_storage_service,
                event_streamer=self._event_streamer,
            )
        )

    #########
    # Cleanup
    #########

    def clear_db(self):
        if os.environ.get("PERSISTENCE") != "1" and is_in_docker and os.path.exists(self.db_path):
            os.remove(self.db_path)
            LOG.info("EventStudio database removed")

    def on_platform_shutdown(self):
        self._event_storage_service.close_connection()
        self.clear_db()


def _handler_inject_trace_header(params: dict[str, Any], context: dict[str, Any], **kwargs):
    trace_context = get_trace_context()
    if trace_context.trace_id and trace_context.parent_id:
        params["headers"][INTERNAL_REQUEST_TRACE_HEADER] = trace_context.json()

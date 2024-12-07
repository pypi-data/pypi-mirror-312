from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Dict, Literal

from pydantic import BaseModel, ConfigDict, model_validator

from eventstudio.api.types.errors import ErrorModel
from eventstudio.api.types.services import ServiceName

RegionName = str
SQSMessageBodyType = Literal["TEXT", "JSON", "XML"]
S3DataType = Literal["TEXT", "BINARY"]
APIGatewayBodyType = Literal["TEXT", "BINARY", "JSON", "XML", "EMPTY"]


class APIGatewayEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: dict | str
    request: dict  # InvocationRequest | IntegrationRequest = Field(...) todo fix using typing_extensions or python3.12


class APIGatewayEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_type: str
    api_name: str
    deployment_id: str
    stage_name: str
    request_type: str
    body_type: APIGatewayBodyType


class DynamoDBEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item: dict[str, str | dict] | None = None
    records: list[dict[str, str | dict]] | None = None


class DynamoDBEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    table_name: str
    operation: Literal["PutItem", "UpdateItem", "DeleteItem", "GetItem"] | None = None
    stream_type: Literal["NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES", "KEYS_ONLY"] | None = None


class EventsEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str
    detail_type: str
    source: str
    resources: list[str] | None
    detail: dict | str


class EventsEventPartialData(BaseModel):  # required for input validation error of eventbridge
    model_config = ConfigDict(extra="forbid")

    version: str
    detail_type: str | None
    source: str | None
    resources: list[str] | None
    detail: dict | str | None


class EventsEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_bus_name: str
    replay_name: str | None = None
    original_time: datetime | None = None


class LambdaEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict | str | None = None


class LambdaEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    function_name: str
    invocation_type: Literal["RequestResponse", "Event", "DryRun"] = "RequestResponse"
    log_type: str | None = None
    qualifier: str | None = None
    client_context: str | None = None


class SNSEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: dict | str


class SNSEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_group_id: str | None = None
    message_structure: Literal["JSON"] | None = None

    topic_arn: str


class SQSEventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: dict | str


class SQSEventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    queue_arn: str

    body_type: SQSMessageBodyType
    message_attributes: dict | None = None
    message_system_attributes: dict | None = None
    original_time: datetime | None = None


class S3EventData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body: str | None = None


class S3EventMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bucket: str
    key: str
    data_type: S3DataType


class InputEventModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    parent_id: str | None = None
    trace_id: str | None = None
    event_id: str | None = None

    version: int = 0
    status: str = "OK"
    is_deleted: bool = False
    is_replayable: bool = False
    is_edited: bool = False

    account_id: str
    region: str
    service: ServiceName
    operation_name: str
    creation_time: datetime | None = None

    SERVICE_MAPPINGS: ClassVar[Dict[ServiceName, Dict[str, tuple]]] = {
        ServiceName.APIGATEWAY: {
            "data": (APIGatewayEventData,),
            "metadata": (APIGatewayEventMetadata,),
        },
        ServiceName.DYNAMODB: {"data": (DynamoDBEventData,), "metadata": (DynamoDBEventMetadata,)},
        ServiceName.EVENTS: {
            "data": (EventsEventData, EventsEventPartialData),
            "metadata": (EventsEventMetadata,),
        },
        ServiceName.LAMBDA: {"data": (LambdaEventData,), "metadata": (LambdaEventMetadata,)},
        ServiceName.SNS: {"data": (SNSEventData,), "metadata": (SNSEventMetadata,)},
        ServiceName.SQS: {"data": (SQSEventData,), "metadata": (SQSEventMetadata,)},
        ServiceName.S3: {"data": (S3EventData,), "metadata": (S3EventMetadata,)},
    }

    @model_validator(mode="before")
    def convert_event_types(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Convert dictionary inputs to proper event types based on service
        handles both dictionary and model inputs"""
        if not isinstance(values, dict):
            values = {
                key: getattr(values, key)
                for key in dir(values)
                if not key.startswith("_") and not callable(getattr(values, key))
            }

        service = values.get("service")
        if isinstance(service, str):
            try:
                values["service"] = ServiceName(service.lower())
            except ValueError:
                raise ValueError(f"Invalid service name: {service}")
        elif isinstance(service, Enum):
            values["service"] = ServiceName(service.value)
        elif not isinstance(service, ServiceName):
            return values

        event_data = values.get("event_data")
        if isinstance(event_data, dict):
            data_type = cls.SERVICE_MAPPINGS[values.get("service")]["data"][0]
            values["event_data"] = data_type.model_validate(event_data)

        event_metadata = values.get("event_metadata")
        if isinstance(event_metadata, dict):
            metadata_type = cls.SERVICE_MAPPINGS[values.get("service")]["metadata"][0]
            values["event_metadata"] = metadata_type.model_validate(event_metadata)

        return values

    event_data: (
        APIGatewayEventData
        | DynamoDBEventData
        | EventsEventData
        | EventsEventPartialData
        | LambdaEventData
        | SNSEventData
        | SQSEventData
        | S3EventData
        | None
    ) = None

    event_metadata: (
        APIGatewayEventMetadata
        | DynamoDBEventMetadata
        | EventsEventMetadata
        | LambdaEventMetadata
        | SNSEventMetadata
        | SQSEventMetadata
        | S3EventMetadata
        | None
    ) = None

    event_bytedata: bytes | None = None

    @model_validator(mode="after")
    def validate_event_data(cls, values):
        service = values.service
        event_data = values.event_data
        event_metadata = values.event_metadata

        # Validate event data
        if event_data is not None:
            expected_data_types = cls.SERVICE_MAPPINGS[service]["data"]
            if not isinstance(event_data, expected_data_types):
                type_names = " or ".join(t.__name__ for t in expected_data_types)
                raise ValueError(
                    f'For service "{service}", event_data must be of type {type_names}.'
                )

        # Validate event metadata
        if event_metadata is not None:
            expected_metadata_types = cls.SERVICE_MAPPINGS[service]["metadata"]
            if not isinstance(event_metadata, expected_metadata_types):
                type_names = " or ".join(t.__name__ for t in expected_metadata_types)
                raise ValueError(
                    f'For service "{service}", event_metadata must be of type {type_names}.'
                )

        return values


class InputEventModelList(BaseModel):
    events: list[InputEventModel]


class EventModel(InputEventModel):
    model_config = ConfigDict(from_attributes=True)

    span_id: str
    errors: list["ErrorModel"] = []

    children: list["EventModel"] = []


class EventModelList(BaseModel):
    events: list[EventModel]

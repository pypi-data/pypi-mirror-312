import json
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Pattern, Tuple, Type, TypeVar, Union

from localstack.aws.api.events import PutEventsRequestEntry
from localstack.http import Request
from pydantic import BaseModel
from sqlalchemy.types import JSON, TypeDecorator

from eventstudio.api.types.events import (
    APIGatewayBodyType,
    EventModel,
    EventModelList,
    EventsEventPartialData,
    SQSMessageBodyType,
)
from eventstudio.api.types.services import ServiceName

LOG = logging.getLogger(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value

        # allow us to work with nested models
        if isinstance(obj, EventModel):
            return obj.model_dump()

        if isinstance(obj, EventModelList):
            return obj.model_dump()

        return super().default(obj)


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = JSON
    cache_ok = True

    def __init__(self, encoder=None, *args, **kwargs):
        self.encoder = encoder or CustomJSONEncoder
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, cls=self.encoder)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


def pars_timestamp_ms(timestamp_ms: str) -> datetime:
    timestamp_s = int(timestamp_ms) / 1000
    parsed_time = datetime.fromtimestamp(timestamp_s)

    return parsed_time


def convert_raw_entry(entry: PutEventsRequestEntry) -> EventsEventPartialData:
    """Convert put event request that can also fail validation"""
    return EventsEventPartialData(
        version="0",
        detail_type=entry.get("DetailType"),
        source=entry.get("Source"),
        resources=entry.get("Resources", []),
        detail=json.loads(entry.get("Detail", "{}")),
    )


T = TypeVar("T", bound=BaseModel)


def parse_request_body(request: Request, model: Type[T]) -> T:
    request_data = request.data.decode("utf-8")
    body_dict = json.loads(request_data)
    return model(**body_dict)


def compile_regex_patterns(patterns: List[str]) -> List[Pattern]:
    """Compile a list of regex patterns."""
    return [re.compile(pattern) for pattern in patterns]


def load_sqs_message_body(body: str) -> Tuple[Union[Dict[Any, Any], str], SQSMessageBodyType]:
    """
    Load message body based on its format (JSON, XML, or plain text).
    """
    # First try JSON as it's most common
    try:
        return json.loads(body), "JSON"
    except json.JSONDecodeError:
        pass

    # Then try XML
    try:
        if body.strip().startswith(("<?xml", "<")):
            root = ET.fromstring(body)
            return xml_to_dict(root), "XML"
    except ET.ParseError:
        pass

    # If neither JSON nor XML, return as plain text
    return body, "TEXT"


def xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """Convert XML to dictionary representation."""
    result = {}

    if element.attrib:
        result.update(element.attrib)

    for child in element:
        child_dict = xml_to_dict(child)
        if child.tag in result:
            # If tag already exists, convert to list or append
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_dict)
        else:
            result[child.tag] = child_dict

    if element.text and element.text.strip():
        if result:
            result["text"] = element.text.strip()
        else:
            result = element.text.strip()

    return result


def dict_to_xml(data: Union[Dict[str, Any], str], root_name: str = "root") -> str:
    def _build_element(parent: ET.Element, data: Union[Dict[str, Any], str, list]) -> None:
        if isinstance(data, dict):
            text_content = data.pop("text", None)

            attrs = {k: v for k, v in data.items() if not isinstance(v, (dict, list))}
            for k in attrs:
                data.pop(k)
            parent.attrib.update({k: str(v) for k, v in attrs.items()})

            for key, value in data.items():
                if isinstance(value, list):
                    for item in value:
                        child = ET.SubElement(parent, key)
                        _build_element(child, item)
                else:
                    child = ET.SubElement(parent, key)
                    _build_element(child, value)

            if text_content is not None:
                parent.text = str(text_content)

        elif isinstance(data, list):
            for item in data:
                _build_element(parent, item)
        else:
            parent.text = str(data)

    # Create the root element
    if isinstance(data, dict):
        root = ET.Element(root_name)
        _build_element(root, data)
    else:
        # If data is a simple value, create a simple element
        root = ET.Element(root_name)
        root.text = str(data)

    # Convert to string with XML declaration
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        root, encoding="unicode", method="xml"
    )


def log_event_studio_error(logger, service: ServiceName, operation: str, error: str):
    logger.error(
        "EventStudio Error",
        extra={"service": service.value, "operation": operation, "error": str(error)},
    )


def run_safe(logger, service: ServiceName, operation: str):
    """Wrapts the EventStudio logic in a try except to make sure the"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_event_studio_error(logger, service, operation, str(e))

        return wrapper

    return decorator


def load_apigateway_body(
    body: bytes | None,
) -> Tuple[Union[Dict[Any, Any], str, bytes], APIGatewayBodyType]:
    """
    Load message body based on its format (BINARY, JSON, XML, or TEXT).
    """
    if body is None:
        return body, "EMPTY"
    try:
        body_data = body.decode("utf-8")
        # First try JSON as it's most common
        try:
            return json.loads(body_data), "JSON"
        except json.JSONDecodeError:
            pass

        # Then try XML
        try:
            if body_data.strip().startswith(("<?xml", "<")):
                root = ET.fromstring(body_data)
                return xml_to_dict(root), "XML"
        except ET.ParseError:
            pass

        # If neither JSON nor XML, return as plain text
        return body_data, "TEXT"

    except UnicodeDecodeError:
        return body, "BINARY"

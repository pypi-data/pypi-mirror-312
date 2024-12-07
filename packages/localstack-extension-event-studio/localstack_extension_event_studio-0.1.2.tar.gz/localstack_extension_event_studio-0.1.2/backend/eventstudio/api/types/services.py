from enum import Enum


class ServiceName(Enum):
    APIGATEWAY = "apigateway"
    DYNAMODB = "dynamodb"
    EVENTS = "events"
    EVENT_STUDIO = "event_studio"
    SQS = "sqs"
    LAMBDA = "lambda"
    SNS = "sns"
    S3 = "s3"

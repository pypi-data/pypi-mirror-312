from enum import Enum
from dataclasses import dataclass


@dataclass
class SuccesProps:
    border_style: str = "cyan"

@dataclass
class ErrorProps:
    border_style: str = "red"

@dataclass
class WarningProps:
    border_style: str = "yellow"


@dataclass
class ResponseType:
    SUCCESS = SuccesProps
    ERROR = ErrorProps
    WARNING = WarningProps



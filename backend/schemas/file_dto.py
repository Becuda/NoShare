from datetime import datetime
from pydantic import BaseModel
from enum import Enum,auto,unique

@unique
class OperationType(Enum):
    UPLOAD = auto()
    RENAME = auto()
    DELETE = auto()
    INFO = auto()
    CREATE=auto()

@unique
class OperationStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()


class FileDTO(BaseModel):
    name: str
    extension: str
    size: int
    is_dir: bool
    timestamp: str
    operation_type: OperationType | None = None
    operation_status: OperationStatus | None = None
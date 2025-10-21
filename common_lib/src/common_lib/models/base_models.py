# common_lib/models/base_models.py
from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, Optional, List
from datetime import datetime, UTC

DataT = TypeVar('DataT')

class ApiResponse(BaseModel, Generic[DataT]):
    success: bool
    data: Optional[DataT] = None
    error: Optional[str] = None
    timestamp: datetime = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now(UTC)
        super().__init__(**data)

class PaginatedResponse(BaseModel, Generic[DataT]):
    items: List[DataT]
    total: int
    page: int
    size: int
    has_next: bool
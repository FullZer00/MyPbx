# common_lib/core/base_service.py
from abc import ABC, abstractmethod
from typing import Any, Dict

from src.common_lib.utils.custom_logger import CustomLogger
from src.common_lib.exceptions import ServiceException

class BaseService(ABC):
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = CustomLogger(service_name).logger
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None):
        """Единообразная обработка ошибок"""
        self.logger.error(f"Error in {self.service_name}", error=error, context=context)
        raise ServiceException(str(error)) from error
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

# common_lib/core/base_repository.py
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass
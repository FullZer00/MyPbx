from typing import Dict, Any
import datetime as dt


class GlobalException(Exception):
    def __init__(self,
                 message: str,
                 details: Dict[str, Any] | None,
                 error_code: str = 'Unknown error',
                 status_code: int = 500,
    ):
        self.message = message
        self.details = details or {}
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": {
                "message": self.message,
                "details": self.details,
                "timestamp": self._get_timestamp()
            }
        }

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return dt.datetime.now(dt.UTC).isoformat() + "Z"

    def __str__(self) -> str:
        return f"Error: {self.message}"
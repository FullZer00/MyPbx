from ..exceptions.global_exception import GlobalException


class ServiceException(GlobalException):
    def __init__(self,
                 message: str,
                 error_code: str = 'INTERNAL_ERROR',
                 status_code: int = 500,
                 service_name: str | None = None,
                 ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.service_name = service_name

    def to_dict(self) -> dict:
        return {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "service": self.service_name,
                "details": self.details,
                "timestamp": self._get_timestamp()
            }
        }

    def __str__(self):
        return f"[{self.error_code}]({self.status_code}): {self.message} \n(Service: {self.service_name})"
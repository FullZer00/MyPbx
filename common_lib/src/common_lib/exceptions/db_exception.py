from ..exceptions import GlobalException


class DBException(GlobalException):
    def __init__(self,
                 error_code: str = "DB_EXCEPTION",
                 **kwargs):
        self.error_code = error_code
        super().__init__(**kwargs)

    def __str__(self):
        return f"{self.error_code}: {self.message}"
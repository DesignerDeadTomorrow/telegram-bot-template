class AppError(Exception):
    """Общие ошибки всего проекта."""

    def __init__(self, error_msg: str, user_msg: str, **kwargs) -> None:
        super().__init__(error_msg)

        self.user_msg = user_msg
        self.extra = kwargs

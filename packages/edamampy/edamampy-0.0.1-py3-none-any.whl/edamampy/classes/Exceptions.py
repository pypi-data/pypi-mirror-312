class EdamamAPIFieldValidationError(Exception):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        super().__init__(f"{key}: {value} - given value is invalid for given key.")


class EdamamAPIFieldKeyError(Exception):
    def __init__(self, key):
        super().__init__(f"{key} - given key is not a valid field for the edamam API.")


class EdamamURLValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EdamamAPIException(Exception):
    """Raised when the edamam api returns an error."""

    def __init__(
        self,
        ret: dict,
        status_code: int,
        additional_message: str,
        message: str = "Edamam API returned an error.",
    ):
        super().__init__(
            f"{message} HTTP status code: {status_code}. Return data: {ret}. Additional messages: {additional_message}"
        )


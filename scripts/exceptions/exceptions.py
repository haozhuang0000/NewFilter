from typing import List
class FilterException(Exception):
    """Base exception for Filter-related errors."""
    pass

class ModelNotFoundError(FilterException):
    """Exception raised when a specified collection does not exist."""
    def __init__(self, model: str, available_models: List[str]):
        message = (
            f"Model '{model}' does not exist. "
            f"Available models: {', '.join(available_models)}. "
            "If you want to use a different model, please contact your server administrator."
        )
        super().__init__(message)
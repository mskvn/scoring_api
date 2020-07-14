class ValidationError(Exception):
    """Raised when the field is not valid"""
    pass


class StoreGetException(Exception):
    """Raised when cant get value from store"""
    pass

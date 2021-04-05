class PhonegramError(Exception):
    """Base class for all errors in Phonegram"""
    message = None
    code = None
    error_name = "PhonegramError"

    def __init__(self, message: str, code: int = None, error_name: str = None):
        super().__init__('{} {}: {}'.format(error_name or self.error_name, code or self.code, message))

        self.code = code
        self.message = message


class IncorrectPhoneNumberError(PhonegramError):
    """
    It raises if any function detected an incorrect phone number using a regex.
    """
    code = 100
    error_name = "IncorrectPhoneNumberError"

    def __init__(self, phone_number: str):
        message = f"Был обнаружен некорректный номер телефона: {phone_number}"
        super().__init__(message)

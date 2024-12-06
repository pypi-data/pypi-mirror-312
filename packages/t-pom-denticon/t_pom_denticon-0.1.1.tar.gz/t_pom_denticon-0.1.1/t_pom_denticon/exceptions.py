"""Module Description: This module defines custom exceptions for use within the application.

These exceptions provide more specific error handling and messaging for various failure scenarios,
improving the robustness and clarity of the code.
"""


class ConversationDefaultException(Exception):
    """Invalid Conversation Default Exception ."""

    pass


class PrimaryCarrierEmptyException(Exception):
    """Invalid Primary Carrier Empty Exception ."""

    pass


class PatientNotFoundException(Exception):
    """Patient Not Found Exception."""

    pass


class SessionExpiredException(Exception):
    """Session Expire Exception."""

    pass

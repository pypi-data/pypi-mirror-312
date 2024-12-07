"""Module Description: This module defines custom exceptions for use within the application.

These exceptions provide more specific error handling and messaging for various failure scenarios,
improving the robustness and clarity of the code.
"""


class PatientNotFoundException(Exception):
    """Patient Not Found Exception."""

    pass


class DataInsertiondException(Exception):
    """Data Insertion Exception."""

    pass

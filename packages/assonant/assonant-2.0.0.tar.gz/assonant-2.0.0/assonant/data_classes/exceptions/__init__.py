"""Assonant data classes exceptions.

This submodule defines Exceptions used all over the data classes module and its submodules.
"""

from .data_classes_exceptions import (
    AssonantDataClassesError,
    AxisInsertionError,
    DataHandlerInsertionError,
    DataHandlerTakeageError,
    FieldInsertionError,
    SubcomponentInsertionError,
)
from .factories_exceptions import (
    AssonantComponentFactoryError,
    AssonantDataHandlerFactoryError,
)

__all__ = [
    "AssonantDataClassesError",
    "AssonantDataHandlerFactoryError",
    "AssonantComponentFactoryError",
    "AxisCreationError",
    "AxisInsertionError",
    "DataHandlerInsertionError",
    "DataHandlerTakeageError",
    "FieldCreationError",
    "FieldInsertionError",
    "SubcomponentInsertionError",
]

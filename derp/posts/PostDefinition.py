"""
PostDefinition.py

Implementation of PostDefinition objects and the FieldType enumeration.
"""

from enum import Enum
import collections
import numbers
import datetime

from derp.language.Grammar import Grammar

class PostDefinition:
    """
    Lists out the details of each field on the post objects returned from a
    module’s query processor. This aids in semantics checking and the planning
    of selection execution in the selection executor factory.

    Keeps track of each field's name and type.
    """

    def __init__(self, field_definitions):
        assert isinstance(field_definitions, collections.Mapping)
        assert len(field_definitions.keys()) != 0
        self.__field_definitions = field_definitions

    def field_exists(self, field_name, field_type=None):
        """
        Checks if a field is a part of a post definition.
        :param field_name: The name of the field to check for
        :param field_type: An optional FieldType to match against
        :return: True if a field matching the provided parameters exists in the post definition
        """
        if field_name not in self.__field_definitions:
            return False
        elif field_type is None:
            return True
        elif self.__field_definitions[field_name] != field_type:
            return False
        else:
            return True

    def get_type(self, field_name):
        """
        Retrieves the type of a field in a post definition.
        :param field_name: The name of the field to get the type for
        :return: The FieldType of the given field, or None if the field does not exist
        """
        if not self.field_exists(field_name):
            return None
        return self.__field_definitions[field_name]

    def field_grammar(self):
        return Grammar({
            "field": self.__field_definitions.keys()
        })


class FieldType(Enum):
    """
    Describes the types of DERP fields that may be contained in posts.
    Each enum value is the corresponding python type.
    """
    STRING = str
    NUMBER = numbers.Number
    BOOLEAN = bool
    DATE = datetime.date

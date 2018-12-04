from lark import Visitor

from derp.exceptions import InvalidFieldDataTypeException
from derp.posts import FieldType


class CheckFieldDataType(Visitor):
    def __init__(self, field_is_type):
        self.__field_is_type = field_is_type

    def date_qualifier(self, node):
        args = node.children
        field = args[0]

        if not self.__field_is_type(field, FieldType.DATE):
            raise InvalidFieldDataTypeException(
                "Field " + field + " cannot be used for date checks")

    def _check_string(self, field):
        if not self.__field_is_type(field, FieldType.STRING):
            raise InvalidFieldDataTypeException(
                "Field " + field + " cannot be used for string checks")

    def string_qualifier(self, node):
        args = node.children
        field = args[1]
        self._check_string(field)

    def substring_qualifier(self, node):
        args = node.children
        field = args[0]
        self._check_string(field)

    def boolean_qualifier(self, node):
        args = node.children
        field = args[0]

        if not self.__field_is_type(field, FieldType.BOOLEAN):
            raise InvalidFieldDataTypeException(
                "Field " + field + " cannot be used for boolean checks")

    def number_qualifier(self, node):
        args = node.children
        field = args[0]

        if not self.__field_is_type(field, FieldType.NUMBER):
            raise InvalidFieldDataTypeException(
                "Field " + field + " cannot be used for numeric checks")

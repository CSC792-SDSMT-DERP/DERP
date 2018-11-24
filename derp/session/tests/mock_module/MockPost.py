
from derp.posts import IPost, PostDefinition, FieldType


class MockPost(IPost):

    def __init__(self, source_module, date, number, string, bool_val):
        self.__source_module = source_module
        self.__data = {
            "mock_date": date,
            "mock_number": number,
            "mock_string": string,
            "mock_boolean": bool_val
        }

    def definition(self):
        return PostDefinition({
            "mock_date": FieldType.DATE,
            "mock_number": FieldType.NUMBER,
            "mock_string": FieldType.STRING,
            "mock_boolean": FieldType.BOOLEAN
        })

    def source(self):
        return self.__source_module

    def field_data(self, field_name):
        return self.__data[field_name]

    def about(self, string):
        return string in self.__data["mock_string"]

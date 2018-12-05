
from derp.posts import IPost, PostDefinition, FieldType


class MockPost(IPost):

    def __init__(self, source_module, date, number, string, bool_val):
        self.__source_module = source_module
        self.__data = {
            "post date": date,
            "points": number,
            "title": string,
            "verified": bool_val
        }

    def definition(self):
        return PostDefinition({
            "title": FieldType.STRING,
            "points": FieldType.NUMBER,
            "verified": FieldType.BOOLEAN,
            "post date": FieldType.DATE,
        })

    def source(self):
        return self.__source_module

    def field_data(self, field_name):
        return self.__data[field_name]

    def about(self, string):
        return string in self.__data["mock_string"]

    def __str__(self):
        return "\n".join([field + ": " + str(self.__data[field]) for field in ["title", "points", "verified", "post date"]])

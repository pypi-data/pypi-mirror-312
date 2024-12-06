from djing.core.Fields.Field import Field

class Color(Field):
    component: str
    def json_serialize(self): ...

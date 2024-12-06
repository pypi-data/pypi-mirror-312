from django.db.models import base as base
from djing.core.Fields.Field import Field
from typing import Self

class ID(Field):
    component: str
    @classmethod
    def for_model(cls, resource: base.Model) -> Self: ...
    def json_serialize(self): ...

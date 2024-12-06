from djing.core.Contracts.ListableField import ListableField
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field

class BelongsToMany(Field, ListableField, RelatableField):
    component: str
    def json_serialize(self): ...

from djing.core.Contracts.BehavesAsPanel import BehavesAsPanel
from djing.core.Contracts.RelatableField import RelatableField
from djing.core.Fields.Field import Field

class BelongsTo(Field, BehavesAsPanel, RelatableField):
    component: str
    def json_serialize(self): ...

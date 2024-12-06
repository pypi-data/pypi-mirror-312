from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from _typeshed import Incomplete
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Makeable import Makeable

class MenuGroup(AuthorizedToSee, Makeable, Collapsable, JsonSerializable):
    component: str
    name: Incomplete
    def __init__(self, name, items=[]) -> None: ...
    def json_serialize(self) -> dict: ...

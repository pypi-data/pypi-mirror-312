from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Makeable import Makeable
from typing import Self

class MenuList(AuthorizedToSee, Makeable, Collapsable, JsonSerializable):
    component: str
    def __init__(self, items) -> None: ...
    def items(self, items=[]) -> Self: ...
    def json_serialize(self) -> dict: ...

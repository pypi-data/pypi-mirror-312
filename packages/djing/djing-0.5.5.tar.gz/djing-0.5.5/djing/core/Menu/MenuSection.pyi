from Illuminate.Contracts.Support.JsonSerializable import JsonSerializable
from _typeshed import Incomplete
from djing.core.AuthorizedToSee import AuthorizedToSee
from djing.core.Dashboard import Dashboard as Dashboard
from djing.core.Fields.Collapsable import Collapsable
from djing.core.Makeable import Makeable
from djing.core.Resource import Resource as Resource
from djing.core.WithIcon import WithIcon

class MenuSection(AuthorizedToSee, Makeable, Collapsable, WithIcon, JsonSerializable):
    component: str
    name: Incomplete
    items: Incomplete
    def __init__(self, name, items=[], icon: str = 'collection') -> None: ...
    def path(self, path: Incomplete | None = None): ...
    @classmethod
    def dashboard(cls, dashboard_class: type['Dashboard']): ...
    @classmethod
    def resource(cls, resource_class: type['Resource']): ...
    def json_serialize(self) -> dict: ...

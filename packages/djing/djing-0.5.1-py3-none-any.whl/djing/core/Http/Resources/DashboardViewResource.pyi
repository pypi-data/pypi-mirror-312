from _typeshed import Incomplete
from djing.core.Dashboard import Dashboard
from djing.core.Http.Requests.DashboardRequest import DashboardRequest as DashboardRequest
from djing.core.Http.Resources.Resource import Resource

class DashboardViewResource(Resource):
    name: Incomplete
    def __init__(self, name) -> None: ...
    def authorized_dashboard_for_request(self, request: DashboardRequest) -> Dashboard: ...
    def json(self, request: DashboardRequest): ...

from djing.core.Http.Requests.DashboardRequest import DashboardRequest as DashboardRequest
from typing import Any

class DashboardController:
    def __call__(self, request: DashboardRequest) -> Any: ...

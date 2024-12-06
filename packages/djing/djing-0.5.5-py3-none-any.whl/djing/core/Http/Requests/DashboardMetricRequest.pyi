from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Http.Requests.QueriesResources import QueriesResources

class DashboardMetricRequest(DjingRequest, QueriesResources):
    request_name: str
    def metric(self): ...
    def available_metrics(self): ...

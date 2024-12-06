from Illuminate.Collections.Collection import Collection as Collection
from djing.core.Http.Requests.DjingRequest import DjingRequest

class DashboardRequest(DjingRequest):
    def available_cards(self, key) -> Collection: ...

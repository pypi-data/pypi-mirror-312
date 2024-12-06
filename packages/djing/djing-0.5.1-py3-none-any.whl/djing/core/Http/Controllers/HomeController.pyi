from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from typing import Any

class HomeController:
    def home(self, request: DjingRequest) -> Any: ...

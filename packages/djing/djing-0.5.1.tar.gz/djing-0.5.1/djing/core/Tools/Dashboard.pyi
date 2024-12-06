from djing.core.HasMenu import HasMenu
from djing.core.Http.Requests.DjingRequest import DjingRequest as DjingRequest
from djing.core.Tool import Tool

class Dashboard(Tool, HasMenu):
    def menu(self, request: DjingRequest): ...

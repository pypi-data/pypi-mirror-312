from Illuminate.Contracts.Debug.ExceptionHandler import ExceptionHandler
from Illuminate.Support.Facades.Gate import Gate
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.ServiceProvider import ServiceProvider
from djing.core.Exceptions.DjingExceptionHandler import DjingExceptionHandler
from djing.core.Facades.Djing import Djing


class DjingApplicationServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.app = app

    def register(self):
        pass

    def boot(self):
        try:
            self.gate()

            self.routes()

            Djing.serving(self.__process_serving)
        except Exception as e:
            print("DjingApplicationServiceProvider.boot", e)

    def __process_serving(self):
        self.authorization()

        self.register_exception_handler()

        self.resources()

        Djing.dashboards(self.dashboards())

        Djing.tools(self.tools())

    def authorization(self):
        def check_auth(request):
            if self.app.make("env") == "development":
                return True

            return Gate.check("view_djing", [Djing.user(request)])

        return Djing.auth(check_auth)

    def register_exception_handler(self):
        self.app.bind(ExceptionHandler, DjingExceptionHandler)

    def resources(self):
        Djing.resources_in(Djing.app_directory())

    def routes(self):
        Djing.routes().with_authentication_routes()

    def gate(self):
        Gate.define(
            "view_djing",
            lambda user: (user.is_authenticated and user.email in []),
        )

    def dashboards(self):
        return []

    def tools(self):
        return []

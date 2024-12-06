import os
import django

from django.conf import settings
from Illuminate.Foundation.Application import Application
from djing.core.Djing import Djing
from djing.core.Providers.DjingCoreServiceProvider import DjingCoreServiceProvider

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    project_name = os.getenv("DJING_PROJECT_NAME", "myproject")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")

    django.setup()

    if not settings.configured:
        settings.configure()


def djing_application():
    return (
        Application.configure(base_path=Djing.base_directory())
        .with_providers([DjingCoreServiceProvider])
        .with_routing()
        .with_middleware()
        .with_exceptions()
        .create()
    )

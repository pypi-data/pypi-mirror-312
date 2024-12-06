import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "My centralized CLI command"

    def handle(self, *args, **options):
        settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")

        if settings_module:
            return settings_module.split(".")[0]
        else:
            raise RuntimeError(
                "DJANGO_SETTINGS_MODULE is not set. Ensure Django is initialized."
            )

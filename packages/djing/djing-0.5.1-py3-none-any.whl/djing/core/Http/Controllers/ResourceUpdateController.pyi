from Illuminate.Validation.ValidationResponse import ValidationResponse as ValidationResponse
from django.db.models import base as base
from djing.core.Http.Requests.UpdateResourceRequest import UpdateResourceRequest as UpdateResourceRequest
from typing import Any

class ResourceUpdateController:
    def __call__(self, request: UpdateResourceRequest) -> Any: ...

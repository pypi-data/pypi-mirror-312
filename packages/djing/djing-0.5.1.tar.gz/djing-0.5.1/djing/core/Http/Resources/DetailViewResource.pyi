from django.db.models import base as base
from djing.core.Http.Requests.ResourceDetailRequest import ResourceDetailRequest as ResourceDetailRequest
from djing.core.Http.Resources.Resource import Resource

class DetailViewResource(Resource):
    def authorized_resource_for_request(self, request: ResourceDetailRequest): ...
    def json(self, request: ResourceDetailRequest): ...

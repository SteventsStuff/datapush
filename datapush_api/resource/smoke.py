from sanic.views import HTTPMethodView
from sanic.response import json


class Smoke(HTTPMethodView):
    def get(self, request):
        return json(
            {
                "service": "DataPush",
                "message": "Service is running!"
            }
        )

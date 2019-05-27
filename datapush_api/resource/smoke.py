from sanic.views import HTTPMethodView
from sanic.response import json


class Smoke(HTTPMethodView):
    def get(self, request):
        return json(
            {"message": "Hello world! Service DataPush is running!"},
            headers={"Service": "DataPush"},
            status=200
        )

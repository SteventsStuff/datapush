from sanic.response import json
from http import HTTPStatus
import aiohttp
import logging


class BaseDomain:
    def __init__(self, url, params=None):
        self.url = url
        self.params = params

    async def get_instances(self, request):
        try:
            async with aiohttp.request(
                    method="GET",
                    url=self.url,
                    params=self.params
            ) as service_response:
                result = await service_response.json()

        except Exception as exc:  # do it this way is not your bro!
            logging.error(exc)
            return json({"Error": "Server is unavailable now"})
        else:
            if service_response.status == HTTPStatus.OK:
                return json(result)
            else:
                pass

    async def get_instance_by_key(self, request):
        pass

    async def get_instances_by_filters(self, request):
        pass

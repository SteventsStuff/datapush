from datapush_api.domain.base_domain import BaseDomain
from sanic.response import text
import aiohttp
import logging


class PaymentsDomain(BaseDomain):
    async def get_payments_contracts(self):
        try:
            async with aiohttp.request(
                method="GET", url=self.url, params=self.params
            ) as service_response:
                result = await service_response.read()
        except Exception as exc:
            logging.error(exc)
            return text("Error server is unavailable now, can't make insert")
        else:
            return text("e boy")

from sanic.views import HTTPMethodView
from datapush_api.domain.contracts import *


class ContractsPayments(HTTPMethodView):
    async def get(self, request):
        request_url = request.url
        url = request_url[request_url.rfind("/") + 1:]

        """
        http://127.0.0.1/contracts/id
        http://127.0.0.1/contracts/
        http://127.0.0.1/contracts/filter
        http://127.0.0.1/contracts/payments

        http://127.0.0.1/payments/contracts
        http://127.0.0.1/payments/id
        http://127.0.0.1/payments/filter
        http://127.0.0.1/payments/
        """

        if "contracts" in request_url:
            if "payments" in url:
                # result = await get_contracts(request)
                pass
            elif "filter" in url:
                # result = await get_contracts(request)
                pass
            elif "id" in url:
                # result = await get_contracts(request)
                pass
            else:
                # result = await get_contracts(request)
                pass
        else:
            if "payments" in url:
                # result = await get_payments(request)
                pass
            elif "filter" in url:
                # result = await get_payments(request)
                pass
            elif "id" in url:
                # result = await get_payments(request)
                pass
            else:
                # result = await get_payments(request)
                pass

        return 0

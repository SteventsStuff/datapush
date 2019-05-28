from sanic.views import HTTPMethodView
from datapush_api.domain.basic_views import parse_url
from datapush_api.domain.payments import PaymentsDomain


class Payments(HTTPMethodView):
    async def get(self, request):
        service_url = parse_url(request.url)

        if service_url == "id":
            # result = await PaymentsDomain(url=url)
            pass
        elif service_url == "filter":
            # result = await get_contracts(request)
            pass
        elif service_url == "contracts":
            # result = await get_contracts(request)
            pass
        else:
            # result = await get_contracts(request)
            pass

        return 0

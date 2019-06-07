from sanic.views import HTTPMethodView
from sanic.response import text
from datapush_api.domain.payments import PaymentsDomain
from datapush_api.constants import (
    PAYMENTS_APP_NAME, SDA_UNREGISTERED_SERVICES_LIST, SERVICE_URL
)
from datapush_api.validation.validator import validate_params
from datapush_api.basic_views import (
    parse_url,
    restructure_params,
    get_service_socket
)


class Payments(HTTPMethodView):
    async def get(self, request):
        print("ashasdjkasd", request.url)
        service_endpoint = await parse_url(request.url)
        service_url = await get_service_socket(PAYMENTS_APP_NAME)
        print(service_url)

        if service_url in SDA_UNREGISTERED_SERVICES_LIST:
            msg = f"Sorry, can not connect to '{PAYMENTS_APP_NAME.upper()}'"
            return text(msg)
        else:
            params = await restructure_params(request.args)
            is_params_valid, validator_message = await validate_params(
                params, PAYMENTS_APP_NAME
            )

            if is_params_valid:
                if service_endpoint[:2] == "id":
                    service_url += "/id"
                    result = await PaymentsDomain(
                        url=service_url, params=params
                    ).get_instance_by_key()
                elif service_endpoint[:9] == "contracts":
                    service_url += "/contract"
                    result = await PaymentsDomain(
                        url=service_url, params=params
                    ).get_instance_by_key()

                else:
                    print(SERVICE_URL)
                    service_url += request.url[len(SERVICE_URL):]
                    print(service_url)
                    result = await PaymentsDomain(
                        url=service_url, params=params
                    ).get_instances()

                return result
            else:
                return text(validator_message)

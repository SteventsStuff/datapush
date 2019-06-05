from sanic.views import HTTPMethodView
from sanic.response import text
from datapush_api.domain.contracts import ContractDomain
from datapush_api.constants import (
    CONTRACTS_APP_NAME, SDA_UNREGISTERED_SERVICES_LIST
)
from datapush_api.validation.validator import validate_params
from datapush_api.basic_views import (
    parse_url,
    restructure_params,
    get_service_socket
)


class Contracts(HTTPMethodView):
    async def get(self, request):
        service_endpoint = await parse_url(request.url)
        service_url = await get_service_socket(CONTRACTS_APP_NAME)

        if service_url in SDA_UNREGISTERED_SERVICES_LIST:
            msg = f"Sorry, can not connect to '{CONTRACTS_APP_NAME.upper()}'"
            return text(msg)
        else:
            params = await restructure_params(request.args)
            is_params_valid, validator_message = await validate_params(
                params, CONTRACTS_APP_NAME
            )

            if is_params_valid:
                if service_endpoint[:2] == "id":
                    service_url += "/id"
                    result = await ContractDomain(
                        url=service_url, params=params
                    ).get_instance_by_key()

                elif service_endpoint[:6] == "filter":
                    service_url += "/filter"
                    result = await ContractDomain(
                        url=service_url, params=params
                    ).get_instances_by_filters()

                elif service_endpoint[:8] == "payments":
                    service_url += "/payments"
                    result = await ContractDomain(
                        url=service_url, params=params
                    ).get_instance_by_key()

                else:
                    result = await ContractDomain(
                        url=service_url, params=params
                    ).get_instances()

                return result
            else:
                return text(validator_message)

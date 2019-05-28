from sanic.views import HTTPMethodView
from datapush_api.domain.basic_views import parse_url, get_service_socket,\
    restructure_params, validate_contacts_params
from datapush_api.domain.contracts import ContractDomain
from datapush_api.constants import CONTRACTS_APP_NAME
from sanic.response import json


class Contracts(HTTPMethodView):
    async def get(self, request):
        service_endpoint = await parse_url(request.url)
        service_url = await get_service_socket(CONTRACTS_APP_NAME)
        # service_url = "http://127.0.0.1:5000/"  # for home tests

        params = await restructure_params(request.args)
        is_params_valid, validator_message = await validate_contacts_params(params)

        if is_params_valid:
            if service_endpoint == "id":
                result = await ContractDomain(
                            url=service_url,
                            params=params
                        ).get_instance_by_key(request)
            elif service_endpoint == "filter":
                result = await ContractDomain(
                            url=service_url,
                            params=params
                        ).get_instances_by_filters(request)
            elif service_endpoint == "payments":
                result = await ContractDomain(
                            url=service_url,
                            params=params
                        ).get_contracts_payments(request)
            else:
                result = await ContractDomain(
                            url=service_url
                        ).get_instances(request)

            return result
        else:
            return json({"message": validator_message})

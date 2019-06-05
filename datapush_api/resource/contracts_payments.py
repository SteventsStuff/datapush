from sanic.views import HTTPMethodView
from sanic.response import text
from datapush_api.domain.contracts_payments import general_request
# from datapush_api.validator_old import validate_params
from datapush_api.constants import (
    PAYMENTS_APP_NAME, CONTRACTS_APP_NAME, SDA_UNREGISTERED_SERVICES_LIST
)
from datapush_api.basic_views import (
    restructure_params, get_service_socket
)


class ContractsPayments(HTTPMethodView):
    async def get(self, request):
        payments_service_url = await get_service_socket(PAYMENTS_APP_NAME)
        contracts_service_url = await get_service_socket(CONTRACTS_APP_NAME)

        if contracts_service_url in SDA_UNREGISTERED_SERVICES_LIST:
            msg = f"Sorry, can not connect to '{CONTRACTS_APP_NAME.upper()}'"
            return text(msg)
        elif payments_service_url in SDA_UNREGISTERED_SERVICES_LIST:
            msg = f"Sorry, can not connect to '{PAYMENTS_APP_NAME.upper()}'"
            return text(msg)
        else:
            params = await restructure_params(request.args)
            is_params_valid, validator_message = await validate_params(params)

            if is_params_valid:
                # mb we will add one more param "file" for user to choose
                # type of data for output (json, csv, pdf)
                payments_service_url += "/contract"
                if len(params.keys()) == 1 and list(params.keys())[0] == "id":
                    result = await general_request(
                        contracts_url=contracts_service_url,
                        payments_url=payments_service_url,
                        params=params
                    )
                else:
                    return text("You must use only ID parameter!")
                return result
            else:
                return text(validator_message)

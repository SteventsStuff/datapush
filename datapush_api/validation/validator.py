from datapush_api.validation.contracts_schema import BandContractsSchema
from datapush_api.validation.payments_schema import BandPaymentsSchema
from datapush_api.constants import ALL_POSSIBLE_OPERATORS, CONTRACTS_APP_NAME
from marshmallow import ValidationError


async def strip_params(params_dict):
    params_list = []
    for param in params_dict["filter"].split("and"):
        params_list.append(param.strip())

    return params_list


async def create_dict_for_validation(params_list):
    dict_for_validation = {}
    dicts_list = []

    for param in params_list:
        for operator in ALL_POSSIBLE_OPERATORS:
            if operator in param and operator == " in ":
                field_name = param.split(operator)[0]
                values_str = param.split(operator)[1][1:-1]
                values_str = values_str.replace(" ", "")
                values_list = values_str.split(",")

                for value in values_list:
                    dict_for_validation[field_name] = value
                    dicts_list.append(dict_for_validation)
                    dict_for_validation = {}

            elif operator in param:
                field_name = param.split(operator)[0]
                value = param.split(operator)[1]

                dict_for_validation[field_name] = value
                dicts_list.append(dict_for_validation)
                dict_for_validation = {}

    print("dicts_list", dicts_list)
    return dicts_list


async def validate_params(params_dict, service_name):
    # print("params:", params_dict)

    is_valid = True
    validator_msg = ""

    if params_dict == {}:
        is_valid = True
        return is_valid, validator_msg
    else:
        if "filter" not in list(params_dict.keys()) \
                or len(params_dict.keys()) > 1:
            is_valid = False
            validator_msg = "Invalid format of endpoint parameters!"
            return is_valid, validator_msg

        params_list = await strip_params(params_dict)
        print("params_list", params_list)
        parsed_data_list = await create_dict_for_validation(params_list)

        if service_name == CONTRACTS_APP_NAME:
            try:
                BandContractsSchema(many=True).load(parsed_data_list)
            except ValidationError as err:
                is_valid = False
                validator_msg = err.messages
                # print(validator_msg)
                return is_valid, str(validator_msg)
        else:
            try:
                BandPaymentsSchema(many=True).load(parsed_data_list)
            except ValidationError as err:
                is_valid = False
                validator_msg = err.messages
                # print(err.messages)
                return is_valid, str(validator_msg)

    return is_valid, validator_msg

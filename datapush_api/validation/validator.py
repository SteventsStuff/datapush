from datapush_api.validation.contracts_schema import BandContractsSchema
from datapush_api.validation.payments_schema import BandPaymentsSchema
from datapush_api.constants import ALL_POSSIBLE_OPERATORS, CONTRACTS_APP_NAME
from marshmallow import ValidationError
from dateutil import parser


async def strip_params(params_dict):
    # print("\nin func strip_params")
    print("params_dict", params_dict)
    params_list = []
    for param in params_dict["filter"].split("and"):
        print(param)
        # param = param.replace("  ", " ")
        params_list.append(param.strip())

    # print()
    return params_list


async def create_dict_for_validation(params_list):
    dict_for_validation = {}
    dicts_list = []

    for param in params_list:
        # print("current param", param)
        for operator in ALL_POSSIBLE_OPERATORS:
            # print("operator", operator)
            if operator in param and operator == " in ":
                field_name = param.split(operator)[0].strip()
                values_str = param.split(operator)[1].strip()[1:-1]
                # print("split", param.split(operator)[1][1:-1])
                values_str = values_str.replace(" ", "")
                values_list = values_str.split(",")

                for value in values_list:
                    print("param", param)
                    if value[0] == "'" and value[-1] == "'":
                        # print("split", values_str[1:-1])s
                        value = value[1:-1]
                    if "date" in field_name:
                        value = parser.parse(value).date()
                        print(value)
                    dict_for_validation[field_name] = value
                    dicts_list.append(dict_for_validation)
                    dict_for_validation = {}
                    # print("dict_for_validation", dict_for_validation)
                    # print("dicts_list", dicts_list)

            elif operator in param:
                # print("param in 'if' operator", param)
                field_name = param.split(operator)[0].strip()
                value = param.split(operator)[1].strip()
                if value[0] == "'" and value[-1] == "'":
                    # print("split", value[1:-1])
                    value = value[1:-1]
                if "date" in field_name:
                    value = parser.parse(value).date()
                    print(value)

                dict_for_validation[field_name] = value
                dicts_list.append(dict_for_validation)
                # print("dict_for_validation", dict_for_validation)
                # print("dicts_list", dicts_list)

                dict_for_validation = {}

    return dicts_list


async def validate_params(params_dict, service_name):
    print("params:", params_dict)

    is_valid = True
    validator_msg = ""

    if params_dict == {}:
        is_valid = True
        return is_valid, validator_msg
    else:
        if "filter" not in list(params_dict.keys()):
            is_valid = False
            validator_msg = "Invalid format of endpoint parameters!"
            return is_valid, validator_msg

        params_list = await strip_params(params_dict)
        print("params_list", params_list)
        parsed_data_list = await create_dict_for_validation(params_list)
        print("parsed_data_list", parsed_data_list)

        if service_name == CONTRACTS_APP_NAME:
            try:
                BandContractsSchema(many=True).dump(parsed_data_list)
            except ValidationError as err:
                is_valid = False
                validator_msg = err.messages
                return is_valid, str(validator_msg)
        else:
            try:
                BandPaymentsSchema(many=True).dump(parsed_data_list)
            except ValidationError as err:
                is_valid = False
                validator_msg = err.messages
                return is_valid, str(validator_msg)

    return is_valid, validator_msg

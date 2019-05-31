from datapush_api.constants import ALL_POSSIBLE_PARAMS_LIST
from dateutil.parser import parse


async def check_id(ids_list):
    is_valid = True
    msg = ""
    # print("id validator: ", ids_list)

    for id in ids_list:
        if len(id) != 36:
            is_valid = False
            msg = f"Error! Length of ID: {id} must be 36!"
            return is_valid, msg

        if id.count("-") != 4:
            is_valid = False
            msg = f"Error! Invalid ID: {id}!"
            return is_valid, msg

    return is_valid, msg


async def check_str_fields(strs_list):
    is_valid = True
    msg = ""
    # print("str validator: ", strs_list)
    for string in strs_list:
        if string == "":
            is_valid = False
            msg = "Error! String fields must be filled!"
            return is_valid, msg

    return is_valid, msg


async def check_amount(amounts_list):
    is_valid = True
    msg = ""
    # print("amount validator: ", amounts_list)

    for amount in amounts_list:
        try:
            f_amount = float(amount)
        except ValueError:
            is_valid = False
            msg = f"Error! amount: {amount} is not float value!"
            return is_valid, msg
        else:
            if f_amount < 0.0:
                is_valid = False
                msg = f"Error! amount: {amount} must be bigger then 0!"
                return is_valid, msg

    return is_valid, msg


async def check_date(dates_list):
    """complete it when i will know am i need to check time?"""
    is_valid = True
    msg = ""
    # print("date validator", dates_list)

    for date in dates_list:
        try:
            parse(date).date()
        except ValueError:
            msg = f"Error! {date} is not valid format for a date!"
            is_valid = False
            return is_valid, msg

    return is_valid, msg


async def validate_params(params_dict: dict):
    """Makes basic validation of every field
    in contracts

    Example of normal data:
    Contracts
    {
        "executor": "Electricite de France",
        "end_date": "2013-01-20",
        "customer": "Costco",
        "title": "Contract-211",
        "id": "ddbd1840-fb63-41e0-b830-802bcf4f356d",
        "start_date": "2012-02-05",
        "amount": 52200
    }
    Payments
    {
        "id": "ddbd1840-fb63-41e0-b830-802bcf4f356d",
        "contributor": "d9999999",
        "amount": 31.55,
        "date": "2019-05-04T05:34:05.287928-04:00",
        "contract_id": "0d571478-0953-4a20-a9f5-506974999228"
    }
    """
    # for now idk what type of datatime other services will use,
    # so i skip its validation
    is_valid = True
    validator_msg = ""

    # print(params_dict)
    if params_dict == {}:
        is_valid = True
    else:
        # check params name
        for key in params_dict:
            if key not in ALL_POSSIBLE_PARAMS_LIST:
                is_valid = False
                validator_msg = f"Error! You entered unknown parameter: {key}"
                return is_valid, validator_msg

        for key in params_dict:
            if key == "id" and is_valid:
                is_valid, validator_msg = await check_id(
                    params_dict[key].split(",")
                )
            if key in ("title", "customer", "executor") and is_valid:
                is_valid, validator_msg = await check_str_fields(
                    params_dict[key].split(",")
                )
            if key in ("end_date", "start_date") and is_valid:
                is_valid, validator_msg = await check_date(
                    params_dict[key].split(",")
                )
            if key == "amount" and is_valid:
                is_valid, validator_msg = await check_amount(
                    params_dict[key].split(",")
                )

    return is_valid, validator_msg

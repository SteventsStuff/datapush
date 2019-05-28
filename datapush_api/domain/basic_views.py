from datapush_api.constants import *
from http import HTTPStatus
import aiohttp
import logging


async def register_on_sda(request):
    """need to delete try block and make it througth if (check status code)"""
    try:
        async with aiohttp.ClientSession() as session:
            sda_response = await session.get(SDA_ADDRESS)

            if sda_response.status == HTTPStatus.OK:
                sda_response = await session.post(url=REGISTRATION_URL)

                if sda_response.status == HTTPStatus.OK:
                    logging.info("successful registration")
    except Exception as exc:
        logging.error(exc)


async def get_service_socket(service_name):
    service_socket = []
    sda_address = f"{SDA_ADDRESS}/{service_name}"

    try:
        async with aiohttp.ClientSession() as session:
            sda_response = await session.get(sda_address)
    except Exception as exc:
        logging.error(exc)

    decoded_response = await sda_response.text()
    raw_ip_port_list = decoded_response.split(",")

    service_socket.append(raw_ip_port_list[0][2:-1])
    service_socket.append(raw_ip_port_list[1][2:-2])

    url = f"http://{service_socket[0]}:{service_socket[1]}/{service_name}"
    return url


async def parse_url(url):
    return url[url.rfind("/") + 1:]


async def restructure_params(args):
    params = {}
    for key in args:
        params[key] = args[key][0]
    return params


async def validate_contacts_params(params):
    """
    {
        "executor": "Electricite de France",
        "end_date": "2013-01-20",
        "customer": "Costco",
        "title": "Contract-211",
        "id": "ddbd1840-fb63-41e0-b830-802bcf4f356d",
        "start_date": "2012-02-05",
        "amount": 52200
    }
    """
    pass


async def validate_payments_params(params):
    """
    {
        "id": "ddbd1840-fb63-41e0-b830-802bcf4f356d",
        "contributor": "d9999999",
        "amount": 31.55,
        "date": "2019-05-04T05:34:05.287928-04:00",
        "contract_id": "0d571478-0953-4a20-a9f5-506974999228"
    }
    """
    pass

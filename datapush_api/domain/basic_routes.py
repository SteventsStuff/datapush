from datapush_api.constants import *
import aiohttp
import logging


async def register_on_sda(request):
    """need to delete try block and make it througth if (check status code)"""
    try:
        async with aiohttp.ClientSession() as session:
            sda_response = await session.get(SDA_ADDRESS)

            if sda_response.status == 200:
                sda_response = await session.post(url=REGISTRATION_URL)
                if sda_response.status == 200:
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


"""



class ContractDomain(BaseDomain):
    pass


data = ContractDomain(url=url).get_instances()


async def get_contracts(request):
    url = await get_service_socket("contracts")  # Move to constants like CONTRACT_APP = 'contracts'
    print(url)
    params = request.args

    try:
        service_response = requests.get(url, params)
    except Exception as exc:
        logging.error(exc)
        return json({"Error": "Server is unavailable now, can't get contracts"})
    else:
        return json(service_response.json())
     if request.status > 200:
         pass
     else:
         pass

"""

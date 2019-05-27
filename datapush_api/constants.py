from datapush_api.config import Config


# names
DEFAULT_SERVICE_NAME = "datapush"
CONTRACTS_APP_NAME = "contracts"
PAYMENTS_APP_NAME = "payments"
# urls for SDA
SDA_ADDRESS = f"http://{Config.SDA_HOST}:{Config.SDA_PORT}"
REGISTRATION_URL = f"""{SDA_ADDRESS}/?name={DEFAULT_SERVICE_NAME}
&ip={Config.SDA_CONNECT}&port={Config.SERVICE_PORT}"""

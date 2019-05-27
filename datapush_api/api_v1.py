from sanic import Sanic
from datapush_api.constants import DEFAULT_SERVICE_NAME
from datapush_api.config import Config
from datapush_api.resource.smoke import Smoke
from datapush_api.resource.contracts import Contracts
from datapush_api.resource.payments import Payments
from datapush_api.resource.contracts_payments import ContractsPayments

# base app config
app = Sanic(DEFAULT_SERVICE_NAME)
app.config.from_object(Config)

# smoke endpoints
app.add_route(Smoke.as_view(), '/')
app.add_route(Smoke.as_view(), '/smoke')
# service endpoints
# general request endpoint
app.add_route(ContractsPayments.as_view(), '/contracts-payments')
# contracts
app.add_route(Contracts.as_view(), '/contracts')
app.add_route(Contracts.as_view(), '/contracts/id')
app.add_route(Contracts.as_view(), '/contracts/payments')
# payments
app.add_route(Payments.as_view(), '/payments')
app.add_route(Payments.as_view(), '/payments/id')
app.add_route(Payments.as_view(), '/payments/contracts')


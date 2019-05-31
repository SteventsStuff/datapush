from sanic.response import json
from sanic.response import file
from datapush_api.domain.payments import PaymentsDomain
from datapush_api.domain.contracts import ContractDomain
import json as non_sanic_json
import csv


async def general_request(contracts_url, payments_url, params):
    facts_and_dimensions = dict()

    res_contracts = await ContractDomain(
        url=contracts_url, params=params
    ).get_instances()
    res_payments = await PaymentsDomain(
        url=payments_url, params=params
    ).get_instance_by_key()

    facts_and_dimensions["facts"] = non_sanic_json.loads(
        res_payments.body.decode("utf-8")
    )
    facts_and_dimensions["dimensions"] = non_sanic_json.loads(
        res_contracts.body.decode("utf-8")
    )

    # file = open("contracts_and_payments.csv", "w")
    # csvwriter = csv.writer(file)
    # count = 0
    #
    # for i in facts_and_dimensions["facts"][0]:
    #     if count == 0:
    #         header = i.keys()
    #         csvwriter.writerow(header)
    #         count += 1
    #
    #     csvwriter.writerow(i.values())
    # file.close()

    return json(facts_and_dimensions)
    # from sanic import response
    # return await response.file('contracts_and_payments.csv')

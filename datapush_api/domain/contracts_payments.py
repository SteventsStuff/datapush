import fpdf
from sanic import response
from datapush_api.domain.base_domain import BaseDomain
import json as non_sanic_json
import csv


async def general_request(contracts_url, payments_url, params):
    facts_and_dimensions = dict()

    res_contracts = await BaseDomain(url=contracts_url).get_instances()
    res_payments = await BaseDomain(url=payments_url).get_instances()

    facts_and_dimensions["facts"] = non_sanic_json.loads(
        res_payments.body.decode("utf-8")
    )
    facts_and_dimensions["dimensions"] = non_sanic_json.loads(
        res_contracts.body.decode("utf-8")
    )

    result = response.json(facts_and_dimensions)

    if "output" in list(params.keys()):
        if params["output"].lower() == "json":
            result = response.json(facts_and_dimensions)
        elif params["output"].lower() == "csv":
            result = await create_cvs_file(facts_and_dimensions)
        elif params["output"].lower() == "pdf":
            result = await create_pdf_file(facts_and_dimensions)

    return result


async def create_cvs_file(facts_and_dimensions):
    filename = "contracts_and_payments.csv"
    file = open(filename, 'w')
    csvwriter = csv.writer(file, delimiter=';')
    count = 0

    for fact in facts_and_dimensions["facts"][0]:
        if count == 0:
            header = fact.keys()
            csvwriter.writerow(header)
            count += 1

        csvwriter.writerow(fact.values())
    count = 0

    for dim in facts_and_dimensions["dimensions"][0]:
        if count == 0:
            header = dim.keys()
            csvwriter.writerow(header)
            count += 1

        csvwriter.writerow(dim.values())

    file.close()

    return await response.file(file)


async def create_pdf_file(facts_and_dimensions):
    filename = "contracts_and_payments.pdf"
    pdf = fpdf.FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    col_width = pdf.w / 2.5
    row_height = pdf.font_size
    pdf.cell(200, 10, txt="Facts", ln=1, align="L")

    for fact in facts_and_dimensions["facts"][0]:
        for header in fact.keys():
            pdf.cell(pdf.w / 4.5, row_height, txt=header, border=1)
            pdf.cell(col_width, row_height, txt=str(fact[header]), border=1)
            pdf.ln(row_height)

        pdf.cell(200, 10, txt=" ", ln=1)

    pdf.cell(200, 10, txt="Dimensions", ln=1, align="L")

    for dim in facts_and_dimensions["dimensions"][0]:
        for header in dim.keys():
            pdf.cell(pdf.w / 4.5, row_height, txt=header, border=1)
            pdf.cell(col_width, row_height, txt=str(dim[header]), border=1)
            pdf.ln(row_height)

        pdf.cell(200, 10, txt=" ", ln=1)

    return await response.file(pdf.output(filename))

from main import app
import unittest


class TestContracts(unittest.TestCase):
    def test_get_contracts_title(self):
        request, response = app.test_client.get("/contracts?filter=title eq 'Contract-1'")
        self.assertEqual(response.status, 200)

    def test_get_contracts_executor(self):
        request, response = app.test_client.get("/contracts/?filter=executor eq 'Airbus Group'")
        self.assertEqual(response.status, 200)

    def test_get_contracts_customer(self):
        request, response = app.test_client.get("/contracts/?filter=customer eq 'SAIC Motor'")
        self.assertEqual(response.status, 200)

    def test_get_contracts_id(self):
        request, response = app.test_client.get("/contracts/?filter=id eq '849973b3-6f0f-4645-8af9-11c9a6d81984'")
        self.assertEqual(response.status, 200)

    def test_get_contract_by_id(self):
        request, response = app.test_client.get("/contract/d4fa26b6-302a-4caf-b7a1-2e8e6df22e69")
        self.assertEqual(response.status, 200)

    def test_get_contracts_amount_and_customer(self):
        request, response = app.test_client.get("/contracts/?filter=amount in ('16000','22800','47800') and customer eq 'Royal Ahold Delhaize'")
        self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()

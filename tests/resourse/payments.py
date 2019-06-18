from main import app
import unittest


class TestPayments(unittest.TestCase):
    def test_get_payments_title(self):
        request, response = app.test_client.get("/payment/264a17e2-1826-48a9-9ef6-39929b1df21b")
        self.assertEqual(response.status, 200)

    def test_get_payments_contributor(self):
        request, response = app.test_client.get("/payments/?filter=contributor eq 'Petrov21'")
        self.assertEqual(response.status, 200)

    def test_get_peyments_customer(self):
        request, response = app.test_client.get("/payments/?filter=amount in (157.55, 172.55)")
        self.assertEqual(response.status, 200)

    def test_get_payments_id(self):
        request, response = app.test_client.get("/payments/?filter=id eq '95463963-ae7b-40e8-9eeb-5a6e066dd887'")
        self.assertEqual(response.status, 200)

    def test_get_payments_date(self):
        request, response = app.test_client.get("/payments/?filter=date gt '2019-05-29'")
        self.assertEqual(response.status, 200)

    def test_get_payments_contracts(self):
        request, response = app.test_client.get("/payments/contracts/?filter=contract_id eq 'd60e5e1a-0cff-4d24-9977-e06ac1705250'")
        self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()

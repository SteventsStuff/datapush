from main import app
import json
import unittest


class AutoRestTests(unittest.TestCase):
    def test_get_smoke_1(self):
        request, response = app.test_client.get("/")
        self.assertEqual(response.status, 200)

        data = json.loads(response.text)
        self.assertEqual(data, "Service DataPush is running!")

    def test_get_smoke_2(self):
        request, response = app.test_client.get("/smoke")
        self.assertEqual(response.status, 200)

        data = json.loads(response.text)
        self.assertEqual(data, "Service DataPush is running!")


if __name__ == "__main__":
    unittest.main()
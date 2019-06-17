import unittest

from datapush_api.basic_views import get_service_socket, restructure_params


class TestBasicViews(unittest.TestCase):
    def setUp(self):
        pass

    async def test_restructure_params_one_parameter(self):
        params = {'filter': ["id in  ('1363330f-4d94-4def-9a3f-550116245ccb', '0d8f691e-2884-4fff-bbe6-750709896e3b')"]}
        expected = {'filter': "id in  ('1363330f-4d94-4def-9a3f-550116245ccb', '0d8f691e-2884-4fff-bbe6-750709896e3b')"}
        self.assertEqual(expected, await restructure_params(params))

    async def test_restructure_params_two_parameters(self):
        params = {'filter': ['amount ge 688.55 and amount le 772.55']}
        expected = {'filter': 'amount ge 688.55 and amount le 772.55'}
        self.assertEqual(expected, await restructure_params(params))

    async def test_restructure_params_three_parameters(self):
        params = {'filter': ["amount gt 50 and date lt '2019-05-29' and contributor ne 'Petrov21'"]}
        expected = {'filter': "amount gt 50 and date lt '2019-05-29' and contributor ne 'Petrov21'"}
        self.assertEqual(expected, await restructure_params(params))

    async def test_restructure_params_zero_parameters(self):
        params = {'filter': []}
        expected = {'filter': ""}
        self.assertEqual(expected, await restructure_params(params))

    async def test_restructure_params_empty_parameters(self):
        params = {}
        expected = {}
        self.assertEqual(expected, await restructure_params(params))

    async def test_get_service_socket(self):
        pass

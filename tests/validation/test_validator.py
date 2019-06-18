import unittest
from mock import Mock
import datetime
from datapush_api.validation.validator import(
    strip_params, validate_params, create_dict_for_validation,
    clear_value_from_garbage_chars
)


class TestValidator(unittest.TestCase):
    async def test_strip_params_one_params(self):
        args = {'filter': ["id in  ('1363330f-4d94-4def-9a3f-550116245ccb', '0d8f691e-2884-4fff-bbe6-750709896e3b')"]}
        expected = {'filter': "id in  ('1363330f-4d94-4def-9a3f-550116245ccb', '0d8f691e-2884-4fff-bbe6-750709896e3b')"}
        res = await strip_params(args)
        self.assertEqual(expected, res)

    async def test_strip_params_two_params_1(self):
        args = {'filter': ["amount gt 50 and date lt '2019-05-29' and contributor ne 'Petrov21'"]}
        expected = {'filter': "amount gt 50 and date lt '2019-05-29' and contributor ne 'Petrov21'"}
        self.assertEqual(expected, await strip_params(args))

    async def test_strip_params_two_params_2(self):
        args = {'filter': ["amount lt '93600' and amount ge '23400'"]}
        expected = {'filter': "amount lt '93600' and amount ge '23400'"}
        self.assertEqual(expected, await strip_params(args))

    async def test_clear_value_from_garbage_chars_str_with_space(self):
        value = 'SAIC Motor'
        field_name = 'customer'
        expected = 'SAIC Motor'
        self.assertEqual(expected, await clear_value_from_garbage_chars(value, field_name))

    async def test_clear_value_from_garbage_chars_with_char_float_value(self):
        value = '93600'
        field_name = 'amount'
        expected = 93600
        self.assertEqual(expected, await clear_value_from_garbage_chars(value, field_name))

    async def test_clear_value_from_garbage_chars_with_parentheses(self):
        value = '(15046.3)'
        field_name = 'amount'
        expected = 15046.3
        self.assertEqual(expected, await clear_value_from_garbage_chars(value, field_name))

    async def test_clear_value_from_garbage_chars_with_float_value(self):
        value = 25471.54
        field_name = 'amount'
        expected = 25471.54
        self.assertEqual(expected, await clear_value_from_garbage_chars(value, field_name))

    async def test_create_dict_for_validation_one_value(self):
        params_list = ["title eq 'Contract-1'"]
        expected = [{'title': 'Contract-1'}]
        self.assertEqual(expected, await create_dict_for_validation(params_list))

    async def test_create_dict_for_validation_two_values_with_operator_in(self):
        params_list = ["amount in ('16000','22800','47800')", "customer eq 'Royal Ahold Delhaize'"]
        expected = [{'amount': '16000'}, {'amount': '22800'}, {'amount': '47800'}, {'customer': 'Royal Ahold Delhaize'}]
        self.assertEqual(expected, await create_dict_for_validation(params_list))

    async def test_create_dict_for_validation_two_values_with_other_operators(self):
        params_list = ['amount gt 50', "date lt '2019-05-29'", "contributor ne 'Petrov21'"]
        expected = [{'amount': '50'}, {'date': datetime.date(2019, 5, 29)}, {'contributor': 'Petrov21'}]
        self.assertEqual(expected, await create_dict_for_validation(params_list))

    async def test_validate_params_validation_pass(self):
        strip_params_mock = Mock()
        create_dict_for_validation_mock = Mock()
        strip_params_mock.strip_params.return_value = ["amount lt '93600'", "amount ge '23400'"]
        create_dict_for_validation_mock.create_dict_for_validation.return_value = [{'amount': '93600'}, {'amount': '23400'}]

        params_dict = {'filter': "amount lt '93600' and amount ge '23400'"}
        service_name = 'payments'
        expected = True, ""
        self.assertEqual(expected, await validate_params(params_dict, service_name))

    async def test_validate_params_validation_invalid_operator(self):
        strip_params_mock = Mock()
        create_dict_for_validation_mock = Mock()
        strip_params_mock.strip_params.return_value = ["amount lt '93600'", "amount ge '23400'"]
        create_dict_for_validation_mock.create_dict_for_validation.return_value = [
            {'amount': '93600'}, {'amount': '23400'}]

        params_dict = 1
        service_name = 2
        expected = True, ""
        self.assertEqual(expected, await validate_params(params_dict, service_name))


if __name__ == '__main__':
    unittest.main()

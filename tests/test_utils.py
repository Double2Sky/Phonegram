import unittest
import os
from phonegram.utils.utils import get_phone_numbers
from phonegram.utils.errors import IncorrectPhoneNumberError


class GetPhoneNumbersTest(unittest.TestCase):
    def setUp(self) -> None:
        self.empty_file = 'empty'

        self.correct_file = 'correct'
        self.correct_numbers = ['81234567890', '8-123-456-78-90', '8(123)456-78-90', '8(123) 456 78-90',
                                '+7(123)456-78-90', '7123456-78-90', '71234567890', '7 123 456 78 90']

        self.incorrect_file = 'incorrect'
        self.incorrect_numbers = ['812345675890', '8-123-456-378-90', '15(123)456-78-90', '9(123) 456 78-90',
                                '+7(123)456-758-90', '712312456-78-90', '71fdf234567890', '7 123 456 78 90']

        with open(self.empty_file, 'w'):
            pass
        with open(self.correct_file, 'w') as file:
            file.write('\n'.join(self.correct_numbers))
        with open(self.incorrect_file, 'w') as file:
            file.write('\n'.join(self.incorrect_numbers))

    def tearDown(self) -> None:
        os.remove(self.empty_file)
        os.remove(self.correct_file)
        os.remove(self.incorrect_file)

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            get_phone_numbers('test')

    def test_empty_file(self):
        numbers = get_phone_numbers(self.empty_file)
        self.assertIsNotNone(numbers)
        self.assertTrue(numbers == [])

    def test_correct_file(self):
        numbers = get_phone_numbers(self.correct_file)
        self.assertEqual(numbers, self.correct_numbers)

    def test_incorrect_file(self):
        numbers = get_phone_numbers(self.incorrect_file)
        self.assertEqual(numbers, ['7 123 456 78 90'])

    def test_incorrect_file_exception(self):
        with self.assertRaises(IncorrectPhoneNumberError):
            get_phone_numbers(self.incorrect_file, ignore_incorrect=False)


if __name__ == '__main__':
    unittest.main()

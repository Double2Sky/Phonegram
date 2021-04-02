import unittest
import os
import configparser
from phonegram.config import constants
from phonegram.config.session import SessionConfig


class SessionTest(unittest.TestCase):
    def setUp(self) -> None:
        # Create empty file
        self.empty_filename = 'empty_file'
        with open(self.empty_filename, 'w'):
            pass

        # Create file with credentials section
        self.credentials_filename = 'credentials_file'
        parser = configparser.ConfigParser()
        parser.add_section(constants.CLIENT_CREDENTIALS_SECTION)
        with open(self.credentials_filename, 'w', encoding='utf-8') as file:
            parser.write(file)

    def tearDown(self) -> None:
        os.remove(self.empty_filename)
        os.remove(self.credentials_filename)

    def test_incorrect_initialize(self):
        with self.assertRaises(FileNotFoundError):
            SessionConfig.initialize('test')

    def test_file_without_credentials_section(self):
        with self.assertRaises(configparser.Error):
            SessionConfig.initialize(self.empty_filename)

    def test_file_without_session_section(self):
        obj = SessionConfig.initialize(self.credentials_filename)
        self.assertIsNotNone(obj)
        self.assertTrue(obj._parser.has_section(constants.SESSION_STRINGS_SECTION))

    def test_empty_session_strings(self):
        obj = SessionConfig.initialize(self.credentials_filename)
        self.assertIsNone(obj.session_strings)

    def test_not_api_id(self):
        obj = SessionConfig.initialize(self.credentials_filename)
        with self.assertRaises(configparser.Error):
            api_id = obj.api_id

    def test_not_hash_id(self):
        obj = SessionConfig.initialize(self.credentials_filename)
        with self.assertRaises(configparser.Error):
            api_hash = obj.api_hash

    def test_dump_config(self):
        obj = SessionConfig.initialize(self.credentials_filename)
        obj._parser.set(constants.CLIENT_CREDENTIALS_SECTION, 'test', 'test_value')
        obj.dump()

        parser = configparser.ConfigParser()
        parser.read(self.credentials_filename)
        self.assertTrue(parser.has_option(constants.CLIENT_CREDENTIALS_SECTION, 'test'))


if __name__ == '__main__':
    unittest.main()

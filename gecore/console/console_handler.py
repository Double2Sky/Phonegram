import argparse
import configparser
import logging
import os

logger = logging.getLogger('console_handler')

SESSION_STRINGS_SECTION = 'SESSION_STRINGS'
CLIENT_CREDENTIALS_SECTION = 'CLIENT_CREDENTIALS'


class ConsoleHandler:
    NAME = 'gecore'
    DESCRIPTION = 'Gecore = GetContact Requests.'
    EPILOG = 'LPSHKN, 2021'

    def __init__(self, args):
        self._parser = self._get_parser(ConsoleHandler.NAME, ConsoleHandler.DESCRIPTION, ConsoleHandler.EPILOG)

        # Parser of the config file
        self._config_parser = None

        # Get parameters from the arguments received from the command line
        self._init_parameters(args)

    @staticmethod
    def _get_parser(program_name: str = None, description: str = None, epilog: str = None) -> argparse.ArgumentParser:
        """
        Method creates the instance of the ArgumentParser class, adds arguments in here and returns that instance.
        :param program_name: name of the program
        :param description: description of the program
        :param epilog: epilog of the program
        :return: an instance of the ArgumentParser class
        """
        parser = argparse.ArgumentParser(prog=program_name, description=description, epilog=epilog)

        parser.add_argument('-c', '--credentials',
                            help='the config file, containing credentials for a telegram client: api_id, api_hash and '
                                 'session strings',
                            default='./config/session.cfg',
                            type=str)

        parser.add_argument('-b', '--bots',
                            help='the config file, containing information about bots',
                            default='./config/bots.cfg',
                            type=str)

        return parser

    def _init_parameters(self, args):
        """
        This method gets all parameters from the args of the command line.
        :param args: list of the arguments of the command line
        :return: parsed arguments
        """
        parameters = self._parser.parse_args(args)

        if not os.path.exists(parameters.credentials):
            logger.error("The configuration file doesn't exist")
            exit(-1)

        self._parameters = parameters
        self._read_config_file()

    def _read_config_file(self):
        # Read the config file
        self._config_parser = configparser.ConfigParser()
        try:
            self._config_parser.read(self.session_file, encoding='utf-8')
            if not self._config_parser.has_section(SESSION_STRINGS_SECTION):
                self._config_parser.add_section(SESSION_STRINGS_SECTION)
        except configparser.Error as error:
            logger.error(error)
            exit(-2)

    @property
    def credentials(self):
        """
        Method reads gets a tuple of API_ID, API_HASH from the config file
        are necessary for the Telegram Client API

        :return: tuple API_ID, API_HASH
        """
        try:
            api_id = self._config_parser.get(CLIENT_CREDENTIALS_SECTION, 'API_ID')
            api_hash = self._config_parser.get(CLIENT_CREDENTIALS_SECTION, 'API_HASH')

            return api_id, api_hash
        except configparser.NoSectionError:
            logger.error(f"The configuration file doesn't contain [{CLIENT_CREDENTIALS_SECTION}] section, please insert "
                         "this section with the API_ID and API_HASH options")
            exit(-3)
        except configparser.NoOptionError:
            logger.error("The configuration file doesn't contain the API_ID or API_HASH options")
            exit(-4)

    @property
    def config_parser(self) -> configparser.ConfigParser:
        return self._config_parser

    @property
    def session_file(self):
        return self._parameters.credentials

    def dump_session_file(self):
        with open(self.session_file, 'w') as file:
            self.config_parser.write(file)
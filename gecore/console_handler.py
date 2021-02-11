import argparse
import configparser
import logging
import os

logger = logging.getLogger('console_handler')


class ConsoleHandler:
    NAME = 'gecore'
    DESCRIPTION = 'Gecore = GetContact Requests.'
    EPILOG = 'LPSHKN, 2021'

    def __init__(self, args):
        self._parser = self._get_parser(ConsoleHandler.NAME, ConsoleHandler.DESCRIPTION, ConsoleHandler.EPILOG)

        # Parser of the config file
        self._config_parser = None

        # Get parameters from the arguments received from the command line
        self._parameters = self._get_parameters(args)

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

        parser.add_argument('config',
                            help='the config file, containing credentials for a telegram client: api_id, api_hash or '
                                 'other parameters',
                            type=str)

        parser.add_argument('phone_number',
                            help='the number of phone that will be passed to the GetContact bot',
                            type=str)

        return parser

    def _get_parameters(self, args):
        """
        This method gets all parameters from the args of the command line.
        :param args: list of the arguments of the command line
        :return: parsed arguments
        """
        parameters = self._parser.parse_args(args)

        if not os.path.exists(parameters.config):
            logger.error("The configuration file doesn't exist")
            exit(-1)

        # Read the config file
        self._config_parser = configparser.ConfigParser()
        try:
            self._config_parser.read(parameters.config, encoding='utf-8')
        except configparser.Error as error:
            logger.error(error)
            exit(-2)

        return parameters

    @property
    def credentials(self):
        """
        Method reads gets a pair API_ID, API_HASH from the config file are necessary for the Telegram Api Client

        :return: pair API_ID, API_HASH
        """
        try:
            api_id = self._config_parser.get('TELEGRAM_API', 'API_ID')
            api_hash = self._config_parser.get('TELEGRAM_API', 'API_HASH')

            return api_id, api_hash
        except configparser.NoSectionError:
            logger.error("The configuration file doesn't contain [TELEGRAM_API] section, please insert this section "
                         "with the API_ID and API_HASH options")
            exit(-3)
        except configparser.NoOptionError:
            logger.error("The configuration file doesn't contain the API_ID and API_HASH options")
            exit(-4)

    @property
    def phone_number(self):
        return self._parameters.phone_number

import argparse
import codecs
import logging
import os
import sys
import json

logger = logging.getLogger('console_handler')


class ConsoleHandler:
    NAME = 'phonegram'
<<<<<<< HEAD:phonegram/console/console_handler.py
    DESCRIPTION = 'Phonegram - Aggregator of OSINT Telegram bots.'
=======
    DESCRIPTION = 'Aggregator of OSINT Telegram bots.'
>>>>>>> develop:phonegram/console_handler.py
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
        subparsers = parser.add_subparsers(title='Commands', dest='command')

        # Request mode
        request_mode = subparsers.add_parser('request',
                                             help='make a request to the bots')

        request_mode.add_argument('number',
                                  help='the phone number that will be passed to bots',
                                  type=str)

        request_mode.add_argument('-c', '--credentials',
                                  help='the config file, containing credentials for a telegram client: '
                                       'api_id, api_hash and session strings',
                                  default='./config/session.cfg',
                                  type=str)

        request_mode.add_argument('-b', '--bots',
                                  help='the config file, containing information about bots',
                                  default='./config/bots.json',
                                  type=str)

        request_mode.add_argument('-o', '--output',
                                  help='where the output result will print to (stdout by default)',
                                  default=sys.stdout,
                                  type=argparse.FileType(mode='w', encoding='utf-8'))

        # Setting mode
        setting_mode = subparsers.add_parser('setting',
                                             help='add session strings in the config file')

        setting_mode.add_argument('-c', '--credentials',
                                  help='the config file, containing credentials for a telegram client: '
                                       'api_id, api_hash and session strings',
                                  default='./config/session.cfg',
                                  type=str)

        return parser

    def _init_parameters(self, args):
        """
        This method gets all parameters from the args of the command line.
        :param args: list of the arguments of the command line
        :return: parsed arguments
        """
        parameters = self._parser.parse_args(args)

        if parameters.command is None:
<<<<<<< HEAD:phonegram/console/console_handler.py
            self._parser.error("Вам необходимо задать одну из двух команд: setting (для настройки) "
                               "или request (для запроса)")
=======
            self._parser.error("Вы не выбрали ни один режим работы. Выберите setting или request.")
>>>>>>> develop:phonegram/console_handler.py

        if not os.path.exists(parameters.credentials):
            logger.error("The configuration file doesn't exist")
            exit(-1)

        if parameters.command == 'request' and not os.path.exists(parameters.bots):
            logger.error("The bots config file doesn't exist")
            exit(-1)

        self._parameters = parameters

    @property
    def phone_number(self):
        return self._parameters.number

    def to_out(self, response: str):
        """
        Save the response into the file (stdout by default).

        :param response: that will be saved
        """
        if self._parameters.output is None:
            print(response)
        else:
            self._parameters.output.write(response)
            self._parameters.output.close()

    @property
    def mode(self):
        return self._parameters.command

    @property
    def bots(self):
        with codecs.open(self._parameters.bots, 'r', encoding='utf-8') as file:
            return json.load(file)

    @property
    def credentials_filename(self):
        return self._parameters.credentials

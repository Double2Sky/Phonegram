import os
import configparser
from typing import AbstractSet

from phonegram.config import constants


class SessionConfig:
    _parser: configparser.ConfigParser
    _config_filename: str

    @classmethod
    def initialize(cls, filename: str):
        """
        Creates the SessionConfig object and reads the config file.

        :param filename: the name of the session config file
        :return: SessionConfig object
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Указанный файл '{filename}' конфигурации сессии не найден")

        # Read the config file
        session_config = SessionConfig()
        session_config._config_filename = filename
        session_config._parser = configparser.ConfigParser()
        session_config._parser.read(filename, encoding='utf-8')

        if not session_config._parser.has_section(constants.CLIENT_CREDENTIALS_SECTION):
            raise configparser.Error(f"Конфигурационный файл сессии не содержит секции "
                                     f"{constants.CLIENT_CREDENTIALS_SECTION}, пожалуйста, добавьте её")

        # Session strings may be omitted. Therefore, creates its section
        if not session_config._parser.has_section(constants.SESSION_STRINGS_SECTION):
            session_config._parser.add_section(constants.SESSION_STRINGS_SECTION)

        return session_config

    @property
    def api_id(self) -> int:
        """
        Returns api_id of a Telegram client from the session config file

        :return: (int) api_id
        """
        try:
            api_id = int(self._parser.get(constants.CLIENT_CREDENTIALS_SECTION, 'API_ID'))
            return api_id
        except configparser.NoSectionError:
            raise configparser.Error(f"Конфигурационный файл сессии не содержит секции "
                                     f"{constants.CLIENT_CREDENTIALS_SECTION}, пожалуйста, добавьте её")
        except configparser.NoOptionError:
            raise configparser.Error("Конфигурационный файл сессии не содержит опции API_ID, пожалуйста, "
                                     "добавьте её")

    @property
    def api_hash(self) -> str:
        """
        Returns api_hash of a Telegram client from the session config file

        :return: (str) api_hash
        """
        try:
            return self._parser.get(constants.CLIENT_CREDENTIALS_SECTION, 'API_HASH')
        except configparser.NoSectionError:
            raise configparser.Error(f"Конфигурационный файл сессии не содержит секции "
                                     f"{constants.CLIENT_CREDENTIALS_SECTION}, пожалуйста, добавьте её")
        except configparser.NoOptionError:
            raise configparser.Error("Конфигурационный файл сессии не содержит опции API_HASH, пожалуйста, "
                                     "добавьте её")

    @property
    def session_strings(self) -> AbstractSet[tuple[str, str]]:
        """
        Returns pair <user_id, session_string> from the session config file.
        This session string allow to authorize in the Telegram client.

        :return: (tuple[str, str]) pairs of <user_id, session_string> or None if it's empty
        """
        try:
            return self._parser[constants.SESSION_STRINGS_SECTION].items()
        except configparser.NoSectionError:
            raise configparser.Error(f"Конфигурационный файл сессии не содержит секции "
                                     f"{constants.SESSION_STRINGS_SECTION}, пожалуйста, добавьте её")

    def dump(self):
        """
        Dumps the parser in the session config file.
        """
        with open(self._config_filename, 'w', encoding='utf-8') as file:
            self._parser.write(file)

    def add_session_string(self, user_id: str, session_string: str, dump=True):
        """
        Adds a session string in the session config file.
        If dump is true, immediately dumps new changes into the config file.

        :param user_id: (int) the id of a user
        :param session_string: (str) the session string that must be serialized
        :param dump: (bool) if it's true, dumps changes into the config file
        """
        self._parser.set(constants.SESSION_STRINGS_SECTION, user_id, session_string)
        if dump:
            self.dump()

    def remove_session_string(self, user_id: str, dump=True):
        """
        Remove a session string from the session config file.
        If dump is true, immediately dumps new changes into the config file.

        :param user_id: (int) the id of a user
        :param dump: (bool) if it's true, dumps changes into the config file
        """
        self._parser.remove_option(constants.SESSION_STRINGS_SECTION, user_id)
        if dump:
            self.dump()

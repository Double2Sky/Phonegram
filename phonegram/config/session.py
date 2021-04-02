import os
from configparser import ConfigParser
from phonegram.config import constants


class SessionConfig(ConfigParser):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create(filename: str):
        """
        Creates the SessionConfig object and reads the config file.

        :param filename: the name of the session config file
        :return: SessionConfig object
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Указанный файл '{filename}' конфигурации сессии не найден")

        # Read the config file
        session_config = SessionConfig()
        session_config.read(filename, encoding='utf-8')

        # Session strings may be omitted. Therefore, creates its section
        if not session_config.has_section(constants.SESSION_STRINGS_SECTION):
            session_config.add_section(constants.SESSION_STRINGS_SECTION)

        return session_config
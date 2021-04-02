import os
import configparser
from phonegram.config import constants


class SessionConfig(configparser.ConfigParser):
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

    @property
    def api_id(self) -> int:
        """
        Returns api_id of a Telegram client from the session config file

        :return: (int) api_id
        """
        try:
            api_id = int(self.get(constants.CLIENT_CREDENTIALS_SECTION, 'API_ID'))
            return api_id
        except configparser.NoSectionError:
            raise configparser.Error(f"Конфигурационный файл сессии не содержит секции "
                                     f"{constants.CLIENT_CREDENTIALS_SECTION}, пожалуйста, добавьте её")

        except configparser.NoOptionError:
            raise configparser.Error("Конфигурационный файл сессии не содержит опции API_ID, пожалуйста, "
                                     "добавьте её")

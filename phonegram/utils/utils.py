import logging
import re
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from phonegram.utils.constants import PHONE_NUMBER_REGEX
from phonegram.utils.errors import IncorrectPhoneNumberError

logging.basicConfig(format='\n[%(asctime)s]: %(message)s\n')


async def get_session_string(api_id, api_hash, verbose=True):
    """
    Function makes connection to the Telegram client and returns the session string of this connection.

    :param api_id: api_id of the client
    :param api_hash: api_hash of the client
    :param verbose: if it's True, a user will see a dialog message in the console
    :return: pair <username, session_string>
    """
    try:
        if verbose:
            while True:
                answer = input("Хотите открыть новую сессию? (да/нет): ")
                if re.match('(да|нет|д|н)', answer, re.IGNORECASE):
                    break
                else:
                    print("Некорректный ввод.")
            if re.match('(нет|н)', answer, re.IGNORECASE):
                return None

        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.start(phone=lambda: input("Пожалуйста, введите ваш номер телефона: "),
                           code_callback=lambda: input("Пожалуйста, введите полученный код подтверждения: "))

        user = await client.get_me()
        user_id = str(user.id)

        session_string = client.session.save()
        await client.disconnect()

        return user_id, session_string

    except PhoneNumberInvalidError:
        logging.error("The invalid number was entered")
        exit(-1)
    except RuntimeError:
        logging.error("3 consecutive sign-in attempts failed. Aborting")
        exit(-1)
    except Exception as e:
        logging.error(e)
        exit(-1)


def get_regex(strings: list):
    """
    Compiles the regular expression from the list of patterns.

    :param strings: a list of patterns
    :return: regex
    """
    return re.compile("(" + "|".join(strings) + ")", re.IGNORECASE)


def get_phone_numbers(filename: str, ignore_incorrect=True) -> list[str]:
    """
    Obtain a list of phone numbers from the file.

    :param filename: the name of a file containing a list of numbers
    :param ignore_incorrect: specifies if an incorrect phone number met, skip it, else raise an exception
    :return: a list of phone numbers
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл со списком мобильных номеров по заданному пути {filename} не найден, "
                                f"либо вы некорректно ввели номер телефона")

    with open(filename, 'r', encoding='utf-8') as file:
        strings = re.split(r'\n+', file.read())

    phone_numbers = []
    if ignore_incorrect:
        phone_numbers = [phone_number.strip() for phone_number in strings
                         if PHONE_NUMBER_REGEX.match(phone_number)]
    else:
        for phone_number in strings:
            if PHONE_NUMBER_REGEX.match(phone_number):
                phone_numbers.append(phone_number)
            else:
                raise IncorrectPhoneNumberError(phone_number)

    return phone_numbers

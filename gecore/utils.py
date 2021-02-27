import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

logging.basicConfig(format='\n[%(asctime)s]: %(message)s\n')


async def get_session_string(api_id, api_hash):
    """
    Function makes connection to the Telegram client and returns the session string of this connection.

    :param api_id: api_id of the client
    :param api_hash: api_hash of the client
    :return: session string
    """
    try:
        async with TelegramClient(StringSession(), api_id, api_hash) as client:
            return client.session.save()
    except PhoneNumberInvalidError:
        logging.error("The invalid number was entered")
        exit(-1)
    except RuntimeError:
        logging.error("3 consecutive sign-in attempts failed. Aborting")
        exit(-1)
    except Exception as e:
        logging.error(e)
        exit(-1)
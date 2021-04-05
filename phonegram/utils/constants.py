import re


PHONE_NUMBER_REGEX = re.compile(r'^\s*(\+?7|8)[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*\d{2}[-. ]*\d{2}\s*$')

import string
import random
from app.core.constants import URL_SHORT_CODE_LENGTH


def generate_short_code() -> str:
    """
    Generate a random short code for URL.
    """
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=URL_SHORT_CODE_LENGTH))

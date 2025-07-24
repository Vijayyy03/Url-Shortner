import random
import string
import re
from urllib.parse import urlparse

def generate_short_code(length=6):
    """Generate a random alphanumeric short code of given length."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def is_valid_url(url):
    """Basic URL validation using urlparse and regex for http(s) schemes."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        # Optional: simple regex for valid URL structure
        regex = re.compile(
            r'^(http|https)://[\w.-]+(?:\.[\w\.-]+)+[/#?]?.*$', re.IGNORECASE)
        return re.match(regex, url) is not None
    except Exception:
        return False
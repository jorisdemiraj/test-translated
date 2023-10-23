from . import *

#util function that generates randomly 6 characters and returns it to be used for the short url
def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code

#a url parser function that takes the url, gets the last 6 letters to be used to search for the long url
def parse_url(url):
    if "http" in url or "/" in url:
        parts = url.split("/")
        return parts[-1]
    return url
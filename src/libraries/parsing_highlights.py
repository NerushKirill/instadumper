import requests

from bs4 import BeautifulSoup

from settings import settings


def list_highlights(url: str, site: str = settings.site) -> dict:
    """
    Get a list of all highlights sections.

    :param site:
    :param url:
    :return: dict
    """

    # Send a request to the server and receive the HTML code of the page
    response = requests.get(url)
    html = response.text

    # Use BeautifulSoup to parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Find all 'a' tags where the 'href' attribute value contains the substring '/highlights/user_nickname/'
    highlight_links = [
        site + a.get("href")
        for a in soup.find_all("a", href=lambda x: x and url.replace(site, "") in x)
    ]
    # Find titles highlight_links
    signs = [tag.text for tag in soup.find_all("p", class_="has-text-weight-semibold")]

    response = dict(zip(signs, set(highlight_links[1:])))

    normalized_response = {
        key.lower().replace(" ", "^").encode("utf-8").decode("utf-8") + "_": value
        for key, value in response.items()
    }

    return normalized_response

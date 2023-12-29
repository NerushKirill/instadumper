import requests

from bs4 import BeautifulSoup

from settings import settings

from src.libraries.supporting import add_data
from src.libraries.supporting import clean_lists


def parser_main(
    url: str,
    out_file: str,
    type_: str = None,
    sign: str = "",
    media_link: str = settings.media_link,
) -> dict:
    """
    Gets links of all media files from a page.

    :param media_link:
    :param url:
    :param out_file:
    :param type_:
    :param sign:
    :return:
    """

    data = {}

    response = requests.get(url)
    html = response.text

    # Парсинг HTML
    soup = BeautifulSoup(html, "html.parser")

    # Находим все теги <img> и <video>
    img_tags = soup.find_all("img")
    video_tags = soup.find_all("video")

    # Собираем ссылки на изображения / видео
    image_urls = [img["src"] for img in img_tags]
    video_urls = [video.source["src"] for video in video_tags]

    for link in image_urls:
        if media_link in link:
            match type_:
                case "posts":
                    if "1080x1080" in link:
                        data = add_data(data, out_file, link, "img_")
                case _:
                    data = add_data(data, out_file, link, "img_" + sign)

    for link in video_urls:
        data = add_data(data, out_file, link, "video_" + sign)

    data_out = clean_lists(data)

    return data_out

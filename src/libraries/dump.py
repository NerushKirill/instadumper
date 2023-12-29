import os
import hashlib
import requests


def download(path, url) -> None:
    response = requests.get(url)

    if response.status_code == 200:
        file_format = ".other"
        if "jpg" in url:
            file_format = ".jpg"
        elif "mp4" in url:
            file_format = ".mp4"

        file_name = hashlib.md5(url.encode()).hexdigest() + file_format
        file_path = os.path.join(path, file_name)

        with open(file_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download from {url}. Status code: {response.status_code}")


def dumping(data: dict, out_path: str) -> None:
    for k, v in data.items():
        path = os.path.join(out_path, k)

        if not os.path.exists(path):
            os.makedirs(path)

        if isinstance(v, dict):
            dumping(v, path)
        elif isinstance(v, list):
            for i in v:
                download(path, i)

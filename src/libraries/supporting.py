# TODO add documentation
# TODO filter methods
# TODO remove unused methods

import os
import re
import datetime
import json
import requests
import hashlib


def add_data(data: dict, key_: str, values_: str, sign_: str = "") -> dict:
    """

    :param data:
    :param key_:
    :param values_:
    :param sign_:
    :return:
    """
    key: str = str(sign_) + str(key_)

    if data.get(key):
        data[key].append(values_)
    else:
        data[key] = []
        data[key].append(values_)

    return data


def clean_lists(data: dict) -> dict:
    """
    Drop duplicates in list.

    :param data:
    :return:
    """
    for key, value in data.items():
        if isinstance(value, list):
            # Keep only unique values in the list
            data[key] = list(set(value))
        elif isinstance(value, dict):
            # Call clean_lists recursively for nested dictionaries
            data[key] = clean_lists(value)

    return data


def to_json(data: dict, out_path: str, file_name: str) -> None:
    """

    :param data:
    :param out_path:
    :param file_name:
    :return:
    """

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    file_ = os.path.join(out_path, file_name + ".json")

    with open(file_, "w", encoding="utf-8") as f:
        json.dump(data, f)


def read_json(file: str) -> dict:
    """

    :param file:
    :return:
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def find_actual(out_dir: str) -> dict:
    """

    :param out_dir:
    :return:
    """
    actual = {"name": "no_dump", "date": None}
    data_ = []

    if os.path.exists(out_dir):
        list_urls_dump = [i for i in os.listdir(out_dir) if "data_" in i]

        for dump in list_urls_dump:
            date_time = re.findall(r"\((.*?)\)", dump)
            if date_time:
                data_.append({"name": dump, "date": date_time[0]})

        if data_:
            actual = sorted(
                data_,
                key=lambda x: datetime.datetime.strptime(x["date"], "%H-%M_%d-%m-%Y"),
                reverse=True,
            )[0]

    return actual


def check_sum(data: list) -> set:
    """

    :param data:
    :return:
    """
    data = {hashlib.md5(i.encode()).hexdigest() for i in data}
    return data


def unpacking_data(data: dict, out_tasks: list) -> list:
    """

    :param data:
    :param out_tasks:
    :return:
    """

    if data:
        for key, value in data.items():
            if isinstance(value, list):
                out_tasks += value
            elif isinstance(value, dict):
                # Recursively call unpacking_data for nested dictionaries
                unpacking_data(value, out_tasks)

    return out_tasks


def get_hash_dump(out_dir: str, dump: dict) -> set:
    """

    :param out_dir:
    :param dump:
    :return:
    """
    file_dump = os.path.join(out_dir, dump["name"])
    data_dump = read_json(file_dump)
    all_urls = unpacking_data(data_dump, [])
    hash_dump = check_sum(all_urls)
    return hash_dump


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


def pars_dict(data, parent_key="", sep="_"):
    result = {}
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            result.update(pars_dict(v, new_key, sep=sep))
        else:
            result[new_key] = v
    return result


def data_for_db(user: str, data: dict) -> list:
    to_db = []

    for key in data.keys():
        file_chapter = key.split("_")[-1]
        albums = re.findall(r"_(.*?)_", key)
        data_type = key.split("_")[-2]

        album = albums[0] if albums else None

        for link in data[key]:
            to_db.append(
                {
                    "user_name": user,
                    "file_chapter": file_chapter,
                    "album": album,
                    "data_type": data_type,
                    "url": link[:-2],
                    "hash": hashlib.md5(link.encode()).hexdigest(),
                }
            )

    return to_db

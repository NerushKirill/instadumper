# TODO add methods for interacting with the database
# TODO add a method to clear out-of-date url_dumps
# TODO add method restoring a dump from a database
# add integration with google drive

import os
import datetime
import pytz
import logging

from settings import settings

from src.libraries import parser_main
from src.libraries import list_highlights

# from src.libraries import dumping

from src.libraries import to_json
from src.libraries import find_actual
from src.libraries import get_hash_dump
from src.libraries import dumping
from src.libraries import pars_dict
from src.libraries import data_for_db
from src.libraries import read_json

from src.models.crud import get_hash_from_db

logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(settings.persistence_vault, "log.log"),
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)


class Parsing:
    # TODO add a method to create a hash matching file

    def __init__(self, user):
        self.user = user

        self._update_frequency = 6  # default - once every 6 hours

        self.__site = settings.site
        # self.__media_link = settings.media_link

        self.default_dir = settings.persistence_vault  # default = "storage"
        self.timezone = pytz.timezone("Europe/Moscow")
        self.dt_format = "%H-%M_%d-%m-%Y"
        self.control_sum_name = "control.sum"

        self.out_dir = os.path.join(self.default_dir, f"downloads_{self.user}")

        self.url_stories = f"{self.__site}/stories/{self.user}"
        self.url_highlights = f"{self.__site}/highlights/{self.user}"
        self.url_posts = f"{self.__site}/posts/{self.user}"

    def get_stories(self) -> dict:
        # get url stories
        data_stories = parser_main(self.url_stories, "stories", type_="stories")
        return data_stories

    def get_posts(self) -> dict:
        # get url posts
        data_posts = parser_main(self.url_posts, "posts", type_="posts")
        return data_posts

    def get_highlights(self) -> dict:
        highlight_links = list_highlights(self.url_highlights)

        data_highlights: dict = {}

        for sign, url in highlight_links.items():
            data_highlights[sign.strip("_")] = parser_main(
                url, "highlights", type_="highlights"
            )
        return data_highlights

    def get_all(self) -> dict:
        all_urls: dict = {
            "stories": self.get_stories(),
            "posts": self.get_posts(),
            "highlights": self.get_highlights(),
        }

        return all_urls

    def get_actual_dump(self) -> dict:
        actual_dump: dict = find_actual(self.out_dir)
        return actual_dump

    def create_urls_dump(self) -> dict:
        marker = (
            datetime.datetime.now().astimezone(self.timezone).strftime(self.dt_format)
        )

        name = f"data_({marker})"
        to_json(data=self.get_all(), out_path=self.out_dir, file_name=name)

        logging.info(f"loading urls dump for user {self.user}")

        return {"name": name + ".json", "date": marker}

    def restore_sum_from_db(self, overwrite_existing: bool = False) -> bool:
        """
        Loading the current dump from the database.
        Since we believe that the database contains the entire publication history
        (including remote ones).
        """
        file_summ = os.path.join(self.out_dir, self.control_sum_name)
        response = False

        if not os.path.isfile(file_summ) or overwrite_existing:
            db_hash = get_hash_from_db(self.user)

            if not os.path.exists(self.out_dir):
                os.makedirs(self.out_dir)

            with open(file_summ, "w", encoding="utf-8") as f:
                for hash_line in db_hash:
                    f.write(hash_line + "\n")

            logging.info(f"restore {self.control_sum_name} for data {self.user} ")

            response = True
        else:
            logging.warning(
                f"restore fail, file {self.control_sum_name} already exists for data {self.user}, "
                f"overwrite_existing={overwrite_existing}"
            )

            print(
                """The recovery was not completed because there is already a file with a checksum. 
                If you want to overwrite, set 'overwrite_existing' to True."""
            )

        return response

    def create_control_sum(self) -> set:
        # TODO rewrite use restore_sum_from_db
        file_summ = os.path.join(self.out_dir, self.control_sum_name)

        # consider replacing it with creating an actual dump when calling the function
        # get_actual_dump() -> create_urls_dump()
        actual_dump: dict = self.get_actual_dump()

        if actual_dump["date"]:
            ad_hash: set = get_hash_dump(self.out_dir, actual_dump)
        else:
            actual_dump = self.create_urls_dump()
            ad_hash: set = get_hash_dump(self.out_dir, actual_dump)

        if os.path.isfile(file_summ):
            with open(file_summ, "r", encoding="utf-8") as f:
                control_sum = set(line.strip() for line in f)
            delta = ad_hash - control_sum
        else:
            delta = ad_hash

        with open(file_summ, "a", encoding="utf-8") as f:
            for hash_line in delta:
                f.write(hash_line + "\n")

        logging.info(
            f"create {self.control_sum_name} for data {self.user} actual dump - {actual_dump['name']}"
        )

        return delta

    def compare_control_sum(self):
        file_summ = os.path.join(self.out_dir, self.control_sum_name)

        if os.path.isfile(file_summ):
            with open(file_summ, "r", encoding="utf-8") as f:
                local_control_sum = set(line.strip() for line in f)
        else:
            local_control_sum = self.create_control_sum()

        db_hash = get_hash_from_db(self.user)

        # db_hash.symmetric_difference(file_summ) - outer join
        return db_hash - local_control_sum

    def create_dump(self) -> None:
        dump = os.path.join(self.out_dir, "dump")
        delta_time: float = self._update_frequency + 1
        actual_dump: dict = self.get_actual_dump()

        if actual_dump["date"]:
            now = datetime.datetime.now().astimezone(self.timezone)

            # Pay attention to the default timezones
            dt = datetime.datetime.strptime(
                actual_dump["date"], self.dt_format
            ).astimezone()

            delta_time = (now - dt).seconds / 60 / 60

        if delta_time > self._update_frequency:
            actual_dump: dict = self.create_urls_dump()

        file_dump_name = os.path.join(self.out_dir, actual_dump["name"])
        file_dump = read_json(file_dump_name)
        dumping(file_dump, dump)

        return actual_dump["name"]

    def full_update_dump(self):
        """
        TODO Restore all links from the database and start downloading from them.:return:
        """
        #
        pass

    def incremental_update(self):
        """
        TODO Check the difference between the checksums.
            Download the difference to a local dump.
            Upload new URLs to the database.
        :return:
        """
        pass

    def dump_to_db(self):
        """
        TODO Check user data in the database.
            If there is, load data from the database,
            create a current dump,
            find the difference
            write the difference to the database.
        :return:
        """



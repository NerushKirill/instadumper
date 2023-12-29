# -*- coding: utf-8 -*-
from src.parser import Parsing
from settings import settings

from src.libraries.supporting import dumping


def main() -> None:
    # user = settings.user1
    # user = settings.user2

    page = Parsing(user)
    print(page.create_urls_dump())

    # print(*page.get_posts().values(), sep="\n")
    # print(dumping(page.get_all(), page.out_dir))

    # page._update_frequency = 0
    # print(page.user)
    # print(page.create_urls_dump())
    #
    # print(page.get_actual_dump())
    # print(page.create_control_sum())

    # print(page.compare_control_sum())

    # print(page.restore_sum_from_db(True))
    # if not page.compare_control_sum():
    #     page.restore_sum_from_db(overwrite_existing=True)

    # print(*check_line_sum(list_), sep="\n")
    # print(list(get_hash_from_db(user)))
    # print(*check_line_sum(page.compare_control_sum()), sep="\n")
    # page.create_dump()


if __name__ == "__main__":
    main()
    # asyncio.run(main())

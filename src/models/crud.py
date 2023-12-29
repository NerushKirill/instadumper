# TODO add function add_to_db()
from sqlalchemy import select
from sqlalchemy.orm import Session

from .tables import Dump
from .engins import pgsql


def get_hash_from_db(user: str) -> set:
    result: set

    with Session(autoflush=False, bind=pgsql.sync_engine) as session:
        query = select(Dump).where(Dump.user_name == user)
        response = session.scalars(query)
        result = {line.hash for line in response}

    return result


def check_line_sum(data: set) -> list:
    with Session(autoflush=False, bind=pgsql.sync_engine) as session:
        query = select(Dump).where(Dump.hash.in_(data))
        response = session.scalars(query)
        result = [line.url for line in response]

    return result


#
# def insert_to_db(data: list):
#     with pgsql.sync_engine.begin() as conn:
#         result = conn.execute(insert(insta_log), data)
#         conn.commit()

# with Session(autoflush=False, bind=pgsql.sync_engine) as db:
#     dump_db = db.query(Dump).all()

# with open("out.txt", "a", encoding="utf-8") as f:
#     # f.write(dump)
#     for i in dump:
#         f.write(str(i))
#         f.write("\n")

# for i in dump_db:
#     print(f"{i.hash}")

# # async query into db
# async with pgsql.engine.begin() as conn:
#     await conn.run_sync(Base.metadata.drop_all)
#     await conn.run_sync(Base.metadata.create_all)
#
# async with pgsql.engine.connect() as conn:
#     result = await conn.execute(select(Dump))
#
#     print(result.fetchall())
#
# await pgsql.engine.dispose()

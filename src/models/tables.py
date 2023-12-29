import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Dump(Base):
    __tablename__ = "insta_log"

    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow()
    )
    user_name: Mapped[str]
    file_chapter: Mapped[str]
    album: Mapped[str]
    data_type: Mapped[str]
    url: Mapped[str]
    hash: Mapped[str]

    def __str__(self) -> str:
        return "InstaDump(id=%s, timestamp=%s)" % (self.id, self.timestamp)

    def __rep__(self) -> str:
        return self.__str__()

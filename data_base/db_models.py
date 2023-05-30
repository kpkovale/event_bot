from sqlalchemy import select, delete
from sqlalchemy import func
from sqlalchemy import Integer, String, ForeignKey, \
    Float, UniqueConstraint, BigInteger, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime, timedelta
from typing import List, Tuple
from typing_extensions import Annotated

from utils.bot_logger import logger
from data_base.database import DBSession, engine, IDUMixin

intpk = Annotated[int, mapped_column(primary_key=True)]

from sqlalchemy.orm import registry

reg = registry()

class Base(DeclarativeBase):
    registry = reg


class User(Base, IDUMixin):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    telegram_id = mapped_column(BigInteger, nullable=False, unique=True)
    enroll_date = mapped_column(DateTime, nullable=False, insert_default=func.now())
    active = mapped_column(Boolean, nullable=False, insert_default=True)

    def __init__(self, *args, **kwargs):
        """
        :param name / telegram_id / enroll_date & active (optional) as kwargs
        """
        super().__init__()
        for key, val in kwargs.items():
            self.__setattr__(key, val)

    def __str__(self):
        return f"*Пользователь*: [{self.name}](tg://user?id={self.telegram_id})\n" \
               f"*Telegram_ID:* `{self.telegram_id}`\n" \
               f"*Может участвовать:* {self.active}"

    def __repr__(self):
        return f"User (id: {self.id}, name: {self.name}, telegram_id: {self.telegram_id}, " \
               f"enroll_date: {self.enroll_date}, active: {self.active})"


def get_user_list(**kwargs) -> List[User]:
    """ Returns list of User objects
    :param kwargs: accepts one or several parameters as:
        id, user_name, phone, email, telegram_id, enroll_date, active
    :return:
    """
    with DBSession() as session:
        cursor = session.execute(select(User).filter_by(**kwargs).order_by(User.id)).all()
        res = []
        if not cursor:
            return None
        for row in cursor:
            res.append(row[0])
    return res


def clear_users():
    with DBSession() as session:
        try:
            session.execute(delete(User))
            session.commit()
        except Exception as e:
            logger.error(e)
            session.rollback()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

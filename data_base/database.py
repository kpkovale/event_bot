from sqlalchemy import create_engine
from config import DB_STRING
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from utils.bot_logger import logger

engine = create_engine(DB_STRING)

# class DBSesson to create sessions for database connection
DBSession = sessionmaker(bind=engine)


class IDUMixin:
    """
    An abstract class to put object changes to the Database
    """

    @classmethod
    def get(cls, **kwargs):
        """ returns single class instance filtered by kwargs
        :param kwargs:
        :return: self
        """
        with DBSession() as session:
            record = session.execute(select(cls).filter_by(**kwargs)).scalar()
            if not record:
                return None
        return record

    @classmethod
    def select(cls, **kwargs):
        """ returns a list of class instances filtered by **kwargs
        :param kwargs:
        :return: List[class objects]
        """
        with DBSession() as session:
            cursor = session.execute(select(cls).
                                     filter_by(**kwargs).order_by(cls.id)).all()
            res = []
            if not cursor:
                return None
            for row in cursor:
                res.append(row[0])
        return res

    def insert(self) -> bool:
        """ inserts new object record into db_module
        :return:
        """
        with DBSession() as session:
            session.add(self)
            try:
                session.commit()
                return True
            except Exception as e:
                logger.error(e)
                session.rollback()
                return False

    def delete(self):
        """ deletes object record from db_module
        :return:
        """
        with DBSession() as session:
            try:
                session.delete(self)
                session.commit()
            except Exception as e:
                logger.error(e)
                session.rollback()

    def update(self):
        """ updates object record data in db_module
        :return:
        """
        with DBSession() as session:
            record = session.get(self.__class__, self.id)
            for key, val in self.__dict__.items():
                record.__setattr__(key, val) if key not in ('_sa_instance_state', 'id') else ''
            if record in session.dirty:
                try:
                    session.flush()
                    session.commit()
                except Exception as e:
                    logger.error(e)
                    session.rollback()
            else:
                logger.debug("Current session cannot see modifications...")
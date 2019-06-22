from contextlib import contextmanager

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Uow:
    def __init__(self, connection_string, echo=False):
        engine = create_engine(connection_string, echo=echo)

        Base.metadata.create_all(engine)

        self._session = sessionmaker(bind=engine)()

    @property
    def session(self):
        return self._session

    @contextmanager
    def __call__(self):
        try:
            yield
        except:
            self._session.rollback()
        else:
            self._session.commit()


class UserTable(Base):
    __tablename__ = 'users'

    uid = Column(String(36), primary_key=True)
    email = Column(String(250))
    password = Column(String(250))

    def __repr__(self):
        return f"<User(uid='{self.uid}', email='{self.email}')>"

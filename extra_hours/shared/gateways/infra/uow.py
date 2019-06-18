from contextlib import contextmanager

from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Uow:
    def __init__(self, connection_string):
        engine = create_engine(connection_string, echo=True)

        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)

        self._session = Session()

    @property
    def session(self):
        return self._session

    @contextmanager
    def __call__(self, *args, **kwargs):
        try:
            yield
        except:
            self._session.rollback()
        else:
            self._session.commit()


class UserTable(Base):
    __tablename__ = 'users'

    uid = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"<User(email='{self.email}')>"

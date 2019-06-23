from contextlib import contextmanager

from sqlalchemy import create_engine, Column, String, Numeric, DateTime, Boolean, ForeignKey
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


class BillingTable(Base):
    __tablename__ = 'billing'

    uid = Column(String(36), primary_key=True)
    title = Column(String(250))
    description = Column(String(500))
    value = Column(Numeric(precision=2, scale=8))
    work_date = Column(DateTime)
    receive_date = Column(DateTime, default=None, nullable=True)
    received = Column(Boolean, default=False)

    user_uid = Column(String(36), ForeignKey('users.uid'))

    def __repr__(self):
        return f"<Billing(uid='{self.uid}', received={self.received})>"

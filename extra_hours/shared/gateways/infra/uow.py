from contextlib import contextmanager

from sqlalchemy import Column, String, create_engine, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Uow:
    def __init__(self, connection_string):
        engine = create_engine(connection_string, connect_args={'check_same_thread': False}, echo=True)

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
    billing = relationship('BillingTable')

    def __repr__(self):
        return f"<User(uid='{self.uid}', email='{self.email}')>"


class BillingTable(Base):
    __tablename__ = 'billing'

    uid = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    value = Column(Float)
    work_date = Column(DateTime)
    received_date = Column(DateTime, nullable=True)
    user_uid = Column(String, ForeignKey('users.uid'))

    def __repr__(self):
        return f"<Billing(uid='{self.uid}', title='{self.title}', value={self.value})>"

    def __eq__(self, other):
        return self.uid == other.uid

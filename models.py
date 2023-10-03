from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime
from db import Base
import datetime


class Services(Base):
    __tablename__ = 'services'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    cost = Column(Integer, default=0, nullable=False)


class Clients(Base):
    __tablename__ = 'clients'

    id = Column(BigInteger, unique=True, primary_key=True, autoincrement=False)
    created = Column(DateTime, default=datetime.datetime.now)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    phone_number = Column(String(255))


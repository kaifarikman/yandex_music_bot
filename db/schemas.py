from sqlalchemy import Column, Integer, BigInteger, Boolean, String
from db.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    peer_id = Column(BigInteger)
    username = Column(String, nullable=True)
    count = Column(Integer)


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    peer_id = Column(BigInteger)

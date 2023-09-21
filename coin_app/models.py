from coin_app.db import BASE
from sqlalchemy import Column, Integer, String


class User(BASE):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    balance = Column(Integer, default=0)



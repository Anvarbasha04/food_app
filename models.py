from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    food_name = Column(String)
    price = Column(Integer)
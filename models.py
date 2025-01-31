from sqlalchemy import Column, Double, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    orders = relationship("Order", back_populates="table")

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Double, nullable=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)
    items = relationship("OrderItem", back_populates="order")
    table_id = Column(Integer, ForeignKey('table.id'), nullable=False)
    table = relationship("Table", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    observation = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")
    menu_item = relationship("Menu")
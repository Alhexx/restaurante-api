from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
import models, schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/menus/batch", response_model=List[schemas.Menu])
def create_menus_batch(menus: schemas.MenuCreateBatch, db: Session = Depends(get_db)):
    db_menus = []
    for menu in menus.menus:
        db_menu = models.Menu(name=menu.name, description=menu.description, price=menu.price)
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        db_menus.append(db_menu)
    return db_menus

@app.get("/menus/", response_model=List[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()
    return menus

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    print(order)
    db_order = models.Order(status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in order.items:
        db_order_item = models.OrderItem(order_id=db_order.id, menu_item_id=item.menu_item_id, observation=item.observation, quantity=item.quantity)
        db.add(db_order_item)
    db.commit()
    return db_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders
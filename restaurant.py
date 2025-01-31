from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Annotated, List
import models, schemas
from database import engine, SessionLocal
from starlette import status
from sqlalchemy.orm import Session
import auth

app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@app.post("/tables/", response_model=schemas.Table)
def create_tables(table: schemas.TableCreate, user: user_dependency, db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=status, detail="nao esta autenticao")

    db_table = models.Table(name=table.name)
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@app.get("/tables/", response_model=List[schemas.Table])
def read_tables(db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    return tables

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
    db_order = models.Order(status=order.status, table_id=order.table_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in order.items:
        db_order_item = models.OrderItem(order_id=db_order.id, menu_item_id=item.menu_item_id, observation=item.observation, quantity=item.quantity)
        db.add(db_order_item)
    db.commit()
    return db_order

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(table_id: int = None, db: Session = Depends(get_db)):
    if table_id:
        orders = db.query(models.Order).filter(models.Order.table_id == table_id).all()
    else:
        orders = db.query(models.Order).all()
    return orders

@app.delete("/order_item/{id}")
def delete_order_item(id: int, db: Session = Depends(get_db)):
    db.query(models.OrderItem).filter(models.OrderItem.id == id).delete()
    db.commit()
    return {"message": "Item deleted"}
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, WebSocket, BackgroundTasks
import uuid
import asyncio
import random
import time

app = FastAPI()
class OrderInput(BaseModel):
    stoks: str
    quantity: float
class Status(Enum):
    pending = 'pending'
    executed = 'executed'
    canceled = 'canceled'
class Stoks(Enum):
    euro = 'EURO'
    usd = 'USD'
    etg = 'ETH'
class OrderOutput(BaseModel):
    id: str
    stoks: str
    quantity: float
    status: Status
class Error(BaseModel):
    code: int
    message: str

ordersDB = []
def find_order_by_id(target_id: str):
    for order in ordersDB:
        if order.id == target_id:
            return order
    return None
def random_short_delay():
    delay = random.uniform(0.1, 1.0)
    return delay
def change_order_status():
    time.sleep(random_short_delay())
    for i in range(len(ordersDB)):
        if ordersDB[i].status == Status.pending:
            ordersDB[i].status = Status.executed
@app.get("/")
async def root():

    time.sleep(random.uniform(0.1, 1.0))
    return {"Server Running"}
@app.get("/orders")
async def orders()->list[OrderOutput]:

    time.sleep(random.uniform(0.1, 1.0))
    if len(ordersDB)<=0:
        raise HTTPException(status_code=404, detail="Order not found")
    return ordersDB

@app.post("/orders",status_code=201)
async def add_orders(order:OrderInput,background_tasks:BackgroundTasks):

    time.sleep(random.uniform(0.1, 1.0))
    if order.stoks not in Stoks._value2member_map_ or order.quantity<=0:
       raise HTTPException(status_code=400, detail="Invalid input")
    else:
        itemDB= OrderOutput(id=str(uuid.uuid4()), stoks=order.stoks, quantity=order.quantity, status=Status.pending)
        ordersDB.append(itemDB)
        background_tasks.add_task(change_order_status)
        return itemDB

@app.post("/orders/nobw",status_code=201)
async def add_orders(order:OrderInput,background_tasks:BackgroundTasks):

    time.sleep(random.uniform(0.1, 1.0))
    if order.stoks not in Stoks._value2member_map_ or order.quantity<=0:
       raise HTTPException(status_code=400, detail="Invalid input")
    else:
        itemDB= OrderOutput(id=str(uuid.uuid4()), stoks=order.stoks, quantity=order.quantity, status=Status.pending)
        ordersDB.append(itemDB)
        return itemDB


@app.get("/orders/{order_id}")
async def query_order(order_id: str)->OrderOutput:

    time.sleep(random.uniform(0.1, 1.0))
    order = find_order_by_id(order_id)
    if order == None:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    else:
        return order


@app.delete("/orders/{order_id}",status_code=204)
async def delete_order(order_id: str, status_code=204):

    time.sleep(random.uniform(0.1, 1.0))
    order = find_order_by_id(order_id)
    if order != None and order.status == Status.pending:
        ordersDB.remove(order)
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/adm/{order_id}")
async def delete_order(order_id: str):

    time.sleep(random.uniform(0.1, 1.0))
    order = find_order_by_id(order_id)
    if order != None:
        ordersDB.remove(order)
    else:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found in pending state")
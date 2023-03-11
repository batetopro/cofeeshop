from fastapi import FastAPI
from .reader import DataReader


app = FastAPI()


@app.get("/customers/birthday")
async def birthday():
    return DataReader().read_birthdays()


@app.get("/products/top-selling-products/{year:int}")
async def birthday(year: int):
    return DataReader().read_top_selling_products(year)


@app.get("/customers/last-order-per-customer")
async def birthday():
    return DataReader().read_last_order_per_customer()

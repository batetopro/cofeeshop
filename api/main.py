from fastapi import FastAPI
from .reader import DataReader


app = FastAPI()


@app.get("/customers/birthday")
async def birthday():
    """
    Get list of customers, which have birthday today.
    """
    return {"customers": DataReader().read_birthdays()}


@app.get("/products/top-selling-products/{year:int}")
async def top_selling_products(year: int):
    """
    The top 10 selling products for a specific year.
    """
    return {"products": DataReader().read_top_selling_products(year)}


@app.get("/customers/last-order-per-customer")
async def last_order_per_customer():
    """
    The last order per customer with their email.
    """
    return {"customers": DataReader().read_last_order_per_customer()}

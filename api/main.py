from fastapi import FastAPI
from .reader import DataReader
from .schemas import BirthdayResponse, TopSellingProductResponse, LastOrderPerCustomerResponse


app = FastAPI()


@app.get("/customers/birthday", response_model=BirthdayResponse)
async def birthday() -> BirthdayResponse:
    """
    Get list of customers, which have birthday today.
    """
    return BirthdayResponse(customers=DataReader().read_birthdays())


@app.get("/products/top-selling-products/{year:int}", response_model=TopSellingProductResponse)
async def top_selling_products(year: int) -> TopSellingProductResponse:
    """
    The top 10 selling products for a specific year.
    """
    return TopSellingProductResponse(products=DataReader().read_top_selling_products(year))


@app.get("/customers/last-order-per-customer", response_model=LastOrderPerCustomerResponse)
async def last_order_per_customer() -> LastOrderPerCustomerResponse:
    """
    The last order per customer with their email.
    """
    return LastOrderPerCustomerResponse(customers=DataReader().read_last_order_per_customer())

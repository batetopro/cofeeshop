from typing import List
from pydantic import BaseModel, EmailStr


class Birthday(BaseModel):
    customer_id: int
    customer_first_name: str


class TopSellingProduct(BaseModel):
    product_name: str
    total_sales: int


class LastOrderPerCustomer(BaseModel):
    customer_id: int
    customer_email: EmailStr
    last_order_date: str


class BirthdayResponse(BaseModel):
    customers: List[Birthday]


class TopSellingProductResponse(BaseModel):
    products: List[TopSellingProduct]


class LastOrderPerCustomerResponse(BaseModel):
    customers: List[LastOrderPerCustomer]

import datetime
from .models import Customer, Staff, SalesOutlet, Product, \
    Receipt, Date, Generation, PastryInventory, SalesTarget


MAPPING = [
    {
        "file": "staff.csv",
        "model": Staff,
        "rename_columns": [],
        "transform_columns": [
            ("start_date", lambda x: datetime.datetime.strptime(x, "%m/%d/%Y").date()),
        ],
    },
    {
        "file": "sales_outlet.csv",
        "model": SalesOutlet,
        "rename_columns": [
            ("Neighorhood", "neighborhood"),
        ],
        "transform_columns": [
            ("manager", lambda x: None if not x else int(x)),
        ],
    },
    {
        "file": "product.csv",
        "model": Product,
        "rename_columns": [],
        "transform_columns": [
            ("current_retail_price", lambda x: float(x.lstrip('$'))),
        ],
    },
    {
        "file": "Dates.csv",
        "model": Date,
        "rename_columns": [
            ("Date_ID", "date_id"),
            ("Week_ID", "week_id"),
            ("Week_Desc", "week_desc"),
            ("Month_ID", "month_id"),
            ("Month_Name", "month_name"),
            ("Quarter_ID", "quarter_id"),
            ("Quarter_Name", "quarter_name"),
            ("Year_ID", "year_id"),
        ],
        "transform_columns": [
            ("transaction_date", lambda x: datetime.datetime.strptime(x, "%m/%d/%Y").date()),
        ],
    },
    {
        "file": "generations.csv",
        "model": Generation,
        "rename_columns": [],
        "transform_columns": [],
    },
    {
        "file": "pastry inventory.csv",
        "model": PastryInventory,
        "rename_columns": [
            ("% waste", "waste_percent"),
        ],
        "transform_columns": [
            ("transaction_date", lambda x: datetime.datetime.strptime(x, "%m/%d/%Y").date()),
            ("waste_percent", lambda x: x.rstrip("%")),
        ],
    },

    {
        "file": "sales targets.csv",
        "model": SalesTarget,
        "rename_columns": [
            ("merchandise _goal", "merchandise_goal"),
        ],
        "transform_columns": [],
    },

    {
        "file": "customer.csv",
        "model": Customer,
        "rename_columns": [
            ("customer_first-name", "name"),
            ("customer_email", "email"),
        ],
        "transform_columns": [
            ("customer_since", lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date()),
            ("birthdate", lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date()),
        ],
    },
    {
        "file": "sales_reciepts.csv",
        "model": Receipt,
        "rename_columns": [],
        "transform_columns": [
            ("transaction_date", lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date()),
            ("transaction_time", lambda x: datetime.datetime.strptime(x, "%H:%M:%S").time()),
            ("customer_id", lambda x: None if not int(x) else int(x)),
        ],
    },
]

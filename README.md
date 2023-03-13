# coffee shop

 ![index](https://github.com/batetopro/coffeeshop/blob/main/assets/index.png?raw=true)

The [task](https://github.com/batetopro/coffeeshop/raw/main/assets/task.pdf) 
wants us to create a REST service with three endpoints:

* **/customers/birthday** - get a list with customers. who have their birthday today.
* **/products/top-selling-products/{year}** - get a list with the top 10 selling products of the year.
* **/customers/last-order-per-customer** - when was the last order per customer together with their email.

The project implementation contains two parts:
* **loader** - a *flask* application, which handles the loading of data from the 
input archive file to the database.
* **api** - a *FastAPI* web service, which uses *SQLAlchemy* to read data from the 
database

## Setup
Create a virtual environment.
```commandline
python -m venv .venv
```

Activate the virtual environment,
```commandline
source .venv/bin/activate
```

Install the requirements. 
```commandline
pip install -r requirements.txt
```

If you want to:
* use SQLite, please follow this [link](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm).
* use MySQL, please follow this [link](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql).
* use postgreSQL, please follow this [link](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e). 

After database setup, you should configure the connection string for the reader.
This is done by using the *DATABASE_URL* environment variable, 

It should have the following format:
* SQLite
> sqlite:///{path to SQLite file}
* MySQL
> mysql+pymysql://{username}:{password}@{host}/{database}
* PostgreSQL
> postgresql+psycopg2://{username}:{password}@{host}/{database}

Initialize and run the migrations
```commandline
flask db init
flask db migrate -m "Make migrations."
flask db upgrade
```

## loader
Load the data from the CSV documents.
```commandline
flask load_data
```

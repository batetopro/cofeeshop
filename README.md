# coffee shop

 ![index](https://github.com/batetopro/coffeeshop/blob/main/assets/index.png?raw=true)

The [task](https://github.com/batetopro/coffeeshop/raw/main/assets/task.pdf) 
wants us to create a web service with three endpoints:

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
Tje *loader* is an application, which is developed using *Flask* and *SQLAlchemy*.
It uses *flask_migrate* to handle the migrations.

The loader package contains:
* **engine** - contains the *DataLoadEngine*, which is responsible of reading 
zip archive with CSV documents and creating records in the database from these documents.
* **mapping** - contains a dictionary, which has rules for the task's context.
* **models** - *SQLAlchemy* models of the CSV documents, which are to be loaded in the database.

One mapping rule should have:
* file - the CSV file from which data is read.
* model - the database model, which is loaded from the file.
* rename_columns - pairs of (name in file, model field name)
* transform_columns - pairs of (model field name, transformation function)

Load the data from the CSV documents.
```commandline
flask load_data
```

The data is loaded into tables, which can be described with the ER diagram:
![ER diagram](https://github.com/batetopro/coffeeshop/blob/main/assets/er.png?raw=true)

## api
Tje *api* is an application, which is developed using *FastAPI*.

The api package contains:
* **engine** - contains the abstract *ReaderEngine*, which is implemented for SQLite, MySQL and PostgresSQL.
Those classes are responsible for executing queries and reading from the database.
* **main** - contains the FastAPI routes.
* **reader** - contains the *DataReader* class, which is adapter if the engine classes.
It takes the connection string and decides which engine should be used.
* **schemas** - uses *pydantic* to define the datatypes, which are used by the FastAPI
endpoints.

The following diagram shows the connections between engine classes and DataReader class.

![ER db engines](https://github.com/batetopro/coffeeshop/blob/main/assets/readers.png?raw=true)

To start the web service:
```commandline
uvicorn api.main:app --reload
```


## tests
To run the tests, execute:
```commandline
flask tests
```

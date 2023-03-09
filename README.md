# coffee shop

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

Initialize and run the migrations
```commandline
flask db init
flask db migrate -m "Make migrations."
flask db upgrade
```

Load the data from the CSV documents.
```commandline
flask load_data
```

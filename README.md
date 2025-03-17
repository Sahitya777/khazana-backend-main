# Project Title

A brief description of what this project does and its purpose.

---

## 🚀 Features

- Database version control using **Alembic**
- API application powered by **FastAPI** (or your framework)
- Hot-reloading with **Uvicorn**
---

## Clone the repo

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name ```

##  Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

## 🗄️ Database Setup with Alembic
## Initialize Alembic (only needed once)

alembic init alembic

## configure Database URL
Make a db url with posgtress from pgAdmin via creating new db from create under databases under postgresssql
Configure username,db name and password
Example url-> postgresql://postgres:admin@localhost:5432/khazana
# Edit alembic.ini and set the sqlalchemy.url to your database connection string.

sqlalchemy.url = postgresql://user:password@localhost:5432/your_db_name

# Edit target metadata and add imports under alembic/env.py
from app.database.database import Base
from app.model.user import User
# Edit target metadata
target_metadata = Base.metadata

## Create New Migration- in bash, use this command
alembic revision --autogenerate -m "create initial tables"

## After Migration- apply the migrations
alembic upgrade head

# Filling Data in db
Please Fill mutual Funds table first as it is connected to other tables
Please Refer to demoInsert.sql for inserting values into the specific tables 

## 🏃 Running the Application
uvicorn main:app --reload

Access the API at: http://127.0.0.1:8000

Swagger UI available at: http://127.0.0.1:8000/docs




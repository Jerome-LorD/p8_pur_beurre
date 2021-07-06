# P8 Pur Beurre
## About
In progress, the project is under construction for the moment.


## Installation
First, you have to create the database
1. Clone the repo
```sh
git clone https://github.com/Jerome-LorD/p8_pur_beurre.git
```
2. Create a virtual environment
```py
py -m venv env
```
3. With `psql`, create the database and a user
```sql
CREATE DATABASE <yourDb> OWNER <yourUser>;
```
4. Install the requirements.txt
```sh
pip install -r requirements.txt
```
5. Create a `.env` file at the root of the project.
```py
DB_ORIGIN_BASE_NAME=<yourDbName>
DB_ORIGIN_BASE_PASSWD=<yourPassword>
DB_APP_USER=<yourUserName>
```

### Usage
Create the database and populate it. In the terminal type :
```py
py manage.py createdb
```

When the job is done, type :
```py
py manage.py runserver
```


# P8 Pur Beurre

## About

The startup Pur Beurre wishes to develop a web platform for its customers. This site will allow anyone to find a healthy substitute for a food considered "Too Fat, Too Sweet, Too Salty" (even though we all know fat is life).

## Installation

1. Clone the repo

```sh
git clone https://github.com/Jerome-LorD/p8_pur_beurre.git
```

2. Create a virtual environment

```py
python -m venv env
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
HOST=<yourHOST>
```

### Usage

Create the tables and populate them. In the terminal type :

```py
python manage.py createdb
```

When the job is done, type :

```py
python manage.py runserver
```

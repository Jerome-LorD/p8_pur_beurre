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

```sh
CREATE DATABASE offdb_p8 OWNER offp8;
```
3. Install the requirements.txt
```sh
pip install -r requirements.txt
```
4. Create a `.env` file at the root of the project.
```py
DB_ORIGIN_BASE_NAME=offdb_p8
DB_ORIGIN_BASE_PASSWD=<yourpassword>
DB_APP_USER=<yourusername>
```

### Usage
Create the database and populate it. In the terminal type :
`py manage.py createdb`
When the job is done, type :
`py manage.py runserver`


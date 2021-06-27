#!/usr/bin/env python
"""Database cnx."""

# import mysql.connector  # type: ignore
import psycopg2

import os
import re
import requests

from psycopg2 import sql
from dotenv import load_dotenv, find_dotenv  # type: ignore
from typing import List, Any

from purapps.purbeurre.models import Product, Category, Nutriscore

# from app.config import SQL_FILE, DB_NAME

load_dotenv(find_dotenv())

user = os.getenv("OFF_USER")
password = os.getenv("OFF_PASSWD")

db_user = os.getenv("DB_APP_USER")
db_password = os.getenv("DB_ORIGIN_BASE_PASSWD")
off_user = os.getenv("DB_APP_USER")
off_password = os.getenv("DB_ORIGIN_BASE_PASSWD")
off_database = os.getenv("DB_ORIGIN_BASE_NAME")
# host = os.getenv("DB_HOST")

host = "127.0.0.1"
SQL_FILE = "sql/offdb_p8.sql"
DB_NAME = "offdb_p8"


class Database:
    """Database class."""

    cnx = None

    def __init__(self, user="", password="", schema=None):
        """Init."""
        self.user: str = user
        self.password: str = password
        self.schema: str = schema

        if not self.cnx:
            self.cnx = psycopg2.connect(
                host=host,
                database=self.schema,
                user=self.user,
                password=self.password,
            )

        self.cursor = self.cnx.cursor()

    @classmethod
    def is_connected(cls):
        """Verify connexion."""
        return cls.cnx is not None


class Create:
    """Create db, user and tables."""

    def __init__(self):
        """Init."""
        self.db = Database(db_user, db_password, off_database)

    # def create_user(self):
    #     """Create user."""
    #     try:
    #         self.db.cursor.execute(
    #             sql.SQL(
    #                 """
    #                 CREATE ROLE {user} WITH ENCRYPTED PASSWORD %s CREATEDB LOGIN;
    #                 CREATE DATABASE offdb_p8 WITH ENCODING 'UTF-8' OWNER {user};
    #                 ALTER ROLE {user} SET client_encoding TO 'utf8';
    #                 ALTER ROLE {user} SET default_transaction_isolation
    #                 TO 'read committed';
    #                 ALTER ROLE {user} SET timezone TO 'Europe/Paris';
    #                 """
    #             ).format(user=sql.Identifier(user)),
    #             (password,),
    #         )

    #         self.db.cnx.commit()

    #     except (Exception, psycopg2.DatabaseError) as err:
    #         print(f"Something went... wrong: {err}")
    #         exit(1)

    def create_db(self):
        """Create db and tables."""
        try:
            with open(SQL_FILE) as f:
                self.db.cursor.execute(f.read())

                # self.db.cursor.execute(
                #     sql.SQL(
                #         "GRANT ALL PRIVILEGES ON DATABASE offdb_p8 TO {user};"
                #     ).format(user=sql.Identifier(user)),
                # )

            self.db.cnx.commit()
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Something went** wrong: {err}")
            exit(1)

        self.db.cnx.close()


class Downloader:
    """Download and extract."""

    def __init__(self, nb_page):
        """Init."""
        self.url = "https://fr.openfoodfacts.org/cgi/search.pl?"
        self.payload = {
            "json": 1,
            "action": "process",
            "lang": "fr",
            "page_size": 1000,
            "page": nb_page,
        }
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

    def extract_data(self):
        """Extract data from API."""
        try:
            r = requests.get(self.url, headers=self.headers, params=self.payload)
            self.result = r.json()
            return self.result["products"]
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)


class Insert:
    """Fill the database."""

    def __init__(self, cleaned_data):
        """Init."""
        self.cleaned_data = cleaned_data
        self.db = Database(db_user, db_password, off_database)

    def is_data_in_db(self):
        """Check if the database contains at least 3000 entries."""
        self.db.cursor.execute("SELECT COUNT(product.id) as tot_prods FROM product")
        if self.db.cursor.fetchone()[0] >= 3000:
            return True
        return False

    def insert_data(self):
        """Insert data into DB."""
        if self.cleaned_data:
            for product in self.cleaned_data:
                if product:
                    try:
                        Nutriscore.objects.get(type=product["nutriscore_grade"])
                    except Nutriscore.DoesNotExist:
                        nut = Nutriscore.objects.create(
                            type=product["nutriscore_grade"]
                        )
                        nut.save()

                    try:
                        Product.objects.get(name=product["product_name_fr"])
                    except Product.DoesNotExist:

                        last_nut = Nutriscore.objects.filter(
                            type=product["nutriscore_grade"]
                        ).values("id")

                        prod = Product.objects.create(
                            name=product["product_name_fr"],
                            url=product["url"],
                            brand=product["brands"],
                            stores=product["stores"],
                            nutriscore_id=last_nut,
                        )

                        last_product_id = Product.objects.filter(
                            name=product["product_name_fr"]
                        ).values("id")[0]

                        prod.save()

                    for category in product["categories"].split(","):
                        categorie = category.strip()
                        try:
                            Category.objects.get(name=categorie)
                        except Category.DoesNotExist:

                            cat = Category.objects.create(name=categorie)
                            cat.save()

                            last_categorie_id = Category.objects.filter(
                                name=categorie
                            ).values("id")[0]

                            prod.categories.add(
                                last_product_id.get("id"),
                                last_categorie_id.get("id"),
                            )


class Cleaner:
    """Clean all data."""

    validators: List[Any] = []
    normalizers: List[Any] = []

    def is_valid(self, data):
        """Verify if the key has a value."""
        for validator in self.validators:
            if not validator(data):
                return False
        return True

    def normalize(self, data):
        """Normalize some entries."""
        for normalizer in self.normalizers:
            data = normalizer(data)
        return data

    def clean(self, collection):
        """Return a data list if is_valid is True."""
        return [self.normalize(data) for data in collection if self.is_valid(data)]


def require_product_name_fr_not_empty(data):
    """Verify if product_name_fr is not empty."""
    return True if data.get("product_name_fr") else False


def require_stores_not_empty(data):
    """Verify if stores is not empty."""
    return True if data.get("stores") else False


def require_nutriscore_grade_not_empty(data):
    """Verify if nutriscore_grade is not empty."""
    return True if data.get("nutriscore_grade") else False


def require_lang_equal_to_fr(data):
    """Verify if lang is equal to fr."""
    return True if data.get("lang") == "fr" else False


def require_categories_lc_equal_to_fr(data):
    """Verify if categories_lc is equal to fr."""
    return True if data.get("categories_lc") == "fr" else False


def require_categories_without_lot_of_dashes(data):
    """Ignore categories with lot of tirets."""
    item = re.search(r"(\w+\-){1,}", data.get("categories"))
    return False if item else True


def normalize_product_without_cariage_return(data):
    """Delete cariage return."""
    if "\n" in data.get("product_name_fr"):
        return data.update(
            product_name_fr=data.get("product_name_fr").replace("\n", " ")
        )
    return data


def normalize_categories_without_suffix_and_bad_datas(data):
    """Delete expr like -> en: and fr: with all that comes after."""
    if data:
        item = re.search(r"\,\s{0,}\w{2}:", data.get("categories"))
        if item:
            return data.update(categories=data.get("categories")[: item.start()])
        return data


class OffCleaner(Cleaner):
    """State."""

    validators = [
        require_product_name_fr_not_empty,
        require_stores_not_empty,
        require_nutriscore_grade_not_empty,
        require_lang_equal_to_fr,
        require_categories_lc_equal_to_fr,
        require_categories_without_lot_of_dashes,
    ]

    normalizers = [
        normalize_product_without_cariage_return,
        normalize_categories_without_suffix_and_bad_datas,
    ]


# if __name__ == "__main__":
#     for page in range(1, 2):
#         down_off = Downloader(page)
#         extracted = down_off.extract_data()
#         cleaner = OffCleaner()
#         cleaned = cleaner.clean(extracted)
#         construct = Insert(cleaned)
#         construct.insert_data()

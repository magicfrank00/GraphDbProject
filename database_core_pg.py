import logging
import os

import psycopg
from psycopg import Error
from psycopg.rows import dict_row

database_pwd = "galileo-ski-watch-orchid-plate-1558"


def log_notice(diag):
    logging.info(f"Database message: {diag.severity} - {diag.message_primary}")


class DatabasePg:
    def __init__(self, db_name="supply_chain"):
        self.connection = None
        self.cursor = None
        self.db_name = db_name
        self.open()

    def __del__(self):
        if self.connection:
            self.close()

    def open(self):
        while True:
            try:
                self.connection = psycopg.connect(
                    host="localhost",
                    port="5433",  # 5432
                    user="supply_chain_user",
                    password=database_pwd,
                    dbname=self.db_name,
                    keepalives=1,
                    keepalives_idle=5,
                    keepalives_interval=2,
                    keepalives_count=2,
                )

                self.connection.add_notice_handler(log_notice)
                self.connection.adapters.register_loader(
                    "numeric", psycopg.types.numeric.FloatLoader
                )
                self.cursor = self.connection.cursor(row_factory=dict_row)
                return
            except Error as err:
                logging.error(
                    f"Error while connecting to PostgreSQL: {err}", exc_info=True
                )
                input("Fix the error and press enter to continue")

    def keep_alive(self):
        if not self.connection:
            self.open()

        try:
            self.connection.isolation_level
        except psycopg.OperationalError:
            self.open()

    def commit(self):
        self.keep_alive()
        self.connection.commit()

    def close(self):
        self.commit()
        self.cursor.close()
        self.connection.close()
        self.connection = None

    def query(self, query, parameters=None):
        self.keep_alive()
        try:
            self.cursor.execute(query, parameters)
            if self.cursor.description is None:
                return []
            return self.cursor.fetchall()
        except Error as err:
            logging.error(f"Error while executing query: {err}", exc_info=True)
            self.close()
            return []

    def creation_query(self, query, parameters=None):
        self.keep_alive()
        try:
            self.cursor.execute(query, parameters)
        except Error as err:
            logging.error(f"Error while executing query: {err}", exc_info=True)
            self.close()


if __name__ == "__main__":
    db = DatabasePg()
    result = db.query(
        """  SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public';"""
    )
    print(result)
    db.close()

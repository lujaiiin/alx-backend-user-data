#!/usr/bin/env python3
"""mod"""
import re
from typing import List
import logging
import mysql.connector
import os
from datetime import datetime


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """mm"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """"fo"""
        original_message = super().format(record)
        filtered_message = filter_datum(self._fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        return filtered_message


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ll"""
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """ll"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """lll"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME', '')

    connection = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )
    return connection


def main():
    """ll"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        message = "name={}; email={}; phone={}; ssn={}; password={};\
ip={}; last_login={}; user_agent={};".format(*tuple(row))
        get_logger().info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

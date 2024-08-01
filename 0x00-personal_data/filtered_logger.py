#!/usr/bin/env python3
"""Some  pyton code and exercises"""

import re
from typing import List
import logging
import mysql.connector
from os import getenv

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function to obfuscate values of fields using regex"""
    return re.sub(f'({"|".join(fields)})=[^{separator}]*',
                  f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting a log record"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Returns logger instance
        """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns database connection"""
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = getenv('PERSONAL_DATA_DB_NAME')

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return connection


def main() -> None:
    """Main function to retrieve data from database"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    logger = get_logger()

    for row in cursor:
        message = '; '.join(f"{field}={value}" for field, value in zip(
            ['name', 'email', 'phone', 'ssn', 'password', 'ip',
             'last_login', 'user_agent'], row))
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

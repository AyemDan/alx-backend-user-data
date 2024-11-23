#!/usr/bin/env python3
"""
This module provides functionality for logging user data with sensitive
information redacted.
Functions:
    filter_datum(fields: List[str], redaction: str, message: str,
    separator: str) -> str:
        Replaces occurrences of specified fields in a message with a
        redaction string.
    get_logger(self) -> logging.Logger:
        Configures and returns a logger with a custom formatter for
        redacting sensitive information.
    get_db() -> mysql.connector.connection.MySQLConnection:
        Establishes and returns a connection to the MySQL database using
        environment variables for configuration.
    main():
        Main function that retrieves user data from the database and logs it
        with sensitive information redacted.
Classes:
    RedactingFormatter(logging.Formatter):
        Custom logging formatter that redacts specified fields in log messages.
        Attributes:
            REDACTION (str): The string used to replace sensitive information.
            FORMAT (str): The log message format.
            SEPARATOR (str): The separator used in log messages.
        Methods:
            __init__(self, fields: List[str]):
                Initializes the formatter with a list of fields to redact.
            format(self, record: logging.LogRecord) -> str:
                Redacts specified fields in the log record message.
Constants:
    PII_FIELDS (tuple): A tuple containing the names of fields that
    contain personally identifiable information.
"""

import logging
import os
import mysql.connector
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replaces occurrences of certain fields in a log message
    with a redaction string.
    Args:
        fields (List[str]): A list of field names to be redacted.
        redaction (str): The string to replace the field values
        with.
        message (str): The log message containing the fields
        to be redacted.
        separator (str): The character that separates the fields
        in the log message.
    Returns:
        str: The log message with the specified fields redacted.
    """

    for field in fields:
        message = re.sub(fr"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger(self) -> logging.Logger:
    """
    Creates and configures a logger for user data.
    This method sets up a logger named "user_data" with an
    INFO logging level.
    It ensures that the logger does not propagate messages to
    the root logger.
    A StreamHandler is added to the logger with the formatter
    set to the instance
    of the class from which this method is called.
    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(self)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database using credentials and
    connection details from environment variables.
    Environment Variables:
        PERSONAL_DATA_DB_HOST (str): The hostname of the database server.
        PERSONAL_DATA_DB_NAME (str): The name of the database.
        PERSONAL_DATA_DB_USERNAME (str): The username for the
        database connection.
        PERSONAL_DATA_DB_PASSWORD (str): The password for the
        database connection.
    Returns:
        mysql.connector.connection.MySQLConnection: A MySQL
        database connection object.
    """

    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "root"),
        database=os.getenv("PERSONAL_DATA_DB_NAME", "root"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    )


def main():
    """
    Main function to fetch user data from the database and log it
    with sensitive information redacted.
    This function performs the following steps:
    1. Connects to the database using `get_db()`.
    2. Executes a SQL query to select all records from the `users` table.
    3. Retrieves the field names from the cursor description.
    4. Initializes a `RedactingFormatter` with the field names.
    5. Sets up a logger with the redacting formatter.
    6. Iterates over the rows in the cursor and logs each row with
    sensitive information redacted.
    7. Closes the cursor and the database connection.
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    fields = [i[0] for i in cursor.description]
    formatter = RedactingFormatter(fields)
    logger = get_logger(formatter)
    for row in cursor:
        logger.info("; ".join(str(field) for field in row))
    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):

    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter instance.
        Args:
            fields (List[str]): A list of field names that need
            to be redacted.
        """

        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record.
        This method overrides the default format method to apply data filtering
        before formatting the log message. It replaces sensitive information in
        the log message with a redaction string.
        Args:
            record (logging.LogRecord): The log record to be formatted.
        Returns:
            str: The formatted log message with sensitive information redacted.
        """

        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")

if __name__ == "__main__":
    """
This module provides functionality for logging user data with sensitive
information redacted.

Functions:
    filter_datum(fields: List[str], redaction: str, message:
    str, separator: str) -> str:
        Replaces occurrences of specified fields in a message
        with a redaction string.
    get_logger(self) -> logging.Logger:
        Configures and returns a logger with a custom formatter for
        redacting sensitive information.
    get_db() -> mysql.connector.connection.MySQLConnection:
        Establishes and returns a connection to the MySQL database using
        environment variables for configuration.
    main():
        Main function that retrieves user data from the database and
        logs it with sensitive information redacted.

Classes:
    RedactingFormatter(logging.Formatter):
        Custom logging formatter that redacts specified fields in log messages.
        Attributes:
            REDACTION (str): The string used to replace sensitive information.
            FORMAT (str): The log message format.
            SEPARATOR (str): The separator used in log messages.
        Methods:
            __init__(self, fields: List[str]):
                Initializes the formatter with a list of fields to redact.
            format(self, record: logging.LogRecord) -> str:
                Redacts specified fields in the log record message.

Constants:
    PII_FIELDS (tuple): A tuple containing the names of fields that
    contain personally identifiable information.
"""
    main()

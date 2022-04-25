"""This model is Database Context Manager"""
import sqlite3
import logging

class DBCM():
    """DBCM class to manage the database connections"""
    logger = logging.getLogger("main." + __name__)
    def __init__(self, db_name):
        """Initializes the variables."""
        try:
            self.db_name = db_name
            self.conn = None
            self.cur = None
        except Exception as error:
            self.logger.error("Error DBCM Init: %s",error)

    def __enter__(self):
        """Opens a connection and cursor."""
        try:
            self.conn = sqlite3.connect(self.db_name)
        except Exception as error:
            self.logger.error("Error opening DB: %s",error)
        try:
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as error:
            self.logger.error("Error database Enter: %s",error)

    def __exit__(self, exc_type, exc_value, exc_trace):
        """Commits changes and closes cursor and connection."""
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as error:
            self.logger.error("Error database Exit: %s",error)

import pymysql
from src.Logger import Logger


class Database:
    def __init__(self, host, user, password="", database="zbd_project"):
        """Initialize database object"""
        # Initialize logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("Database logger has started.")
        # Initialize database connection
        try:
            self.logger.debug("Trying to attempt connection with database.")
            self.connection = pymysql.connect(host=host, user=user, passwd=password, database=database)
        except Exception as e:
            self.logger.critical(f"Could not connect to database! Error = {e}")
            raise ConnectionRefusedError(f"Could not connect to database! Error = {e}")
        self.logger.info("Database connection is stable.")
        # Initialize global cursor
        self.logger.debug("Creating global cursor.")
        self.cursor = self.connection.cursor()
        self.logger.debug("Global cursor created.")

    def executeStatement(self, statement):
        """ Execute an statement using database cursor"""
        try:
            self.logger.debug(f"Executing statement = {statement}")
            self.cursor.execute(statement)
        except Exception as e:
            self.logger.error(f"Could not realize an execute statement. Statement = {statement}. Error = {e}")
            return False
        result = self.cursor.fetchall()
        self.logger.debug(f"Result = {result}")
        return result

    def __del__(self):
        """ Close connection with database """
        # Close database connection
        self.logger.info("Closing database connection.")
        self.connection.close()

import pymysql
from src.Logger import Logger
import json


class Database:
    def __init__(self, host, user, password="", database="zbd_project"):
        """Initialize database object"""
        # Initialize logger
        self.logger = Logger(__name__, loggingLevel="debug")
        self.logger.debug("Database logger has started.")
        self.connection = None
        # Initialize database connection
        try:
            self.logger.debug("Trying to attempt connection with database.")
            self.connection = pymysql.connect(host=host, user=user, passwd=password, database=database)
        except Exception as e:
            self.logger.critical(f"Could not connect to database! Error = {e}")
            raise ConnectionRefusedError(f"Could not connect to database! Error = {e}")
        self.logger.info("Database connection is stable.")

        self.config = dict()
        try:
            with open("config.json") as f:
                self.config = {**self.config, **json.load(f)}
        except IOError as e:
            self.logger.error(f"Error occured while reading config from .json file!. Error = {e}")
            exit(-1)
        self.logger.debug("Config has been read.")

        # Initialize global cursor
        self.logger.debug("Creating global cursor.")
        self.cursor = self.connection.cursor()
        self.logger.debug("Global cursor created.")

    def __del__(self):
        """ Close connection with database """
        # Close database connection
        if self.connection:
            self.logger.info("Closing database connection.")
            try:
                self.connection.close()
            except:
                pass

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

    def getTableNames(self):
        """ Get all table names read from config file """
        return self.config["table_names"]

    def getRawData(self, tableName):
        """ Gets data and return its in list form """
        statement = "SELECT * FROM " + tableName + ";"
        #self.connection.commit()
        return self.executeStatement(statement)

    def getColumns(self, tableName):
        """Create and execute statement"""
        tableName = "'" + tableName + "'"
        statement = "SELECT column_name FROM information_schema.columns WHERE table_name = " + tableName + ";"
        #self.connection.commit()
        return self.executeStatement(statement)

    def getData(self, tableName):
        """ Gets data and return it in dict form """
        rowData = self.getRawData(tableName)
        columns = self.getColumns(tableName)
        result = dict()
        for noR, row in enumerate(rowData):
            result[f"cer{noR + 1}"] = dict()
            for noC, column in enumerate(columns):
                result[f"cer{noR + 1}"][f"{column[0]}"] = row[noC]

        return result


    def addOvner(self, nip, companyName='NULL', name='NULL', surname='NULL'):
        """Add ' at the beggining and at the end of a string"""
        if companyName != 'NULL':
            companyName = "'" + companyName + "'"
        if name != 'NULL':
            name = "'" + name + "'"
        if surname != 'NULL':
            surname = "'" + surname + "'"

        """Create and execute statement"""
        nip = str(nip)
        statement = "INSERT INTO `wlasciciele`(`nip`, `nazwa_firmy`, `imie`, `nazwisko`) VALUES ( " + nip + ", " + companyName + ", " + name + ", " + surname + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addAuthor(self, name, surname, birthday, deathday ='NULL'):
        """Add ' at the beggining and at the end of a string"""
        if name != 'NULL':
            name = "'" + name + "'"
        if surname != 'NULL':
            surname = "'" + surname + "'"
        if birthday != 'NULL':
            birthday = "'" + birthday + "'"
        if deathday != 'NULL':
            deathday = "'" + deathday + "'"

        """Create and execute statement"""
        statement = "INSERT INTO `autorzy`(`imie`, `nazwisko`, `data_urodzenia`, `data_smierci`) VALUES ( " + name + ", " + surname + ", " + birthday + ", " + deathday + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addGenre(self, name):
        """Add ' at the beggining and at the end of a string"""
        if name != 'NULL':
            name = "'" + name + "'"

        """Create and execute statement"""
        statement = "INSERT INTO `gatunki`(`gatunek`) VALUES ( " + name + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addSection(self, name, location):
        """Add ' at the beggining and at the end of a string"""
        if name != 'NULL':
            name = "'" + name + "'"
        if location != 'NULL':
            location = "'" + location + "'"

        """Create and execute statement"""
        statement = "INSERT INTO `dzialy`(`nazwa`, `lokalizacja`) VALUES ( " + name + ", " + location + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addReader(self, name, surname):
        """Add ' at the beggining and at the end of a string"""
        if name != 'NULL':
            name = "'" + name + "'"
        if surname != 'NULL':
            surname = "'" + surname + "'"

        """Create and execute statement"""
        statement = "INSERT INTO `czytelnicy`(`imie`, `nazwisko`) VALUES ( " + name + ", " + surname + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addLibrary(self, name, location):
        """Add ' at the beggining and at the end of a string"""
        if name != 'NULL':
            name = "'" + name + "'"
        if location != 'NULL':
            location = "'" + location + "'"

        """Create and execute statement"""
        statement = "INSERT INTO `biblioteki`(`nazwa`, `lokalizacja`) VALUES ( " + name + ", " + location + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addBookstand(self, number, capacity, booksCount, sectionName):
        """Add ' at the beggining and at the end of a string"""
        if sectionName != 'NULL':
            sectionName = "'" + sectionName + "'"

        """Create and execute statement"""
        number = str(number)
        capacity = str(capacity)
        booksCount = str(booksCount)
        statement = "INSERT INTO `regaly`(`numer`, `pojemnosc`, `liczba_ksiazek`, `dział_nazwa`) VALUES ( " + number + ", " + capacity + ", " + booksCount + ", " + sectionName + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addBook(self, title, publicationDate, genre):
        """Add ' at the beggining and at the end of a string"""
        if title != 'NULL':
            title = "'" + title + "'"
        if publicationDate != 'NULL':
            publicationDate = "'" + publicationDate + "'"
        if genre != 'NULL':
            genre = "'" + genre + "'"

        """Create and execute statement"""
        statement = "INSERT INTO `ksiazki`(`tytul`, `data_opublikowania`, `gatunek`) VALUES ( " + title + ", " + publicationDate + ", " + genre + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addAuthorBook(self, author_id, book_id):
        """Create and execute statement"""
        author_id = str(author_id)
        book_id = str(book_id)
        statement = "INSERT INTO `autor_ksiazka`(`autorzy_autor_id`, `ksiazki_ksiazka_id`) VALUES ( " + author_id + ", " + book_id + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addSpecimen(self, book_id, bookstandNumber):
        """Create and execute statement"""
        book_id = str(book_id)
        bookstandNumber = str(bookstandNumber)
        statement = "INSERT INTO `egzemplarze`(`ksiazka_id`, `regal_numer`) VALUES ( " + book_id + ", " + bookstandNumber + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addWorker(self, name, surname, function, boss_id = 'NULL'):
        """Add ' at the beggining and at the end of a string"""
        if name != 'NULL':
            name = "'" + name + "'"
        if surname != 'NULL':
            surname = "'" + surname + "'"
        if function != 'NULL':
            function = "'" + function + "'"

        """Create and execute statement. Disable FK checking"""
        boss_id = str(boss_id)
        statement = "INSERT INTO `pracownicy`(`szef_id`, `imie`, `nazwisko`, `funkcja`) VALUES ( " + boss_id + ", " + name + ", " + surname + ", " + function + " );"
        self.executeStatement("SET FOREIGN_KEY_CHECKS = 0;")
        self.executeStatement(statement)
        self.executeStatement("SET FOREIGN_KEY_CHECKS = 1;")
        self.connection.commit()

    def addOvnerLibrary(self, ovner_nip, library_name):
        """Add ' at the beggining and at the end of a string"""
        if library_name != 'NULL':
            library_name = "'" + library_name + "'"

        """Create and execute statement"""
        ovner_nip = str(ovner_nip)
        statement = "INSERT INTO `wlasciciel_biblioteka`(`wlasciciel_nip`, `biblioteka_nazwa`) VALUES ( " + ovner_nip + ", " + library_name + " );"
        self.executeStatement(statement)
        self.connection.commit()

    def addOperation(self, date, library_name, worker_id, reader_id, specimen_id, operationType, returnDelay, comments):
        """Add ' at the beggining and at the end of a string"""
        if date != 'NULL':
            date = "'" + date + "'"
        if library_name != 'NULL':
            library_name = "'" + library_name + "'"
        if operationType != 'NULL':
            operationType = "'" + operationType + "'"
        if comments != 'NULL':
            comments = "'" + comments + "'"

        """Create and execute statement"""
        worker_id = str(worker_id)
        reader_id = str(reader_id)
        specimen_id = str(specimen_id)
        returnDelay = str(returnDelay)
        statement = "INSERT INTO `historia_operacji`(`data`, `biblioteka_nazwa`, `pracownik_id`, `czytelnik_id`, `egzemplarz_id`, `rodzaj_operacji`, `opoznienie`, `uwagi`) VALUES ( " + date + ", " + library_name + ", " + worker_id + ", " + reader_id + ", " + specimen_id + ", " + operationType + ", " + returnDelay + ", " + comments + " );"
        self.executeStatement(statement)
        self.connection.commit()

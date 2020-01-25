import pymysql
from src.Logger import Logger
import json
import random


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

        self.generateDataBase()

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
            result[f"rec{noR + 1}"] = dict()
            for noC, column in enumerate(columns):
                result[f"rec{noR + 1}"][f"{column[0]}"] = row[noC]
        return result

    def addRecord(self, tableName, values):
        """Create columns_str string to hold columns names ready to put into mysql question"""
        columns = self.getColumns(tableName)
        columns_str = "("
        for c in columns:
            newColumn = str(c)
            newColumn = "`" + newColumn[2:-3] + "`"
            columns_str += newColumn + ", "
        columns_str = columns_str[:-2] + ")"

        """Create values_str string to hold columns values ready to put into mysql question"""
        values_str = "("
        for v in values:
            newValue = v
            if newValue != 'NULL':
                newValue = "'" + str(v) + "'"
            values_str += newValue + ", "
        values_str = values_str[:-2] + ")"

        """Create and execute statement"""
        tableName = "`" + tableName + "`"
        statement = "INSERT INTO " + tableName + columns_str + " VALUES " + values_str + ";"
        self.executeStatement(statement)
        self.connection.commit()

    def generateDataBase(self):
        names = ['Piotr', 'Maciej', 'Jan', 'Jakub', 'Karol', 'Joanna', 'Marta', 'Magda', 'Natalia', 'Olga']
        surnames = ['Krol', 'Nowak', 'Zima', 'Leszczyk', 'Karol', 'Nowaczyk', 'Kowalczyk', 'Wozniak', 'Mazur', 'Krawczyk']
        dates = ['1997-05-05', '1993-12-25', '1991-08-01', '1988-07-17', '1992-10-11', '1991-01-22', '1987-03-30', '1997-11-28', '1990-09-03', '1980-04-14']
        libraryNames = ['Czytam_ksiazki', 'Czytanie_jest_fajne', 'Ksiazki_sa_super', 'Biblioteka_dziecieca', 'Biblioteka_szkolna', 'Biblioteka_miejska', 'Warto_czytac', 'Super_Biblioteka', 'Biblioteka_na_rynku', 'Biblioteka_na_Kwiatowej']
        adresses = ['Kwiatowa_10', 'Rzeczypospolitej_5', 'Dluga_4', 'Krutka_1', 'Poznanska_12', 'Wroclawska_43', 'Zawila_3', 'Czysta_21', 'Powstancow_2', 'Brudna_31']
        genres = ['fantasy', 'horror', 'klasyka', 'kryminal', 'sensacja', 'thriller', 'literatura_mlodziezowa', 'literatura_obyczajowa', 'romans', 'powiesc_historyczna']
        operationTypes = ['wyporzyczenie', 'zwrot', 'przedluzenie']
        comments = ['pierwszy raz od dawna', 'sprawna operacja', 'bez uwag']
        booksTitles = ['Szeptucha', 'Polska_odwraca_oczy', 'On', 'Zycie_na_pelnej_petardzie', 'Okularnik', 'Najgorszy_czlowiek_na_swiecie', 'Inna_dusza', 'Ksiegi_Jakubowe', 'Gniew', 'Trociny']
        firmNames = ['Januszpol', 'Toyota', 'Adidas', 'Walkman', 'Red_Bull', 'Junkers', 'Ikea', 'Tesco', 'CCC', 'Bakoma']
        workersFunctions = ['szef', 'sprzatanie', 'obsluga_bazy', 'kucharz']

        """Generate authors"""
        for _ in range(10):
            author_id = 'NULL'
            name = random.choice(names)
            surname = random.choice(surnames)
            birthday = random.choice(dates)
            deathday = random.choice(['NULL', random.choice(dates)])
            values = [author_id, name, surname, birthday, deathday]
            self.addRecord('autorzy', values)

        """Generate libraries"""
        for i in range(10):
            name = libraryNames[i]
            adres = random.choice(adresses)
            values = [name, adres]
            self.addRecord('biblioteki', values)

        """Generate readers"""
        for _ in range(10):
            reader_id = 'NULL'
            name = random.choice(names)
            surname = random.choice(surnames)
            values = [reader_id, name, surname]
            self.addRecord('czytelnicy', values)

        """Generate sections"""
        for i in range(10):
            name = 'dzial' + str(i)
            location = 'lokalizacja' + str(i)
            values = [name, location]
            self.addRecord('dzialy', values)
            
        """Generate genres"""
        for i in range(10):
            name = genres[i]
            values = [name]
            self.addRecord('gatunki', values)
        
        """Generate books"""
        for i in range(10):
            book_id = 'NULL'
            title = booksTitles[i]
            date = random.choice(dates)
            genre = random.choice(genres)
            values = [book_id, title, date, genre]
            self.addRecord('ksiazki', values)
        
        """Generate bookstands"""
        for i in range(10):
            number = i
            capacity = random.randint(100,10000)
            booksCount = capacity - random.randint(0, capacity)
            section = random.randint(0,9)
            section = 'dzial' + str(section)
            values = [number, capacity, booksCount, section]
            self.addRecord('regaly', values)
        
        """Generate ovners"""
        tmp = random.randint(100,10000)
        for i in range(10):
            nip = tmp + i
            if random.randint(0,1) == 1:
                firmName = random.choice(firmNames)
                name = 'NULL'
                surname = 'NULL'
            else:
                firmName = 'NULL'
                name = random.choice(names)
                surname = random.choice(surnames)
            values = [nip, firmName, name, surname]
            self.addRecord('wlasciciele', values)
        
        """Generate ovner-library"""
        tmp = self.getRawData('wlasciciele')
        nips = [record[0] for record in tmp]
        tmp = self.getRawData('biblioteki')
        libraries = [record[0] for record in tmp]
        for i in range(len(libraries)):
            nip = random.choice(nips)
            library = libraries[i]
            values = [nip, library]
            self.addRecord('wlasciciel_biblioteka', values)
        
        """Generate author-book"""
        tmp = self.getRawData('autorzy')
        authors_ids = [record[0] for record in tmp]
        tmp = self.getRawData('ksiazki')
        books_ids = [record[0] for record in tmp]
        for i in range(len(books_ids)):
            author_id = random.choice(authors_ids)
            book_id = books_ids[i]
            values = [author_id, book_id]
            self.addRecord('autor_ksiazka', values)
        
        """Generate specimens"""
        tmp = self.getRawData('ksiazki')
        books_ids = [record[0] for record in tmp]
        tmp = self.getRawData('regaly')
        bookstandsNumbers = [record[0] for record in tmp]
        for _ in range(10):
            specimen_id = 'NULL'
            book_id = random.choice(books_ids)
            bookstandNumber = random.choice(bookstandsNumbers)
            values = [specimen_id, book_id, bookstandNumber]
            self.addRecord('egzemplarze', values)
        
        """Generate workers. Disable FK checking"""
        self.executeStatement("SET FOREIGN_KEY_CHECKS = 0;")
        for i in range(10):
            worker_id = 'NULL'
            if i != 0:
                boss_id = random.choice(['NULL', random.randint(0, i - 1)])
            else:
                boss_id = 'NULL'
            name = random.choice(names)
            surname = random.choice(surnames)
            function = random.choice(workersFunctions)
            values = [worker_id, boss_id, name, surname, function]
            self.addRecord('pracownicy', values)
        self.executeStatement("SET FOREIGN_KEY_CHECKS = 1;")

        """Generate operations"""
        tmp = self.getRawData('biblioteki')
        libraries = [record[0] for record in tmp]
        tmp = self.getRawData('pracownicy')
        workers_ids = [record[0] for record in tmp]
        tmp = self.getRawData('czytelnicy')
        readers_ids = [record[0] for record in tmp]
        tmp = self.getRawData('egzemplarze')
        specimens_ids = [record[0] for record in tmp]
        for _ in range(10):
            operation_id = 'NULL'
            date = random.choice(dates)
            library = random.choice(libraries)
            worker_id = random.choice(workers_ids)
            reader_id = random.choice(readers_ids)
            specimen_id = random.choice(specimens_ids)
            operationType = random.choice(operationTypes)
            delay = random.choice(['NULL', random.randint(1,20)])
            comment = random.choice(['NULL', random.choice(comments)])
            values = [operation_id, date, library, worker_id, reader_id, specimen_id, operationType, delay, comment]
            self.addRecord('historia_operacji', values)

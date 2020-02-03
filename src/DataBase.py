import pymysql
from src.Logger import Logger
import json
import random
import re


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

        print(self.getColumnKeys('historia_operacji'))

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
            raise Exception(e)
        result = self.cursor.fetchall()
        self.logger.debug(f"Result = {result}")
        return result

    def getTableNames(self):
        """ Get all table names read from config file """
        return self.config["table_names"]

    def getRawData(self, tableName):
        """ Gets data and return its in list form """
        statement = "SELECT * FROM " + tableName + ";"
        return self.executeStatement(statement)

    def getColumns(self, tableName):
        """Create and execute statement"""
        tableName = "'" + tableName + "'"
        statement = "SELECT column_name FROM information_schema.columns WHERE table_name = " + tableName + ";"
        return self.executeStatement(statement)

    def getColumnTypes(self, tableName):
        """Create and execute statement"""
        tableName = "'" + tableName + "'"
        statement = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = " + tableName + ";"
        columns = self.executeStatement(statement)
        res = {}
        for column in columns:
            res[column[0]] = column[1]
        return res

    """Create dictionary res[columnName] = [keyType, refTable, refColumn]"""
    def getColumnKeys(self, tableName):
        tableName = "'" + tableName + "'"
        statement = "SELECT column_name, column_key FROM information_schema.columns WHERE table_name = " + tableName + ";"
        columns = self.executeStatement(statement)
        res = {}
        for column in columns:
            name = column[0]
            key = column[1]
            if key == 'MUL':
                statement = "SELECT referenced_table_name, referenced_column_name FROM information_schema.key_column_usage WHERE table_name = " + tableName + " AND column_name = " + "'" + name + "'" + ";"
                tmp = self.executeStatement(statement)[0]
                refTable = tmp[0]
                refColumn = tmp[1]
            else:
                refTable = 'NULL'
                refColumn = 'NULL'

            res[name] = [key, refTable, refColumn]

        return res

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
        self.logger.debug(f"Adding new record to table {tableName}. Values = {values}")

        try:
            """Check if values are in correct format"""
            self.logger.debug("Checking if values are in correct format.")
            columnTypes = self.getColumnTypes(tableName)
            tmp = self.getColumns(tableName)
            columnNames = []
            for column in tmp:
                newColumn = str(column)
                newColumn = newColumn[2:-3]
                columnNames.append(newColumn)
            for i in range(len(columnTypes)):
                name = columnNames[i]
                type = columnTypes[name]
                value = values[i]
                value = str(value)
                if value in ('NULL', None, ''):
                    continue
                elif type == 'int':
                    if not re.match('^[0-9]+$', value):
                        raise Exception(f"Wrong {name}. Make sure {name} contains only digits.")
                elif type == 'date':
                    condition = self.executeStatement(f"SELECT (SELECT CURDATE()) < '{value}'")
                    if not re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', value):
                        raise Exception(f"Wrong {name}. Make sure {name} is in 'YYYY-MM-DD' format.")
                    elif condition == ((1,),):
                        raise Exception(f"Wrong {name}. Date can't be from the future.")

            self.logger.debug("Creating addRecord statement.")

            """Create columns_str string to hold columns names ready to put into mysql question"""
            columns_str = "("
            for column in columnNames:
                newColumn = "`" + column + "`"
                columns_str += newColumn + ", "
            columns_str = columns_str[:-2] + ")"

            """Create values_str string to hold columns values ready to put into mysql question"""
            values_str = "("
            for v in values:
                newValue = v
                if newValue in ('NULL', None, ''):
                    newValue = 'NULL'
                else:
                    newValue = "'" + str(v) + "'"
                values_str += newValue + ", "
            values_str = values_str[:-2] + ")"

            """Create statement"""
            tableName = "`" + tableName + "`"
            statement = "INSERT INTO " + tableName + columns_str + " VALUES " + values_str + ";"
            self.logger.debug(f"AddRecord statement created succesfully. Statement = {statement}")

            """Executing statement"""
            self.executeStatement(statement)
            self.logger.debug(f"Record {values[0]} added succesfully.")
            return True

        except Exception as e:
            self.logger.error(f"Could not realize an addRecord function. Error = {e}")
            raise Exception(e)

    def modifyRecord(self, tableName, oldValues, values):
        self.logger.debug(f"Modifying record {oldValues[0]} from {tableName}. New values = {values}")

        try:
            """Check if values are in correct format"""
            self.logger.debug("Checking if values are in correct format.")
            columnTypes = self.getColumnTypes(tableName)
            tmp = self.getColumns(tableName)
            columnNames = []
            for column in tmp:
                newColumn = str(column)
                newColumn = newColumn[2:-3]
                columnNames.append(newColumn)
            for i in range(len(columnTypes)):
                name = columnNames[i]
                type = columnTypes[name]
                value = values[i]
                value = str(value)
                if value in ('NULL', None, ''):
                    continue
                elif type == 'int':
                    if not re.match('^[0-9]+$', value):
                        raise Exception(f"Wrong {name}. Make sure {name} contains only digits.")
                elif type == 'date':
                    condition = self.executeStatement(f"SELECT (SELECT CURDATE()) < '{value}'")
                    if not re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', value):
                        raise Exception(f"Wrong {name}. Make sure {name} is in 'YYYY-MM-DD' format.")
                    elif condition == ((1,),):
                        raise Exception(f"Wrong {name}. Date can't be from the future.")
            self.logger.debug("Creating modifyRecord statement.")

            """Create columns names ready to put into mysql question"""
            columns = []
            tmp = self.getColumns(tableName)
            for column in tmp:
                newColumn = str(column)
                newColumn = "`" + newColumn[2:-3] + "`"
                columns.append(newColumn)

            """Create set_str ready to put into mysql question"""
            set_str = ""
            for i in range(len(columns)):
                if str(values[i]) in ('NULL', None, ''):
                    set_str += columns[i] + " = "
                    set_str += 'NULL' + ", "
                else:
                    set_str += columns[i] + " = "
                    set_str += "'" + str(values[i]) + "', "
            set_str = set_str[:-2]

            """Create where_str ready to put into mysql question"""
            where_str = ""
            for i in range(len(columns)):
                oldValue = oldValues[i]
                if oldValue in ('NULL', None, ''):
                    where_str += columns[i] + " IS NULL AND "
                else:
                    where_str += columns[i] + " = "
                    oldValue = str(oldValues[i])
                    where_str += "'" + oldValue + "' AND "
            where_str = where_str[:-5]

            """Create statement"""
            tableName = "`" + tableName + "`"
            statement = "UPDATE " + tableName + " SET " + set_str + " WHERE " + where_str + ";"
            self.logger.debug(f"ModifyRecord statement created succesfully. Statement = {statement}")

            """Executing statement"""
            self.executeStatement(statement)
            self.logger.debug(f"Record {oldValues[0]} modified succesfully.")
            return True

        except Exception as e:
            self.logger.error(f"Could not realize an modifyRecord function. Error = {e}")
            raise Exception(e)

    def deleteRecord(self, tableName, values):
        self.logger.debug(f"Deleting record {values[0]} from {tableName}.")

        try:
            self.logger.debug("Creating deleteRecord statement.")

            """Create columns names ready to put into mysql question"""
            columns = []
            tmp = self.getColumns(tableName)
            for column in tmp:
                newColumn = str(column)
                newColumn = "`" + newColumn[2:-3] + "`"
                columns.append(newColumn)

            """Create where_str ready to put into mysql question"""
            where_str = ""
            for i in range(len(columns)):
                value = values[i]
                if value in ('NULL', None, ''):
                    where_str += columns[i] + " IS NULL AND "
                else:
                    where_str += columns[i] + " = "
                    value = str(values[i])
                    where_str += "'" + value + "' AND "
            where_str = where_str[:-5]

            """Create statement"""
            tableName = "`" + tableName + "`"
            statement = "DELETE FROM " + tableName + " WHERE " + where_str + ";"
            self.logger.debug(f"DeleteRecord statement created succesfully. Statement = {statement}")

            """Executing statement"""
            self.executeStatement(statement)
            self.logger.debug(f"Record {values[0]} deleted succesfully.")
            return True

        except Exception as e:
            self.logger.error(f"Could not realize an deleteRecord function. Error = {e}")
            raise Exception(e)

    def borrowBook(self, libraryName, workerName, workerSurname,
                    readerName, readerSurname, bookTitle,
                    bookDate, bookGenre, comments):
        self.logger.debug("Borrowing book.")

        try:
            self.executeStatement(f"CALL borrowBook('{libraryName}', '{workerName}', '{workerSurname}',"
                                  f"'{readerName}', '{readerSurname}', '{bookTitle}',"
                                  f"'{bookDate}', '{bookGenre}', '{comments}');")
            self.logger.debug("Book borrowed succesfully.")
            return True

        except Exception as e:
            self.logger.error(f"Could not realize an borrowBook function. Error = {e}")
            raise Exception(e)

    def findBestBook(self, bookDateYear):
        self.logger.debug("Finding best book.")

        try:
            bestBookBorrowCount = self.executeStatement(f"SELECT findBestBookBorrowCount({bookDateYear});")
            bestBookID = self.executeStatement(f"SELECT findBestBookID({bookDateYear});")
            self.logger.debug(f"Book found succesfully. BookID = {bestBookID}. Count = {bestBookBorrowCount}")
            return [bestBookID, bestBookBorrowCount]

        except Exception as e:
            self.logger.error(f"Could not realize an findBestBook function. Error = {e}")
            raise Exception(e)

    def generateDataBase(self):
        self.logger.debug(f"Generating new data base started.")

        names = ['Piotr', 'Maciej', 'Jan', 'Jakub', 'Karol', 'Joanna', 'Marta', 'Magda', 'Natalia', 'Olga']
        surnames = ['Krol', 'Nowak', 'Zima', 'Leszczyk', 'Karol', 'Nowaczyk', 'Kowalczyk', 'Wozniak', 'Mazur', 'Krawczyk']
        dates = ['1970-05-05', '1971-12-25', '1972-08-01', '1973-07-17', '1974-10-11', '1975-01-22', '1976-03-30', '1977-11-28', '1978-09-03', '1979-04-14']
        libraryNames = ['Czytam_ksiazki', 'Czytanie_jest_fajne', 'Ksiazki_sa_super', 'Biblioteka_dziecieca', 'Biblioteka_szkolna', 'Biblioteka_miejska', 'Warto_czytac', 'Super_Biblioteka', 'Biblioteka_na_rynku', 'Biblioteka_na_Kwiatowej']
        adresses = ['Kwiatowa_10', 'Rzeczypospolitej_5', 'Dluga_4', 'Krutka_1', 'Poznanska_12', 'Wroclawska_43', 'Zawila_3', 'Czysta_21', 'Powstancow_2', 'Brudna_31']
        genres = ['fantasy', 'horror', 'klasyka', 'kryminal', 'sensacja', 'thriller', 'literatura_mlodziezowa', 'literatura_obyczajowa', 'romans', 'powiesc_historyczna']
        operationTypes = ['wypozyczenie', 'zwrot', 'przedluzenie']
        comments = ['pierwszy raz od dawna', 'sprawna operacja', 'bez uwag']
        booksTitles = ['Szeptucha', 'Polska_odwraca_oczy', 'On', 'Zycie_na_pelnej_petardzie', 'Okularnik', 'Najgorszy_czlowiek_na_swiecie', 'Inna_dusza', 'Ksiegi_Jakubowe', 'Gniew', 'Trociny']
        firmNames = ['Januszpol', 'Toyota', 'Adidas', 'Walkman', 'Red_Bull', 'Junkers', 'Ikea', 'Tesco', 'CCC', 'Bakoma']
        workersFunctions = ['szef', 'sprzatanie', 'obsluga_bazy', 'kucharz']

        self.logger.debug("Random collumn values created succesfully.")

        """Generate authors"""
        self.logger.debug("Generating authors. Putting records to `autorzy` table.")
        for i in range(10):
            author_id = 'NULL'
            name = random.choice(names)
            surname = surnames[i]
            birthday = random.choice(dates)
            tmp = random.choice([True, False])
            if tmp:
                deathday = 'NULL'
            else:
                deathYear = birthday[:4]
                deathYear = int(deathYear)
                tmp = random.randint(1,40)
                deathYear = deathYear + tmp
                deathYear = str(deathYear)
                tmp = random.choice(dates)
                deathday = deathYear + tmp[4:]
            values = [author_id, name, surname, birthday, deathday]
            self.addRecord('autorzy', values)
        self.logger.debug("Authors records put into 'autorzy' table succesfully.")

        """Generate libraries"""
        self.logger.debug("Generating libraries. Putting records to `biblioteki` table.")
        for i in range(10):
            name = libraryNames[i]
            adres = adresses[i]
            values = [name, adres]
            self.addRecord('biblioteki', values)
        self.logger.debug("Libraries records put into 'biblioteki' table succesfully.")

        """Generate readers"""
        self.logger.debug("Generating readers. Putting records to `czytelnicy` table.")
        for i in range(10):
            reader_id = 'NULL'
            name = random.choice(names)
            surname = surnames[i]
            values = [reader_id, name, surname]
            self.addRecord('czytelnicy', values)
        self.logger.debug("Readers records put into 'czytelnicy' table succesfully.")

        """Generate sections"""
        self.logger.debug("Generating sections. Putting records to `dzialy` table.")
        for i in range(10):
            name = 'dzial' + str(i)
            location = 'lokalizacja' + str(i)
            values = [name, location]
            self.addRecord('dzialy', values)
        self.logger.debug("Sections records put into 'dzialy' table succesfully.")
            
        """Generate genres"""
        self.logger.debug("Generating genres. Putting records to `gatunki` table.")
        for i in range(10):
            name = genres[i]
            values = [name]
            self.addRecord('gatunki', values)
        self.logger.debug("Genres records put into 'gatunki' table succesfully.")
        
        """Generate books"""
        self.logger.debug("Generating books. Putting records to `ksiazki` table.")
        for i in range(10):
            book_id = 'NULL'
            title = booksTitles[i]
            date = random.choice(dates)
            genre = random.choice(genres)
            values = [book_id, title, date, genre]
            self.addRecord('ksiazki', values)
        self.logger.debug("Books records put into 'ksiazki' table succesfully.")

        """Generate bookstands"""
        self.logger.debug("Generating bookstands. Putting records to `regaly` table.")
        for i in range(10):
            number = i
            capacity = random.randint(5,9)
            booksCount = 0
            section = random.randint(0,9)
            section = 'dzial' + str(section)
            values = [number, capacity, booksCount, section]
            self.addRecord('regaly', values)
        self.logger.debug("Bookstands records put into 'regaly' table succesfully.")
        
        """Generate ovners"""
        self.logger.debug("Generating ovners. Putting records to `wlasciciele` table.")
        tmp = random.randint(1000000000,2000000000)
        for i in range(10):
            nip = tmp + i
            if random.randint(0,1) == 1:
                firmName = firmNames[i]
                name = 'NULL'
                surname = 'NULL'
            else:
                firmName = 'NULL'
                name = random.choice(names)
                surname = surnames[i]
            values = [nip, firmName, name, surname]
            self.addRecord('wlasciciele', values)
        self.logger.debug("Ovners records put into 'wlasciciele' table succesfully.")
        
        """Generate ovner-library"""
        self.logger.debug("Generating ovner-library. Putting records to `wlasciciel_biblioteka` table.")
        tmp = self.getRawData('wlasciciele')
        nips = [record[0] for record in tmp]
        tmp = self.getRawData('biblioteki')
        libraries = [record[0] for record in tmp]
        for i in range(len(libraries)):
            nip = random.choice(nips)
            library = libraries[i]
            values = [nip, library]
            self.addRecord('wlasciciel_biblioteka', values)
        self.logger.debug("Ovner-library records put into 'wlasciciel_biblioteka' table succesfully.")
        
        """Generate author-book"""
        self.logger.debug("Generating author-book. Putting records to `autor_ksiazka` table.")
        tmp = self.getRawData('autorzy')
        authors_ids = [record[0] for record in tmp]
        tmp = self.getRawData('ksiazki')
        books_ids = [record[0] for record in tmp]
        for i in range(len(books_ids)):
            author_id = random.choice(authors_ids)
            book_id = books_ids[i]
            values = [author_id, book_id]
            self.addRecord('autor_ksiazka', values)
        self.logger.debug("Author-book records put into 'autor_ksiazka' table succesfully.")
        
        """Generate specimens"""
        self.logger.debug("Generating specimens. Putting records to `egzemplarze` table.")
        tmp = self.getRawData('ksiazki')
        books_ids = [record[0] for record in tmp]
        tmp = self.getRawData('regaly')
        bookstandsNumbers = [record[0] for record in tmp]
        for _ in range(10):
            specimen_id = 'NULL'
            book_id = random.choice(books_ids)
            bookstandNumber = random.choice(bookstandsNumbers)
            """Increment bookstand books count"""
            statement = "SELECT `liczba_ksiazek` FROM `regaly` WHERE `numer` = " + str(bookstandNumber) + ";"
            booksCount = self.executeStatement(statement)
            statement = "SELECT `pojemnosc` FROM `regaly` WHERE `numer` = " + str(bookstandNumber) + ";"
            capacity = self.executeStatement(statement)
            if booksCount < capacity:
                statement = "UPDATE `regaly` SET `liczba_ksiazek` = `liczba_ksiazek` + 1 WHERE `numer` = " + str(bookstandNumber) + ";"
                self.executeStatement(statement)
                """Add specimen"""
                values = [specimen_id, book_id, bookstandNumber]
                self.addRecord('egzemplarze', values)
            else:
                self.logger.error(f"Could not add specimen to bookstand {bookstandNumber}. Not enough space on the bookstand")
                return False
        self.logger.debug("Specimens records put into 'egzemplarze' table succesfully.")

        
        """Generate workers. Disable FK checking"""
        self.logger.debug("Generating workers. Putting records to `pracownicy` table.")
        self.executeStatement("SET FOREIGN_KEY_CHECKS = 0;")
        self.logger.debug("FOREIGN_KEY_CHECKS disabled")
        for i in range(10):
            worker_id = 'NULL'
            if i != 0:
                boss_id = random.choice(['NULL', random.randint(0, i - 1)])
            else:
                boss_id = 'NULL'
            name = random.choice(names)
            surname = surnames[i]
            function = random.choice(workersFunctions)
            values = [worker_id, boss_id, name, surname, function]
            self.addRecord('pracownicy', values)
        self.executeStatement("SET FOREIGN_KEY_CHECKS = 1;")
        self.logger.debug("FOREIGN_KEY_CHECKS enabled")
        self.logger.debug("Workers records put into 'pracownicy' table succesfully.")

        """Generate operations"""
        self.logger.debug("Generating operations. Putting records to `historia_operacji` table.")
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
        self.logger.debug("Operations records put into 'historia_operacji' table succesfully.")

        """Commit"""
        self.connection.commit()
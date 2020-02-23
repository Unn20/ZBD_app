-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 23 Lut 2020, 13:40
-- Wersja serwera: 10.4.11-MariaDB
-- Wersja PHP: 7.2.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `zbd_project`
--

--
-- Czyszczenie starych procedur i funkcji
--
DROP PROCEDURE IF EXISTS `borrowBook`;
DROP FUNCTION IF EXISTS `findBestBookBorrowCount`;
DROP FUNCTION IF EXISTS `findBestBookTitle`;

DELIMITER $$
--
-- Procedury
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `borrowBook` (IN `libraryName` VARCHAR(50), IN `workerName` TEXT, IN `workerSurname` TEXT, IN `readerName` TEXT, IN `readerSurname` TEXT, IN `bookTitle` VARCHAR(100), IN `comments` TEXT)  BEGIN
    /*
    Declaring needed variables
    */
    DECLARE operation_id INT;
    DECLARE operationDate date;
    DECLARE worker_id INT;
    DECLARE reader_id INT;
    DECLARE book_id INT;
    DECLARE specimen_id INT;
    DECLARE operationType text;
    DECLARE delay INT;
    DECLARE bookstandNumber INT;

    SET FOREIGN_KEY_CHECKS = 0;

    /*
    Finding needed values
    */
    SET operation_id = NULL;
    SELECT CURDATE() INTO operationDate;
    SELECT pracownik_id FROM pracownicy WHERE imie = workerName AND nazwisko = workerSurname
        INTO worker_id;
    SELECT czytelnik_id FROM czytelnicy WHERE imie = readerName AND nazwisko = readerSurname
        INTO reader_id;
    SELECT ksiazka_id FROM ksiazki WHERE tytul = bookTitle
        INTO book_id;
    SELECT egzemplarz_id FROM egzemplarze WHERE ksiazka_id = book_id LIMIT 1
        INTO specimen_id;
    SET operationType = 'wypozyczenie';
    SET delay = NULL;
    SELECT regal_numer FROM egzemplarze WHERE egzemplarz_id = specimen_id
        INTO bookstandNumber;

    /*
    Handle errors
    */
    IF worker_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = 'There is no worker with this name and surname.';
    ELSEIF reader_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = 'There is no reader with this name and surname.';
    ELSEIF book_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = 'There is no book with this title date and genre.';
    ELSEIF specimen_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = 'There is no specimen for this book in this library';
    END IF;

    /*
    Add borrow action to the operation history
    */
    INSERT INTO historia_operacji(operacja_id, data, biblioteka_nazwa, pracownik_id,
                                czytelnik_id, egzemplarz_id, rodzaj_operacji, opoznienie, uwagi)
        VALUES(operation_id, operationDate, libraryName, worker_id,
                reader_id, specimen_id, operationType, delay, comments);

    /*
    Remove specimen from bookstand
    */
    UPDATE regaly SET liczba_ksiazek = liczba_ksiazek - 1 WHERE numer = bookstandNumber;

    SET FOREIGN_KEY_CHECKS = 1;
END$$

--
-- Funkcje
--
CREATE DEFINER=`root`@`localhost` FUNCTION `findBestBookBorrowCount` (`bookDateYear` INT) RETURNS INT(11) BEGIN
    RETURN(
        WITH
            bookOperations AS (
                SELECT k.tytul as bookTitle, count(*) as borrowCount
                FROM historia_operacji AS h JOIN egzemplarze AS e ON h.egzemplarz_id = e.egzemplarz_id
                        JOIN ksiazki AS k ON e.ksiazka_id = k.ksiazka_id
                WHERE rodzaj_operacji = 'wypozyczenie' AND (SELECT YEAR(h.data)) = bookDateYear
                group by bookTitle
            )
        SELECT MAX(borrowCount)
        FROM bookOperations
        LIMIT 1
    );
END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `findBestBookTitle` (`bookDateYear` INT) RETURNS VARCHAR(100) CHARSET utf8 COLLATE utf8_polish_ci BEGIN
    RETURN(
        WITH
            bookOperations AS (
                SELECT k.tytul as bookTitle, count(*) as borrowCount
                FROM historia_operacji AS h JOIN egzemplarze AS e ON h.egzemplarz_id = e.egzemplarz_id
                        JOIN ksiazki AS k ON e.ksiazka_id = k.ksiazka_id
                WHERE rodzaj_operacji = 'wypozyczenie' AND (SELECT YEAR(h.data)) = bookDateYear
                group by bookTitle
            )
        SELECT bookTitle
        FROM bookOperations
        HAVING MAX(borrowCount)
        LIMIT 1
    );
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Czyszczenie starych tablic
--

DROP TABLE IF EXISTS `autorzy`, `autor_ksiazka`, `biblioteki`,
            `czytelnicy`, `dzialy`, `egzemplarze`,
            `gatunki`, `historia_operacji`, `ksiazki`,
            `pracownicy`, `regaly`, `wlasciciele`, `wlasciciel_biblioteka`;

DROP TRIGGER IF EXISTS `authorsAddTriger`;
DROP TRIGGER IF EXISTS `authorsUpdateTriger`;
DROP TRIGGER IF EXISTS `author_bookAddTriger`;
DROP TRIGGER IF EXISTS `author_bookUpdateTriger`;
DROP TRIGGER IF EXISTS `librariesAddTriger`;
DROP TRIGGER IF EXISTS `librariesUpdateTriger`;
DROP TRIGGER IF EXISTS `readersAddTriger`;
DROP TRIGGER IF EXISTS `readersUpdateTriger`;
DROP TRIGGER IF EXISTS `sectionsAddTriger`;
DROP TRIGGER IF EXISTS `sectionsUpdateTriger`;
DROP TRIGGER IF EXISTS `specimensAddTriger`;
DROP TRIGGER IF EXISTS `specimensUpdateTriger`;
DROP TRIGGER IF EXISTS `genresAddTriger`;
DROP TRIGGER IF EXISTS `genresUpdateTriger`;
DROP TRIGGER IF EXISTS `operationsAddTriger`;
DROP TRIGGER IF EXISTS `operationsUpdateTriger`;
DROP TRIGGER IF EXISTS `booksAddTriger`;
DROP TRIGGER IF EXISTS `booksUpdateTriger`;
DROP TRIGGER IF EXISTS `workersAddTriger`;
DROP TRIGGER IF EXISTS `workersUpdateTriger`;
DROP TRIGGER IF EXISTS `bookstandsAddTriger`;
DROP TRIGGER IF EXISTS `bookstandsUpdateTriger`;
DROP TRIGGER IF EXISTS `ovnersAddTriger`;
DROP TRIGGER IF EXISTS `ovnersUpdateTriger`;
DROP TRIGGER IF EXISTS `ovner_libraryAddTriger`;
DROP TRIGGER IF EXISTS `ovner_libraryUpdateTriger`;

--
-- Struktura tabeli dla tabeli `autorzy`
--

CREATE TABLE `autorzy` (
  `autor_id` int(11) NOT NULL,
  `imie` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `nazwisko` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `data_urodzenia` date NOT NULL,
  `data_smierci` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `autorzy`
--

INSERT INTO `autorzy` (`autor_id`, `imie`, `nazwisko`, `data_urodzenia`, `data_smierci`) VALUES
(0, 'Jan', 'Krol', '1978-09-03', NULL),
(1, 'Maciej', 'Nowak', '1976-03-30', NULL),
(2, 'Jakub', 'Zima', '1974-10-11', '1990-10-11'),
(3, 'Natalia', 'Leszczyk', '1971-12-25', NULL),
(4, 'Piotr', 'Karol', '1971-12-25', '1991-07-17'),
(5, 'Piotr', 'Nowaczyk', '1973-07-17', NULL),
(6, 'Marta', 'Kowalczyk', '1974-10-11', NULL),
(7, 'Joanna', 'Wozniak', '1978-09-03', '2003-01-22'),
(8, 'Jakub', 'Mazur', '1973-07-17', '2007-08-01'),
(9, 'Jakub', 'Krawczyk', '1973-07-17', NULL);

--
-- Wyzwalacze `autorzy`
--
DELIMITER $$
CREATE TRIGGER `authorsAddTriger` BEFORE INSERT ON `autorzy` FOR EACH ROW BEGIN
    SET @name = NEW.imie;
    SET @surname = NEW.nazwisko;
    SET @birthDay = NEW.data_urodzenia;
    SET @deathDay = NEW.data_smierci;

    IF (SELECT EXISTS (SELECT * FROM autorzy WHERE imie = @name AND nazwisko = @surname AND data_urodzenia = @birthDay)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "This author already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @surname IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. You need to set surname it can't be none.";
    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF (SELECT (SELECT CURDATE()) < @birthDay) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong birthDay. Date can't be from the future.";
    ELSEIF @birthDay IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong birthDay. You need to set birthDay it can't be none.";
    ELSEIF @birthDay = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong birthDay. Make sure date is in 'YYYY-MM-DD' format.";

    ELSEIF (SELECT (SELECT CURDATE()) < @deathDay) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong deathDay. Date can't be from the future.";
    ELSEIF @deathDay = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong deathDay. Make sure date is in 'YYYY-MM-DD' format.";
    ELSEIF @deathDay < @birthDay THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong deathDay. deathDay can't be before birthDay";
    ELSEIF @deathDay IS NULL AND DATEDIFF(CURDATE(), @birthDay) > 43830 THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Death day can't be null with this birthday. This author would have lived over 120 years.";
    ELSEIF DATEDIFF(@deathDay, @birthDay) > 43830 THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Birthday and deathday are set uncorrectly. This author would have lived over 120 years.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `authorsUpdateTriger` BEFORE UPDATE ON `autorzy` FOR EACH ROW BEGIN
    SET @name = NEW.imie;
    SET @oldName = OLD.imie;
    SET @oldSurname = OLD.nazwisko;
    SET @surname = NEW.nazwisko;
    SET @birthDay = NEW.data_urodzenia;
    SET @oldBirthDay = OLD.data_urodzenia;
    SET @deathDay = NEW.data_smierci;

    IF (SELECT EXISTS (SELECT * FROM autorzy WHERE imie = @name AND nazwisko = @surname AND data_urodzenia = @birthDay)
        AND @name <> @oldName AND @surname <> @oldSurname AND @birthDay <> @oldBirthDay) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "This author already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @surname IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. You need to set surname it can't be none.";
    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF (SELECT (SELECT CURDATE()) < @birthDay) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong birthDay. Date can't be from the future.";
    ELSEIF @birthDay IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong birthDay. You need to set birthDay it can't be none.";
    ELSEIF @birthDay = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong birthDay. Make sure date is in 'YYYY-MM-DD' format.";

    ELSEIF (SELECT (SELECT CURDATE()) < @deathDay) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong deathDay. Date can't be from the future.";
    ELSEIF @deathDay = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong deathDay. Make sure date is in 'YYYY-MM-DD' format.";
    ELSEIF @deathDay < @birthDay THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong deathDay. deathDay can't be before birthDay";
    ELSEIF @deathDay IS NULL AND DATEDIFF(CURDATE(), @birthDay) > 43830 THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Death day can't be null with this birthday. This author would have lived over 120 years.";
    ELSEIF DATEDIFF(@deathDay, @birthDay) > 43830 THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Birthday and deathday are set uncorrectly. This author would have lived over 120 years.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `autor_ksiazka`
--

CREATE TABLE `autor_ksiazka` (
  `autorzy_autor_id` int(11) NOT NULL,
  `ksiazki_ksiazka_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `autor_ksiazka`
--

INSERT INTO `autor_ksiazka` (`autorzy_autor_id`, `ksiazki_ksiazka_id`) VALUES
(1, 1),
(7, 1),
(5, 1),
(2, 2),
(3, 3),
(4, 4),
(2, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(0, 0),
(2, 0);

--
-- Wyzwalacze `autor_ksiazka`
--
DELIMITER $$
CREATE TRIGGER `author_bookAddTriger` BEFORE INSERT ON `autor_ksiazka` FOR EACH ROW BEGIN
    SET @author_id = NEW.autorzy_autor_id;
    SET @ksiazka_id = NEW.ksiazki_ksiazka_id;

    IF (SELECT EXISTS (SELECT * FROM autor_ksiazka WHERE autorzy_autor_id = @author_id
            AND ksiazki_ksiazka_id = @ksiazka_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "This book has already been written by this author.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM autorzy WHERE autor_id = @author_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Author with this author_id dosn't exist.";
    ELSEIF @author_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong author_id. You need to set autor_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM ksiazki WHERE ksiazka_id = @ksiazka_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Book with this book_id dosn't exist.";
    ELSEIF @ksiazka_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong ksiazka_id. You need to set ksiazka_id it can't be none.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `author_bookUpdateTriger` BEFORE UPDATE ON `autor_ksiazka` FOR EACH ROW BEGIN
    SET @author_id = NEW.autorzy_autor_id;
    SET @oldAuthor_id = OLD.autorzy_autor_id;
    SET @ksiazka_id = NEW.ksiazki_ksiazka_id;
    SET @oldKsiazka_id = OLD.ksiazki_ksiazka_id;

    IF (SELECT EXISTS (SELECT * FROM autor_ksiazka WHERE ksiazki_ksiazka_id = @ksiazka_id AND autorzy_autor_id = @author_id)
            AND @ksiazka_id <> @oldKsiazka_id AND @author_id <> @oldAuthor_id) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "This book has already been written by this author.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM autorzy WHERE autor_id = @author_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Author with this author_id dosn't exist.";
    ELSEIF @author_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong author_id. You need to set autor_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM ksiazki WHERE ksiazka_id = @ksiazka_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Book with this book_id dosn't exist.";
    ELSEIF @ksiazka_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong ksiazka_id. You need to set ksiazka_id it can't be none.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `biblioteki`
--

CREATE TABLE `biblioteki` (
  `nazwa` varchar(50) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `lokalizacja` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `biblioteki`
--

INSERT INTO `biblioteki` (`nazwa`, `lokalizacja`) VALUES
('Biblioteka_dziecieca', 'Krutka_1'),
('Biblioteka_miejska', 'Wroclawska_43'),
('Biblioteka_na_Kwiatowej', 'Brudna_31'),
('Biblioteka_na_rynku', 'Powstancow_2'),
('Biblioteka_szkolna', 'Poznanska_12'),
('Czytam_ksiazki', 'Kwiatowa_10'),
('Czytanie_jest_fajne', 'Rzeczypospolitej_5'),
('Ksiazki_sa_super', 'Dluga_4'),
('Super_Biblioteka', 'Czysta_21'),
('Warto_czytac', 'Zawila_3');

--
-- Wyzwalacze `biblioteki`
--
DELIMITER $$
CREATE TRIGGER `librariesAddTriger` BEFORE INSERT ON `biblioteki` FOR EACH ROW BEGIN
    SET @name = NEW.nazwa;
    SET @location = NEW.lokalizacja;

    IF (SELECT EXISTS (SELECT * FROM biblioteki WHERE nazwa = @name)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Library with this name already exists.";
    ELSEIF (SELECT EXISTS (SELECT * FROM biblioteki WHERE lokalizacja = @location)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Library with this location already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter.";

    ELSEIF @location IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong location. You need to set location it can't be none.";
    ELSEIF NOT @location REGEXP BINARY '^[A-Z]{1}[a-z]*_[0-9]+$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong location. Make sure location is in 'Address_X' format.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `librariesUpdateTriger` BEFORE UPDATE ON `biblioteki` FOR EACH ROW BEGIN
    SET @name = NEW.nazwa;
    SET @location = NEW.lokalizacja;

    SET @oldName = OLD.nazwa;
    SET @oldLocation = OLD.lokalizacja;

    IF @name <> @oldName AND (SELECT EXISTS (SELECT * FROM biblioteki WHERE nazwa = @name)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Library with this name already exists.";
    ELSEIF @location <> @oldLocation AND (SELECT EXISTS (SELECT * FROM biblioteki WHERE lokalizacja = @location)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Library with this location already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter.";

    ELSEIF @location IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong location. You need to set location it can't be none.";
    ELSEIF NOT @location REGEXP BINARY '^[A-Z]{1}[a-z]*_[0-9]+$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong location. Make sure location is in 'Address_X' format.";

    END IF;

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `czytelnicy`
--

CREATE TABLE `czytelnicy` (
  `czytelnik_id` int(11) NOT NULL,
  `imie` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `nazwisko` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `czytelnicy`
--

INSERT INTO `czytelnicy` (`czytelnik_id`, `imie`, `nazwisko`) VALUES
(0, 'Marta', 'Krawczyk'),
(1, 'Jakub', 'Krol'),
(2, 'Olga', 'Nowak'),
(3, 'Magda', 'Zima'),
(4, 'Magda', 'Leszczyk'),
(5, 'Piotr', 'Karol'),
(6, 'Natalia', 'Nowaczyk'),
(7, 'Natalia', 'Kowalczyk'),
(8, 'Karol', 'Wozniak'),
(9, 'Karol', 'Mazur');

--
-- Wyzwalacze `czytelnicy`
--
DELIMITER $$
CREATE TRIGGER `readersAddTriger` BEFORE INSERT ON `czytelnicy` FOR EACH ROW BEGIN
    SET @name = NEW.imie;
    SET @surname = NEW.nazwisko;

    IF (SELECT EXISTS (SELECT * FROM czytelnicy WHERE imie = @name AND nazwisko = @surname)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Reader with this name and surname already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @surname IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. You need to set surname it can't be none.";
    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure surname starts with upper letter and doesn't contain any non letter chracters.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `readersUpdateTriger` BEFORE UPDATE ON `czytelnicy` FOR EACH ROW BEGIN
    SET @name = NEW.imie;
    SET @oldName = OLD.imie;
    SET @surname = NEW.nazwisko;
    SET @oldSurname = OLD.nazwisko;

    IF (SELECT EXISTS (SELECT * FROM czytelnicy WHERE imie = @name AND nazwisko = @surname)
            AND @name <> @oldName AND @surname <> @oldSurname) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Reader with this name and surname already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @surname IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. You need to set surname it can't be none.";
    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure surname starts with upper letter and doesn't contain any non letter chracters.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `dzialy`
--

CREATE TABLE `dzialy` (
  `nazwa` varchar(20) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `lokalizacja` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `dzialy`
--

INSERT INTO `dzialy` (`nazwa`, `lokalizacja`) VALUES
('dzial0', 'lokalizacja0'),
('dzial1', 'lokalizacja1'),
('dzial2', 'lokalizacja2'),
('dzial3', 'lokalizacja3'),
('dzial4', 'lokalizacja4'),
('dzial5', 'lokalizacja5'),
('dzial6', 'lokalizacja6'),
('dzial7', 'lokalizacja7'),
('dzial8', 'lokalizacja8'),
('dzial9', 'lokalizacja9');

--
-- Wyzwalacze `dzialy`
--
DELIMITER $$
CREATE TRIGGER `sectionsAddTriger` BEFORE INSERT ON `dzialy` FOR EACH ROW BEGIN
    SET @name = NEW.nazwa;
    SET @location = NEW.lokalizacja;

    IF (SELECT EXISTS (SELECT * FROM dzialy WHERE nazwa = @name)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Section with this name already exists.";
    ELSEIF (SELECT EXISTS (SELECT * FROM dzialy WHERE lokalizacja = @location)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Section with this location already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";

    ELSEIF @location IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong location. You need to set location it can't be none.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `sectionsUpdateTriger` BEFORE UPDATE ON `dzialy` FOR EACH ROW BEGIN
    SET @name = NEW.nazwa;
    SET @location = NEW.lokalizacja;

    SET @oldName = OLD.nazwa;
    SET @oldLocation = OLD.lokalizacja;

    IF @oldName <> @name AND (SELECT EXISTS (SELECT * FROM dzialy WHERE nazwa = @name)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Section with this name already exists.";
    ELSEIF @oldLocation <> @location AND (SELECT EXISTS (SELECT * FROM dzialy WHERE lokalizacja = @location)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Section with this location already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";

    ELSEIF @location IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong location. You need to set location it can't be none.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `egzemplarze`
--

CREATE TABLE `egzemplarze` (
  `egzemplarz_id` int(11) NOT NULL,
  `ksiazka_id` int(11) NOT NULL,
  `regal_numer` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `egzemplarze`
--

INSERT INTO `egzemplarze` (`egzemplarz_id`, `ksiazka_id`, `regal_numer`) VALUES
(0, 4, 8),
(1, 5, 5),
(2, 3, 6),
(3, 3, 4),
(4, 4, 0),
(5, 1, 2),
(6, 3, 7),
(7, 4, 6),
(8, 7, 1),
(9, 8, 7),
(10, 5, 4),
(11, 8, 2),
(12, 1, 8),
(13, 7, 0),
(14, 9, 0),
(15, 4, 6),
(16, 0, 7),
(17, 6, 8),
(18, 6, 7),
(19, 2, 8);


--
-- Wyzwalacze `egzemplarze`
--
DELIMITER $$
CREATE TRIGGER `specimensAddTriger` BEFORE INSERT ON `egzemplarze` FOR EACH ROW BEGIN
    SET @book_id = NEW.ksiazka_id;
    SET @bookstand_number = NEW.regal_numer;

    IF (SELECT NOT EXISTS (SELECT * FROM ksiazki WHERE ksiazka_id = @book_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Book with this book_id dosn't exist.";
    ELSEIF @book_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong book_id. You need to set book_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM regaly WHERE numer = @bookstand_number)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Bookstand with this number dosn't exist.";
    ELSEIF @bookstand_number IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong bookstand number. You need to set bookstand_number it can't be none.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `specimensUpdateTriger` BEFORE UPDATE ON `egzemplarze` FOR EACH ROW BEGIN
    SET @book_id = NEW.ksiazka_id;
    SET @bookstand_number = NEW.regal_numer;

    IF (SELECT NOT EXISTS (SELECT * FROM ksiazki WHERE ksiazka_id = @book_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Book with this book_id dosn't exist.";
    ELSEIF @book_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong book_id. You need to set book_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM regaly WHERE numer = @bookstand_number)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Bookstand with this number dosn't exist.";
    ELSEIF @bookstand_number IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong bookstand number. You need to set bookstand_number it can't be none.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `gatunki`
--

CREATE TABLE `gatunki` (
  `gatunek` varchar(20) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `gatunki`
--

INSERT INTO `gatunki` (`gatunek`) VALUES
('fantasy'),
('horror'),
('klasyka'),
('kryminal'),
('literatura_mlodziezo'),
('literatura_obyczajow'),
('powiesc_historyczna'),
('romans'),
('sensacja'),
('thriller');

--
-- Wyzwalacze `gatunki`
--
DELIMITER $$
CREATE TRIGGER `genresAddTriger` BEFORE INSERT ON `gatunki` FOR EACH ROW BEGIN
    SET @name = NEW.gatunek;

    IF (SELECT EXISTS (SELECT * FROM gatunki WHERE gatunek = @name)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Genre with this name already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `genresUpdateTriger` BEFORE UPDATE ON `gatunki` FOR EACH ROW BEGIN
    SET @name = NEW.gatunek;
    SET @oldName = OLD.gatunek;

    IF (SELECT EXISTS (SELECT * FROM gatunki WHERE gatunek = @name) AND @name <> @oldName) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Genre with this name already exists.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `historia_operacji`
--

CREATE TABLE `historia_operacji` (
  `operacja_id` int(11) NOT NULL,
  `data` date NOT NULL,
  `biblioteka_nazwa` varchar(50) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `pracownik_id` int(11) NOT NULL,
  `czytelnik_id` int(11) NOT NULL,
  `egzemplarz_id` int(11) NOT NULL,
  `rodzaj_operacji` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL CHECK (`rodzaj_operacji` in ('wypozyczenie','zwrot','przedluzenie')),
  `opoznienie` int(11) DEFAULT NULL,
  `uwagi` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `historia_operacji`
--

INSERT INTO `historia_operacji` (`operacja_id`, `data`, `biblioteka_nazwa`, `pracownik_id`, `czytelnik_id`, `egzemplarz_id`, `rodzaj_operacji`, `opoznienie`, `uwagi`) VALUES
(0, '1972-08-01', 'Biblioteka_na_rynku', 7, 7, 4, 'wypozyczenie', NULL, 'bez uwag'),
(1, '1975-01-22', 'Ksiazki_sa_super', 1, 1, 9, 'wypozyczenie', NULL, NULL),
(2, '1978-09-03', 'Biblioteka_na_rynku', 1, 4, 8, 'wypozyczenie', NULL, 'pierwszy raz od dawna'),
(3, '1978-09-03', 'Biblioteka_dziecieca', 2, 1, 7, 'wypozyczenie', NULL, NULL),
(4, '1976-03-30', 'Super_Biblioteka', 3, 9, 5, 'wypozyczenie', NULL, 'bez uwag'),
(5, '1973-07-17', 'Czytam_ksiazki', 1, 2, 4, 'wypozyczenie', NULL, 'sprawna operacja'),
(6, '1978-09-03', 'Biblioteka_dziecieca', 7, 6, 4, 'wypozyczenie', NULL, NULL),
(7, '1972-08-01', 'Czytanie_jest_fajne', 8, 2, 8, 'wypozyczenie', NULL, 'pierwszy raz od dawna'),
(8, '1975-01-22', 'Biblioteka_na_Kwiatowej', 9, 1, 8, 'wypozyczenie', NULL, 'bez uwag'),
(9, '1973-07-17', 'Czytam_ksiazki', 7, 9, 3, 'wypozyczenie', NULL, NULL),
(10, '1973-07-17', 'Biblioteka_dziecieca', 1, 6, 16, 'wypozyczenie', NULL, NULL),
(11, '1971-12-25', 'Biblioteka_na_rynku', 5, 4, 15, 'wypozyczenie', NULL, 'pierwszy raz od dawna'),
(12, '1976-03-30', 'Super_Biblioteka', 3, 5, 18, 'wypozyczenie', NULL, 'sprawna operacja'),
(13, '1973-07-17', 'Czytam_ksiazki', 4, 3, 13, 'wypozyczenie', NULL, NULL),
(14, '1976-03-30', 'Ksiazki_sa_super', 5, 3, 15, 'wypozyczenie', NULL, 'bez uwag'),
(15, '1970-05-05', 'Ksiazki_sa_super', 2, 3, 14, 'wypozyczenie', NULL, 'sprawna operacja'),
(16, '1979-04-14', 'Czytam_ksiazki', 7, 4, 18, 'wypozyczenie', NULL, NULL),
(17, '1971-12-25', 'Super_Biblioteka', 2, 1, 12, 'wypozyczenie', NULL, 'bez uwag'),
(18, '1973-07-17', 'Ksiazki_sa_super', 9, 1, 16, 'wypozyczenie', NULL, NULL),
(19, '1977-11-28', 'Biblioteka_dziecieca', 0, 4, 18, 'wypozyczenie', NULL, 'bez uwag');


--
-- Wyzwalacze `historia_operacji`
--
DELIMITER $$
CREATE TRIGGER `operationsAddTriger` BEFORE INSERT ON `historia_operacji` FOR EACH ROW BEGIN
    SET @date = NEW.data;
    SET @libraryName = NEW.biblioteka_nazwa;
    SET @worker_id = NEW.pracownik_id;
    SET @reader_id = NEW.czytelnik_id;
    SET @specimen_id = NEW.egzemplarz_id;
    SET @operationType = NEW.rodzaj_operacji;
    SET @delay = NEW.opoznienie;
    SET @comments = NEW.uwagi;

    IF (SELECT EXISTS (SELECT * FROM historia_operacji WHERE data = @date AND biblioteka_nazwa = @libraryName
            AND pracownik_id = @worker_id AND czytelnik_id = @reader_id AND egzemplarz_id = @specimen_id
            AND rodzaj_operacji = @operationType AND opoznienie = @delay AND uwagi = @comments)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "This operation already exists.";

    ELSEIF (SELECT (SELECT CURDATE()) < @date) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Date can't be from the future.";
    ELSEIF @date IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. You need to set date it can't be none.";
    ELSEIF @date = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Make sure date is in 'YYYY-MM-DD' format.";

    ELSEIF @libraryName IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong libraryName. You need to set libraryName it can't be none.";
    ELSEIF NOT @libraryName REGEXP BINARY '^[A-Z]{1}' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong libraryName. Make sure libraryName starts with upper letter.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM pracownicy WHERE pracownik_id = @worker_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Worker with this worker_id dosn't exist.";
    ELSEIF @worker_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong worker_id. You need to set worker_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM czytelnicy WHERE czytelnik_id = @reader_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Reader with this reader_id dosn't exist.";
    ELSEIF @reader_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong reader_id. You need to set reader_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM egzemplarze WHERE egzemplarz_id = @specimen_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Specimen with this specimen_id dosn't exist.";
    ELSEIF @specimen_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong specimen_id. You need to set specimen_id it can't be none.";

    ELSEIF @operationType IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong operation type. You need to set operation type it can't be none.";
    ELSEIF @operationType NOT IN ('zwrot', 'wypozyczenie', 'przedluzenie') THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "You need to set operation type to 'zwrot', 'wypozyczenie' or 'przedluzenie'.";

    ELSEIF @delay IS NOT NULL AND @delay < 0 THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong delay. You need to set positive delay.";
    ELSEIF @delay IS NOT NULL AND 1000 < @delay THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong delay. You need to set less then 1000.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `operationsUpdateTriger` BEFORE UPDATE ON `historia_operacji` FOR EACH ROW BEGIN
    SET @date = NEW.data;
    SET @oldDate = OLD.data;
    SET @libraryName = NEW.biblioteka_nazwa;
    SET @oldLibraryName = OLD.biblioteka_nazwa;
    SET @worker_id = NEW.pracownik_id;
    SET @oldWorker_id = OLD.pracownik_id;
    SET @reader_id = NEW.czytelnik_id;
    SET @oldReader_id = OLD.czytelnik_id;
    SET @specimen_id = NEW.egzemplarz_id;
    SET @oldSpecimen_id = OLD.egzemplarz_id;
    SET @operationType = NEW.rodzaj_operacji;
    SET @oldOperationType = OLD.rodzaj_operacji;
    SET @delay = NEW.opoznienie;
    SET @oldDelay = OLD.opoznienie;
    SET @comments = NEW.uwagi;
    SET @oldComments = OLD.uwagi;

    IF (SELECT EXISTS (SELECT * FROM historia_operacji WHERE data = @date AND biblioteka_nazwa = @libraryName
            AND pracownik_id = @worker_id AND czytelnik_id = @reader_id AND egzemplarz_id = @specimen_id
            AND rodzaj_operacji = @operationType
            AND (@date <> @oldDate OR @libraryName <> @oldLibraryName OR @worker_id <> @oldWorker_id
            OR @reader_id <> @oldReader_id OR @specimen_id <> @oldSpecimen_id OR @operationType <> @oldOperationType))) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "This operation already exists.";

    ELSEIF (SELECT (SELECT CURDATE()) < @date) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Date can't be from the future.";
    ELSEIF @date IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. You need to set date it can't be none.";
    ELSEIF @date = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Make sure date is in 'YYYY-MM-DD' format.";

    ELSEIF @libraryName IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong libraryName. You need to set libraryName it can't be none.";
    ELSEIF NOT @libraryName REGEXP BINARY '^[A-Z]{1}' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong libraryName. Make sure libraryName starts with upper letter.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM pracownicy WHERE pracownik_id = @worker_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Worker with this worker_id dosn't exist.";
    ELSEIF @worker_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong worker_id. You need to set worker_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM czytelnicy WHERE czytelnik_id = @reader_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Reader with this reader_id dosn't exist.";
    ELSEIF @reader_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong reader_id. You need to set reader_id it can't be none.";

    ELSEIF (SELECT NOT EXISTS (SELECT * FROM egzemplarze WHERE egzemplarz_id = @specimen_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Specimen with this specimen_id dosn't exist.";
    ELSEIF @specimen_id IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong specimen_id. You need to set specimen_id it can't be none.";

    ELSEIF @operationType IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong operation type. You need to set operation type it can't be none.";
    ELSEIF @operationType NOT IN ('zwrot', 'wypozyczenie', 'przedluzenie') THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong operation type. You need to set operation type to 'zwrot', 'wypozyczenie' or 'przedluzenie'.";

    ELSEIF @delay IS NOT NULL AND @delay < 0 THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong delay. You need to set positive delay.";
    ELSEIF @delay IS NOT NULL AND 1000 < @delay THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong delay. You need to set less then 1000.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `ksiazki`
--

CREATE TABLE `ksiazki` (
  `ksiazka_id` int(11) NOT NULL,
  `tytul` varchar(100) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `data_opublikowania` date NOT NULL,
  `gatunek` varchar(20) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `ksiazki`
--

INSERT INTO `ksiazki` (`ksiazka_id`, `tytul`, `data_opublikowania`, `gatunek`) VALUES
(0, 'Trociny', '1989-04-14', 'powiesc_historyczna'),
(1, 'Szeptucha', '1989-04-14', 'fantasy'),
(2, 'Polska_odwraca_oczy', '1980-05-05', 'horror'),
(3, 'On', '1989-04-14', 'klasyka'),
(4, 'Zycie_na_pelnej_petardzie', '1988-09-03', 'kryminal'),
(5, 'Okularnik', '1982-08-01', 'sensacja'),
(6, 'Najgorszy_czlowiek_na_swiecie', '1987-11-28', 'thriller'),
(7, 'Inna_dusza', '1982-08-01', 'literatura_mlodziezo'),
(8, 'Ksiegi_Jakubowe', '1984-10-11', 'literatura_obyczajow'),
(9, 'Gniew', '1984-10-11', 'romans');

--
-- Wyzwalacze `ksiazki`
--
DELIMITER $$
CREATE TRIGGER `booksAddTriger` BEFORE INSERT ON `ksiazki` FOR EACH ROW BEGIN
    SET @title = NEW.tytul;
    SET @date = NEW.data_opublikowania;
    SET @genre = NEW.gatunek;

    IF (SELECT EXISTS (SELECT * FROM ksiazki WHERE tytul = @title)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Book with this title already exists.";

    ELSEIF @title IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong title. You need to set title it can't be none.";
    ELSEIF NOT @title REGEXP BINARY '^[A-Z]{1}' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong title. Make sure title starts with upper letter.";

    ELSEIF (SELECT (SELECT CURDATE()) < @date) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Date can't be from the future.";
    ELSEIF @date IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. You need to set date it can't be none.";
    ELSEIF @date = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Make sure date is in 'YYYY-MM-DD' format.";

    ELSEIF @genre IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong genre. You need to set genre it can't be none.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `booksUpdateTriger` BEFORE UPDATE ON `ksiazki` FOR EACH ROW BEGIN
    SET @title = NEW.tytul;
    SET @oldTitle = OLD.tytul;
    SET @date = NEW.data_opublikowania;
    SET @genre = NEW.gatunek;

    IF (SELECT EXISTS (SELECT * FROM ksiazki WHERE tytul = @title) AND @title <> @oldTitle) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Book with this title already exists.";

    ELSEIF @title IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong title. You need to set title it can't be none.";
    ELSEIF NOT @title REGEXP BINARY '^[A-Z]{1}' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong title. Make sure title starts with upper letter.";

    ELSEIF (SELECT (SELECT CURDATE()) < @date) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Date can't be from the future.";
    ELSEIF @date IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. You need to set date it can't be none.";
    ELSEIF @date = '0000-00-00' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong date. Make sure date is in 'YYYY-MM-DD' format.";

    ELSEIF @genre IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong genre. You need to set genre it can't be none.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `pracownicy`
--

CREATE TABLE `pracownicy` (
  `pracownik_id` int(11) NOT NULL,
  `szef_id` int(11) DEFAULT NULL,
  `imie` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `nazwisko` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `funkcja` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `pracownicy`
--

INSERT INTO `pracownicy` (`pracownik_id`, `szef_id`, `imie`, `nazwisko`, `funkcja`) VALUES
(0, 3, 'Jan', 'Krol', 'obsluga_bazy'),
(1, 3, 'Joanna', 'Nowak', 'sprzatanie'),
(2, NULL, 'Jan', 'Zima', 'obsluga_bazy'),
(3, NULL, 'Marta', 'Leszczyk', 'szef'),
(4, NULL, 'Karol', 'Karol', 'kucharz'),
(5, 6, 'Olga', 'Nowaczyk', 'kucharz'),
(6, NULL, 'Karol', 'Kowalczyk', 'szef'),
(7, NULL, 'Maciej', 'Wozniak', 'obsluga_bazy'),
(8, 6, 'Jakub', 'Mazur', 'kucharz'),
(9, NULL, 'Piotr', 'Krawczyk', 'obsluga_bazy');

--
-- Wyzwalacze `pracownicy`
--
DELIMITER $$
CREATE TRIGGER `workersAddTriger` BEFORE INSERT ON `pracownicy` FOR EACH ROW BEGIN
    SET @boss_id = NEW.szef_id;
    SET @name = NEW.imie;
    SET @surname = NEW.nazwisko;
    SET @function = NEW.funkcja;

    IF (SELECT EXISTS (SELECT * FROM pracownicy WHERE imie = @name AND nazwisko = @surname)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Worker with this name and surname already exists.";

    ELSEIF @boss_id IS NOT NULL AND (SELECT NOT EXISTS (SELECT * FROM pracownicy WHERE pracownik_id = @boss_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Worker with this worker_id dosn't exist.";
    ELSEIF @boss_id IS NOT NULL AND (SELECT funkcja FROM pracownicy WHERE pracownik_id = @boss_id) <> 'szef' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Boss has to have 'szef' function.";
    ELSEIF @boss_id = NEW.pracownik_id THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Worker can't be the boss for himself.";
    ELSEIF @boss_id IS NOT NULL AND (SELECT szef_id FROM pracownicy WHERE pracownik_id = @boss_id) = NEW.pracownik_id THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Boss hierarchy problem.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @surname IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. You need to set surname it can't be none.";
    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure surname starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @function IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong function. You need to set function it can't be none.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `workersUpdateTriger` BEFORE UPDATE ON `pracownicy` FOR EACH ROW BEGIN
    SET @boss_id = NEW.szef_id;
    SET @name = NEW.imie;
    SET @oldName = OLD.imie;
    SET @surname = NEW.nazwisko;
    SET @oldSurname = OLD.nazwisko;
    SET @function = NEW.funkcja;

    IF (SELECT EXISTS (SELECT * FROM pracownicy WHERE imie = @name AND nazwisko = @surname)
            AND @name <> @oldName AND @surname <> @oldSurname) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Worker with this name and surname already exists.";

    ELSEIF @boss_id IS NOT NULL AND (SELECT NOT EXISTS (SELECT * FROM pracownicy WHERE pracownik_id = @boss_id)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Worker with this worker_id dosn't exist.";
    ELSEIF @boss_id IS NOT NULL AND (SELECT funkcja FROM pracownicy WHERE pracownik_id = @boss_id) <> 'szef' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Boss has to have 'szef' function.";
    ELSEIF @boss_id = NEW.pracownik_id THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Worker can't be the boss for himself.";
    ELSEIF @boss_id IS NOT NULL AND (SELECT szef_id FROM pracownicy WHERE pracownik_id = @boss_id) = NEW.pracownik_id THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong boss_id. Boss hierarchy problem.";

    ELSEIF @name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. You need to set name it can't be none.";
    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @surname IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. You need to set surname it can't be none.";
    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure surname starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF @function IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong function. You need to set function it can't be none.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `regaly`
--

CREATE TABLE `regaly` (
  `numer` int(11) NOT NULL,
  `pojemnosc` int(11) NOT NULL,
  `liczba_ksiazek` int(11) NOT NULL,
  `dzial_nazwa` varchar(20) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `regaly`
--

INSERT INTO `regaly` (`numer`, `pojemnosc`, `liczba_ksiazek`, `dzial_nazwa`) VALUES
(0, 6, 3, 'dzial0'),
(1, 8, 1, 'dzial1'),
(2, 5, 2, 'dzial2'),
(3, 7, 0, 'dzial3'),
(4, 9, 2, 'dzial4'),
(5, 6, 1, 'dzial5'),
(6, 5, 3, 'dzial6'),
(7, 8, 4, 'dzial7'),
(8, 8, 4, 'dzial8'),
(9, 9, 0, 'dzial9');

--
-- Wyzwalacze `regaly`
--
DELIMITER $$
CREATE TRIGGER `bookstandsAddTriger` BEFORE INSERT ON `regaly` FOR EACH ROW BEGIN
    SET @number = NEW.numer;
    SET @capacity = NEW.pojemnosc;
    SET @booksCount = NEW.liczba_ksiazek;
    SET @sectionName = NEW.dzial_nazwa;

    IF NOT (@number REGEXP BINARY '^[0-9]+$') THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Bookstand number need to be intiger.";
    ELSEIF (SELECT EXISTS (SELECT * FROM regaly WHERE numer = @number)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Bookstand with this number already exists.";

    ELSEIF @capacity IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong capacity. You need to set capacity it can't be none.";

    ELSEIF @booksCount IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong books count. You need to set books count it can't be none.";
    ELSEIF @capacity < @booksCount THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong books count. Books count can't be greater than bookstand capacity.";

    ELSEIF @sectionName IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong section name. You need to set section name it can't be none.";
    ELSEIF NOT (SELECT EXISTS (SELECT * FROM dzialy WHERE nazwa = @sectionName)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Section with this name dosn't exist.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `bookstandsUpdateTriger` BEFORE UPDATE ON `regaly` FOR EACH ROW BEGIN
    SET @capacity = NEW.pojemnosc;
    SET @booksCount = NEW.liczba_ksiazek;
    SET @sectionName = NEW.dzial_nazwa;

    IF @capacity IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong capacity. You need to set capacity it can't be none.";

    ELSEIF @booksCount IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong books count. You need to set books count it can't be none.";
    ELSEIF @capacity < @booksCount THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong books count. Books count can't be greater than bookstand capacity.";

    ELSEIF @sectionName IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong section name. You need to set section name it can't be none.";
    ELSEIF NOT (SELECT EXISTS (SELECT * FROM dzialy WHERE nazwa = @sectionName)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Section with this name dosn't exist.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wlasciciele`
--

CREATE TABLE `wlasciciele` (
  `nip` varchar(50) COLLATE utf8mb4_polish_ci NOT NULL,
  `nazwa_firmy` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `imie` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `nazwisko` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `wlasciciele`
--

INSERT INTO `wlasciciele` (`nip`, `nazwa_firmy`, `imie`, `nazwisko`) VALUES
('1532573818', 'Januszpol', NULL, NULL),
('1532573819', 'Toyota', NULL, NULL),
('1532573820', 'Adidas', NULL, NULL),
('1532573821', NULL, 'Natalia', 'Leszczyk'),
('1532573822', NULL, 'Jakub', 'Karol'),
('1532573823', NULL, 'Jan', 'Nowaczyk'),
('1532573824', 'Ikea', NULL, NULL),
('1532573825', 'Tesco', NULL, NULL),
('1532573826', NULL, 'Karol', 'Mazur'),
('1532573827', NULL, 'Magda', 'Krawczyk');

--
-- Wyzwalacze `wlasciciele`
--
DELIMITER $$
CREATE TRIGGER `ovnersAddTriger` BEFORE INSERT ON `wlasciciele` FOR EACH ROW BEGIN
    SET @nip = NEW.nip;
    SET @companyName = NEW.nazwa_firmy;
    SET @name = NEW.imie;
    SET @surname = NEW.nazwisko;

    IF (SELECT EXISTS (SELECT * FROM wlasciciele WHERE nip = @nip)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this nip already exists.";
    ELSEIF (SELECT EXISTS (SELECT * FROM wlasciciele WHERE nazwa_firmy = @companyName AND nazwa_firmy IS NOT NULL)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this company name already exists.";
    ELSEIF (SELECT EXISTS (SELECT * FROM wlasciciele WHERE imie = @name AND nazwisko = @surname AND nazwisko IS NOT NULL)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this name and surname already exists.";
    ELSEIF NOT ((@companyName IS NOT NULL AND (@name IS NULL AND @surname IS NULL))
            OR (@companyName IS NULL AND (@name IS NOT NULL AND @surname IS NOT NULL))) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "You need to set firm name or ovner name and surname.";

    ELSEIF @nip IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong nip. You need to set nip it can't be none.";
    ELSEIF NOT (@nip REGEXP '^[0-9]{10}$') THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong nip. Make sure nip has 10 digits.";

    ELSEIF NOT @companyName REGEXP BINARY '^[A-Z]{1}' AND @companyName IS NOT NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong company name. Make sure company name starts with upper letter.";

    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' AND @name IS NOT NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' AND @surname IS NOT NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure surname starts with upper letter and doesn't contain any non letter chracters.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `ovnersUpdateTriger` BEFORE UPDATE ON `wlasciciele` FOR EACH ROW BEGIN
    SET @nip = NEW.nip;
    SET @oldNip = OLD.nip;
    SET @companyName = NEW.nazwa_firmy;
    SET @oldCompanyName = OLD.nazwa_firmy;
    SET @name = NEW.imie;
    SET @oldName = OLD.imie;
    SET @surname = NEW.nazwisko;
    SET @oldSurname = OLD.nazwisko;

    IF (SELECT EXISTS (SELECT * FROM wlasciciele WHERE nip = @nip) AND @nip <> @oldNip) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this nip already exists.";
    ELSEIF (SELECT EXISTS (SELECT * FROM wlasciciele WHERE nazwa_firmy = @companyName AND nazwa_firmy IS NOT NULL)
            AND IFNULL(@companyName <> @oldCompanyName, 1) ) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this company name already exists.";
    ELSEIF (SELECT EXISTS (SELECT * FROM wlasciciele WHERE imie = @name AND nazwisko = @surname
            AND nazwisko IS NOT NULL) AND @name <> @oldName AND @surname <> @oldSurname) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this name and surname already exists.";
     ELSEIF NOT ((@companyName IS NOT NULL AND (@name IS NULL AND @surname IS NULL))
             OR (@companyName IS NULL AND (@name IS NOT NULL AND @surname IS NOT NULL))) THEN
         SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "You need to set firm name or ovner name and surname.";

    ELSEIF @nip IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong nip. You need to set nip it can't be none.";
    ELSEIF NOT (@nip REGEXP '^[0-9]{10}$') THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong nip. Make sure nip has 10 digits.";

    ELSEIF NOT @companyName REGEXP BINARY '^[A-Z]{1}' AND @companyName IS NOT NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong company name. Make sure company name starts with upper letter.";

    ELSEIF NOT @name REGEXP BINARY '^[A-Z]{1}[a-z]*$' AND @name IS NOT NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong name. Make sure name starts with upper letter and doesn't contain any non letter chracters.";

    ELSEIF NOT @surname REGEXP BINARY '^[A-Z]{1}[a-z]*$' AND @surname IS NOT NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong surname. Make sure surname starts with upper letter and doesn't contain any non letter chracters.";

    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wlasciciel_biblioteka`
--

CREATE TABLE `wlasciciel_biblioteka` (
  `wlasciciel_nip` varchar(50) COLLATE utf8mb4_polish_ci NOT NULL,
  `biblioteka_nazwa` varchar(50) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `wlasciciel_biblioteka`
--

INSERT INTO `wlasciciel_biblioteka` (`wlasciciel_nip`, `biblioteka_nazwa`) VALUES
('1532573818', 'Biblioteka_dziecieca'),
('1532573819', 'Biblioteka_miejska'),
('1532573820', 'Biblioteka_na_Kwiatowej'),
('1532573821', 'Biblioteka_na_rynku'),
('1532573822', 'Biblioteka_szkolna'),
('1532573823', 'Czytam_ksiazki'),
('1532573824', 'Czytanie_jest_fajne'),
('1532573825', 'Ksiazki_sa_super'),
('1532573826', 'Super_Biblioteka'),
('1532573827', 'Warto_czytac');

--
-- Wyzwalacze `wlasciciel_biblioteka`
--
DELIMITER $$
CREATE TRIGGER `ovner_libraryAddTriger` BEFORE INSERT ON `wlasciciel_biblioteka` FOR EACH ROW BEGIN
    SET @ovner_nip = NEW.wlasciciel_nip;
    SET @library_name = NEW.biblioteka_nazwa;

    IF @ovner_nip IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong nip. You need to set nip it can't be none.";
    ELSEIF (SELECT NOT EXISTS (SELECT * FROM wlasciciele WHERE nip = @ovner_nip)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this nip dosn't exist.";

    ELSEIF @library_name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong library name. You need to set library name it can't be none.";
    ELSEIF (SELECT NOT EXISTS (SELECT * FROM biblioteki WHERE nazwa = @library_name)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Library with this name dosn't exist.";

    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `ovner_libraryUpdateTriger` BEFORE UPDATE ON `wlasciciel_biblioteka` FOR EACH ROW BEGIN
    SET @ovner_nip = NEW.wlasciciel_nip;
    SET @library_name = NEW.biblioteka_nazwa;
    SET @oldLibrary_name = OLD.biblioteka_nazwa;

    IF @ovner_nip IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong nip. You need to set nip it can't be none.";
    ELSEIF (SELECT NOT EXISTS (SELECT * FROM wlasciciele WHERE nip = @ovner_nip)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Ovner with this nip dosn't exist.";

    ELSEIF @library_name IS NULL THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Wrong library name. You need to set library name it can't be none.";
    ELSEIF (SELECT NOT EXISTS (SELECT * FROM biblioteki WHERE nazwa = @library_name)) THEN
        SIGNAL SQLSTATE '55555' SET MESSAGE_TEXT = "Library with this name dosn't exist.";

    END IF;
END
$$
DELIMITER ;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `autorzy`
--
ALTER TABLE `autorzy`
  ADD PRIMARY KEY (`autor_id`),
  ADD KEY `au_id` (`autor_id`);

--
-- Indeksy dla tabeli `autor_ksiazka`
--
ALTER TABLE `autor_ksiazka`
  ADD PRIMARY KEY (`autorzy_autor_id`,`ksiazki_ksiazka_id`) USING BTREE,
  ADD KEY `autor_ksiazka_ksiazka_fk` (`ksiazki_ksiazka_id`);

--
-- Indeksy dla tabeli `biblioteki`
--
ALTER TABLE `biblioteki`
  ADD PRIMARY KEY (`nazwa`) USING BTREE;

--
-- Indeksy dla tabeli `czytelnicy`
--
ALTER TABLE `czytelnicy`
  ADD PRIMARY KEY (`czytelnik_id`),
  ADD KEY `cz_id` (`czytelnik_id`);

--
-- Indeksy dla tabeli `dzialy`
--
ALTER TABLE `dzialy`
  ADD PRIMARY KEY (`nazwa`) USING BTREE,
  ADD KEY `dz_na` (`nazwa`);

--
-- Indeksy dla tabeli `egzemplarze`
--
ALTER TABLE `egzemplarze`
  ADD PRIMARY KEY (`egzemplarz_id`),
  ADD KEY `egzemplarz_ksiazka_fk` (`ksiazka_id`),
  ADD KEY `egzemplarz_regal_fk` (`regal_numer`),
  ADD KEY `eg_id` (`egzemplarz_id`);

--
-- Indeksy dla tabeli `gatunki`
--
ALTER TABLE `gatunki`
  ADD PRIMARY KEY (`gatunek`) USING BTREE;

--
-- Indeksy dla tabeli `historia_operacji`
--
ALTER TABLE `historia_operacji`
  ADD PRIMARY KEY (`operacja_id`),
  ADD KEY `biblioteka_nazwa` (`biblioteka_nazwa`,`pracownik_id`,`czytelnik_id`) USING BTREE,
  ADD KEY `historia_czytelnik_fk` (`czytelnik_id`),
  ADD KEY `historia_egzemplarz_fk` (`egzemplarz_id`),
  ADD KEY `historia_pracownik_fk` (`pracownik_id`),
  ADD KEY `op_id` (`operacja_id`);

--
-- Indeksy dla tabeli `ksiazki`
--
ALTER TABLE `ksiazki`
  ADD PRIMARY KEY (`ksiazka_id`),
  ADD KEY `gatunek` (`gatunek`) USING BTREE,
  ADD KEY `ks_id` (`ksiazka_id`);

--
-- Indeksy dla tabeli `pracownicy`
--
ALTER TABLE `pracownicy`
  ADD PRIMARY KEY (`pracownik_id`),
  ADD KEY `szef_id` (`szef_id`),
  ADD KEY `pr_id` (`pracownik_id`);

--
-- Indeksy dla tabeli `regaly`
--
ALTER TABLE `regaly`
  ADD PRIMARY KEY (`numer`),
  ADD KEY `dzial_nazwa` (`dzial_nazwa`) USING BTREE,
  ADD KEY `re_nu` (`numer`);

--
-- Indeksy dla tabeli `wlasciciele`
--
ALTER TABLE `wlasciciele`
  ADD PRIMARY KEY (`nip`),
  ADD KEY `wl_ni` (`nip`);

--
-- Indeksy dla tabeli `wlasciciel_biblioteka`
--
ALTER TABLE `wlasciciel_biblioteka`
  ADD PRIMARY KEY (`wlasciciel_nip`,`biblioteka_nazwa`) USING BTREE,
  ADD KEY `wlasciciel_biblioteka_b_fk` (`biblioteka_nazwa`);

--
-- AUTO_INCREMENT dla tabel zrzutów
--

--
-- AUTO_INCREMENT dla tabeli `autorzy`
--
ALTER TABLE `autorzy`
  MODIFY `autor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT dla tabeli `czytelnicy`
--
ALTER TABLE `czytelnicy`
  MODIFY `czytelnik_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT dla tabeli `egzemplarze`
--
ALTER TABLE `egzemplarze`
  MODIFY `egzemplarz_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT dla tabeli `historia_operacji`
--
ALTER TABLE `historia_operacji`
  MODIFY `operacja_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT dla tabeli `ksiazki`
--
ALTER TABLE `ksiazki`
  MODIFY `ksiazka_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT dla tabeli `pracownicy`
--
ALTER TABLE `pracownicy`
  MODIFY `pracownik_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `autor_ksiazka`
--
ALTER TABLE `autor_ksiazka`
  ADD CONSTRAINT `autor_ksiazka_autor_fk` FOREIGN KEY (`autorzy_autor_id`) REFERENCES `autorzy` (`autor_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `autor_ksiazka_ksiazka_fk` FOREIGN KEY (`ksiazki_ksiazka_id`) REFERENCES `ksiazki` (`ksiazka_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `egzemplarze`
--
ALTER TABLE `egzemplarze`
  ADD CONSTRAINT `egzemplarz_ksiazka_fk` FOREIGN KEY (`ksiazka_id`) REFERENCES `ksiazki` (`ksiazka_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `egzemplarz_regal_fk` FOREIGN KEY (`regal_numer`) REFERENCES `regaly` (`numer`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `historia_operacji`
--
ALTER TABLE `historia_operacji`
  ADD CONSTRAINT `historia_biblioteka_fk` FOREIGN KEY (`biblioteka_nazwa`) REFERENCES `biblioteki` (`nazwa`) ON UPDATE CASCADE ON DELETE CASCADE,
  ADD CONSTRAINT `historia_czytelnik_fk` FOREIGN KEY (`czytelnik_id`) REFERENCES `czytelnicy` (`czytelnik_id`) ON UPDATE CASCADE ON DELETE CASCADE,
  ADD CONSTRAINT `historia_egzemplarz_fk` FOREIGN KEY (`egzemplarz_id`) REFERENCES `egzemplarze` (`egzemplarz_id`) ON UPDATE CASCADE ON DELETE CASCADE,
  ADD CONSTRAINT `historia_pracownik_fk` FOREIGN KEY (`pracownik_id`) REFERENCES `pracownicy` (`pracownik_id`) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Ograniczenia dla tabeli `ksiazki`
--
ALTER TABLE `ksiazki`
  ADD CONSTRAINT `ksiazka_gatunek_fk` FOREIGN KEY (`gatunek`) REFERENCES `gatunki` (`gatunek`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `pracownicy`
--
ALTER TABLE `pracownicy`
  ADD CONSTRAINT `pracownik_szef_fk` FOREIGN KEY (`szef_id`) REFERENCES `pracownicy` (`pracownik_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `regaly`
--
ALTER TABLE `regaly`
  ADD CONSTRAINT `regal_dzial_fk` FOREIGN KEY (`dzial_nazwa`) REFERENCES `dzialy` (`nazwa`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `wlasciciel_biblioteka`
--
ALTER TABLE `wlasciciel_biblioteka`
  ADD CONSTRAINT `wlasciciel_biblioteka_b_fk` FOREIGN KEY (`biblioteka_nazwa`) REFERENCES `biblioteki` (`nazwa`) ON UPDATE CASCADE ON DELETE CASCADE,
  ADD CONSTRAINT `wlasciciel_biblioteka_w_fk` FOREIGN KEY (`wlasciciel_nip`) REFERENCES `wlasciciele` (`nip`) ON UPDATE CASCADE ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

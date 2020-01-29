-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 28 Sty 2020, 15:12
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

-- --------------------------------------------------------

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
(1, 'Olga', 'Krol', '1991-08-01', '1993-12-25'),
(2, 'Jan', 'Nowak', '1988-07-17', NULL),
(3, 'Joanna', 'Zima', '1997-11-28', '1980-04-14'),
(4, 'Marta', 'Leszczyk', '1997-11-28', NULL),
(5, 'Jan', 'Karol', '1997-05-05', '1987-03-30'),
(6, 'Jakub', 'Nowaczyk', '1997-11-28', '1991-08-01'),
(7, 'Joanna', 'Kowalczyk', '1991-01-22', '1997-05-05'),
(8, 'Natalia', 'Wozniak', '1997-11-28', NULL),
(9, 'Olga', 'Mazur', '1991-08-01', NULL),
(10, 'Maciej', 'Krawczyk', '1993-12-25', '1988-07-17');

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
(3, 6),
(3, 9),
(5, 3),
(5, 4),
(5, 5),
(5, 10),
(6, 1),
(6, 2),
(6, 7),
(8, 8);

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
('Biblioteka_dziecieca', 'Czysta_21'),
('Biblioteka_miejska', 'Krutka_1'),
('Biblioteka_na_Kwiatowej', 'Brudna_31'),
('Biblioteka_na_rynku', 'Powstancow_2'),
('Biblioteka_szkolna', 'Brudna_31'),
('Czytam_ksiazki', 'Krutka_1'),
('Czytanie_jest_fajne', 'Dluga_4'),
('Ksiazki_sa_super', 'Dluga_4'),
('Super_Biblioteka', 'Zawila_3'),
('Warto_czytac', 'Poznanska_12');

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
(1, 'Jan', 'Krol'),
(2, 'Marta', 'Nowak'),
(3, 'Jan', 'Zima'),
(4, 'Magda', 'Leszczyk'),
(5, 'Maciej', 'Karol'),
(6, 'Marta', 'Nowaczyk'),
(7, 'Joanna', 'Kowalczyk'),
(8, 'Joanna', 'Wozniak'),
(9, 'Jakub', 'Mazur'),
(10, 'Maciej', 'Krawczyk');

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
(1, 8, 4),
(2, 7, 8),
(3, 7, 2),
(4, 7, 6),
(5, 6, 0),
(6, 8, 7),
(7, 8, 5),
(8, 2, 7),
(9, 5, 8),
(10, 4, 5);

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
  `rodzaj_operacji` text CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL,
  `opoznienie` int(11) DEFAULT NULL,
  `uwagi` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `historia_operacji`
--

INSERT INTO `historia_operacji` (`operacja_id`, `data`, `biblioteka_nazwa`, `pracownik_id`, `czytelnik_id`, `egzemplarz_id`, `rodzaj_operacji`, `opoznienie`, `uwagi`) VALUES
(1, '1992-10-11', 'Super_Biblioteka', 6, 1, 10, 'zwrot', 7, NULL),
(2, '1992-10-11', 'Biblioteka_na_Kwiatowej', 10, 8, 7, 'wypozyczenie', NULL, 'sprawna operacja'),
(3, '1997-05-05', 'Biblioteka_na_rynku', 1, 4, 2, 'zwrot', NULL, NULL),
(4, '1993-12-25', 'Biblioteka_na_Kwiatowej', 8, 1, 2, 'przedluzenie', NULL, NULL),
(5, '1987-03-30', 'Warto_czytac', 7, 1, 8, 'wypozyczenie', NULL, NULL),
(6, '1980-04-14', 'Warto_czytac', 5, 6, 4, 'przedluzenie', 3, 'sprawna operacja'),
(7, '1988-07-17', 'Czytanie_jest_fajne', 10, 5, 10, 'zwrot', 8, NULL),
(8, '1992-10-11', 'Biblioteka_dziecieca', 10, 6, 2, 'wypozyczenie', 11, NULL),
(9, '1980-04-14', 'Czytam_ksiazki', 4, 5, 9, 'zwrot', 4, 'pierwszy raz od dawna'),
(10, '1980-04-14', 'Super_Biblioteka', 6, 3, 2, 'wypozyczenie', 17, NULL);

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
(1, 'Szeptucha', '1990-09-03', 'klasyka'),
(2, 'Polska_odwraca_oczy', '1992-10-11', 'kryminal'),
(3, 'On', '1993-12-25', 'thriller'),
(4, 'Zycie_na_pelnej_petardzie', '1980-04-14', 'thriller'),
(5, 'Okularnik', '1988-07-17', 'powiesc_historyczna'),
(6, 'Najgorszy_czlowiek_na_swiecie', '1987-03-30', 'kryminal'),
(7, 'Inna_dusza', '1990-09-03', 'fantasy'),
(8, 'Ksiegi_Jakubowe', '1992-10-11', 'thriller'),
(9, 'Gniew', '1987-03-30', 'literatura_mlodziezo'),
(10, 'Trociny', '1992-10-11', 'horror');

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
(1, NULL, 'Joanna', 'Krol', 'kucharz'),
(2, NULL, 'Piotr', 'Nowak', 'szef'),
(3, 1, 'Maciej', 'Zima', 'szef'),
(4, 2, 'Natalia', 'Leszczyk', 'kucharz'),
(5, 0, 'Joanna', 'Karol', 'obsluga_bazy'),
(6, NULL, 'Jakub', 'Nowaczyk', 'sprzatanie'),
(7, 3, 'Piotr', 'Kowalczyk', 'obsluga_bazy'),
(8, 1, 'Piotr', 'Wozniak', 'kucharz'),
(9, 7, 'Olga', 'Mazur', 'kucharz'),
(10, NULL, 'Joanna', 'Krawczyk', 'obsluga_bazy');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `regaly`
--

CREATE TABLE `regaly` (
  `numer` int(11) NOT NULL,
  `pojemnosc` int(11) NOT NULL,
  `liczba_ksiazek` int(11) NOT NULL,
  `dział_nazwa` varchar(20) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `regaly`
--

INSERT INTO `regaly` (`numer`, `pojemnosc`, `liczba_ksiazek`, `dział_nazwa`) VALUES
(0, 6, 1, 'dzial6'),
(1, 8, 0, 'dzial5'),
(2, 9, 1, 'dzial9'),
(3, 9, 0, 'dzial6'),
(4, 5, 1, 'dzial6'),
(5, 8, 2, 'dzial5'),
(6, 7, 1, 'dzial3'),
(7, 8, 2, 'dzial7'),
(8, 8, 2, 'dzial2'),
(9, 7, 0, 'dzial3');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wlasciciele`
--

CREATE TABLE `wlasciciele` (
  `nip` int(11) NOT NULL CHECK (`nip` between 1000000000 and 9999999999),
  `nazwa_firmy` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `imie` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `nazwisko` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `wlasciciele`
--

INSERT INTO `wlasciciele` (`nip`, `nazwa_firmy`, `imie`, `nazwisko`) VALUES
(1698602050, NULL, 'Magda', 'Kowalczyk'),
(1698602051, NULL, 'Piotr', 'Nowak'),
(1698602052, 'Tesco', NULL, NULL),
(1698602053, 'Bakoma', NULL, NULL),
(1698602054, 'Januszpol', NULL, NULL),
(1698602055, NULL, 'Natalia', 'Krawczyk'),
(1698602056, NULL, 'Jakub', 'Zima'),
(1698602057, 'Walkman', NULL, NULL),
(1698602058, 'Walkman', NULL, NULL),
(1698602059, 'Junkers', NULL, NULL);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wlasciciel_biblioteka`
--

CREATE TABLE `wlasciciel_biblioteka` (
  `wlasciciel_nip` int(11) NOT NULL,
  `biblioteka_nazwa` varchar(50) CHARACTER SET utf8 COLLATE utf8_polish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `wlasciciel_biblioteka`
--

INSERT INTO `wlasciciel_biblioteka` (`wlasciciel_nip`, `biblioteka_nazwa`) VALUES
(1698602050, 'Super_Biblioteka'),
(1698602051, 'Czytanie_jest_fajne'),
(1698602053, 'Warto_czytac'),
(1698602055, 'Czytam_ksiazki'),
(1698602056, 'Biblioteka_miejska'),
(1698602057, 'Biblioteka_na_Kwiatowej'),
(1698602057, 'Ksiazki_sa_super'),
(1698602059, 'Biblioteka_dziecieca'),
(1698602059, 'Biblioteka_na_rynku'),
(1698602059, 'Biblioteka_szkolna');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `autorzy`
--
ALTER TABLE `autorzy`
  ADD PRIMARY KEY (`autor_id`);

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
  ADD PRIMARY KEY (`czytelnik_id`);

--
-- Indeksy dla tabeli `dzialy`
--
ALTER TABLE `dzialy`
  ADD PRIMARY KEY (`nazwa`) USING BTREE;

--
-- Indeksy dla tabeli `egzemplarze`
--
ALTER TABLE `egzemplarze`
  ADD PRIMARY KEY (`egzemplarz_id`),
  ADD KEY `egzemplarz_ksiazka_fk` (`ksiazka_id`),
  ADD KEY `egzemplarz_regal_fk` (`regal_numer`);

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
  ADD KEY `historia_pracownik_fk` (`pracownik_id`);

--
-- Indeksy dla tabeli `ksiazki`
--
ALTER TABLE `ksiazki`
  ADD PRIMARY KEY (`ksiazka_id`),
  ADD KEY `gatunek` (`gatunek`) USING BTREE;

--
-- Indeksy dla tabeli `pracownicy`
--
ALTER TABLE `pracownicy`
  ADD PRIMARY KEY (`pracownik_id`),
  ADD KEY `szef_id` (`szef_id`);

--
-- Indeksy dla tabeli `regaly`
--
ALTER TABLE `regaly`
  ADD PRIMARY KEY (`numer`),
  ADD KEY `dział_nazwa` (`dział_nazwa`) USING BTREE;

--
-- Indeksy dla tabeli `wlasciciele`
--
ALTER TABLE `wlasciciele`
  ADD PRIMARY KEY (`nip`);

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
  MODIFY `autor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT dla tabeli `czytelnicy`
--
ALTER TABLE `czytelnicy`
  MODIFY `czytelnik_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT dla tabeli `egzemplarze`
--
ALTER TABLE `egzemplarze`
  MODIFY `egzemplarz_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT dla tabeli `historia_operacji`
--
ALTER TABLE `historia_operacji`
  MODIFY `operacja_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT dla tabeli `ksiazki`
--
ALTER TABLE `ksiazki`
  MODIFY `ksiazka_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT dla tabeli `pracownicy`
--
ALTER TABLE `pracownicy`
  MODIFY `pracownik_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `autor_ksiazka`
--
ALTER TABLE `autor_ksiazka`
  ADD CONSTRAINT `autor_ksiazka_autor_fk` FOREIGN KEY (`autorzy_autor_id`) REFERENCES `autorzy` (`autor_id`),
  ADD CONSTRAINT `autor_ksiazka_ksiazka_fk` FOREIGN KEY (`ksiazki_ksiazka_id`) REFERENCES `ksiazki` (`ksiazka_id`);

--
-- Ograniczenia dla tabeli `egzemplarze`
--
ALTER TABLE `egzemplarze`
  ADD CONSTRAINT `egzemplarz_ksiazka_fk` FOREIGN KEY (`ksiazka_id`) REFERENCES `ksiazki` (`ksiazka_id`),
  ADD CONSTRAINT `egzemplarz_regal_fk` FOREIGN KEY (`regal_numer`) REFERENCES `regaly` (`numer`);

--
-- Ograniczenia dla tabeli `historia_operacji`
--
ALTER TABLE `historia_operacji`
  ADD CONSTRAINT `historia_biblioteka_fk` FOREIGN KEY (`biblioteka_nazwa`) REFERENCES `biblioteki` (`nazwa`),
  ADD CONSTRAINT `historia_czytelnik_fk` FOREIGN KEY (`czytelnik_id`) REFERENCES `czytelnicy` (`czytelnik_id`),
  ADD CONSTRAINT `historia_egzemplarz_fk` FOREIGN KEY (`egzemplarz_id`) REFERENCES `egzemplarze` (`egzemplarz_id`),
  ADD CONSTRAINT `historia_pracownik_fk` FOREIGN KEY (`pracownik_id`) REFERENCES `pracownicy` (`pracownik_id`);

--
-- Ograniczenia dla tabeli `ksiazki`
--
ALTER TABLE `ksiazki`
  ADD CONSTRAINT `ksiazka_gatunek_fk` FOREIGN KEY (`gatunek`) REFERENCES `gatunki` (`gatunek`);

--
-- Ograniczenia dla tabeli `pracownicy`
--
ALTER TABLE `pracownicy`
  ADD CONSTRAINT `pracownik_szef_fk` FOREIGN KEY (`pracownik_id`) REFERENCES `pracownicy` (`szef_id`);

--
-- Ograniczenia dla tabeli `regaly`
--
ALTER TABLE `regaly`
  ADD CONSTRAINT `regal_dzial_fk` FOREIGN KEY (`dział_nazwa`) REFERENCES `dzialy` (`nazwa`);

--
-- Ograniczenia dla tabeli `wlasciciel_biblioteka`
--
ALTER TABLE `wlasciciel_biblioteka`
  ADD CONSTRAINT `wlasciciel_biblioteka_b_fk` FOREIGN KEY (`biblioteka_nazwa`) REFERENCES `biblioteki` (`nazwa`),
  ADD CONSTRAINT `wlasciciel_biblioteka_w_fk` FOREIGN KEY (`wlasciciel_nip`) REFERENCES `wlasciciele` (`nip`);

CREATE INDEX au_id ON autorzy(autor_id);
CREATE INDEX cz_id ON czytelnicy(czytelnik_id);
CREATE INDEX dz_na ON dzialy(nazwa);
CREATE INDEX eg_id ON egzemplarze(egzemplarz_id);
CREATE INDEX op_id ON historia_operacji(operacja_id);
CREATE INDEX ks_id ON ksiazki(ksiazka_id);
CREATE INDEX pr_id ON pracownicy(pracownik_id);
CREATE INDEX re_nu ON regaly(numer);
CREATE INDEX wl_ni ON wlasciciele(nip);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

--
-- Procedury i funkcje
--

DROP PROCEDURE IF EXISTS `borrowBook`;
DROP FUNCTION IF EXISTS `findBestBookBorrowCount`;
DROP FUNCTION IF EXISTS `findBestBookID`;

delimiter //

--
-- Procedura wypożyczKsiazke
--

CREATE PROCEDURE borrowBook(IN libraryName varchar(50), IN workerName text, IN workerSurname text,
                            IN readerName text, IN readerSurname text, IN bookTitle varchar(100),
                            IN bookDate date, IN bookGenre varchar(20), IN comments text)
BEGIN
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
    SELECT ksiazka_id FROM ksiazki WHERE tytul = bookTitle AND data_opublikowania = bookDate AND gatunek = bookGenre
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

    /*
    Delete specimen
    */
    DELETE FROM egzemplarze WHERE egzemplarz_id = specimen_id;

    SET FOREIGN_KEY_CHECKS = 1;
END; //

--
-- Funkcja znajdz najczesciej wypożyczana ksiazke
--

CREATE FUNCTION findBestBookBorrowCount (bookDateYear INT)
    RETURNS INT
    DETERMINISTIC
BEGIN
    RETURN(
        SELECT count(*) as borCount
        FROM (
            SELECT(
                SELECT ksiazka_id
                FROM egzemplarze AS e
                WHERE e.egzemplarz_id = h.egzemplarz_id
            ) as ksiazka
            FROM historia_operacji AS h
            WHERE h.rodzaj_operacji = 'wypozyczenie' AND (SELECT YEAR(h.data)) = bookDateYear
        ) as tab1
        GROUP BY ksiazka
        HAVING borCount = (
            SELECT MAX(borCount)
            FROM(
                SELECT ksiazka, count(*) as borCount
                FROM (
                    SELECT(
                        SELECT ksiazka_id
                        FROM egzemplarze AS e
                        WHERE e.egzemplarz_id = h.egzemplarz_id
                    ) as ksiazka
                    FROM historia_operacji AS h
                    WHERE h.rodzaj_operacji = 'wypozyczenie' AND (SELECT YEAR(h.data)) = bookDateYear
                ) as tab1
                GROUP BY ksiazka
            ) as tab2
        ) LIMIT 1
    );
END; //

CREATE FUNCTION findBestBookID (bookDateYear INT)
    RETURNS INT
    DETERMINISTIC
BEGIN
    RETURN(
        SELECT ksiazka
        FROM (
            SELECT(
                SELECT ksiazka_id
                FROM egzemplarze AS e
                WHERE e.egzemplarz_id = h.egzemplarz_id
            ) as ksiazka
            FROM historia_operacji AS h
            WHERE h.rodzaj_operacji = 'wypozyczenie' AND (SELECT YEAR(h.data)) = bookDateYear
        ) as tab1
        GROUP BY ksiazka
        HAVING count(*) = (
            SELECT MAX(borCount)
            FROM(
                SELECT ksiazka, count(*) as borCount
                FROM (
                    SELECT(
                        SELECT ksiazka_id
                        FROM egzemplarze AS e
                        WHERE e.egzemplarz_id = h.egzemplarz_id
                    ) as ksiazka
                    FROM historia_operacji AS h
                    WHERE h.rodzaj_operacji = 'wypozyczenie' AND (SELECT YEAR(h.data)) = bookDateYear
                ) as tab1
                GROUP BY ksiazka
            ) as tab2
        ) LIMIT 1
    );
END; //
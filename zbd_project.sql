-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 25 Sty 2020, 13:09
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
(1, 'Maciej', 'Zima', '1990-09-03', '1992-10-11'),
(2, 'Maciej', 'Nowaczyk', '1991-08-01', '1991-08-01'),
(3, 'Marta', 'Kowalczyk', '1991-08-01', '1990-09-03'),
(4, 'Maciej', 'Karol', '1991-01-22', '1997-11-28'),
(5, 'Joanna', 'Kowalczyk', '1991-01-22', NULL),
(6, 'Magda', 'Karol', '1988-07-17', NULL),
(7, 'Joanna', 'Karol', '1997-11-28', '1988-07-17'),
(8, 'Joanna', 'Wozniak', '1997-11-28', '1980-04-14'),
(9, 'Jakub', 'Nowak', '1980-04-14', NULL),
(10, 'Piotr', 'Leszczyk', '1988-07-17', '1987-03-30');

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
(1, 6),
(2, 3),
(3, 5),
(3, 7),
(3, 8),
(3, 9),
(3, 10),
(6, 1),
(7, 4),
(10, 2);

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
('Biblioteka_dziecieca', 'Zawila_3'),
('Biblioteka_miejska', 'Brudna_31'),
('Biblioteka_na_Kwiatowej', 'Dluga_4'),
('Biblioteka_na_rynku', 'Brudna_31'),
('Biblioteka_szkolna', 'Brudna_31'),
('Czytam_ksiazki', 'Krutka_1'),
('Czytanie_jest_fajne', 'Zawila_3'),
('Ksiazki_sa_super', 'Brudna_31'),
('Super_Biblioteka', 'Poznanska_12'),
('Warto_czytac', 'Dluga_4');

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
(1, 'Natalia', 'Krol'),
(2, 'Jakub', 'Leszczyk'),
(3, 'Jan', 'Mazur'),
(4, 'Joanna', 'Krol'),
(5, 'Jan', 'Kowalczyk'),
(6, 'Jan', 'Mazur'),
(7, 'Magda', 'Krawczyk'),
(8, 'Jan', 'Karol'),
(9, 'Maciej', 'Nowaczyk'),
(10, 'Jakub', 'Zima');

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
(1, 3, 2),
(2, 1, 3),
(3, 2, 9),
(4, 2, 6),
(5, 10, 3),
(6, 3, 8),
(7, 8, 3),
(8, 10, 3),
(9, 4, 1),
(10, 9, 1);

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
(1, '1997-11-28', 'Super_Biblioteka', 5, 9, 7, 'przedluzenie', NULL, NULL),
(2, '1990-09-03', 'Biblioteka_dziecieca', 6, 7, 1, 'zwrot', NULL, NULL),
(3, '1990-09-03', 'Ksiazki_sa_super', 5, 1, 6, 'przedluzenie', 14, NULL),
(4, '1988-07-17', 'Biblioteka_na_rynku', 4, 1, 8, 'przedluzenie', NULL, NULL),
(5, '1993-12-25', 'Biblioteka_na_rynku', 7, 4, 4, 'przedluzenie', NULL, NULL),
(6, '1990-09-03', 'Biblioteka_na_rynku', 5, 7, 10, 'przedluzenie', NULL, NULL),
(7, '1980-04-14', 'Super_Biblioteka', 3, 6, 1, 'wyporzyczenie', 8, 'pierwszy raz od dawna'),
(8, '1993-12-25', 'Biblioteka_na_Kwiatowej', 1, 6, 9, 'przedluzenie', NULL, 'pierwszy raz od dawna'),
(9, '1980-04-14', 'Warto_czytac', 6, 8, 9, 'wyporzyczenie', NULL, 'bez uwag'),
(10, '1997-05-05', 'Czytanie_jest_fajne', 7, 7, 9, 'przedluzenie', NULL, NULL);

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
(1, 'Szeptucha', '1997-05-05', 'literatura_obyczajow'),
(2, 'Polska_odwraca_oczy', '1980-04-14', 'romans'),
(3, 'On', '1997-11-28', 'horror'),
(4, 'Zycie_na_pelnej_petardzie', '1991-01-22', 'kryminal'),
(5, 'Okularnik', '1980-04-14', 'literatura_obyczajow'),
(6, 'Najgorszy_czlowiek_na_swiecie', '1980-04-14', 'literatura_mlodziezo'),
(7, 'Inna_dusza', '1997-11-28', 'literatura_obyczajow'),
(8, 'Ksiegi_Jakubowe', '1997-05-05', 'sensacja'),
(9, 'Gniew', '1991-08-01', 'literatura_mlodziezo'),
(10, 'Trociny', '1990-09-03', 'sensacja');

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
(1, NULL, 'Maciej', 'Wozniak', 'obsluga_bazy'),
(2, 0, 'Piotr', 'Karol', 'kucharz'),
(3, 0, 'Natalia', 'Zima', 'kucharz'),
(4, NULL, 'Magda', 'Wozniak', 'obsluga_bazy'),
(5, NULL, 'Natalia', 'Zima', 'obsluga_bazy'),
(6, NULL, 'Jakub', 'Leszczyk', 'sprzatanie'),
(7, 3, 'Karol', 'Wozniak', 'kucharz'),
(8, 0, 'Joanna', 'Kowalczyk', 'kucharz'),
(9, 7, 'Jakub', 'Kowalczyk', 'obsluga_bazy'),
(10, 4, 'Maciej', 'Karol', 'szef');

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
(0, 5, 0, 'dzial6'),
(1, 9, 2, 'dzial6'),
(2, 7, 1, 'dzial9'),
(3, 7, 4, 'dzial6'),
(4, 6, 0, 'dzial2'),
(5, 7, 0, 'dzial4'),
(6, 5, 1, 'dzial1'),
(7, 8, 0, 'dzial0'),
(8, 7, 1, 'dzial4'),
(9, 8, 1, 'dzial6');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wlasciciele`
--

CREATE TABLE `wlasciciele` (
  `nip` int(11) NOT NULL,
  `nazwa_firmy` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `imie` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL,
  `nazwisko` text CHARACTER SET utf8 COLLATE utf8_polish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_polish_ci;

--
-- Zrzut danych tabeli `wlasciciele`
--

INSERT INTO `wlasciciele` (`nip`, `nazwa_firmy`, `imie`, `nazwisko`) VALUES
(1938106794, NULL, 'Jan', 'Kowalczyk'),
(1938106795, NULL, 'Karol', 'Krawczyk'),
(1938106796, NULL, 'Olga', 'Karol'),
(1938106797, 'Junkers', NULL, NULL),
(1938106798, 'Red_Bull', NULL, NULL),
(1938106799, 'CCC', NULL, NULL),
(1938106800, 'Bakoma', NULL, NULL),
(1938106801, NULL, 'Jakub', 'Krawczyk'),
(1938106802, NULL, 'Natalia', 'Nowak'),
(1938106803, 'Junkers', NULL, NULL);

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
(1938106795, 'Biblioteka_szkolna'),
(1938106796, 'Biblioteka_dziecieca'),
(1938106796, 'Czytam_ksiazki'),
(1938106798, 'Czytanie_jest_fajne'),
(1938106801, 'Biblioteka_na_rynku'),
(1938106802, 'Biblioteka_miejska'),
(1938106802, 'Biblioteka_na_Kwiatowej'),
(1938106802, 'Super_Biblioteka'),
(1938106802, 'Warto_czytac'),
(1938106803, 'Ksiazki_sa_super');

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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

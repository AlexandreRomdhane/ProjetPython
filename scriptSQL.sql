-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  lun. 02 nov. 2020 à 21:28
-- Version du serveur :  5.7.26
-- Version de PHP :  7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `memecontainer`
--

-- --------------------------------------------------------

--
-- Structure de la table `followers`
--

DROP TABLE IF EXISTS `followers`;
CREATE TABLE IF NOT EXISTS `followers` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf16 COLLATE=utf16_bin;

-- --------------------------------------------------------

--
-- Structure de la table `post`
--

DROP TABLE IF EXISTS `post`;
CREATE TABLE IF NOT EXISTS `post` (
  `PostID` int(11) NOT NULL AUTO_INCREMENT,
  `UtilisateurID` int(11) NOT NULL,
  `NomPost` varchar(128) COLLATE utf8_bin NOT NULL,
  `ContenuPost` varchar(255) COLLATE utf8_bin NOT NULL,
  `DatePost` date NOT NULL,
  PRIMARY KEY (`PostID`),
  KEY `DatePost` (`DatePost`),
  KEY `FK_UtilisateurID` (`UtilisateurID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Déchargement des données de la table `post`
--

INSERT INTO `post` (`PostID`, `UtilisateurID`, `NomPost`, `ContenuPost`, `DatePost`) VALUES
(3, 10, 'Test', 'Test', '2020-11-02'),
(4, 10, 'Test1', 'Test1', '2020-11-02');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE IF NOT EXISTS `utilisateur` (
  `UtilisateurID` int(11) NOT NULL AUTO_INCREMENT,
  `Mail` varchar(100) COLLATE utf8_bin NOT NULL,
  `Motdepasse` varchar(128) COLLATE utf8_bin NOT NULL,
  `NomUtilisateur` varchar(50) COLLATE utf8_bin NOT NULL,
  `DateCreation` date NOT NULL DEFAULT '2020-11-01',
  PRIMARY KEY (`UtilisateurID`),
  KEY `idx_Utilisateur_Mail` (`Mail`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`UtilisateurID`, `Mail`, `Motdepasse`, `NomUtilisateur`, `DateCreation`) VALUES
(10, 'alexandre.romdhane@ipilyon.net', '$2b$12$cuHKFMa6jmWK7jDVz6mh5eqHRU4Te0bPTGH/RzqIdvawNLwsbstI6', 'Alexandre', '2020-11-02');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

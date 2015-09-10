-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 02, 2015 at 03:43 PM
-- Server version: 5.6.19-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `iitbxblended`
--

-- --------------------------------------------------------

--
-- Table structure for table `SIP_lookup`
--

CREATE TABLE IF NOT EXISTS `SIP_lookup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(75) NOT NULL,
  `code` int(11) NOT NULL,
  `description` varchar(100) NOT NULL,
  `comment` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=44 ;

--
-- Dumping data for table `SIP_lookup`
--

INSERT INTO `SIP_lookup` (`id`, `category`, `code`, `description`, `comment`, `is_active`) VALUES
(1, 'Designation', 1, 'Assistant Lecturer', '', 1),
(2, 'Designation', 12, 'Lecturer', '', 1),
(3, 'Designation', 14, 'Principal', '', 1),
(4, 'Designation', 15, 'Professor', '', 1),
(5, 'Designation', 16, 'Reader', '', 1),
(6, 'Designation', 17, 'Research Scholar', '', 1),
(7, 'Designation', 18, 'Scientist', '', 1),
(8, 'Designation', 2, 'Assistant Professor', '', 1),
(9, 'Designation', 20, 'Senior Lecturer', 'Activated for IITBX BMW workshop', 1),
(10, 'Designation', 28, 'Vice Chancellor', '', 1),
(11, 'Designation', 29, 'Vice Principal', '', 1),
(12, 'Designation', 3, 'Associate Professor', '', 1),
(13, 'Designation', 32, 'Teaching Fellow', 'To be added for Envirmental Studies ', 1),
(14, 'Designation', 33, 'Associate Dean', 'Added for IIBX BMW Workshop', 1),
(15, 'Designation', 4, 'Dean', '', 1),
(16, 'Designation', 5, 'Director', '', 1),
(17, 'Designation', 7, 'Guest Lecturer', '', 1),
(18, 'Designation', 8, 'Head of Department', '', 1),
(19, 'ParticipantTitle', 1, 'Dr.', '', 1),
(20, 'ParticipantTitle', 2, 'Mr.', '', 1),
(21, 'ParticipantTitle', 3, 'Mrs.', '', 1),
(22, 'ParticipantTitle', 4, 'Ms.', '', 1),
(23, 'ParticipantTitle', 5, 'Prof.', '', 1),
(24, 'Qualification', 1, 'B.E', '', 1),
(25, 'Qualification', 10, 'B.Arch', '', 1),
(26, 'Qualification', 11, 'M.Arch', '', 1),
(27, 'Qualification', 12, 'M.B.A', '', 1),
(28, 'Qualification', 13, 'M. A', 'Added only for Environmental studies workshop', 1),
(29, 'Qualification', 14, 'M.Pharm', 'Added only for Enivronmental studies workshop', 1),
(30, 'Qualification', 2, 'B.Tech', '', 1),
(31, 'Qualification', 3, 'M.E', '', 1),
(32, 'Qualification', 4, 'M.Tech', '', 1),
(33, 'Qualification', 5, 'B.Sc', '', 1),
(34, 'Qualification', 6, 'M.Sc', '', 1),
(35, 'Qualification', 7, 'MCA', '', 1),
(36, 'Qualification', 8, 'Ph.D', '', 1),
(37, 'Qualification', 9, 'Post Doc.', '', 1),
(38, 'Role', 1, 'Admin', 'System Administrator', 1),
(39, 'Role', 2, 'HOI', 'Head', 1),
(40, 'Role', 3, 'PC', 'Program Coordinator', 1),
(41, 'Role', 4, 'CC', 'Course Coordinator', 1),
(42, 'Role', 5, 'TA', 'Teacher', 1),
(43, 'Designation', 99, 'Registrar', '', 1);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

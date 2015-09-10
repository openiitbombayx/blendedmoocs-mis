-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 02, 2015 at 03:28 PM
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
-- Table structure for table `SIP_emailcontent`
--

CREATE TABLE IF NOT EXISTS `SIP_emailcontent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `systype` varchar(30) NOT NULL,
  `name` varchar(100) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=32 ;

--
-- Dumping data for table `SIP_emailcontent`
--

INSERT INTO `SIP_emailcontent` (`id`, `systype`, `name`, `subject`, `message`) VALUES
(1, 'Registration', 'request_verification_success', 'IITBombayX Partner System Email Verification', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to Information System for IITBombayX Blended MOOCS\n\nDear %s, \r\n\r\nYou have registered on IITBombayX Partner System. Please verify your email id by clicking the on  link below:\r\n%s  \r\n\r\nAfter verification,your request will be sent to your institute''s Program coordinator. \r\n\r\nThanks & Regards,\r\nIITBombayX Blended Moocs Coordinator'),
(2, 'Registration', 'approval', 'Request for Approval', 'THIS IS A SAMPLE MESSAGE.\r\nDear Member, \r\n\r\nFollowing request has been received on IITBombayX Blended MOOCs system. \r\n\r\nName: %s  \r\nRole: %s \r\nCourse: %s  \r\nInstitute: %s  \r\n\r\nPlease visit your IITBombayX Blended MOOCs System profile to accept or reject the request.  \r\n\r\nRegards,\r\nIITBombayX Blended Moocs Coordinator'),
(3, 'Registration', 'request_filed', 'Request Submitted', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nYour request for registration on the IITBombayX Blended MOOCs system has sent for approval.\r\n\r\nRole: %s  \r\nCourse:%s \r\nInstitute: %s   \r\n\r\nRegards,\r\nIITBombayX Blended Moocs Coordinator'),
(4, 'Registration', 'register', 'Invite to Register', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nYour request has been accepted on the IITBombayX Blended MOOCs System.\r\nRole: %s\r\nCourse: %s\r\nInstitute: %s\r\n\r\nPlease click this link to complete the registration process. \r\nhttp://10.105.22.21:9005/register/5/1\r\n\r\nAfter registration, your IITBombayX Partner System account will be created. \r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Coordinator'),
(5, 'Registration', 'rejected', '', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s,\r\n\r\nWe regret to inform that your request has not been accepted on IITBombayX Blended MOOCs System. \r\n                                                                            Role: %s                                                                         \r\nCourse: %s                                                                      Institute: %s \r\n\r\nThanks for your interest.                                                                                                                                                      Regards,\r\nIITBombayX Blended MOOCs Coordinator\r\n'),
(6, 'Registrations', 'register', 'Invite to Register', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nYour request has been accepted on the IITBombayX Blended MOOCs System.\r\nRole: %s\r\nCourse: %s\r\nInstitute: %s\r\nPlease click this link to complete the registration process. \r\n\r\nhttp://10.105.22.21:9005/register/5/1\r\n\r\nAfter registration, your IITBombayX Partner System account will be created. \r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Coordinator'),
(7, 'Registration', 'home', 'Successful Registration', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to IITBombayX Blended MOOCs System!                                                                        \r\n\r\nDear %s,                                                                                                                                                            You are now successfully registered in the IITBombayX Blended MOOCs System.                                                                                                                                                      Role:%s                                                                         Course:%s                                                                       Institute:%s                                                                                                                                                    To upload your students'' data and view their IITBombayX Course grades / marks, you need to log in to your account.For your account security, we advise you not to disclose your password to anybody.\r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Coordinator'),
(8, 'Registration', '', 'Successful Registration', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to IITBombayX Blended MOOCs System!                                                                        \r\n\r\nDear %s,                                                                                                                                                            You are now successfully registered in the IITBombayX Blended MOOCs System.                                                                                                                                                      Role:%s                                                                         Course:%s                                                                       Institute:%s                                                                                                                                                    To upload your students'' data and view their IITBombayX Course grades / marks, you need to log in to your account.For your account security, we advise you not to disclose your password to anybody.\r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Coordinator'),
(9, 'TM_MGMT_PC', 'register', 'Invite to register', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to IITBombayX Blended MOOCs System!                                                                         \r\n\r\nDear %s,                                                                                                                                                             You have been invited to register at IITBombayX Blended MOOCs System.\r\nRole:%s                                                                       Course:%s                                                                       Institute: %s \r\n\r\nPlease click on the following link to register \r\n6-3x8-ffa49749814fe3da8b0d/\r\n\r\nRegards,\r\nIITBombayX Blended MOOCs Coordinator'),
(10, 'Login', 'resetpassword', 'Reset Password', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to Information System for Blended MOOCs\r\n\r\nDear %s, \r\n\r\nPlease click on the following link to reset the password.\r\n%s\r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Support\r\n\r\n\r\n'),
(11, 'Login', 'success', 'Reset Password Successfully', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s,\r\n\r\nYour password has been reset successfully. \r\n\r\nRegards, \r\nIITBombayX Blended MOOCs Support'),
(12, 'TM_MGMT_PC', 'consent,dissent', 'Program Coordinator''s Consent ', 'THIS IS A SAMPLE MESSAGE.\r\nHello %s,\r\nYou are invited as: \r\nRole: %s                                                                         Course: %s                                                                       Institute: %s \r\n\r\nPlease click on the link below if you wish to accept:\r\nclick here: %s\r\n\r\nPlease click on the link below if you wish to decline:\r\nclick here: %s\r\n\r\nThanks and Regards,\r\nBlended MOOCs Coordinator'),
(13, 'TM_MGMT_C', 'register', 'Invitation from IITBombayX Blended MOOCs System', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to IITBombayX Blended MOOCs System!\r\nDear%s,                                                                         You have been invited to register for the following role at IITBombayX Blended MOOCs System.\r\n\r\nRole: %s                                                                         Course: %s                                                                       Institute: %s \r\n\r\nPlease click on the following link to register: \r\n6-3x8-ffa49749814fe3da8b0d/\r\n\r\nRegards,\r\nIITBombayX Blended MOOCs Support'),
(14, 'TM_MGMT_C', 'consent,dissent', 'Consent to be Program Coordinator', 'THIS IS A SAMPLE MESSAGE.\r\nHello %s,\r\n\r\nYou are invited as: \r\nRole:%s                                                                         Course:%s                                                                       Institute: %s \r\n\r\nPlease click on the link below if you wish to accept:\r\nclick here: %s\r\n\r\nPlease click on the link below if you wish to decline:\r\nclick here: %s\r\n\r\n\r\nThanks and Regards,\r\nBlended MOOCs Coordinator'),
(15, 'TM_MGMT_C', 'approved', 'Request approved', 'THIS IS A SAMPLE MESSAGE.\r\nHello %s,\r\n\r\nYour request has been accepted.\r\nRole: %s                                                                           Course: %s                                                                         Institute: %s \r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Coordinator'),
(16, 'TM_MGMT_C', 'rejected', 'Request not approved', 'THIS IS A SAMPLE MESSAGE.\r\nHello %s,\r\n\r\nYour request has not been accepted.\r\nRole:%s                                                                         Course:%s                                                                         Institute: %s \r\nThanks for your interest.\r\n                                                                               Regards,\r\nIITBombayX Blended MOOCs Coordinator'),
(17, 'TM_MGMT_C', 'cancelled', 'Request cancelled', 'THIS IS A SAMPLE MESSAGE.\r\nHello %s,\r\n\r\nThe following invitation has been cancelled:\r\nRole:%s                                                                         Course:%s                                                                         Institute: %s \r\nThanks for your interest.                                                                                \r\nRegards,\r\nIITBombayX Blended MOOCs Coordinator'),
(18, 'TM_MGMT_C', 'removed', 'Service discontinued', 'THIS IS A SAMPLE MESSAGE.\r\nHello %s,\r\n\r\nYour services are no longer required:\r\nRole: %s                                                                         Course: %s                                                                         Institute: %s \r\n\r\nThanks for your interest.                                                                                \r\nRegards,\r\nIITBombayX Blended MOOCs Coordinator'),
(19, 'TM_MGMT_C', 'dissented', 'Invite not accepted', 'THIS IS A SAMPLE MESSAGE.\r\nHello %s,\r\n\r\nThe following invitation has been turned down.\r\nName: %s\r\nRole: %s                                                                         Course: %s                                                                         Institute: %s \r\n\r\nRegards,\r\nIITBombayX Blended MOOCs Coordinator'),
(20, 'Course', 'update', 'Course Name updated', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s,\r\n\r\nThe previous course %s taught in your institute has been renamed to %s.\r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Team'),
(21, 'Course', 'enroll', 'Course Enrollment on IITBombayX Blended MOOCs System', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to IITBombayX Blended MOOCs System!                                                                           \r\n\r\nDear %s,\r\n\r\nYour institute has been enrolled successfully for the course %s.\r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs Coordinator'),
(22, 'Course', 'unenroll', 'Course Unenrollment on IITBombayX Blended MOOCs System', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s,\r\n\r\nYour institute has been unenrolled successfully from the course %s.\r\n\r\nThanks and Regards,\r\nIITBombayX Blended MOOCs '),
(23, 'Login', 'changepass', 'Password Changed Successfully', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nYour password has been changed successfully. \r\n\r\nRegards, \r\nIITBombayX Blended MOOCs Coordinator'),
(24, 'Student Module', 'Unenrollment of student', 'Unenrollment from IITBombayX Blended MOOC', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\nYour teacher %s has unenrolled you from the course %s. \r\nThanks for the interest.\r\n \r\nRegards,\r\nIITBombayX Blended MOOCs Coordinator'),
(25, 'Student Module', 'Enrollment of student', 'Enrollment in IITBombayX Blended MOOC', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nYour teacher %s has enrolled you successfully to the Course %s. \r\n\r\nRegards, \r\nIITBombayX Blended MOOCs Coordinator '),
(26, 'Student Module', 'Change of roll number', 'Roll number change', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nThis is to update that your teacher %s has changed your roll number to %s, for the Course %s. \r\n\r\nRegards, \r\nIITBombayX Blended MOOCs Coordinator '),
(27, 'Student Module', 'Course unenrollment', 'Unenrollment from IITBombayX Blended MOOC', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nThis is to update that you have unenrolled Mr./Mrs./Ms. %s from the Course %s. \r\n\r\nRegards,\r\nIITBombayX Blended MOOCs Coordinator'),
(28, 'Student Module', 'Enrollment of student by teacher', 'Enrollment in  IITBombayX Blended MOOC', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\nYou have enrolled Mr./Mrs./Ms. %s successfully to the Course %s. \r\n\r\nRegards, \r\nIITBombayX Blended MOOCs Coordinator'),
(29, 'Student Module', 'Roll number change by teacher', 'Roll number change', 'THIS IS A SAMPLE MESSAGE.\r\nDear %s, \r\n\r\nYou have changed the roll number of Mr./Mrs/Ms. to %s for the Course %s. \r\n\r\nRegards, \r\nIITBombayX Blended MOOCs Coordinator  '),
(30, 'Login', 'createpassword', 'Create  Password', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to Information System for IITBombayX Blended MOOCs Dear %s, Please click on the following link to create a password %s Regards, Blended MOOCs Support '),
(31, 'Login', 'create_success', 'Password  Created Successfully', 'THIS IS A SAMPLE MESSAGE.\r\nWelcome to Information System for IITBombayX Blended MOOCs.\r\n\r\nDear %s,\r\n\r\nYour password has been created successfully. To know more, you can now log in through the following link:\r\n\r\nhttp://bmwinfo.iitbombayx.in/\r\n\r\nRegards,\r\nBlended Moocs Support');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

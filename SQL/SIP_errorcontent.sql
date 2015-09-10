-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 02, 2015 at 03:40 PM
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
-- Table structure for table `SIP_errorcontent`
--

CREATE TABLE IF NOT EXISTS `SIP_errorcontent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `systype` varchar(30) NOT NULL,
  `name` varchar(100) NOT NULL,
  `errorcode` varchar(20) NOT NULL,
  `error_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `errorcode` (`errorcode`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=120 ;

--
-- Dumping data for table `SIP_errorcontent`
--

INSERT INTO `SIP_errorcontent` (`id`, `systype`, `name`, `errorcode`, `error_message`) VALUES
(1, 'SM', 'CSV UPLOAD', 'inv_rec', 'Invalid Record'),
(2, 'SM', 'CSV UPLOAD', 'noerror', 'SUCCESS'),
(3, 'SM', 'CSV UPLOAD', 'duplicate', 'Student Already Exists'),
(4, 'SM', 'CSV UPLOAD', 'invalidrol', 'Invalid Roll no'),
(5, 's', 'CSV UPLOAD', 'blankline', 'Empty Record'),
(6, 'SM', 'CSV UPLOAD', 'inv_email', 'Email Address  not found'),
(7, 'SM', 'CSV UPLOAD', 'invaliduse', 'Username not found'),
(8, 'SM', 'CSV UPLOAD', 'not_enroll', 'Student not enrolled'),
(9, 'Login', 'Login', 'LN_INV', 'Invalid Login or Password.'),
(10, 'CM', 'corresponding course name', 'CM_ECCN', 'Please fill the corresponding course name.'),
(11, 'CM', 'invalid corresponding course name', 'CM_SCCN', 'Corresponding course name cannot start with a space.'),
(12, 'CM', 'invalid corresponding course name', 'CM_ACCN', 'Corresponding course name must contain at least one alphabet. '),
(13, 'CM', 'empty start date', 'CM_STD', 'Please enter the start date.'),
(14, 'CM', 'empty end date', 'CM_ED', 'Please enter the end date.'),
(15, 'CM', 'invalid end date', 'CM_IED', 'End date must be after start date.'),
(16, 'CM', 'total number of students attending course on IITBombayX', 'CM_ETS', 'Please enter the total number of students to attend the course on IITBombayX from your institute.'),
(17, 'CM', 'total number of students attending that course in institute', 'CM_ETSP', 'Please enter the total number of students attending the corresponding course at your institute.'),
(18, 'CM', 'invalid number of students', 'CM_INS', 'Total number of students attending the course at IITBombayX cannot be greater than that at your institute.'),
(19, 'CM', 'invalid reason of cancellation', 'CM_IRC', 'Please provide a reason of unenrolling the course.'),
(41, 'Login', 'Forgot_Pass', 'NO_ERR', 'We have emailed you instructions to set a new password. '),
(42, 'Login', 'Forgot_Pass', 'EML_INV', 'The email is not registered.'),
(43, 'Login', 'Reset_Pass', 'NO_MTCH', 'Password did not match. Please enter again!!!'),
(44, 'Login', 'Reset_Pass', 'PWD_SET', 'Password changed successfully.'),
(45, 'Login', 'Change_Pass', 'OLD_NO_MTCH', 'Your old password did not match. Please enter again.'),
(46, 'Login', 'Change_Pass', 'PWD_NO_MTCH', 'Password didn''t match. Please enter again.'),
(47, 'Login', 'Pwd_empty', 'PASS_EMPTY', 'Please enter password.'),
(48, 'Login', 'Pwd_invalid', 'INV_PASS', 'Please enter a valid password.'),
(49, 'Login', 'Change_Pass', 'MTCH_ERR', 'Your old and new password can''t be same. Please enter again.'),
(50, 'Login', 'Email_invalid', 'INV_EML', 'Please enter a valid email.'),
(51, 'Login', 'Email_empty', 'EML_EMPTY', 'Please enter email.'),
(52, 'BMC', 'empty role', 'BMC_ER', 'Please select the role.'),
(53, 'ADM', 'empty report name', 'ADM_ER', 'Please select a report.'),
(54, 'BMC', 'empty institute', 'BMC_EI', 'Please select the institute.'),
(55, 'CM', 'alphabet less reason', 'CM_AR', 'Reason cannot be a number. '),
(56, 'CM', 'reason beginning with space', 'CM_SR', 'Reason cannot begin with a space.'),
(57, 'CM', 'empty year', 'CM_EY', 'Please select the academic year of students to which this course is to be taught.'),
(58, 'CM', 'empty program', 'CM_EP', 'Please select the program to which this course is to be taught.'),
(59, 'PC_IFN', 'First Name', 'firstname', 'Enter Valid First Name'),
(60, 'PC_ILN', 'Last Name', 'lastname', 'Enter Valid Last Name'),
(61, 'PC_IEMAIL', 'Email', 'email', 'Enter Valid Email Address'),
(62, 'PC_REMAIL', 'Registered Email', 'regemail', 'Email already registered in somebody''s name. Please enter another'),
(63, 'SM_IBODY', 'Subject', 'submis', 'Enter the subject'),
(64, 'SM_ISUB', 'Body', 'bodymis', 'Enter the Message in the Body'),
(65, 'INV_EMAIL', 'Invalid Email', 'invemail', 'Invalid Email'),
(66, 'INV_STDATE', 'Start Date', 'invsdate', 'Invalid Start Date. Please Choose a valid Start Date'),
(67, 'INV_EDATE', 'End Date', 'invedate', 'Invalid End Date. Please Choose a valid End Date'),
(68, 'INV_DUR', 'Duration', 'invdur', 'The duration of period selected is invalid. Please select a valid duration'),
(69, 'CC_ACTIVE', 'ActiveCC', 'activeCC', 'The Course Coordinator for the Selected Subject is Still Active. If you wish to appoint another kindly deactivate him / her from your dashboard'),
(70, 'CC_REQUEST', 'RequestCC', 'requestCC', 'A Course Coordinator for the selected course has already been invited. Kindly cancel his invitation to continue'),
(71, 'SM', 'CSV UPLOAD', 'not_registered', 'User is not registered with iitBombayX'),
(72, 'SM', 'CSV upload', 'invalidemail', 'Email is not valid'),
(73, 'SM', 'CSV upload', 'invaliduser', 'User name is not valid'),
(74, 'SM', 'CSV upload', 'inactive_user', 'User is not active'),
(75, 'SM', 'CSV UPLOAD', 'fields_empty', 'All Fields are Required.'),
(76, 'SM', 'CSV UPLOAD', 'dup_entry', 'Student was already assigned to you.No change'),
(77, 'SM', 'CSV upload', 'invalidfilename', 'Invalid File Name'),
(78, 'SM', 'CSV upload', 'invalidheading', 'Invalid Header Record'),
(79, 'SM', 'unenrollment', 'cancelled_enrollment', 'User has cancelled enrollment from the course'),
(80, 'Login', 'get_multi_roles', 'person_not_exit', 'unique person for logged in  user does not exit'),
(81, 'Login', 'selectrole', 'roleid_not_exit', 'Category for code Roleid in roleselect doesn not exist.'),
(83, 'Login', 'set_single_role', 'category_not_exit', 'Category for code Roleid doesnot  exist in set_single_role.'),
(85, 'Login', 'singlerole', 'unique_person', 'Cannot fetch unique person or institute for this logged-in session'),
(86, 'Login', 'Forgotpass', 'Email_cant_send', 'Email cannot send at this moment.'),
(87, 'Login', 'resetpass', 'no_unique_person', 'unique person for the user does not exist'),
(90, 'Login', 'resetpass', 'resetpass_email', 'Email Content for success in resetpass doesnot  exist.'),
(91, 'Login', 'createpass', 'no_person', 'person  does not exist'),
(92, 'course enrolled', 'course', 'no_course', 'cannot get unique entry for course'),
(93, 'SM', 'teacherlist', 'course_not_present', 'Cannot get  course for given courseid.'),
(94, 'SM', 'studentdetails', 'no_course_entry', 'cannot get entry for course'),
(95, 'SM', 'Student_details', 'not_valid_teacher', 'You are not valid Teacher for this course'),
(97, 'SM', 'update', 'no_unique_course', 'Cannot get unique course for given courseid or Courseleveluser in Update function.'),
(98, 'SM', 'update', 'no_pid', 'Cannot get iitbx_auth_user for given pid in Update function.'),
(99, 'SM', 'update', 'no_teacher', 'Cannot get unique entry for given course and techer in studentdetail table in Update Function'),
(100, 'SM', 'upload', 'upload_csvfile', '!!! Please Upload .csv File!!!'),
(101, 'SM', 'uploadcsv', 'upload_csv', 'Please upload  a csv file'),
(102, 'Login', 'teacherhome', 'session_not_active', 'Person Doesn''t exist or session is not active.'),
(105, 'course', 'teacherhome', 'no_edxcourse_present', 'Course is not present in edxcourses in teacher home function.'),
(106, 'SM', 'unenrollstudent', 'no_default_teacher', 'Default teacher information is missing for the course.'),
(107, 'SM', 'unenrollstudent', 'stu_not_register', 'Student  is not registered on IITBombayX.'),
(108, 'Login', 'change_pass', 'changepass_email', 'Email Content of success for changepass function does not exist.'),
(109, 'Login', 'change_pass', 'not_logged_in', 'you are not logged in.Please login to change your password'),
(110, 'Login', 'blendedadmin_home', 'no_person_info', 'Person Information not available. Please send email to software support'),
(112, 'SM', 'grades', 'no_IITBombayX_course', 'IITBombayX course is not present.'),
(113, 'SM', 'grades_report', 'teacher_not_valid', 'You are not valid Teacher for the course'),
(114, 'Faculty module', 'course_faculty', 'not_valid_user', 'You are not valid user for IITBombayX System.Contact Workshop team. '),
(115, 'course', 'course_faculty', 'not_valid_faculty', 'You are not valid Faculty of IITBombayX  for the Blended course'),
(116, 'SM', 'teacherstudent', 'not_selected', 'You have not selected either institute,course or teacher<br> .'),
(117, 'SM', 'teacherstudent', 'select_all', 'Please Select all details.<br>'),
(118, 'SM', 'evaluation', 'select_quiz', 'Please select quiz'),
(119, 'SM', 'allcourses', 'select_course', 'Please select course');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

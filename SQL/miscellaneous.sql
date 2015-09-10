INSERT INTO `iitbxblended`.`auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES (NULL, 'pbkdf2_sha256$20000$pKkw9KIa51hy$Nfp5EpUTpHzqYNgu9txPfbxnPJj1n+Rv5Ywo8d41PaM=', '2015-09-01 00:00:00', '0', 'admin@workshop.com', '', '', 'admin@workshop.com', '1', '1', '2015-09-02 00:00:00');

INSERT INTO `iitbxblended`.`SIP_personinformation` (`id`, `email`, `titleid`, `firstname`, `lastname`, `designation`, `gender`, `streamid`, `instituteid_id`, `experience`, `qualification`, `telephone1`, `telephone2`, `createdondate`, `isactive`) VALUES (NULL, 'admin@workshop.com', NULL, 'Workshop', 'Administrator', NULL, NULL, NULL, '1', NULL, NULL, '', NULL, '2015-09-01', '1');

INSERT INTO `iitbxblended`.`SIP_userlogin` (`id`, `user_id`, `usertypeid`, `status`, `last_login`, `nooflogins`) VALUES (NULL, '1', '1', '1', '0000-00-00 00:00:00', NULL);

INSERT INTO `iitbxblended`.`SIP_t10kt_institute` (`instituteid`, `institutename`, `state`, `city`, `pincode`, `address`) VALUES ('1', 'IITBombayX', 'MAHARASHTRA', 'Mumbai', '0', 'Default');

INSERT INTO `iitbxblended`.`SIP_t10kt_remotecenter` (`remotecenterid`, `remotecentername`, `state`, `city`, `instituteid_id`, `autonomous`) VALUES ('1', 'IITBombayX', 'MAHARASHTRA', 'Mumbai', '1', '0');

INSERT INTO `iitbxblended`.`SIP_t10kt_approvedinstitute` (`id`, `remotecenterid_id`, `instituteid_id`) VALUES (NULL, '1', '1');

INSERT INTO `iitbxblended`.`SIP_edxcourses` (`id`, `tag`, `org`, `course`, `name`, `courseid`, `coursename`, `enrollstart`, `enrollend`, `coursestart`, `courseend`, `image`, `instructor`, `coursesubtitle`) VALUES (NULL, 'i4x', 'IITBombayX', 'CS101.1xA15', '2015_T1', 'IITBombayX/CS101.1xA15/2015_T1', 'Introduction to Computer Programming', NULL, NULL, NULL, NULL, 'https://iitbombayx.in/c4x/IITBombayX/CS101.1xA15/asset/unnamed.jpg', '', '');

INSERT INTO `iitbxblended`.`SIP_courseenrollment` (`id`, `courseid_id`, `instituteid_id`, `corresponding_course_name`, `start_date`, `end_date`, `year`, `program`, `total_moocs_students`, `total_course_students`, `enrollment_date`, `enrolledby_id`, `comments`, `cancelled_date`, `cancelledby_id`, `reason_of_cancellation`, `status`) VALUES (NULL, 'IITBombayX/CS101.1xA15/2015_T1', '1', '', '2015-09-07', '', '', '', '', '', '2015-09-04', '1', NULL, NULL, NULL, NULL, '1');

INSERT INTO `iitbxblended`.`SIP_courselevelusers` (`id`, `personid_id`, `instituteid_id`, `courseid_id`, `roleid`, `startdate`, `enddate`) VALUES (NULL, '1', '1', '1', '5', '2015-09-07', '');

INSERT INTO `iitbxblended`.`SIP_institutelevelusers` (`id`, `personid_id`, `instituteid_id`, `roleid`, `startdate`, `enddate`) VALUES (NULL, '1', '1', '2', '2015-09-07', '');

INSERT INTO `iitbxblended`.`SIP_institutelevelusers` (`id`, `personid_id`, `instituteid_id`, `roleid`, `startdate`, `enddate`) VALUES (NULL, '1', '1', '3', '2015-09-07', '');


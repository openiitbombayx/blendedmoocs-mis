'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', 'SIP.views.sessionlogin',name='course'),
     url(r'^get_multi_roles/$', 'SIP.views.get_multi_roles',name='get_multi_roles'),
     url(r'^set_role/(?P<role>[0-9])/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<cid>[0-9]{1,40})$', 'SIP.views.set_single_role',name='set_single_role'),	
    url(r'^teacher/(?P<tid>[0-9]+|-[0-9])/$','SIP.views.teacherhome'),
    url(r'^studentsinformation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','SIP.views.studentdetails',name='studentdetails'),
	url(r'^updatestudentinformation/(?P<pid>[0-9]+|-[0-9]+)/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<t_id>[0-9]+)/$','SIP.views.Update'),
    
    url(r'^downloadcsv1/(?P<course>[\w{}\.\-\/]{1,40})/(?P<id>[0-9]+|-[0-9])/$','SIP.views.downloadcsv',name='downloadcsv'),
    url(r'^uploads_studentsinfo/(?P<code>[0-9])/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'SIP.views.upload'),
    
    url(r'^downloadcsv/(?P<code>[0-9])/$', 'SIP.views.output_csv'),
	url(r'^unenroll/(?P<pid>[0-9-]+)/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<t_id>[0-9]+)/$','SIP.views.unenrollstudent'),
	
   	url(r'^teacherslist/(?P<courseid>[\w{}\.\-\/]{1,40})/$','SIP.views.teacherlist'),
    url(r'^ccourses/',views.ccourse, name='ccourses'),
    url(r'^blendedadmin_home/','SIP.views.blendedadmin_home',name='blendedadmin_home'),
    url(r'^blendedadmin/(?P<report_id>[\w{}\.\-\/]{1,5})/$','SIP.views.blendedadmin',name='blendedadmin'),
    url(r'^instructoradmin/(?P<report_id>[\w{}\.\-\/]{1,5})/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<param_id>[\w{}\.\-\/]{1,40})/$', 'SIP.views.instructoradmin',name='instructoradmin'),
	url(r'^grades/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/$','SIP.views.grades_report',name='grades_report'),
    url(r'^downloadgradecsv/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','SIP.views.downloadgradecsv',name='downloadgradecsv'),
    url(r'^faculty_report/$','SIP.views.course_faculty',name='faculty_report'),
    url(r'^instructor_course_report/(?P<course>[\w{}\.\-\/]{1,40})/$','SIP.views.display_instructor_report', name='display_instructor_report' ),
    url(r'^approvedinstitute/$','SIP.views.approvedinstitute',name='approvedinstitute'),
    url(r'^institutecourses$','SIP.views.institutecourses',name='institutecourses'),
    url(r'^courseteachers$','SIP.views.courseteachers',name='courseteachers'),
    url(r'^teacherstudent/$','SIP.views.teacherstudent',name='teacherstudent'),
    url(r'^evaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/(?P<evalflag>[0-9])/$','SIP.views.evaluation',name='evaluation'),
    url(r'^quizdata/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/$','SIP.views.quizdata',name='quizdata'),
    url(r'^downloadquizcsv/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalid>[0-9]+|-[0-9])/$','SIP.views.downloadquizcsv',name='downloadquizcsv'),
    url(r'^coursedescription/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','SIP.views.coursedescription',name='coursedescription'),
    url(r'^allcourses/(?P<courseflag>[0-9])/$','SIP.views.allcourses',name='allcourses'),
    url(r'^evalstatus/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/(?P<evalflag>[0-9])/$','SIP.views.evalstatus',name='evalstatus'),
    url(r'^studentstatus/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/(?P<report>[0-9])/$','SIP.views.studentstatus',name='studentstatus'),
    url(r'^downloadstatucsv/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/(?P<report>[0-9])/$','SIP.views.downloadstatucsv',name='downloadstatuscsv'),
    url(r'^adminuploaderinfo/$','SIP.views.adminuploaderinfo',name='adminuploaderinfo'),
    url(r'^adminupload/(?P<code>[0-9])/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<teacher>[0-9]+|-[0-9])/(?P<rcid>[0-9]+)/$','SIP.views.adminupload',name='adminupload'),
    url(r'^registrationinterface/(?P<role>[0-9]+)/$','SIP.views.registrationinterface',name='registrationinterface'),
    url(r'^register/(?P<role>[0-9]+)/$','SIP.views.register',name='register'),
    url(r'^instiname$','SIP.views.instiname',name='instiname'),
    url(r'^reginstiname$','SIP.views.reginstiname',name='reginstiname'),
    url(r'^bulkmoveupdate/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<persid>[0-9]+|-[0-9])/(?P<instituteid>[0-9]+)/$','SIP.views.bulkmoveupdate',name='bulkmoveupdate'),
    url(r'^teacherunenroll/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<tid>[0-9]+|-[0-9])/$','SIP.views.teacherunenroll'),
    url(r'^courseadminhome/$', 'SIP.views.courseadminhome',name='courseadminhome'),
    url(r'^manualupload/$','SIP.views.manualupload',name='manualupload'),
    url(r'^sendmanual/$','SIP.views.sendmanual',name='sendmanual'),
    url(r'^facultygenericinterface/(?P<courseid>[\w{}\.\-\/]{1,40})/$','SIP.views.facultygenericinterface',name='facultygenericinterface'),
    url(r'^iitbxhome/$', 'SIP.views.iitbxhome',name='iitbxhome'),
    

    url(r'^home/(?P<bflag>[0-9]+|-[0-9])/$', 'iitbx.views.home',name='home'),
    url(r'coursedesc/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)$', 'iitbx.views.coursedesc', name='coursedesc'),
    url(r'^participantdetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','iitbx.views.studentdetails',name='studentdetails'),
    url(r'^coursedetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','iitbx.views.coursedetails',name='coursedetails'),
    url(r'^systemreports/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.systemreports',name='systemreports'),
    url(r'^genevalstatus/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.genevalstatus',name='evalstatus'),
    url(r'^genstudentstatus/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<report>[0-9])/$','iitbx.views.genstudentstatus',name='genstudentstatus'),
    url(r'^genevaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.genevaluation',name='genevaluation'),
    url(r'^genquizdata/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.genquizdata',name='genquizdata'),
    url(r'^downloadgenquizcsv/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.downloadgenquizcsv',name='downloadgenquizcsv'),
    url(r'^gengrades/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.gengrades_report',name='gengrades_report'),
    url(r'^downloadgengradecsv/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.downloadgengradecsv',name='downloadgengradecsv'),
    url(r'^courseenrollment/$', 'iitbx.views.courseenrollment',name='courseenrollment'),
    
    url(r'^genevaluationoption/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','managerapp.views.genevaluationoption',name='genevaluationoption'),
   url(r'^genquizanswers/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','managerapp.views.genquizanswers',name='genquizanswers'),
   url(r'^genevaluationoption/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','managerapp.views.genevaluationoption',name='genevaluationoption'),
   url(r'^genquizanswers/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','managerapp.views.genquizanswers',name='genquizanswers'),

   url(r'^evaluationoption/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/(?P<evalflag>[0-9])/$','SIP.views.evaluationoption',name='evaluationoption'),
   url(r'^quizanswers/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/$','SIP.views.quizanswers',name='quizanswers'),
   url(r'^instructor_course_oldreport/(?P<course>[\w{}\.\-\/]{1,40})/$','SIP.views.display_instructor_oldreport', name='display_instructor_oldreport' ),
   url(r'^geninactiveevaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','SIP.views.geninactiveevaluation',name='genevaluation'),
   url(r'^inactivequizdata/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','SIP.views.inactivequizdata',name='inactivequizdata'),
   url(r'^geninactivegrades/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<mailflag>[0-9])/$','SIP.views.geninactivegrades_report',name='geninactivegrades_report'),
   url(r'^marksheetdownloademail/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','SIP.views.marksheetdownloademail',name='marksheetdownloademail'),
   url(r'^assignmentevaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.assignmentevaluation',name='assignmentevaluation'),
   url(r'^assignmentsummary/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.assignmentsummary',name='assignmentsummary'),
   url(r'^assignmentanswers/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<aid>[0-9]+|-[0-9])/(?P<pid>[0-9]+|-[0-9])/(?P<score>\d+\.\d+|[0-9]+)/$','iitbx.views.assignmentanswers',name='assignmentanswers'), 
   #######course_module structure###############
   url(r'^get_course/','SIP.views.get_course',name='get_course'),
   url(r'^course_chapter','SIP.views.course_chapter',name='course_chapter'),
   url(r'^chapter_sequential','SIP.views.chapter_sequential',name='chapter_sequential'),
   url(r'^sequential_vertical','SIP.views.sequential_vertical',name='sequential_vertical'),
   url(r'^vertical_module','SIP.views.vertical_module',name='vertical_module'),
   #######course_module structure############### 

   url(r'^instilistforevalwise/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/$','SIP.views.instilistforevalwise',name='instilistforevalwise'),
   url(r'^evallistforinstiwise/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<instituteidid>[0-9]+)/$','SIP.views.evallistforinstiwise',name='evallistforinstiwise'),
   url(r'^pcheadmanager/$', 'SIP.views.pcheadmanager',name='pcheadmanager'),
   url(r'^instituteheadpc$','SIP.views.instituteheadpc',name='instituteheadpc'),
   url(r'^userinfo$','SIP.views.userinfo',name='userinfo'),
   url(r'^editprofile$','SIP.views.editprofile',name='editprofile'),
   url(r'^probdetail/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<instituteidid>[0-9]+)/(?P<evalid>\d+)/(?P<qcount>\d+)/(?P<teacherid>[0-9]+|-[0-9])/(?P<qattempt>[0-9]+|-[0-9])/$','SIP.views.probdetail',name='probdetail'),
   url(r'^admineditprofile$','SIP.views.admineditprofile',name='admineditprofile'),
   url(r'^institutebmuser$','SIP.views.institutebmuser',name='institutebmuser'),
   url(r'^ajaxrole$','SIP.views.ajaxrole',name='ajaxrole'),
   url(r'^allstudentinfo/$','SIP.views.allstudentinfo',name='allstudentinfo'),
   url(r'^courseallevaluationdata/(?P<courseid>[\w{}\.\-\/]{1,40})/$','SIP.views.courseallevaluationdata',name='evaluation'),
 ]

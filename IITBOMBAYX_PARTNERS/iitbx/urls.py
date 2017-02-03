'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^studentprofile/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'iitbx.views.studentprofile',name='studentprofile'),
     url(r'^postalinfo/$', 'iitbx.views.postalinfo',name='postalinfo'),
     url(r'^weeklyreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'iitbx.views.weeklyreport',name='weeklyreport'),
     url(r'^problemwiseevaluation/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.problemwiseevaluation',name='problemwiseevaluation'),
     url(r'^problemwisedata$','iitbx.views.problemwisedata',name='problemwisedata'),
     url(r'^problemwisedetails/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.problemwisedetails',name='problemwisedetails'),
     url(r'^problemwisedetailsreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.problemwisedetailsreport',name='problemwisedetailsreport'),
     url(r'^problemwisereport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.problemwisereport',name='problemwisereport'),  
     url(r'^problem_sequential','iitbx.views.problem_sequential',name='problem_sequential'),  
     url(r'^problem_unittype','iitbx.views.problem_unittype',name='problem_unittype'), 
     url(r'^assignmentdetails/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.assignmentdetails',name='assignmentdetails'),
     url(r'^assignmentmultipleoptions/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<aid>[0-9]+|-[0-9])/(?P<part>[0-9]+|-[0-9])/$','iitbx.views.assignmentmultipleoptions',name='assignmentmultipleoptions'), 
      url(r'^assignmentmarksdata/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.assignmentmarksdata',name='assignmentmarksdata'), 
    url(r'^assignmentmarksdetails/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.assignmentmarksdetails',name='assignmentmarksdetails'),   
    url(r'^courseenrollment/$', 'iitbx.views.courseenrollment',name='courseenrollment'),  
    url(r'^gradesumary/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.gradesumary',name='gradesumary'),  
    url(r'^nongradedevaluation/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.nongradedevaluation',name='nongradedevaluation'),   
    url(r'^nongradedassignmentsummary/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.nongradedassignmentsummary',name='nongradedassignmentsummary'), 
    url(r'^nongradedanswers/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<aid>[0-9]+|-[0-9])/(?P<pid>[0-9]+|-[0-9])/(?P<score>\d+\.\d+|[0-9]+)/$','iitbx.views.nongradedanswers',name='nongradedanswers'),
    url(r'^nongradedmultipleoptions/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<aid>[0-9]+|-[0-9])/(?P<part>[0-9]+|-[0-9])/$','iitbx.views.nongradedmultipleoptions',name='nongradedmultipleoptions'), 
    url(r'^nongradedproblemwiseevaluation/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.nongradedproblemwiseevaluation',name='nongradedproblemwiseevaluation'),
    url(r'^nongradedproblemwisedata$','iitbx.views.nongradedproblemwisedata',name='nongradedproblemwisedata'),
    url(r'^nongradedproblemwisedetails/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.nongradedproblemwisedetails',name='nongradedproblemwisedetails'),
     url(r'^discussionforumdata/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.discussionforumdata',name='discussionforumdata'),
    #######course_module structure###############
    url(r'^course_chapter/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.course_chapter',name='course_chapter'),
    url(r'^chapter_sequential','iitbx.views.chapter_sequential',name='chapter_sequential'),
    url(r'^sequential_unittype','iitbx.views.sequential_unittype',name='sequential_vertical'),
    url(r'^vertical_module','iitbx.views.vertical_module',name='vertical_module'),
    url(r'^display_type','iitbx.views.display_type',name='display_type'),
    url(r'^problem_compare','iitbx.views.problem_compare',name='problem_compare'),
    #######course_module structure############### 
    url(r'^closedcoursegrade/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'iitbx.views.closedcoursegrade',name='closedcoursegrade'),
    ########closed course grades from csv #######
    url(r'^closed_courses_grades_report/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.closed_courses_grades_report',name='closed_courses_grades'),
#######For comparing two problems############
    url(r'^problemwiseevaluation_comparision/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.problemwiseevaluation_comparision',name='problemwiseevaluation_comparision'),
    url(r'^problemcompare_report/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.problemcompare_report',name='problemcompare_report'),
    url(r'^certified_participant/$', 'iitbx.views.certified_participant',name='certified_participant'),
    url(r'^managerhome/$', 'iitbx.views.managerhome',name='managerhome'),
    url(r'^invited_participant/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.invited_participant',name='invited_participant'),
    url(r'^inviteduserlist/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.inviteduserlist',name='inviteduserlist'),
    url(r'^problemcomparegraph/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.problemcomparegraph',name='problemcomparegraph'),
    ######For discusson_forum########
    url(r'^discussionforum_user_participation_count/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'iitbx.views.discussionforum_user_participation_count',name='discussionforum_user_participation_count'),
    url(r'^discussionforum_user_date_wise_count/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'iitbx.views.discussionforum_user_date_wise_count',name='discussionforum_user_date_wise_count'),
    #################################
    url(r'^survey_sequential','iitbx.views.survey_sequential',name='survey_sequential'),  
    url(r'^survey_unittype','iitbx.views.survey_unittype',name='survey_unittype'), 
    url(r'^surveydetailreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.surveydetailreport',name='surveydetailreport'),
    url(r'^surveyreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.surveyreport',name='surveyreport'),
    
    url(r'^poll_sequential','iitbx.views.poll_sequential',name='poll_sequential'),  
    url(r'^poll_unittype','iitbx.views.poll_unittype',name='poll_unittype'), 
    url(r'^polldetailreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.polldetailreport',name='polldetailreport'),
    url(r'^pollreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.pollreport',name='pollreport'),
    
    url(r'^open_assessment_sequential','iitbx.views.open_assessment_sequential',name='open_assessment_sequential'),  
    url(r'^open_assessment_unittype','iitbx.views.open_assessment_unittype',name='open_assessment_unittype'), 
    url(r'^open_assessment_detailreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.open_assessment_detailreport',name='open_assessment_detailreport'),
    url(r'^openassessment_report/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$','iitbx.views.openassessment_report',name='openassessment_report'),
    
 ]

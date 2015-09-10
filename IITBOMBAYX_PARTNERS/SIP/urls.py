'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''
from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^$', 'SIP.views.sessionlogin',name='course'),
     url(r'^get_multi_roles/', 'SIP.views.get_multi_roles',name='get_multi_roles'),
     url(r'^set_role/(?P<role>[0-9])/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<cid>[0-9]{1,40})$', 'SIP.views.set_single_role',name='set_single_role'),	
    url(r'^teacher/(?P<tid>[0-9]+)/$','SIP.views.teacherhome'),
    url(r'^studentsinformation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','SIP.views.studentdetails',name='studentdetails'),
	url(r'^updatestudentinformation/(?P<pid>[0-9]+)/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<t_id>[0-9]+)/$','SIP.views.Update'),
    
    url(r'^downloadcsv1/(?P<course>[\w{}\.\-\/]{1,40})/(?P<id>[0-9]+)/$','SIP.views.downloadcsv',name='downloadcsv'),
    url(r'^uploads_studentsinfo/(?P<code>[0-9])/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'SIP.views.upload'),
    #url(r'^upload/uploaded/', 'SIP.views.uploaded'),
    url(r'^downloadcsv/(?P<code>[0-9])/$', 'SIP.views.output_csv'),
	url(r'^unenroll/(?P<pid>[0-9-]+)/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<t_id>[0-9]+)/$','SIP.views.unenrollstudent'),
	#url(r'^report/(?P<option>[a-z]+)/(?P<course>[\w{}\.\-\/]{1,40})/$','SIP.views.report'),
   	url(r'^teacherslist/(?P<courseid>[\w{}\.\-\/]{1,40})/$','SIP.views.teacherlist'),
    url(r'^ccourses/',views.ccourse, name='ccourses'),
    url(r'^blendedadmin_home/','SIP.views.blendedadmin_home',name='blendedadmin_home'),
    url(r'^blendedadmin/(?P<report_id>[\w{}\.\-\/]{1,5})/$','SIP.views.blendedadmin',name='blendedadmin'),
    url(r'^instructoradmin/(?P<report_id>[\w{}\.\-\/]{1,5})/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<param_id>[\w{}\.\-\/]{1,40})/$', 'SIP.views.instructoradmin',name='instructoradmin'),
	url(r'^grades/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','SIP.views.grades_report',name='grades_report'),
    url(r'^downloadgradecsv/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','SIP.views.downloadgradecsv',name='downloadgradecsv'),
    url(r'^faculty_report/$','SIP.views.course_faculty',name='faculty_report'),
    url(r'^instructor_course_report/(?P<course>[\w{}\.\-\/]{1,40})/$','SIP.views.display_instructor_report', name='display_instructor_report' ),
    url(r'^approvedinstitute/$','SIP.views.approvedinstitute',name='approvedinstitute'),
    url(r'^institutecourses$','SIP.views.institutecourses',name='institutecourses'),
    url(r'^courseteachers$','SIP.views.courseteachers',name='courseteachers'),
    url(r'^teacherstudent/$','SIP.views.teacherstudent',name='teacherstudent'),
    url(r'^evaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/(?P<evalflag>[0-9])/$','SIP.views.evaluation',name='evaluation'),
    url(r'^quizdata/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','SIP.views.quizdata',name='evaluation'),
    url(r'^downloadquizcsv/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','SIP.views.downloadquizcsv',name='downloadquizcsv'),
    url(r'^coursedescription/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','SIP.views.coursedescription',name='coursedescription'),
    url(r'^allcourses/(?P<courseflag>[0-9])/$','SIP.views.allcourses',name='allcourses'),
 ]

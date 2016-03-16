'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^studentprofile/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'iitbx.views.studentprofile',name='studentprofile'),
     url(r'^postalinfo/$', 'iitbx.views.postalinfo',name='postalinfo'),
     url(r'^weeklyreport/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'iitbx.views.weeklyreport',name='weeklyreport'),
     url(r'^problemwiseevaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.problemwiseevaluation',name='problemwiseevaluation'),
     url(r'^problemwisedata$','iitbx.views.problemwisedata',name='problemwisedata'),
     url(r'^problemwisedetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.problemwisedetails',name='problemwisedetails'), 
     url(r'^assignmentmultipleoptions/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<aid>[0-9]+|-[0-9])/(?P<part>[0-9]+|-[0-9])/$','iitbx.views.assignmentmultipleoptions',name='assignmentmultipleoptions'), 
        
 ]

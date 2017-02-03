'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^usersummary/$', 'managerapp.views.usersummary',name='usersummary'),
     url(r'^registrationsummary/$', 'managerapp.views.registrationsummary',name='registrationsummary'),
     url(r'^userjoinedsummary$', 'managerapp.views.userjoinedsummary',name='userjoinedsummary'),
     url(r'^courseenrrollment/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'managerapp.views.courseenrrollment',name='courseenrrollment'),
     url(r'^coursedailyreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'managerapp.views.coursedailyreport',name='coursedailyreport'),
     url(r'^courseweeklyreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'managerapp.views.courseweeklyreport',name='courseweeklyreport'),
     url(r'^coursemonthlyreport/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'managerapp.views.coursemonthlyreport',name='coursemonthlyreport'),
     url(r'^ataglance/$', 'managerapp.views.ataglance',name='ataglance'),
     url(r'^activityrep/$', 'managerapp.views.activityrep',name='activityrep'),
     url(r'^studentdemography/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'managerapp.views.studntdemography',name='studntdemography'),
     #url(r'^activity/(?P<courseid>[\w{}:\.\-\+\/]{1,40})$', 'managerapp.views.activity', name='activity' ),
     url(r'^activity_day_wise/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'managerapp.views.activity_day_wise', name='activity_day_wise'),
     url(r'^activity_date_wise/(?P<courseid>[\w{}:\.\-\+\/]{1,40})/$', 'managerapp.views.activity_date_wise', name='activity_date_wise')
 ]

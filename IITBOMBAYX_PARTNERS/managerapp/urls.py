from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^usersummary/$', 'managerapp.views.usersummary',name='usersummary'),
     url(r'^registrationsummary/$', 'managerapp.views.registrationsummary',name='registrationsummary'),
     url(r'^userjoinedsummary$', 'managerapp.views.userjoinedsummary',name='userjoinedsummary'),
     url(r'^courseenrrollment/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'managerapp.views.courseenrrollment',name='courseenrrollment'),
     url(r'^coursedailyreport/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'managerapp.views.coursedailyreport',name='coursedailyreport'),
     url(r'^courseweeklyreport/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'managerapp.views.courseweeklyreport',name='courseweeklyreport'),
     url(r'^coursemonthlyreport/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'managerapp.views.coursemonthlyreport',name='coursemonthlyreport'),
     url(r'^ataglance/$', 'managerapp.views.ataglance',name='ataglance'),
     url(r'^activityrep/$', 'managerapp.views.activityrep',name='activityrep'),
     url(r'^studentdemography/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'managerapp.views.studntdemography',name='studntdemography'),
 ]

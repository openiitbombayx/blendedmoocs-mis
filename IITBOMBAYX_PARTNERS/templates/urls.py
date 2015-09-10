from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', 'SIP.views.sessionlogin',name='course'),
    #url(r'^mutiir', views.multinstrole, name = 'mutiir'),
	# REGISTRATION (Dhiraj)
    url(r'^home/$', 'SIP.views.home'),
    url(r'^request_registration/$', 'SIP.views.requestregister'),
    url(r'^register/(?P<reqid>\d+)/$', 'SIP.views.register'), #(?P<password>[0-9]+)/(?P<email>[a-zA-Z0-9@_.]+)
    url(r'^auth_register/(?P<appinsid>\d+)/$', 'SIP.views.auth_register'),
	url(r'^request_verification_success/(?P<reqid>\d+)/$', 'SIP.views.request_verification_success'),
	url(r'^resend_verification_mail/(?P<ec_id>[0-9]+)/(?P<pk>[0-9]+)/$','SIP.views.resend_verification_mail'),
	#url(r'^admin_upload/$','SIP.views.admin_upload'),  # Admin upload
	url(r'^performance/$','SIP.views.get_grade'),
	url(r'^display_grade/$','SIP.views.display_grade'),





	#Apoorva Agrawal
    url(r'^head/pc/', views.pc, name='pc'),	
    url(r'^dash/', views.dash, name = 'dash'),
    url(r'^invite/', views.invite, name = 'invite'),
    url(r'^approve/(?P<req_pid>[0-9]+)/', views.approve, name = 'approve'),
    url(r'^reject/(?P<req_pid>[0-9]+)/', views.reject, name = 'reject'),
    url(r'^consent/(?P<req_pid>[0-9]+)/', views.consent, name = 'consent'),
    url(r'^dissent/(?P<req_pid>[0-9]+)/', views.dissent, name = 'dissent'),
    url(r'^remove/(?P<clu_pid>[0-9]+)/', views.removeCLU, name = 'remove'),


     
	#Course management
    url(r'^enrollfinal/IITBombayX/(?P<course>[a-zA-Z0-9.]+)/(?P<years>[0-9-]+)/$', views.enrollfinal, name = 'enrollfinal'),
    url(r'^unenroll/(?P<course>[a-zA-Z0-9.]+)/(?P<year>[0-9-]+)/$', views.unenroll, name='unenroll'),
    url(r'^enrolled/(?P<course>[a-zA-Z0-9.]+)/$', views.enrolled, name='enrolled'),
    url(r'^updated/(?P<course>[a-zA-Z0-9.]+)/$', views.updated, name='updated'),
    url(r'^unenrolled/(?P<args>[a-zA-Z0-9.]+)/$', views.unenrolled, name='unenrolled'),
    url(r'^ccourses/',views.ccourse, name='ccourses'),
    url(r'^allcourses/',views.allcourses, name='allcourses'),
    url(r'^update/IITBombayX/(?P<course>[a-zA-Z0-9.]+)/(?P<years>[0-9-]+)/$',views.updatecourses, name='update'),
    url(r'^IITBombayX/(?P<course>[a-zA-Z0-9.]+)/(?P<year>[0-9-]+)/$',views.course, name='course'),
	 # end of course management 


      #Student management team
     

     
    url(r'^update/(?P<pid>[0-9-]+)/(?P<courseid>[a-zA-Z0-9.]+)$','SIP.views.Update', name='update'),
    url(r'^teacherhome/$','SIP.views.Course_template'),
    url(r'^teacherlist/$','SIP.views.teacherlist'),    
    url(r'^coordinatorhome/$','SIP.views.courselist'),
    url(r'^parse/(?P<course>[\w{}\.\-\/]{1,40})$','SIP.views.studentdetails'),
   #url(r'^print/(?P<row>[\w{}.-]{1,40})/$','SIP.views.Print'),
    url(r'^updatestudent/(?P<pid>[0-9])/(?P<courseid>[\w{}.-]{1,40})/$','SIP.views.Update'),
    url(r'^movestudents$','SIP.views.movestudents'),
    url(r'^downloadcsv1/(?P<course>[a-zA-Z0-9]+)/$','SIP.views.downloadcsv',name='downloadcsv'),
    #url(r'^print$','SIP.views.Print'),
    url(r'^upload/(?P<code>[0-9])/$', 'SIP.views.upload'),
    url(r'^upload/uploaded/', 'SIP.views.uploaded'),
    #url(r'^getcsv/()', 'SIP.views.get_csv'),
    #url(r'^getvalidcsv/()', 'SIP.views.get_validcsv'),
    url(r'^downloadcsv/(?P<code>[0-9])/$', 'SIP.views.output_csv'),
    url(r'^unenroll/(?P<pid>[0-9-]+)/(?P<courseid>[a-zA-Z0-9./-]+)$','SIP.views.unenrollstudent'),
      # end of student management 
    

]

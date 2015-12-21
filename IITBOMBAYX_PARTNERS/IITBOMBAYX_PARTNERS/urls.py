"""IITBOMBAYX_PARTNERS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles import views
from django.views.static import serve
handler404 = 'SIP.views.bmwcustom404'
handler500 = 'SIP.views.bmwcustom404'
handler403 = 'SIP.views.bmwcustom404'
urlpatterns = (
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('SIP.urls'), name = "SIP"),
    url(r'^logout/$', 'SIP.views.logout'),
     # If user is not login it will redirect to login page
    url(r'^forgot_password/$', 'SIP.views.forgot_pass'),
   # url(r'^resetpass/(?P<emailid>[0-9]+)$', 'SIP.views.resetpass'),
    #url(r'^createpass/(?P<emailid>[0-9]+)$', 'SIP.views.createpass'),
    #url(r'^login_success/$','SIP.views.login_success'),
    url(r'^changepassword/$','SIP.views.change_pass'),
        ################encrypted link t#######################
   url(r'^resetpassword/(?P<token>[\w.$\-_=]+)/$',
     'SIP.views.resetpass'),
   url(r'^createpassword/(?P<personid>[\w.$\-_=]+)/$',
     'SIP.views.createpass'),
   url(r'^createpasswordemail/$', 'SIP.views.createpasslink'),
   url(r'^manager/', include('managerapp.urls'),name='managerapp'), 
     
)

if settings.DEBUG is False:
    urlpatterns += (
   
   url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'static'), 'show_indexes': settings.DEBUG}),
) 


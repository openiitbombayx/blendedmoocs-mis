'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''
 
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from datetime import date,timedelta
from django.db import transaction
from django.contrib import auth
from django.template import Context
from django.core import signing
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User
from SIP.models import Userlogin
from SIP.validations import retrieve_error_message,validate_login,validate_email
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.cache import cache_control
from django.core.cache import cache
from .models import *
from .validations import *
from django.template.loader import get_template
from forms import UploadForms
from django.contrib import messages
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.conf.urls.static import static
from django.db.models import Q
from django.core.files import File
from SIP.models import *
import MySQLdb
from time import time
from SIP.validations import *
from django.utils import timezone
import glob 
from iitbx.models import *
from managerapp.models import *
#from easygui import *
import csv
import operator
#from bs4 import *
from urllib2 import urlopen
import sys
import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from cgi import escape
import urllib2,cookielib
from django.db import connection, transaction
import json
from globalss import *
from IITBOMBAYX_PARTNERS.settings import *
import subprocess
import collections
#############################end of import statements by student management#######################################
current=timezone.now
default_password="Welcome123"
default_end_date="4712-12-31"

########################views Starts from Here ###################################

@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_multi_roles(request): 
    rolelen=-1   
    args={}
    try:
       person=Personinformation.objects.get(email=request.session['email_id'])
    except Exception as e:
          args['error_message'] = getErrorContent("person_not_exit")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)
    

    if request.POST:        
        
        institute_id = request.POST.get('institute_id')
        #print request.POST.get('institute_id')
        request.session['institute_id']=request.POST.get('institute_id')#institute id set
        instiroles,colevelroles,args= roleselect(request,institute_id,person,args)
        rolelen=len(instiroles)+len(colevelroles[0])+len(colevelroles[1])
        if rolelen==1:
            if len(instiroles)==1:
               return onerole(request,instiroles,args)
            elif len(colevelroles[0])==1:
               return onerole(request,colevelroles[0],args)
            elif len(colevelroles[1])==1:
               return onerole(request,colevelroles[1],args)
        elif rolelen==0:
            args['norole']="You currently have no roles"
            return render(request,selectrole_,args)
        args.update(csrf(request)) 
        args['rolelen']=rolelen
        return render(request,selectrole_,args)
           
                 
    l=[]  
    request.session['person_id']=person.id#person id set   
   
    insti_obj=Institutelevelusers.objects.filter(personid=person.id).values("instituteid").distinct()
    
    
    for i in insti_obj:
        
        insti_x=T10KT_Institute.objects.filter(instituteid=i["instituteid"])
        x= insti_x[0].institutename
        l.append([i["instituteid"],x])

    insti_obj=Courselevelusers.objects.filter(personid=person.id).values("instituteid").distinct()
    
    for i in insti_obj:
        flag=True
        insti_x=T10KT_Institute.objects.filter(instituteid=i["instituteid"])
        x= insti_x[0].institutename
        for row in l:
                if row[0]==i["instituteid"]:
                        flag=False
        if flag:
                l.append([i["instituteid"],x])
  
    if len(l)==1:
       return oneinstitute(request,person)
    
        
    try:
       request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=institute_id).remotecenterid.remotecenterid
    except:
       request.session['rcid']="   " 
    args={"l":l,'flag':True}
    args['firstname']=person.firstname
    args['lastname']=person.lastname
    args['email']=request.session['email_id'] 
    args['rcid']=request.session['rcid'] 
    args.update(csrf(request))
    
    return render(request,selectrole_,args)    
        
##########return list of all roles of logged in peron in selected institute#####################

################

@login_required(login_url='/')
def roleselect(request,institute_id,person,args):
    args['rolename']="Super User"
    try:
        instiroles=[]
        clrolelist=[]
        ccclrolelist=[]
        arcclrolelist=[]
        obj = Institutelevelusers.objects.filter(instituteid=institute_id,roleid__gte=0).filter(personid=request.session['person_id']).values("roleid").distinct()
        for row in obj:
            obj=Lookup.objects.get(category='role', code=row['roleid'])
            
            instiroles.append([obj.comment,row['roleid'],0])
        sevenenddate=timezone.now()-timezone.timedelta(days=7)
        cobj = Courselevelusers.objects.filter(instituteid__instituteid=institute_id,roleid__gte=0,courseid__courseend__gte=sevenenddate).filter(personid=request.session['person_id']).order_by("-courseid__courseend")
        for row in cobj:
            obj=Lookup.objects.get(category='role', code=row.roleid)
           # print row.courseid.id,row.roleid,obj.comment
            ccclrolelist.append([obj.comment,row.roleid,row.courseid,1])       
        arccobj = Courselevelusers.objects.filter(instituteid__instituteid=institute_id,roleid__gte=0,courseid__courseend__lt=sevenenddate).filter(personid=request.session['person_id']).order_by("-courseid__courseend")
        for row in   arccobj:
            obj=Lookup.objects.get(category='role', code=row.roleid)
            #print row.courseid.id,row.roleid,obj.comment,"blended",row.courseid.blended_mode
            if row.courseid.blended_mode == 1:
               arcclrolelist.append([obj.comment,row.roleid,row.courseid,0])
        args['flag']=False
        args['instiroles']=instiroles 
        args['ccclrolelist']=ccclrolelist
        args['arcclrolelist']=arcclrolelist
        args['firstname']=person.firstname
        args['lastname']=person.lastname
        args['institutename']=T10KT_Institute.objects.get(instituteid=request.session['institute_id']).institutename
        args['email']=request.session['email_id']
        colevelroles=[ccclrolelist,arcclrolelist]
        
        return instiroles,colevelroles,args
    except Exception as e:
          args['error_message'] = getErrorContent("roleid_not_exit")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)


###################Set institue directly in session if only one institute is present for logged in user#################
@login_required(login_url='/')
def oneinstitute(request,person):
    rolelen=-1
    args={}
    if Institutelevelusers.objects.filter(personid=person.id).exists():
        institute_id=Institutelevelusers.objects.filter(personid=person.id)[0].instituteid.instituteid
    else:
        institute_id=Courselevelusers.objects.filter(personid=person.id)[0].instituteid.instituteid
    request.session['institute_id']=institute_id#institute id set
    try:
       request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=institute_id).remotecenterid.remotecenterid
       #Added Org request session 
       request.session['org']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=institute_id).remotecenterid.org
       print "check" ,request.session['org']
    except:
       request.session['rcid']="   "  
       #Added Org request session 
       request.session['org']="None"    
    #insti_x=T10KT_Institute.objects.filter(instituteid=institute_id)
    #x= insti_x[0].institutename
    args['rcid']=request.session['rcid']
    args['org']=request.session['org']
    
    instiroles,colevelroles,args=roleselect(request,institute_id,person,args)
    rolelen=len(instiroles)+len(colevelroles[0])+len(colevelroles[1])
    if rolelen==1:
            if len(instiroles)==1:
               return onerole(request,instiroles,args)
            elif len(colevelroles[0])==1:
               return onerole(request,colevelroles[0],args)
            elif len(colevelroles[1])==1:
               return onerole(request,colevelroles[1],args)   

    elif rolelen==0:
         args['norole']="You currently have no roles"
         return render(request,selectrole_,args)
    args.update(csrf(request)) 
    args['rolelen']=rolelen
    return render(request,selectrole_,args)

############# set role directly in session if only one role is present for logged in user###################################
def onerole(request,rolelist,args):
    if rolelist[0][2]:
       args.update(csrf(request))
                    # print "role list",rolelist[0][2]
       return set_single_role(request,rolelist[0][1],rolelist[0][2].courseid,rolelist[0][2].id)        
    args.update(csrf(request))
    return set_single_role(request,rolelist[0][1],0,0)
    

######################set selected roles in session for logged in user###################################
#************** Begin decorator for setting roles****
#def rolesetdeocorator(argfunc):
 #   def _decoratedfun(request,*args, **kwargs):
  #      # maybe do something before the view_func call
   #     print "decorator executed"
    #    get_multi_roles(request)
     #   response = argfunc(request,*args, **kwargs)
      #  # maybe do something after the view_func call
       # return response
    #return _decoratedfun
#************** End decorator ***********************


#@rolesetdeocorator
@login_required(login_url='/')
def set_single_role(request,role,courseid,cid):
    try:    
        request.session['role_id']=int(role)
        request.session['rolename']=Lookup.objects.get(category="Role",code=role).comment
        request.session['courseid']=courseid#role id set
        request.session['edxcourseid']=cid#role id set
        args=sessiondata(request)
        return ccourse(request)
    
    except Exception as e:
          #args['error_message'] = getErrorContent("category_not_exit")
          #args['error_message'] = "Error " + str(e.message) + str(type(e))
          print "Error " + str(e.message) + str(type(e))
          return sessionlogin(request)
          #return render(request,error_,args)

#Return dictionary with default data of session institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid
@login_required(login_url='/')
def sessiondata(request):
    args = {}
    args.update(csrf(request))
    try:
       person=Personinformation.objects.get(email=request.session['email_id'])
       args['institute']=institute=T10KT_Institute.objects.get(instituteid=request.session['institute_id'])
       args['person']=person
    except Exception as e:
          args['error_message'] = getErrorContent("unique_person")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)
    
    args['institutename']=institute.institutename
    args['firstname']=person.firstname
    args['lastname']=person.lastname
    args['email']=request.session['email_id']
    args['role_id']=int(request.session['role_id'])
    lu_obj=Lookup.updatedate()
   
    
    args['refreshdate']=lu_obj
   
    try:
       args['rolename']=request.session['rolename']
    except:
       pass
    args['rcid']=request.session['rcid'] 
    #Added for org
    args['org']=request.session['org']
    print args['org']
    try: 
       args['courseid']= request.session['courseid']
    except:
       pass
    try:
       args['edxcourseid']=request.session['edxcourseid']
    except:
       pass
    args['rooturl']=ROOT_URL
    return args             
###########On root url(home page) checking If session is active then redirect to institute  select page or blended admin home page based on usertypeid  Else redirect to login page ############################# 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sessionlogin(request):
            
    args = {}
    args.update(csrf(request)) 
    try:
            if request.session['email_id']:
               
               user = User.objects.get(email=request.session['email_id'])
               user_info=Userlogin.objects.get(user=user)
               if user_info.usertypeid==0 or user_info.usertypeid==9 or user_info.usertypeid==10:
                   print user_info.usertypeid
                   return HttpResponseRedirect(iitbxhome_)
               elif user_info.usertypeid==2 or user_info.usertypeid==3:
                    return commonhome(request)
               #elif user_info.usertypeid==3:
                    
                   #return HttpResponseRedirect(courseadminhome_)
               else:
                   return HttpResponseRedirect(get_multi_roles_)
            else:               
                return loginn(request)
    except:
                    
            return loginn(request)


@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def iitbxhome(request):
    args={}
    try:
       args['usertype']=request.session['usertype']
       args['email_id']= request.session['email_id']
       person=Personinformation.objects.get(email=request.session['email_id'])
       args['institute']=institute=T10KT_Institute.objects.get(instituteid=person.instituteid_id)
       args['person']=person
       args['institutename']=institute.institutename
       args['firstname']=person.firstname
       args['lastname']=person.lastname
       request.session['lastname']=person.lastname
       request.session['institutename']=institute.institutename
       request.session['firstname']=person.firstname
       request.session['role_id'] =0
       request.session['rolename']="Super User"
       args['role_id'] =0
       args['rolename']="Super User"
       args['email']=request.session['email_id']
       #Start change of org
       #request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=person.instituteid_id).remotecenterid.remotecenterid
       request.session['org']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=person.instituteid_id).remotecenterid.org
       #End change of org
       args['rcid']= request.session['rcid'] 
       args['org']=request.session['org']
       print "request session"
    except Exception as e:
          args['error_message'] = getErrorContent("person_not_exit")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)
    

    if request.POST:        
        
        institute_id = request.POST.get('institute_id')
        request.session['institute_id']=request.POST.get('institute_id')#institute id set
        
        args['institutename']=institute.institutename
    return render_to_response("iitbxhome.html",args)
# end iitbxhome

###############checking credential of user and redirect to home page or login page ##########################
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginn(request):
    
    page = LOGIN_
    module = LOGIN_
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        args['email']= request.POST['email']
        args['error_message']=[]
        #args = emailid_validate(request,args)
        if args['error_message']:
            return render_to_response(login_,args)            
        loginlist = validate_login(request) 
        request.session['usertype'] =loginlist
## If the emailid exists, then call the page according to the role
        if (loginlist==1):      
            return HttpResponseRedirect(get_multi_roles_)
## If the emailid does not exist,display error message
        elif (loginlist == 0 or loginlist == 9 or loginlist == 10):
             return HttpResponseRedirect(iitbxhome_)
        elif (loginlist == 2) or (loginlist == 3):
             #request.session['faculty']=1
             return commonhome(request)#return HttpResponseRedirect(facultyreport_)
        #elif (loginlist == 3):
            # return HttpResponseRedirect(courseadminhome_)
        elif (loginlist == 4):
            error_message=retrieve_error_message(module,page,'LN_INV')##required to create error content message           
            args['error_message']=error_message
            return render_to_response(login_,args)              

        else:
            error_message=retrieve_error_message(module,page,'LN_INV')            
            args['error_message']=error_message
            return render_to_response(login_,args)            
    return render_to_response(login_,args)
           
   
   
################### Send mail for generating link of new password on click of forget password ink ######################   
def forgot_pass(request):
    module = LOGIN_
    page = FORGOTPASS_
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':        
        email = request.POST['email']
        per_id= validate_email(email)
## If valid email id, then a mail is sent to his email alongwith a link to reset his password 
        if per_id != -1:     
            args['message']= retrieve_error_message(module,page,'NO_ERR')
            try:
               ec_id = EmailContent.objects.get(systype='Login', name='resetpassword').id
            except Exception as e:
               args['error_message'] = getErrorContent("Email_cant_send")
               args['error_message'] = "\n Error " + str(e.message) + str(type(e))
               return render(request,error_,args)
           #print ec_id
            send_email(request,ec_id, per_id, per_id)
            return render_to_response(forgotpassword_,args)      
                           
        else:
## If invalid email, displays an error message
            args['message']=retrieve_error_message(module,page,'EML_INV')
            return render_to_response(forgotpassword_,args)        
    return render_to_response(forgotpassword_,args)



#################### Check and Reset new password for user on request of forgot password ##########################
def resetpass(request,token):
    emailid = signer.unsign(token)
    per_id = emailid
     
    module = LOGIN_
    page = RESETPASS_
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':

        args['password1']= password1=request.POST.get('new_password1','')
        args['password2']= password2=request.POST.get('new_password2','')
        args['message']=[]
        args = pwd_field_empty(request,args,'Password')
        if args['message']:
            return render_to_response(resetpassword_,args)

        
        else:
## If the two new passwords match, password is changed and a mail is sent to the user regarding the change
            try: 
                userid=Personinformation.objects.get(id=emailid)           
                user = User.objects.get(email=userid.email)
            except Exception as e:
               args['error_message'] = getErrorContent("no_unique_person")
               args['error_message'] = "\n Error " + str(e.message) + str(type(e))
               return render(request,error_,args)
            user.set_password(password1)
            user.save()
            args['message']= retrieve_error_message(module,page,'PWD_SET')
            try: 
                ec_id = EmailContent.objects.get(systype='Login', name='success').id
            except Exception as e:
               args['error_message'] = getErrorContent("resetpass_email")
               args['error_message'] = "\n Error " + str(e.message) + str(type(e))
               return render(request,error_,args)
            send_email(request,ec_id, per_id, per_id)
            return render_to_response(changepasswordsuccess_,args)            
  
    return render_to_response(resetpassword_,args)


#############Create Link to create  password for user on registration by Python Registration scripts if status is 0 ########################


def createpasslink(request):
    module = LOGIN_
    page = FORGOTPASS_
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':        
        email = request.POST['email']
        per_id= validate_email(email)
## If valid email id, then a mail is sent to his email alongwith a link to create his password 
        if per_id != -1:     
            args['message']= retrieve_error_message(module,page,'NO_ERR')
            try:
               ec_id = EmailContent.objects.get(systype = 'Login', name = 'createpassword').id
               mail_obj = EmailContent.objects.get(id=ec_id)
            except Exception as e:
               args['error_message'] = getErrorContent("Email_cant_send")
               args['error_message'] = "\n Error " + str(e.message) + str(type(e))
               return render(request,error_,args)
            per_obj = Personinformation.objects.get(email=email)
            fname = per_obj.firstname
            email = per_obj.email
            per_id=signer.sign(per_obj.id)
            link = ROOT_URL + mail_obj.name + '/%s' %per_id
            message = mail_obj.message %(fname, link)  
            send_mail(mail_obj.subject, message ,DEFAULT_FROM_EMAIL ,[email], fail_silently=False)
            return render_to_response(mailsendsuccessfully_,args)      
                           
        else:
## If invalid email, displays an error message
            args['message']=retrieve_error_message(module,page,'EML_INV')
            return render_to_response(createpasswordlink_,args)        
    return render_to_response(createpasswordlink_,args)

#############Create password for user on registration by Python Registration scripts if status is 0 ########################



def createpass(request,personid):
    emailid = signer.unsign(personid)
    per_id = emailid
    module = LOGIN_
    page = RESETPASS_
    args = {}
    args.update(csrf(request))
    try:
       userid=Personinformation.objects.get(id=emailid)
       
       if Userlogin.objects.get(user=User.objects.get(email=userid.email)).status==False:   
		  

		     args['password1']=password1= request.POST.get('new_password1','')
		     args['password2']=password2= request.POST.get('new_password2','')
		     args['message']=[]
		     args = pwd_field_empty(request,args,'Password')
		     if args['message']:
		        return render_to_response(createpassword_,args)


		     else:  
	  ## If the two new passwords match, password is changed and a mail is sent to the user regarding the change 
		                 
		        userid=Personinformation.objects.get(id=emailid)           
		        user = User.objects.get(email=userid.email)           
		        user.set_password(password1)
		        user.save()
		        user_info=Userlogin.objects.get(user=user)
		        user_info.status=1
		        user_info.save()
		        args['message']= retrieve_error_message(module,page,'PWD_SET')
		        ec_id = EmailContent.objects.get(systype='Login', name='create_success').id
		        send_email(request,ec_id, per_id, per_id)
		        return render_to_response(createpasswordsuccess_,args)            
	  
		  #return render_to_response(createpassword_,args)
       return  render_to_response(passwordalreadycreated_,args)

    except Exception as e:
           args['error_message'] = getErrorContent("no_person")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)



#################### Delete session and redirect to login page on logout click#######################################

@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    #logout_obj = User.objects.get(email=request.session['email_id'])
   # logout_obj.loginstatus='False'
   # logout_obj.save()
    try:
		full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
		dirpath=os.path.join(full_path,'static/tmp/')
		a=os.listdir(dirpath)
		for f in os.listdir(dirpath):
		
		   full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
		   reqpath=os.path.join(full_path,'static/tmp/',f)
		   filestat=os.stat(reqpath).st_mtime
		   now = time()
		   if filestat < (now-86400):		      
		      os.remove(reqpath)
		      print f ,"is removed",filestat,"now",now
		
		request.session.flush()
		cache.clear()
		auth.logout(request)
		#return HttpResponseRedirect('/')
		response = redirect('/')
		response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
		response.delete_cookie()
		return response
   
    except:
        return HttpResponseRedirect('/')



########################Set Home Page for different roles.For Head and Program Coordinator display list of courses enrolled by their


@login_required(login_url='/')
def ccourse(request):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
    try:
       args =sessiondata(request)
    except Exception as e:
          print e.message
          return sessionlogin(request)
    input_list={}
    
    input_list.update(args)
    input_list.update(csrf(request))
    input_list['roleid']=args['role_id']
    sevenenddate=timezone.now()-timezone.timedelta(days=7)    
    if input_list['roleid']==4:
		return HttpResponse('/coordinatorhome/')
    if input_list['roleid']==5:
		
		return teacherhome(request,args['person'].id)
    input_list['viewer'] = args['person'].id

    enrolled_courses=courseenrollment.objects.filter(status=1, instituteid__instituteid=args['institute']).order_by("-courseid__courseend")

    edx_enrolled_courses=[]
    edx_unenrolled_courses=[]
    #unenrollcurrentedxcourse=edxcourses.objects.filter(blended_mode=1,courseend__gte=sevenenddate).exclude(courseid__in=enrolled_courses.values_list('courseid__courseid', flat=True)).order_by("-courseend")
    unenrollcurrentedxcourse=edxcourses.objects.filter(blended_mode=1,courseend__gte=sevenenddate,org=args['org']).exclude(courseid__in=enrolled_courses.values_list('courseid__courseid', flat=True)).order_by("-courseend")
    unenrollarchivedcourse=edxcourses.objects.filter(blended_mode=1,courseend__lt=sevenenddate,org=args['org']).exclude(courseid__in=enrolled_courses.values_list('courseid__courseid', flat=True)).order_by("-courseend")
    try:
       for index in enrolled_courses:
		  edx_enrolled_courses.append(edxcourses.objects.get(courseid=index.courseid.courseid))
    except Exception as e:
           args['error_message'] = getErrorcontent("no_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

    input_list['courselist'] = edx_enrolled_courses
    input_list['cid']=args['edxcourseid']
    input_list['unenrollcurrentedxcourse']=unenrollcurrentedxcourse
    input_list['unenrollarchivedcourse']=unenrollarchivedcourse
    return render(request,enrolled_course_, input_list)




################ Display list of Teacher's of  particular course and institute from Courselevelusers based on session ##################.


@login_required(login_url='/')
def teacherlist(request,courseid):
        # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
        try:
             args =sessiondata(request)
             args.update(csrf(request))
        except Exception as e:
             print e.message
             return sessionlogin(request)
        
        teacherlist = []    
        sevenenddate=timezone.now()-timezone.timedelta(days=7)
             
        users = Courselevelusers.objects.filter(instituteid = args['institute'],roleid = 5).filter(courseid__courseid = courseid)
        for user in users:
                teacherlist.append(user)  
                args['coursename'] = user.courseid.coursename

        args['teacherlist'] = teacherlist
        args['courseid']=request.session['courseid'] = courseid
        request.session['edxcourseid']=edxcourses.objects.get(courseid=request.session['courseid']).id
        try:
            courseobj=edxcourses.objects.get(courseid=courseid)
            args['course']=courseobj.course
            if courseobj.courseend >=sevenenddate:
               args['currentflag']=1
            else:
                args['currentflag']=0
        except Exception as e:
           args['error_message'] = getErrorContent("course_not_present")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
        return render_to_response(teacherlist_,args, context_instance=RequestContext(request))



@login_required(login_url='/')
def courselist(request):
    #args = {}
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)   
    obj = Courselevelusers.objects.filter(personid_id = request.session['person_id'],courseid__courseid =args['courseid'],instituteid=args['institute'],roleid =args['role_id'])     
    args['courses'] = obj
    for i in obj:
        args['coursename'] = i.courseid.coursename        
    return render_to_response(coordinatorhome_,args,context_instance=RequestContext(request))

    

  
###############Display details of student of logged-in teacher for selected institute for selected course from Student Tables#############


@login_required(login_url='/')
def studentdetails(request,courseid,pid):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    faculty=request.session['faculty']
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       sevenenddate=timezone.now()+timezone.timedelta(days=7)
       if courseobj.courseend >=sevenenddate:
               args['currentflag']=1
       else:
                args['currentflag']=0
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
    except Exception as e:
           args['error_message'] = getErrorContent("no_course_entry")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['personid']=request.session['person_id']

    data=[]
    try:
        if int(pid)==-1:
            args['teachername']=""
            if args['role_id']==5:
                if args['currentflag']==1:
                     header=["S.No","Roll Number","Teacher","UserName","Email","Select","Unenroll"]
                else:
                     header=["S.No","Roll Number","Teacher","UserName","Email"]
            else:
                header=["S.No","Roll Number","Teacher","UserName","Email"]
            if faculty != 1:
               courselevelid=Courselevelusers.objects.filter(courseid__courseid=courseid,instituteid=args['institute'],roleid=5,startdate__lte=current,enddate__gte=current)
            
        else:
             if args['role_id']==5:
                
                if args['currentflag']==1:
                     header=["S.No","Roll Number","UserName","Email","Select","Unenroll"]
                else:
                     header=["S.No","Roll Number","UserName","Email"]
             else:
                header=["S.No","Roll Number","UserName","Email"]
             if faculty != 1:
                 courselevelid=Courselevelusers.objects.filter(personid__id=pid,courseid__courseid=courseid,instituteid=args['institute'],roleid=5,startdate__lte=current,enddate__gte=current)
                 args['teachername']= courselevelid[0].personid.firstname +" "+ courselevelid[0].personid.lastname
        if faculty != 1:
           for courseiter in courselevelid:
                teachername= courseiter.personid.firstname +" "+ courseiter.personid.lastname
                students = studentDetails.objects.filter(teacherid__id=courseiter.id,courseid=courseid,edxis_active=1)
                for student in students:   
                  try:
                     if int(pid)==-1:
          			    data.append([student.edxuserid.pk,student.roll_no,teachername,student.edxuserid.username,student.edxuserid.email])
                     else:
                         data.append([student.edxuserid.pk,student.roll_no,student.edxuserid.username,student.edxuserid.email])
                  except :
				         continue
        else:
                students = studentDetails.objects.filter(courseid=courseid,edxis_active=1)
                for student in students:   
                  try:
                        data.append([student.edxuserid.pk,student.roll_no,student.edxuserid.username,student.edxuserid.email])
                  except :
			continue

    except Exception as e:
           args['error_message'] = getErrorContent("not_valid_teacher")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    
                
    data.sort()
    try:
     args['faculty']=faculty
    except:
     pass
    args['header']=header  	
    args['info']=data
    args['id'] = pid
    return render_to_response(studentdetails_,args,RequestContext(request))



@login_required(login_url='/')
def downloadcsv(request,course,id):
    
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    faculty=request.session['faculty']
    if faculty == 1:
      course_id=edxcourses.objects.get(course=course).courseid

    name=args['person'].firstname+"_"+course+"  student_details"+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)     
     
    try:
        if int(id)==-1:
             writer.writerow(["RollNumber", "Teacher","UserName","Email"]) 
             courselevelid=Courselevelusers.objects.filter(courseid__courseid=course,instituteid=args['institute'],roleid=5,startdate__lte=current,enddate__gte=current)
        else:
             writer.writerow(["RollNumber", "UserName","Email"]) 
             if faculty !=1 :
                courselevelid=Courselevelusers.objects.filter(personid__id=id,instituteid=args['institute'],courseid__courseid=course,roleid=5,startdate__lte=current,enddate__gte=current)
    except Exception as e:
           args['error_message'] = getErrorContent("not_valid_teacher")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    if faculty !=1 :
      for clid in courselevelid:
        teachername= clid.personid.firstname +" "+ clid.personid.lastname
        students = studentDetails.objects.filter(teacherid__id=clid.id,courseid=course,edxis_active=1)  
        for student in students:   
		    try:
		       if int(id)==-1:
		            writer.writerow([student.roll_no,teachername,student.edxuserid.username,student.edxuserid.email])
		       else:
		             writer.writerow([student.roll_no,student.edxuserid.username,student.edxuserid.email])
		    except :
				     continue
    else:
        students = studentDetails.objects.filter(courseid=course_id,edxis_active=1)
        for student in students:   
		    try:
		       if int(id)==-1:
		            writer.writerow([student.roll_no,teachername,student.edxuserid.username,student.edxuserid.email])
		       else:
		             writer.writerow([student.roll_no,student.edxuserid.username,student.edxuserid.email])
		    except :
		       continue

    return response

#########################Update student data(roll number) on edit of student details in studentDetails table #############################



@login_required(login_url='/')
def Update(request,pid,courseid,t_id):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 

    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    try:
       args['course']=edxcourses.objects.get(courseid=courseid).course
       courselevel=Courselevelusers.objects.get(personid=Personinformation.objects.get(id=t_id),courseid=edxcourses.objects.get(courseid=courseid),instituteid=args['institute'])
    except Exception as e:
           args['error_message'] = getErrorContent("no_unique_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    if request.method == 'POST':        
        studentDetails.objects.filter(edxuserid__username = request.POST['username'],courseid=courseid,teacherid=courselevel,edxis_active=1).update(roll_no = request.POST['roll_no'])  
        try:      
           user = iitbx_auth_user.objects.get(edxuserid = pid)
        except Exception as e:
           args['error_message'] = getErrorContent("no_pid")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
              
        return HttpResponseRedirect(students_information+courseid+'/'+t_id)
    else:
        try:
           student = studentDetails.objects.get(edxuserid__edxuserid=pid,courseid=courseid,teacherid=courselevel,edxis_active=1)
        except Exception as e:
           args['error_message'] = getErrorContent("no_teacher")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
       
        args.update(csrf(request))
        args['info']=student
        args['courseid']=courseid
        args['pid']=pid
        args['t_id'] = t_id
        return render_to_response(updateinfo_,args)

     
##############Check that student data  uploaded  by teacher is present iitbx_auth_user table and store that data in student interface table with generating csv of valid and invalid students ################  


@login_required(login_url='/')
def upload(request,code,courseid):

   # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
   try:
             args =sessiondata(request)
             args.update(csrf(request))
   except Exception as e:
             print e.message
             return sessionlogin(request)
   try:      
     person=Personinformation.objects.get(email=args['email'])   
     args['coursename']=edxcourses.objects.get(courseid=courseid).courseid
   
     if request.POST:
        form = UploadForms(request.POST, request.FILES)
        teacher_id = request.session['person_id'] 
        fname=request.FILES['filename'].name        
        if form.is_valid():
           
            a = form.save()
            for p in uploadedfiles.objects.raw('SELECT * FROM SIP_uploadedfiles where uploadedby_id = 1 ORDER BY id DESC LIMIT 1 '):
                    changedfname = str(p.filename)
            args['fname']=fname
            uploadedfiles.objects.filter(filename = fname).update(uploadedby = teacher_id)
            extension = validate_file_extension(fname)
            if  extension:
                if code == "2":
                    
                    context = validatefileinfo(request,courseid,changedfname,teacher_id)
                    context.update(args)
                    
                    if context['error']=='':
                       return render(request, fileupload_, context)
                    else:
                        form = UploadForms()
                        args.update(csrf(request))
                        args['form'] = form
                        args['message'] = context['error']+ " in "+fname
                        return render_to_response(uploadfile_, args)
            else:
                message = getErrorContent("upload_csvfile")
                form = UploadForms()
                
                args.update(csrf(request))
    
                args['form'] = form
                args['message'] = message
                return render_to_response(uploadfile_, args)
           
     else:
        form = UploadForms() 
   except Exception as e:
           args['error_message'] = getErrorContent("upload_csv")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
           
     
   args['form'] = form
   args['courseid']=courseid
   return render_to_response(uploadfile_, args)

############ Create csv of valid and invalid reports if error_message is blank or not blank respectively in student_interface table  ############


@login_required(login_url='/')
def output_csv(request,code):
   
    for p in uploadedfiles.objects.raw('SELECT * FROM SIP_uploadedfiles ORDER BY id DESC LIMIT 1 '):
        fname = str(p.filename)    
    personid = request.session['person_id']   
    timestr = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    response = HttpResponse(content_type='text/csv')
    courseid=request.session['courseid']

    if(int(code)==1):
        downloadfile = "%s_%s_%s_%s" % ("report","valid",courseid,timestr)#1
        downloadfile=downloadfile+".csv"
        response['Content-Disposition'] = 'attachment; filename="%s"'%(downloadfile)        
        writer = csv.writer(response)
        csvdata = student_interface.objects.filter(status="Valid",fileid__filename = fname)  
        writer.writerow(["RollNo", "Username","Email"])
        for row in csvdata:
            writer.writerow([row.roll_no, row.username, row.email])

    elif(int(code)==2):
        downloadfile = "%s_%s_%s_%s" % ("report","ignore",courseid,timestr)#1
        downloadfile=downloadfile+".csv"
        response['Content-Disposition'] = 'attachment; filename="%s"'%(downloadfile)
        writer = csv.writer(response)
        csvdata = student_interface.objects.filter(Q(status="Ignore"),fileid__filename = fname)
 
        writer.writerow(["RollNo", "Username","Email"])
        for row in csvdata:
            writer.writerow([row.roll_no, row.username, row.email])
    elif(int(code)==3):
        downloadfile = "%s_%s_%s_%s" % ("report","invalid",courseid,timestr)#1
        downloadfile=downloadfile+".csv"
        response['Content-Disposition'] = 'attachment; filename="%s"'%(downloadfile)
        writer = csv.writer(response)
        csvdata = student_interface.objects.filter(Q(status="Error"),fileid__filename = fname)
 
        writer.writerow(["RollNo", "Username","Email","Message"])
        for row in csvdata:
            writer.writerow([row.roll_no, row.username, row.email,row.error_message])
    return response
           
            
############# Display homepage of logged-in teacher for selected institute contains list of courses and link of upload and student details ############  

@login_required(login_url='/')
def teacherhome(request,tid):
     
# args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    current_date=date.today()
    #args.update(csrf(request))
    faculty=0
    request.session['faculty']=faculty
    try:
      if int(tid)==-1:
           args['teachername']="All Teachers"
      else:
           person=Personinformation.objects.get(id=tid)
           args['teachername']=person.firstname+" "+person.lastname
    except Exception as e:
           args['error_message'] =  getErrorContent("session_not_active")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['pid']=tid
    
    a=[]
    #select courselevel object of the teacher who has login
    #person = Courselevelusers.objects.get(personid = request.session['person_id'],courseid=request.session['edxcourseid'],startdate__lte=current_date,enddate__gte=current_date,instituteid=request.session[)
    
    #select all the courses from edxcourses table
    try:
        course=edxcourses.objects.get(id=args['edxcourseid'])
        sevenenddate=course.courseend+timezone.timedelta(days=7)
        if sevenenddate>=timezone.now():
             previousflag=1
        else:
             previousflag=0
        #courseend + timezone.timedelta(365/12)) <=timezone.now()
    except Exception as e:
           args['error_message'] = getErrorContent("no_edxcourse_present")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    a.append(course)
    #Context = {'courses_list': a} #send the context to the html page to display the courses
    args['courses_list'] = a
    args['previousflag'] = previousflag
    return render_to_response(teacherhome_,args, context_instance=RequestContext(request))

############## unenroll student by updating teacher id to default teacherid =1 in studentDetails Teacher###############


@login_required(login_url='/')
def unenrollstudent(request,pid,courseid,t_id):
	# args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
	try:
             args =sessiondata(request)
             args.update(csrf(request))
        except Exception as e:
             print e.message
             return sessionlogin(request)
        
        try:
           edxcourses_obj=edxcourses.objects.get(courseid=courseid)
           #Org specific changes
           #personalinformation_obj=Personinformation.objects.get(id=1) 
           if (edxcourses_obj.org == "IITBombayX" or edxcourses_obj.org == "IITBombay"):
             default_email=iitbx_default
           else:
             default_email= iimbx_default
           personalinformation_obj=Personinformation.objects.get(email=default_email)
           #End of Org specfic changes   
           courselevelusers_obj=Courselevelusers.objects.get(personid=personalinformation_obj,courseid=edxcourses_obj).id 

        except Exception as e:
           args['error_message'] = getErrorContent("no_default_teacher"),courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
 
	studentDetails.objects.filter(edxuserid__edxuserid = pid).filter(courseid = courseid,edxis_active=1).update(teacherid =courselevelusers_obj )
	try:
	    user = iitbx_auth_user.objects.get(edxuserid = pid)
	except Exception as e:
           args['error_message'] = getErrorContent("stu_not_register")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

	return HttpResponseRedirect(students_information+courseid+"/"+t_id)



########change password on confirmation of old password  and after change password delete logged-in session , logout and redirect to login page for login with new passwords     ##########################



def change_pass(request):
   
    module = LOGIN_
    page = CHANGEPASS_
    args={}
    args.update(csrf(request))
    if request.method == 'POST':
       args={}
       try: 
		   
		   args.update(csrf(request))
		   args['old_password']=oldpwd=request.POST.get('old_password','')
		   user=User.objects.get(username=request.session['email_id'])
		   args['password1']=password1= request.POST.get('new_password1','')
		   args['password2']=password2= request.POST.get('new_password2','')
		   args['message']=[]
		   args = pwd_field_empty(request,args,'Password')
		   per_id=Personinformation.objects.get(email=request.session['email_id']).id
		   if args['message']:
			  return render_to_response(changepassword_,args)
		   else: 
		       
		         if user.check_password(oldpwd):
			         
				            
				        user.set_password(password1)
				        user.save()
                     
				        #args['message']= retrieve_error_message(module,page,'PWD_SET')
				        try:
				            ec_id = EmailContent.objects.get(systype='Login', name='success').id
				        except Exception as e:
				               args['error_message'] = getErrorContent("changepass_email")
				               args['error_message'] = "\n Error " + str(e.message) + str(type(e))
				               return render(request,error_,args)
				        send_email(request,ec_id, per_id, per_id)
                        
				        del request.session['person_id']
				        del request.session['email_id']
				        del request.session['institute_id']
				        request.session.flush()
				        cache.clear()
				        auth.logout(request)
		#return HttpResponseRedirect('/')
				        
				        #response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
				        #response.delete_cookie()
	
				        return render_to_response(changepasswordsuccess_,args)            
		         args['message']= retrieve_error_message(module,page,'OLD_NO_MTCH')
		         return render_to_response(changepassword_,args)
       except:
               
               args['error_message']= getErrorContent("not_logged_in")
               return render_to_response(login_,args)
    return  render_to_response(changepassword_,args)

####################################Admin Report ######################################################################################


#showing reports to blended mooc reports admin
@login_required(login_url='/')
def blendedadmin_home(request):
    args={}
    exclude=["19","9","10","11","12","4","5","16","17","15"]
    try:
       if request.session['usertype']==0 or 9 or 10:
         input_list={}
         request.session['faculty']=0
         input_list['usertype']=request.session['usertype'] 
       #Set session parameters
         try:
           
           person=Personinformation.objects.get(email=request.session['email_id'])
           request.session['institute_id']=person.instituteid_id
           institute=institute=T10KT_Institute.objects.get(instituteid=request.session['institute_id'])
           
           request.session['firstname']=person.firstname
           request.session['lastname']=person.lastname 
           request.session['role_id']=1
           
           request.session['rolename']=Lookup.objects.get(category="Role",code=1).comment
           print "after role"
           request.session['institutename']=institute.institutename
          
           try:
             #Start of org changes
             #request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
             request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=person.instituteid_id ).remotecenterid.remotecenterid
             print request.session['rcid']
             request.session['org']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=person.instituteid_id).remotecenterid.org
          
             print request.session['org']
             #End of org changes
           except:
             request.session['rcid']="   " 
             request.session['org']="None"
             print "none org"
         except:
             input_list['error_message'] = getErrorContent("no_person_info")
             return render(request,error_,input_list)
         if person.instituteid_id == 0:
            default_org="IITBombayX"
         else:
            default_org="IIMBx"
         report_name_list=[]
         report_list=Reports.objects.filter(usertype=0,org=default_org).order_by("category")   #fetching all reports from database whose usertype =0
         cat="";rlist=[];clist=[]
         for i in report_list:
             if i.reportid in exclude:
                 continue
             else:
                 if(i.category==cat):
                       clist.append([i.reportid,i.report_title,i.comments])
                 else:
                  rlist.append([cat,clist])
                  clist=[[i.reportid,i.report_title,i.comments]]
                  cat=i.category 
         
         rlist.pop(0) 
         rlist.append([cat,clist])
         
         input_list['report_list']=rlist        #names of all reports to be displayed 
         request.session['courseid']=""
         request.session['edxcourseid']=""
         
         input_list['rcid']=request.session['rcid']
     
         try:
             args =sessiondata(request)
             args.update(csrf(request))
         except Exception as e:
             print e.message
             return sessionlogin(request)
         input_list['temrem']=["19","9","10","11","12","4","5","16","17","15"]
         input_list.update(args)
         return render(request,admin_home_,input_list)
       else:
           args['error_message'] = "You do not have permission to view this page"
           return render(request,error_,args)
     
    except Exception as e:
             print e.message
             args['error_message'] = "You are not logged-in"
             return render(request,error_,args)



@login_required(login_url='/')
def blendedadmin(request,report_id):
 
        input_list={}
        flag=0
        errors=[]
        input_list['errors']=errors
        report_obj=Reports.objects.get(reportid=report_id)
        last_reportid=0
        input_list['report_name']=report_obj.report_title
        if not input_list['errors']:
            input_list['report_description']=report_obj.comments
            query=report_obj.sqlquery
            reports1=Userlogin.objects.raw(query)
            reportsout=Userlogin.objects.raw(query)
        reports=[]
          
        for id,row in enumerate(reportsout):
              record=[]
              if id== 0:
               record.append("S.No.")
              elif (id=='Total'):
               record.append("Total")
              else: 
               record.append(row.id)
              if 1<= report_obj.num_cols:
                 record.append(row.A)
              if 2<= report_obj.num_cols:
                 record.append(row.B)
              if 3<= report_obj.num_cols:
                 record.append(row.C)
              if 4<= report_obj.num_cols:
                 record.append(row.D)
              if 5<= report_obj.num_cols:
                 record.append(row.E)
              if 6<= report_obj.num_cols:
                 record.append(row.F)
              if 7<= report_obj.num_cols:
                 record.append(row.G)
              if 8<= report_obj.num_cols:
                 record.append(row.H)
              if 9<= report_obj.num_cols:
                 record.append(row.I)
              if 10<= report_obj.num_cols:
                 record.append(row.J)
              if 11<= report_obj.num_cols:
                 record.append(row.K)
              if 12<= report_obj.num_cols:
                 record.append(row.L)
              if 13<= report_obj.num_cols:
                 record.append(row.M)
              if 14<= report_obj.num_cols:
                 record.append(row.N)
              if 15<= report_obj.num_cols:
                 record.append(row.O)
              if 16<= report_obj.num_cols:
                 record.append(row.P)
              if 17<= report_obj.num_cols:
                 record.append(row.Q)
              if 18<= report_obj.num_cols:
                 record.append(row.R)
              if 19<= report_obj.num_cols:
                 record.append(row.S)
              if 20<= report_obj.num_cols:
                 record.append(row.T)
              if 21<= report_obj.num_cols:
                 record.append(row.U)
              if 22<= report_obj.num_cols:
                 record.append(row.V)
              if 23<= report_obj.num_cols:
                 record.append(row.W)
              if 24<= report_obj.num_cols:
                 record.append(row.X)
              if 25<= report_obj.num_cols:
                 record.append(row.Y)
              if 26<= report_obj.num_cols:
                 record.append(row.Z)   
              reports.append(record)   
        input_list['heading']=reports.pop(0)
        input_list['reports']=reports
        input_list['facultyflag']=request.session['faculty']

        return render(request,display_report_,input_list)


@login_required(login_url='/')
def instructoradmin(request,report_id,courseid,param_id=0):
 
        input_list={}
        lu_obj=Lookup.updatedate()
   
    
        input_list['refreshdate']=lu_obj
        flag=0
        errors=[]
        input_list['errors']=errors
        report_obj=Reports.objects.get(reportid=report_id)
        last_reportid=0
        input_list['report_name']=report_obj.report_title
        if report_obj.usertype==2:
             subreport=report_obj.reportid.split("_")[2]
             title=report_obj.report_title
             report_id=report_obj.reportid
             course=courseid
             
             #if(last_reportid!=report_obj.reportid):
               #reports.append([report_obj.report_title,report_obj.reportid])
             if subreport == "A" :
               query=report_obj.sqlquery %(course)
               flag=1
             elif subreport == "B" :
               query=report_obj.sqlquery %(course) 
               flag=2 
             elif subreport == "C" :
               query=report_obj.sqlquery %(course)
               flag=3  
             reportsout=Courselevelusers.objects.raw(query)

        elif report_obj.usertype==-2:
             subreport=report_obj.reportid.split("_")[2]
             title=report_obj.report_title
             report_id=report_obj.reportid
             course=courseid

             if subreport == "A" :
               query=report_obj.sqlquery %(course)

             elif subreport == "B" :
              
                query=report_obj.sqlquery %(course,param_id,param_id) 
              
             elif subreport == "C" :
              
                query=report_obj.sqlquery %(course,param_id)  
             reportsout=Courselevelusers.objects.raw(query)
             
            
        else:
            input_list['report_description']=report_obj.comments
            query=report_obj.sqlquery
            reports1=Userlogin.objects.raw(query)
            reportsout=Userlogin.objects.raw(query)

        reports=[]
          
        for id,row in enumerate(reportsout):
              record=[]
              if id== 0:
               
               record.append("S.No.")
              else: 
               record.append(int(row.id))
              if 1<= report_obj.num_cols:
                 record.append(row.A)
              if 2<= report_obj.num_cols:
                 record.append(row.B)
              if 3<= report_obj.num_cols:
                 record.append(row.C)
              if 4<= report_obj.num_cols:
                 record.append(row.D)
              if 5<= report_obj.num_cols:
                 record.append(row.E)
              if 6<= report_obj.num_cols:
                 record.append(row.F)
              if 7<= report_obj.num_cols:
                 record.append(row.G)
              if 8<= report_obj.num_cols:
                 record.append(row.H)
              if 9<= report_obj.num_cols:
                 record.append(row.I)
              if 10<= report_obj.num_cols:
                 record.append(row.J)
              if subreport == "C" and report_obj.usertype==2:
                   reports.append({"instituteid":row.A,"res":record}) 
              else:
                   reports.append(record) 
        if subreport == "C" and report_obj.usertype==2:
              dct=reports.pop(0)
              input_list['heading']=dct['res']               
        else:  
             input_list['heading']=reports.pop(0)
        input_list['reports']=reports
        input_list['reptype'] =subreport
        
        input_list['usertype']=report_obj.usertype
        input_list['course']=courseid
        input_list['flag']=flag
        return render(request,display_faculty_report_,input_list)

    
    

#################################### End Admin Report ####################################################################################

#################################### Start of grades Report ###########################################################################

@login_required(login_url='/')
def grades_report(request,courseid,pid,instituteidid):
    faculty=request.session['faculty']
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    try:
        course = edxcourses.objects.get(courseid = courseid).courseid
        args['course']=course
    except Exception as e:
        print "ERROR occured",str(e.message),str(type(e))  
        return [-1,-1]
    header=[] 
    ttheader=[]
    dwnldttheader=[]
    headerwithtt=[]
    try: 
       header=headings.objects.get(section=courseid).heading
       header_data=map(str,header.split(","))           
    except Exception as e:
       print "1 Header does not exists"
       #Error code#
       print "Header does not exists",str(e.message),str(type(e))
       args['error_message'] = "No Records"
       #return render(request,error_,args)

    try :
       ttheader=headings.objects.get(section="TT"+course).heading
       ttheader=",,,,"+ttheader
       dwnldttheader=map(str,ttheader.split(","))
       
       ttheader_data=map(str,ttheader.split(","))
       
       for i in range(0,len(header_data)):
            headerwithtt.append([header_data[i],ttheader_data[i]])
    except Exception as e:
       dwnldttheader=[]
       for i in range(0,len(header_data)):
            headerwithtt.append([header_data[i],""])
       print "TTHeader does not exists",str(e.message),str(type(e))
    try:
      if faculty != 1:
         if int(pid)==-1:
            courselevelid=Courselevelusers.objects.filter(courseid__courseid=courseid,instituteid=instituteidid,roleid=5,startdate__lte=current,enddate__gte=current)
           
         else:
           courselevelid=Courselevelusers.objects.filter(personid__id=pid,courseid__courseid=courseid,instituteid=instituteidid,roleid=5,startdate__lte=current,enddate__gte=current)        
           teacher=str(courselevelid[0].personid.firstname)+str(courselevelid[0].personid.lastname)
        #courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,instituteid=args['institute'])
         if int(pid) == -1:
           args['teacher']="All Teachers"
         else:
           person=Personinformation.objects.get(id=pid)
           args['teacher']= str(person.firstname)+' '+str(person.lastname)
          
    except Exception as e:
        print "Error occured",str(e.message),str(type(e))
    student_record=[]
    if faculty != 1:
      for clid in courselevelid:
        student_details=studentDetails.objects.filter(teacherid=clid,courseid=courseid,edxis_active=1).order_by('edxuserid__edxuserid')
        for student_detail in student_details:
           try:
              gradestable_obj=gradestable.objects.get(course=courseid,stud=student_detail)
           except Exception as e:               
              print "grade does not exist",str(e.message),str(type(e))             
              #return render(request,coursegrades_,args)
           marks=(gradestable_obj.eval).split(",")
           grade=gradestable_obj.grade
           if int(pid)==-1:
               student_record.append([str(gradestable_obj.stud.roll_no),str(gradestable_obj.stud.teacherid.personid.email), str(gradestable_obj.stud.edxuserid.username),str(gradestable_obj.stud.edxuserid.email),grade,marks])
           else:
                student_record.append([str(gradestable_obj.stud.roll_no), str(gradestable_obj.stud.edxuserid.username),str(gradestable_obj.stud.edxuserid.email),grade,marks])
    else:
       try:
        student_details=studentDetails.objects.filter(courseid=courseid,edxis_active=1)
        for student_detail in student_details:
           try:
              gradestable_obj=gradestable.objects.get(course=courseid,stud=student_detail)
           except Exception as e:
              print "grade does not exist",str(e.message),str(type(e))             
              return render(request,coursegrades_,args)
           marks=(gradestable_obj.eval).split(",")
           grade=gradestable_obj.grade
           student_record.append([str(gradestable_obj.stud.roll_no), str(gradestable_obj.stud.edxuserid.username),str(gradestable_obj.stud.edxuserid.email),grade,marks])
       except Exception as e:
         print "Error ocurred",str(e.message),str(type(e))
    #args['filename']='tmp/'+downloadheadercsv(request,courseid,pid,header_data,dwnldttheader)
    #full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    #command = "python "+full_path+"/manage.py collectstatic  --noinput"
   # subprocess.call(command, shell=True)
    t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
    args['selectedinstitute']=t10kt_obj.institutename
    headerfix=[header_data,dwnldttheader]
    request.session['grade_heading']= headerfix 
    args['headings']=header_data
    args['headerwithtt']=headerwithtt           
    request.session['student_record']= student_record         
    args['student_record']=student_record
    args['pid']=pid
    args['instituteidid']=instituteidid
    return render(request,coursegrades_,args)  



# end grades_report
#################################### End of grades Report ############################################################################

##################################### Beginning of download grade Report #############################################################

@login_required(login_url='/')
def downloadgradecsv(request,courseid,pid):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H%M")
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseobj.courseid
       args['pid']=pid
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['teacher']= str(args['firstname'])+' '+str(args['lastname'])
    header_data = request.session['grade_heading'] 
    header = [h.replace('<br>', '\n') for h in header_data[0]]
    result=request.session['student_record']
   
    name= str(courseobj.course)+"-Progress Report"+currenttime+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    
    
    if int(pid)==-1:
       ttheader=[""]+header_data[1]
       ttheader_data=ttheader
       count=0
       teacherheader=[]
       for i in header:
           count = count +1
           if count == 2:
              teacherheader.append("Teacher")
              teacherheader.append(i)
           else:
               teacherheader.append(i)
       writer.writerow(ttheader_data)
       writer.writerow(teacherheader)
       for j in result:
        count=0
        list1 =[]
        for data in j:            
            count = count +1
            if count==6:                
                for row in data:
                    list1.append(row)                
            else:                
                list1.append(data)
                
        writer.writerow(list1)  
    else:
      ttheader=header_data[1]
      ttheader_data=ttheader
      writer.writerow(ttheader_data)
      writer.writerow(header)
      for j in result:
        count=0
        list1 =[]
        for data in j:            
            count = count +1
            if count==5:                
                for row in data:
                    list1.append(row)                
            else:                
                list1.append(data)
                
        writer.writerow(list1)   
    return response
##################### End of download grade report ####################################################################################
@login_required(login_url='/')
def facultysessiondata(request):
    args = {}
    args.update(csrf(request))
    faculty=1
    request.session['faculty']=faculty
    lu_obj=Lookup.updatedate()
   
    #args['usertype']=int(request.session['usertype'])
    args['refreshdate']=lu_obj

    try:
        person=Personinformation.objects.get(email=request.session['email_id'])
        
        args['firstname']=request.session['firstname']
        args['lastname']=request.session['lastname']
        args['institutename']=request.session['institutename']
        args['rcid']=request.session['rcid']
        args['institute_id']=request.session['institute_id']
        args['email']= request.session['email_id']
        args['usertype']=int(request.session['usertype'])
        args['role_id']=int(request.session['role_id'])
        args['person']=person
    except Exception as e:
        print e.message
        args['error_message'] = getErrorContent("not_valid_user")
        args['error_message'] += "\n" + str(e.message)+ "," +str(type(e))
        return render(request,error_,args)
     
    return args    
@login_required(login_url='/')
def course_faculty(request):
    
    list_of_courses=[]
    faculty=1
    request.session['faculty']=faculty
    #lu_obj=Lookup.updatedate()
    
    
    #args['refreshdate']=lu_obj

    try:
        person=Personinformation.objects.get(email=request.session['email_id'])
        request.session['firstname']=person.firstname
        request.session['lastname']= person.lastname
        request.session['role_id']=1
        remote_center=T10KT_Remotecenter.objects.get(instituteid=person.instituteid)
        request.session['rcid']=remote_center.remotecenterid
        request.session['pid']=person.id

        institute=T10KT_Institute.objects.get(instituteid=person.instituteid_id)
        request.session['institutename']=institute.institutename
        request.session['institute_id']=institute.instituteid
        request.session['faculty']=faculty


    except Exception as e:
        args['error_message'] = getErrorContent("not_valid_user")
        args['error_message'] += "\n" + str(e.message)+ "," +str(type(e))
        return render(request,error_,args)
    args=facultysessiondata(request)
    args['manualtype']=3
    coursefaculty_obj=coursefaculty.objects.filter(person=person)
    no_of_courses=len(coursefaculty_obj)
    list_of_oldcourses=[]
    for course in coursefaculty_obj:
         if (course.course.courseend + timezone.timedelta(365/12)) <=timezone.now() and course.course.blended_mode==0:
             list_of_oldcourses.append([course.course.courseid,course.course.coursename,course.course.coursestart.date(),course.course.courseend.date()])
         else :
               list_of_courses.append([course.course.courseid,course.course.coursename,course.course.coursestart.date(),course.course.courseend.date()])
    if no_of_courses > 1: 
       list_of_courses.sort(key=operator.itemgetter(1),reverse=False)
       args['list_of_courses']=list_of_courses 
       args['list_of_oldcourses']=list_of_oldcourses 
       #args['email']= request.session['email_id']
       #args['firstname']=request.session['firstname']
       #args['lastname']=request.session['lastname']
       #args['institutename']=request.session['institutename']
       #args['rcid']=request.session['rcid']
       #args['institute_id']=request.session['institute_id']
       request.session['courselist_flag']=1
       
       return render(request,facultycourseparticipation_,args)
    elif no_of_courses == 1: 
       request.session['courselist_flag']=0
       return display_instructor_report(request,course.course.courseid)    
    else:
       args['error_message'] = getErrorContent("not_valid_faculty")
       return render(request,error_,args)
 
   
@login_required(login_url='/')
def display_instructor_report(request,course):
    check=0
    args=facultysessiondata(request)
    #lu_obj=Lookup.updatedate()
   
    args['manualtype']=3
    #args['refreshdate']=lu_obj
    #args['course']=course
    try:
       refresh=Lookup.objects.get(category='Refresh Status',code=1,description='On')
       print "refresh", refresh.comment
       args['refresh']=refresh.comment
    except:
       args['refresh']=''

    #request.session['course']=course
    course_obj=edxcourses.objects.get(courseid=course)  
    currentdate = datetime.now().date()
    sevenenddate=course_obj.courseend.date()+timezone.timedelta(days=7)
    if sevenenddate >= currentdate:
        check=1
    else:
        check=0  
    #args['email']=request.session['email_id']
    if (course_obj.blended_mode==1): 
      args['institute_id']=request.session['institute_id']
      report_list=Reports.objects.filter(usertype=2).order_by("reportid")
      record_list=[]
      record=[]
      row={}
      for report in report_list:
        if  report.reportid.endswith("A") :
        
         if len(record) > 0:
            row['record'] =record
            record_list.append(row)
            row={}
            record=[]
         row['name']=report.report_title
        record.append(report.reportid)
      if len(record) > 0:
       row['record']=record
       record_list.append(row)
       args['blended_mode']=1 
    else:
       record_list=[]
       args['blended_mode']=0 
    #args['firstname']=request.session['firstname']
   # args['lastname']=request.session['lastname']
    args['pid']=request.session['pid']
    #args['institute_id']=request.session['institute_id']

   # args['institutename']=request.session['institutename']
   # args['rcid']=request.session['rcid']
    args['courselist_flag']=request.session['courselist_flag']
    args['course']=course
    args['record']=record_list
    args['coursename']=course_obj.coursename 
    args['coursestart']=course_obj.coursestart.date()
    args['courseend']=course_obj.courseend.date()
    args['check']=check  
    args['org']=course_obj.org
    return render(request,coursefacultyreport_,args)

def display_instructor_intro(request,course):
    check=0
    args=facultysessiondata(request)
    #lu_obj=Lookup.updatedate()
   
    args['manualtype']=3
    #args['refreshdate']=lu_obj
    #args['course']=course
    try:
       refresh=Lookup.objects.get(category='Refresh Status',code=1,description='On')
       print "refresh", refresh.comment
       args['refresh']=refresh.comment
    except:
       args['refresh']=''

    #request.session['course']=course
    course_obj=edxcourses.objects.get(courseid=course)  
    currentdate = datetime.now().date()
    sevenenddate=course_obj.courseend.date()+timezone.timedelta(days=7)
    if sevenenddate >= currentdate:
        check=1
    else:
        check=0  
    #args['email']=request.session['email_id']
    if (course_obj.blended_mode==1): 
      args['institute_id']=request.session['institute_id']
      report_list=Reports.objects.filter(usertype=2).order_by("reportid")
      record_list=[]
      record=[]
      row={}
      for report in report_list:
        if  report.reportid.endswith("A") :
        
         if len(record) > 0:
            row['record'] =record
            record_list.append(row)
            row={}
            record=[]
         row['name']=report.report_title
        record.append(report.reportid)
      if len(record) > 0:
       row['record']=record
       record_list.append(row)
       args['blended_mode']=1 
    else:
       record_list=[]
       args['blended_mode']=0 
    #args['firstname']=request.session['firstname']
   # args['lastname']=request.session['lastname']
    args['pid']=request.session['pid']
    #args['institute_id']=request.session['institute_id']

   # args['institutename']=request.session['institutename']
   # args['rcid']=request.session['rcid']
    args['courselist_flag']=request.session['courselist_flag']
    args['course']=course
    args['record']=record_list
    args['coursename']=course_obj.coursename 
    args['coursestart']=course_obj.coursestart.date()
    args['courseend']=course_obj.courseend.date()
    args['check']=check   
    return render(request,"course_faculty_report_intro.html",args)
################################ Begin Teachers Student Report module  #################################################################
def approvedinstitute(request):
    args ={}
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    #apprinstitute=T10KT_Approvedinstitute.objects.all().exclude(remotecenterid__remotecenterid=0).order_by('remotecenterid__remotecenterid')
    apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
    approvinstitute=[]
    for i in apprinstitute:
         approvinstitute.append([i.remotecenterid.remotecenterid,i.id])  
    args['approvinstitute']=approvinstitute
    return render(request,listofinstitute_,args)  
################################ End Teachers Student Report module  #################################################################

def institutecourses(request):
    instituteid=request.GET['id']
    courseenroll=[]
    institute=T10KT_Approvedinstitute.objects.get(id=instituteid)
    institutename=institute.instituteid.institutename
    args ={}
    institutecourseenroll=courseenrollment.objects.filter(instituteid=institute).order_by("-courseid__courseend")
    for i in institutecourseenroll:
         courseenroll.append(i.courseid.courseid) 
    
    output=[institutename,courseenroll] 
    
    #data = serializers.serialize('json',institutecourseenroll)
   
    return HttpResponse(json.dumps(output), content_type="application/json")
    


def courseteachers(request):
    courseid=request.GET['cid']
    instituteid=request.GET['iid']
    args ={}
    teachers=[]
    selectapinrinfo=T10KT_Approvedinstitute.objects.get(id=instituteid)
    instituteid=selectapinrinfo.instituteid
    courseteacher=Courselevelusers.objects.filter(courseid=edxcourses.objects.get(courseid=courseid),instituteid=instituteid,roleid=5)
    for i in courseteacher:
        teachers.append(i.personid.email)   
    
    combineddata=[teachers,selectapinrinfo.remotecenterid.remotecenterid]
    
    #data = serializers.serialize('json',institutecourseenroll)
   
    return HttpResponse(json.dumps(combineddata), content_type="application/json")


@login_required(login_url='/')
def teacherstudent(request):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    if request.method == 'POST':
       try:
          institute=request.POST['Institute']
          course=request.POST['Course']
          teacher=request.POST['Teacher']
    
          
          #apprinstitute=T10KT_Approvedinstitute.objects.all().exclude(remotecenterid__remotecenterid=0).order_by('remotecenterid__remotecenterid')
          apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
          approvinstitute=[]
          args['course']=course
          for i in apprinstitute:
               approvinstitute.append([i.remotecenterid.remotecenterid,i.id])  
          args['approvinstitute']=approvinstitute
          approvinst_obj=T10KT_Approvedinstitute.objects.get(id=institute)
          args['instituteid']=approvinst_obj.remotecenterid.remotecenterid
    
    
    
         # args['courseenroll']=[course]
          #args['courseteacher']=[teacher]
    
          
          try:
     
                 instituteid=T10KT_Approvedinstitute.objects.get(id=institute).instituteid
                
                 args['apinstitutename']=instituteid.institutename
                 edxcourse_obj=edxcourses.objects.get(courseid=course)
                 if  teacher=="All Teachers":
                     student=[['S.NO','Rollno','Email Id','Username',"Teacher"]]
                     args['teacher']="All Teachers"
               
                     courselevel_obj=Courselevelusers.objects.filter(courseid=edxcourse_obj,instituteid=instituteid,roleid=5) 
                     jcount=0
                     for j in courselevel_obj:
                       
                       teacherstudent=studentDetails.objects.filter(courseid=edxcourse_obj.courseid,teacherid=j,edxis_active=1)
                       for i in teacherstudent:
                             jcount=jcount+1
                             student.append([jcount,i.roll_no,i.edxuserid.email,i.edxuserid.username,i.teacherid.personid.firstname+" "+i.teacherid.personid.lastname])
                 else:
                     student=[['S.No','Rollno','Email Id','Username']]
                     person=Personinformation.objects.get(email=teacher)
                     args['teacher']=person.firstname +" "+person.lastname
                     courselevel_obj=Courselevelusers.objects.filter(courseid=edxcourse_obj,personid=person,instituteid=instituteid,roleid=5)
                     jcount=0
                     for j in courselevel_obj:
                       
                       teacherstudent=studentDetails.objects.filter(courseid=edxcourse_obj.courseid,teacherid=j,edxis_active=1)
                       for i in teacherstudent:
                             jcount=jcount+1
                             student.append([jcount,i.roll_no,i.edxuserid.email,i.edxuserid.username])
              
          except Exception as e:
                 
                 args['error_message'] = getErrorContent("not_selected")+ "\n Error " + str(e.message) + str(type(e))
                 return render(request,error_,args)
    
    
         
    

          args['student']=student
          return render(request,listofinstitute_, args)
       except Exception as e:
           
           args['error_message'] = getErrorContent("select_all")+"\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    else:
         return approvedinstitute(request)
################################ End Teachers Student Report module   #########################################################

##################### Begin of evaluation module   ####################################################################################

@login_required(login_url='/')
def evaluation(request,courseid,pid,instituteidid,evalflag):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
       args['selectedinstitute']=t10kt_obj.institutename
       args['instituteidid']=instituteidid
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    if int(pid) == -1:
         args['teacher']="All Teachers"
    else:
       person=Personinformation.objects.get(id=pid)    
       args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    #try:
       # courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,startdate__lte=current,enddate__gte=current)
    #except Exception as e:
          # args['error_message'] = getErrorContent("teacher_not_valid"),courseid
          # args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           #return render(request,error_,args)
    #evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name','due_date').distinct().order_by('-due_date')
    evaluation_obj=evaluations.objects.raw('''SELECT a.id, a.sec_name "sec_name " ,a.sectionid "sectionid" ,release_date,due_date,type FROM `SIP_evaluations` a, `SIP_course_modlist` b
where a.course_id=b.course
and a.sectionid=b.module_id
and a.course_id=%s and a.release_date <= current_date()
order by b.order ASC
        ''',[courseobj.id])
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,evaluation_,args)



@login_required(login_url='/')
def quizdata(request,courseid,pid,instituteidid):
    faculty= request.session['faculty']
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    header=[]
    ques_dict={}
    stud_rec=[]
    try:
       secid=request.POST['quiz']

       evalu=evaluations.objects.filter(sectionid=secid,course__courseid=courseid).distinct()
       args['secname']=evalu[0].sec_name
       args['evalid']=evalu[0].id
    except Exception as e:
           return evaluation(request,courseid,pid,instituteidid,1)
    if faculty != 1:
      try: 
         t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
         args['selectedinstitute']=t10kt_obj.institutename
         if int(pid)==-1:
            courselevelid=Courselevelusers.objects.filter(courseid__courseid=courseid,roleid=5,instituteid=t10kt_obj,startdate__lte=current,enddate__gte=current)
         else:
           courselevelid=Courselevelusers.objects.filter(personid__id=pid,courseid__courseid=courseid,roleid=5,instituteid=t10kt_obj,startdate__lte=current,enddate__gte=current)
      except Exception as e:
           args['error_message'] ="You are not valid Teacher for the course ",courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['instituteidid']=instituteidid
       args['pid']=pid
       if int(pid) == -1:
          args['teacher']="All Teachers"
       else:
          person=Personinformation.objects.get(id=pid)
          args['teacher']= str(person.firstname)+' '+str(person.lastname)
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    
    try:
      head_str=headings.objects.get(section=secid).heading


      heading=map(str,head_str.split(","))
      print heading,"before "

    except Exception as e:
      print str(e.message),str(type(e))
      if not head_str:
         return render(request,quizdata_,args)
    
    #ques_dict={}
    #stud_rec=[]
    if faculty !=1:

      for clid in courselevelid:
    
        marks_obj=markstable.objects.filter(section=secid,stud__teacherid=clid,stud__edxis_active=1)  #.values_list(stud.roll_no,stud.edxuserid.email,stud.edxuserid.username,eval).order_by(stud.roll_no)
        for studvalue in marks_obj:
            marks=studvalue.eval.split(",")
            total=studvalue.total
            if int(pid) == -1:
               stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.teacherid.personid.email), str(studvalue.stud.edxuserid.username),str(studvalue.stud.edxuserid.email), total,marks]) 
            else:
               stud_rec.append([str(studvalue.stud.roll_no), str(studvalue.stud.edxuserid.username),str(studvalue.stud.edxuserid.email), total,marks]) 
    else:
      try:
        stud_obj=  studentDetails.objects.filter(courseid=courseid,edxis_active=1) 
        marks_obj=markstable.objects.filter(section=secid,stud=stud_obj) 
        for studvalue in marks_obj:
            marks=studvalue.eval.split(",")
            total=studvalue.total
            stud_rec.append([str(studvalue.stud.roll_no), str(studvalue.stud.edxuserid.username),str(studvalue.stud.edxuserid.email), total,marks])
      except Exception as e:
           print "Error Ocurred",str(e.message),str(type(e))

    request.session['evaluation_heading']= heading       
    request.session['heading']= heading           	 	
    args['headings']=heading              
    request.session['stud_rec']= stud_rec          
    args['stud_rec']=stud_rec
    return render(request,quizdata_,args)
  




@login_required(login_url='/')
def downloadquizcsv(request,courseid,pid,evalid):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=course=courseobj.course
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    try:
       evalu=evaluations.objects.filter(id=evalid)
       secname=evalu[0].sec_name
    except Exception as e:
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    if int(pid) == -1:
          args['teacher']="All Teachers"
    else:
          person=Personinformation.objects.get(id=pid)
          args['teacher']= str(person.firstname)+' '+str(person.lastname)
    
    result=request.session['stud_rec']
    
   # name=  "quizreport"+"_"+str(courseobj.id)+"_"+str(pid)+"_"+currenttime+'.csv'
    name=  str(course)+"_"+str(secname)+"_report_"+str(args['refreshdate'])+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    heading=request.session['evaluation_heading']
    heading = [h.replace('<br>', '\n') for h in heading]
    
    
    
    if int(pid) == -1:
       count=0
       teacherheader=[]
       for i in heading:
           count = count +1
           if count == 2:
              teacherheader.append("Teacher")
              teacherheader.append(i)
           else:
               teacherheader.append(i)
       writer.writerow(teacherheader)
       for data in result:
                count=0
                createrow=[]
                for row in data:
                    count=count+1
                    if count==6:
                       for r in row: 
                           
                           createrow.append(r)
                       
                    else:
                         createrow.append(row)
                writer.writerow(createrow)
    else:   
          writer.writerow(heading)
          for data in result:
                count=0
                createrow=[]
                for row in data:
                    count=count+1
                    if count==5:
                       for r in row: 
                           
                           createrow.append(r)
                       
                    else:
                         createrow.append(row)
                writer.writerow(createrow)
    return response



##################### End of evaluation module     ####################################################################################

#################### Begin of CourseDesciption module #################################################################################
@login_required(login_url='/')
def coursedescription(request,courseid,pid):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       if courseobj.id > 50:
          args['coursestart']=courseobj.coursestart
          args['courseend']=courseobj.courseend
          args['enrollstart']=courseobj.enrollstart
          args['enrollend']=courseobj.enrollend
       else:
          args['coursestart']=courseobj.coursestart.date()
          args['courseend']=courseobj.courseend.date()
          args['enrollstart']=courseobj.enrollstart.date()
          args['enrollend']=courseobj.enrollend.date()
    except Exception as e:
           print e.message

           args['error_message'] ="cannot get entry for course"
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    policy=[["Assignment","Total","Mandatory","Weight(%)","Comments"]]
    criteria=[["Grade","Min %","Max %"]]
    evaluate=[["Assignment","Assignment Type","Due Date"]]
    try:
        grpolicy=gradepolicy.objects.filter(courseid__courseid=courseid)
        for gp in grpolicy:
            if gp.drop_count==0:
                policy.append([gp.type+' ('+ gp.short_label +')',gp.min_count,gp.min_count-gp.drop_count,(gp.weight *100),""])
            else:
                 policy.append([gp.type+' ('+ gp.short_label +')',gp.min_count,gp.min_count-gp.drop_count,(gp.weight * 100),"Best of "+str((gp.min_count-gp.drop_count))])
        grcriteria=gradescriteria.objects.filter(courseid__courseid=courseid).values('cutoffs','grade').order_by('cutoffs').reverse().distinct()
        l=len(grcriteria)
        for  gc in range(0,len(grcriteria)):
             # print grcriteria,gc
              if gc==0:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs']*100,100])
              else:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs']*100,grcriteria[gc-1]['cutoffs']*100])
        #evaluat=evaluations.objects.filter(course__courseid=courseid).values('sectionid','sec_name','type','due_date').order_by('-due_date').distinct()
        evaluat=evaluations.objects.raw('''
        SELECT a.id, a.sec_name,release_date,due_date,type FROM `SIP_evaluations` a, `SIP_course_modlist` b
where a.course_id=b.course
and a.sectionid=b.module_id
and a.course_id=%s
order by b.order ASC
        ''',[courseobj.id])

        for eva in evaluat:
            evaluate.append([eva.sec_name,eva.type,eva.due_date])
        
    except Exception as e:
           print e
           args['error_message'] = getErrorContent("not_valid_teacher")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['evaluate']=evaluate
    args['criteria']=criteria
    args['policy']=policy
    args['id'] = pid
    return render_to_response(coursedescription_,args,RequestContext(request))



##################### End of CourseDesciption module  #################################################################################


##################### Begin admin CourseDesciption page ###############################################################################

@login_required(login_url='/')
def allcourses(request,courseflag):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    courseobj =edxcourses.objects.filter(blended_mode=1,org=args['org'],courseend__gte=datetime.now())
    args['courseobj']=courseobj
   
    if int(courseflag)==1:
        courseid=request.POST['courseid']
        if courseid !="Select":
            return coursedescription(request,courseid,0)
        else:
              args['error_message'] = getErrorContent("select_course")+"<br>"
              return render(request,'allcourses.html',args)
    
    
    return render(request,'allcourses.html',args)



##################### End admin CourseDesciption page ###############################################################################

##################### Begin of evaluation Status  module  ###########################################################################
@login_required(login_url='/')
def evalstatus(request,courseid,pid,instituteidid,evalflag):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['instituteidid']=instituteidid
       t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
       args['selectedinstitute']=t10kt_obj.institutename
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    if int(pid) == -1:
          args['teacher']="All Teachers"
    else:
          person=Personinformation.objects.get(id=pid)
          args['teacher']= str(person.firstname)+' '+str(person.lastname)  
  
    #evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name','due_date').distinct().order_by('-due_date')
    evaluation_obj=evaluations.objects.raw('''SELECT a.id, a.sec_name "sec_name " ,a.sectionid "sectionid" ,release_date,due_date,type FROM `SIP_evaluations` a, `SIP_course_modlist` b
where a.course_id=b.course
and a.sectionid=b.module_id
and a.course_id=%s and release_date <= current_date()
order by b.order ASC
        ''',[courseobj.id])
    if evalflag==1:
        args['error_message'] = "Please select any quiz"
    
    args['evaluation']=evaluation_obj
    return render(request,'evalstatus.html',args)



@login_required(login_url='/')
def studentstatus(request,courseid,pid,instituteidid,report):
    if request.POST:
           if request.POST['status']=="Select":
              return evalstatus(request,courseid,pid,instituteidid,1)
           request.session['secid']=request.POST['status']
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    header=[]

    try:
        t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
        args['selectedinstitute']=t10kt_obj.institutename
        if int(pid)==-1:
            heading=['Student RollNo','Teacher','Student Email']
            args['teacher']="All Teachers"
            courselevelid=Courselevelusers.objects.filter(courseid__courseid=courseid,instituteid=t10kt_obj,startdate__lte=current,enddate__gte=current,roleid=5)
            
        else:
           heading=['Student RollNo','Student Email']
           courselevelid=Courselevelusers.objects.filter(personid__id=pid,courseid__courseid=courseid,instituteid=t10kt_obj,startdate__lte=current,enddate__gte=current,roleid=5)
           person=Personinformation.objects.get(id=pid)
           args['teacher']= str(person.firstname)+' '+str(person.lastname)
    except Exception as e:
           args['error_message'] ="You are not valid Teacher for the course ",courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    try:
       secid=request.session['secid']
       marks_obj=[]
       for  clid in courselevelid:
            
            marks=markstable.objects.filter(section=secid,stud__teacherid=clid,stud__edxis_active=1)
            for i in marks:
               
                marks_obj.append(i)
      
    except Exception as e:
           return evalstatus(request,courseid,pid,1)
    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['instituteidid']=instituteidid
       args['pid']=pid
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)    
    evalobj=evaluations.objects.filter(sectionid=secid,course=courseobj)
    args['secname']=evalobj[0].sec_name
    args['evalid']=evalid=evalobj[0].id
    #args=probwiseattempt(request,args,marks_obj)
    ques_dict={}
    NA_stud_rec=[]; PA_stud_rec=[]; AA_stud_rec=[]
    NA_count=0; PA_count=0; AA_count=0
    
    for studvalue in marks_obj: 
           evallist=studvalue.eval.split(",")      
                
            #if studvalue.total=="0" ;
           if all(item == "NA" for item in evallist):      
                   NA_count=NA_count+1
                   if int(pid)==-1:
                       NA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.teacherid.personid.email),str(studvalue.stud.edxuserid.email)])
                   else:
                       NA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.edxuserid.email)])
           elif any(item == "NA" for item in evallist):             
                  PA_count=PA_count+1
                  if int(pid)==-1:
                      PA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.teacherid.personid.email),str(studvalue.stud.edxuserid.email)])
                  else:
                      PA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.edxuserid.email)])

           else:                  
                 AA_count=AA_count+1
                 if int(pid)==-1:
                     AA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.teacherid.personid.email),str(studvalue.stud.edxuserid.email)])
                 else:
                      AA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.edxuserid.email)])
    if NA_count>0 or AA_count>0:            
       args=probwiseattempt(request,args,marks_obj)
    args['NA_count']= NA_count; args['PA_count']= PA_count ; args['AA_count']= AA_count
    args['heading']= heading
    if int(report) == 0:
         return render(request,'studentstatus.html',args) 
    elif int(report) == 5:
          args['stud_rec']= NA_stud_rec          
    elif int(report) == 6:          
          args['stud_rec']= PA_stud_rec           
    else:
          args['stud_rec']= AA_stud_rec 
    if int(report) == 5 or int(report) == 6 or int(report) == 7:
          args['filename']='tmp/'+downloadstatucsv(request,courseid,pid,report,args['stud_rec'])    
          full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))        
          return render(request,'studentdetailattempt.html',args) 
    
    request.session['stud_rec']=args['stud_rec']    
    command = "python "+full_path+"/manage.py collectstatic  --noinput"
    subprocess.call(command, shell=True)
    return render(request,'studentstatus.html',args)



def probwiseattempt(request,args,marks_obj):
     
    eval_inst=evaluations.objects.get(id=args['evalid'])
    head_obj=headings.objects.get(section=eval_inst.sectionid)
    head_list=head_obj.heading.split(",")[4:]
    prob_heading=([s.split('<br>')[0] for s in head_list])
    if int(args['pid'])== -1:
          args['pid']==-1
       #mark_obj=markstable.objects.filter(section=eval_inst.sectionid,stud__edxis_active=1)
    else:
          person=Personinformation.objects.get(id=int(args['pid']))
          #mark_obj=markstable.objects.filter(section=eval_inst.sectionid,stud__teacherid__personid=person,stud__edxis_active=1)
    ques_obj=questions.objects.filter(eval=args['evalid'])
    
    problist=[]
    qlist=[]
    count=ques_obj.count()    
    marklist=[]
    qcount=0
    for i in ques_obj:#range(0,count):
        NAcount=0
        Acount=0
        for j in marks_obj:
            evalist=(j.eval).split(",")
            try:
               qval=evalist[qcount]
            except:
                   print "Duplicate Data in question table"
                   break
            if qval =="NA":
                NAcount=NAcount+1
            else:
                Acount=Acount+1
        problist.append([prob_heading[qcount],i.q_name,Acount,NAcount,qcount])
        qcount=qcount+1   
    args['secname']=eval_inst.sec_name
    args['problist']=problist   
         
    return args


@login_required(login_url='/')
def probdetail(request,courseid,instituteidid,evalid,qcount,teacherid,qattempt):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    try:
       courseobj = edxcourses.objects.get(courseid=courseid)
       t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
       args['selectedinstitute']=t10kt_obj.institutename
       args['coursename']=courseobj.coursename
       args['course']=courseobj.courseid
       args['courseid']=courseid
       args['instituteidid']=instituteidid
       args['pid']=teacherid
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           return render(request,error_,args)    
    eval_inst=evaluations.objects.get(id=evalid)
    if int(teacherid)== -1:
       mark_obj=markstable.objects.filter(section=eval_inst.sectionid,stud__teacherid__courseid__courseid=courseid,stud__teacherid__roleid=5,stud__teacherid__instituteid=t10kt_obj,stud__edxis_active=1)
       args['teacher']= "All Teachers"
    else:
          person=Personinformation.objects.get(id=int(teacherid))
          mark_obj=markstable.objects.filter(section=eval_inst.sectionid,stud__teacherid__courseid__courseid=courseid,stud__teacherid__roleid=5,stud__teacherid__personid=person,stud__teacherid__instituteid=t10kt_obj,stud__edxis_active=1)
          args['teacher']= str(person.firstname)+' '+str(person.lastname) 
    ques_obj=questions.objects.filter(eval=evalid)[int(qcount)]
    args['qname']=ques_obj.q_name 
    
    probuserdetail=[]
    
    for j in mark_obj:
            evalist=(j.eval).split(",")
      
            qval=evalist[int(qcount)]
            if qattempt =="0" and qval=="NA":
                probuserdetail.append([str(j.stud.roll_no),str(j.stud.edxuserid.email),str(j.stud.edxuserid.username)])
            elif qattempt =="1" and qval !="NA":
                probuserdetail.append([str(j.stud.roll_no),str(j.stud.edxuserid.email),str(j.stud.edxuserid.username)])
            else:
                print "Error"
                continue
    args['qattempt']=qattempt        
    args['secname']=eval_inst.sec_name
    args['probuserdetail']=probuserdetail       
    return render(request,'qwisedetail.html',args) 


@login_required(login_url='/')
def downloadstatucsv(request,courseid,pid,report,stud_rec):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    args['teacher']= str(args['firstname'])+' '+str(args['lastname'])
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    
    if int(report) == 5:
       realname= "student_notattempted_"+str(courseobj.id)+"_"+str(pid)+'.csv'
       
    elif int(report) == 6:
       realname= "student_attemptsomeques_"+str(courseobj.id)+"_"+str(pid)+'.csv'
    else:
       realname= "student_attemptall_"+str(courseobj.id)+"_"+str(pid)+'.csv'
    name=os.path.join(full_path,'static/tmp/',realname)
    with open(name,"wb") as downloadfile:
         writer=csv.writer(downloadfile,delimiter=',')
         if int(pid)==-1:
            heading=['Student RollNo','Teacher','Student Email']
         else:
              heading=['Student RollNo','Student Email']
         writer.writerow(heading)
         for row in  stud_rec:
             writer.writerow(row)
    
    return realname


##################### End of evaluation Status module    ####################################################################


##################### Begin of admin upload  module  #############################################################################


@login_required(login_url='/')
def teacherstudentlist(request,institute,course,teacher):
          try:
             args =sessiondata(request)
             args.update(csrf(request))
          except Exception as e:
             print e.message  
             return sessionlogin(request)     
          apprinstitute=T10KT_Approvedinstitute.objects.all().exclude(remotecenterid__remotecenterid=0).order_by('remotecenterid__remotecenterid')
          approvinstitute=[]
          args['course']=course
          for i in apprinstitute:
               approvinstitute.append([i.remotecenterid.remotecenterid,i.id])  
          args['approvinstitute']=approvinstitute
          approvinst_obj=T10KT_Approvedinstitute.objects.get(id=institute)
          args['instituteid']=approvinst_obj.remotecenterid.remotecenterid
 
          try:
     
                 instituteid=T10KT_Approvedinstitute.objects.get(id=institute).instituteid                
                 args['apinstitutename']=instituteid.institutename
                 edxcourse_obj=edxcourses.objects.get(courseid=course)
                 if  teacher=="All Teachers":
                     student=[['Rollno','Email Id','Username',"Teacher"]]
                     args['teacher']="All Teachers"
               
                     courselevel_obj=Courselevelusers.objects.filter(courseid=edxcourse_obj,instituteid=instituteid) 
                     for j in courselevel_obj:
                       
                       teacherstudent=studentDetails.objects.filter(courseid=edxcourse_obj.courseid,teacherid=j,edxis_active=1)
                       for i in teacherstudent:
                             student.append([i.roll_no,i.edxuserid.email,i.edxuserid.username,i.teacherid.personid.firstname+" "+i.teacherid.personid.lastname])
                 else:
                     student=[['Rollno','Email Id','Username']]
                     person=Personinformation.objects.get(email=teacher)
                     args['teacher']=person.firstname +" "+person.lastname
                     courselevel_obj=Courselevelusers.objects.filter(courseid=edxcourse_obj,personid=person,instituteid=instituteid)
                     for j in courselevel_obj:
                       
                       teacherstudent=studentDetails.objects.filter(courseid=edxcourse_obj.courseid,teacherid=j,edxis_active=1)
                       for i in teacherstudent:
                             student.append([i.roll_no,i.edxuserid.email,i.edxuserid.username])
              
          except Exception as e:
                 
                 args['error_message'] = getErrorContent("not_selected")+ "\n Error " + str(e.message) + str(type(e))
                 return render(request,error_,args)    

          args['student']=student
          
          return render(request,"studentlist.html", args)




@login_required(login_url='/')
def adminuploaderinfo(request):
   args={}
   try:
       if request.session['usertype']==0 or 10:
              try:
                   args =sessiondata(request)
                   args.update(csrf(request))
              except Exception as e:
                  print e.message  
                  return sessionlogin(request) 
       else:
           args['error_message'] = "You do not have permission to view this page"
           return render(request,error_,args)
     
   except:
             args['error_message'] = "You are not logged-in"
             return render(request,error_,args)
   #apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
   apprinstitute=T10KT_Approvedinstitute.objects.filter(remotecenterid__in=T10KT_Remotecenter.objects.filter(org=args['org'])).order_by('remotecenterid__remotecenterid')
   approvinstitute=[]
   for i in apprinstitute:
       approvinstitute.append([i.remotecenterid.remotecenterid,i.id])  
   args['approvinstitute']=approvinstitute
   if request.POST: 
       #rcid=request.POST['rcid']
       teacher=request.POST['Teacher']
       course=request.POST['Course']
             
       rcidid=request.POST['Institute']
       if teacher == "noteacher":
          args['error_message'] = "Please select Teacher"
          return render(request,"uploaderinfo.html",args)
       elif course == "nocourse":
          args['error_message'] = "Please select Course"
          return render(request,"uploaderinfo.html",args)
       
       elif rcidid == "noinstitute":
          args['error_message'] = "Please select RCID"
          return render(request,"uploaderinfo.html",args)
       else:
            
            
           try:     
                   courseid=edxcourses.objects.get(courseid=course)
                   sevenenddate=timezone.now()-timezone.timedelta(days=7)
                   apinstituteid=T10KT_Approvedinstitute.objects.get(id=rcidid)
                   instituteid=apinstituteid.instituteid  
                   args['institute']=apinstituteid.instituteid     
                   if teacher == "All Teachers":
                      persid=-1
                      couselevel=Courselevelusers.objects.filter(courseid=courseid,instituteid=instituteid)
                   else:
                      person=Personinformation.objects.get(email=teacher)
                      args['teacher']=person.id
                      persid=person.id
                      couselevel=Courselevelusers.objects.filter(personid=person,courseid=courseid,instituteid=instituteid)
                           
           except:
                      args['error_message'] = "Enter valid Uploader Info"
                      return render(request,"uploaderinfo.html",args)
       
       if couselevel.exists():
              if "studentupload" in request.POST:
                  if teacher == "All Teachers":
                     args['error_message'] = "Not valid  for all teacher option"
                     return render(request,error_,args)  
                  
                  if courseid.courseend < sevenenddate:
                         args['error_message'] = "This functionalty is not for archived courses. Please select current course."
                         return render(request,"uploaderinfo.html",args) 
                  args['uploaderrcid']=apinstituteid.remotecenterid.remotecenterid
                  args['courseid']=courseid.courseid
                  form = UploadForms() 
                  args['form'] = form
                  return render_to_response('adminupload.html', args)
              elif "teacherstudent" in request.POST:
                 return teacherstudentlist(request,rcidid,courseid.courseid,teacher)
              elif "evaluation" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     if courseid.courseend < sevenenddate:
                         args['error_message'] = "This functionalty is not for archived courses. Please select current course."
                         return render(request,"uploaderinfo.html",args) 
                     return evaluation(request,courseid.courseid,persid,instituteid.instituteid,0)
              elif "evaluationstatus" in request.POST:
                     if courseid.courseend < sevenenddate:
                         args['error_message'] = "This functionalty is not for archived courses. Please select current course."
                         return render(request,"uploaderinfo.html",args) 
                     return evalstatus(request,courseid.courseid,persid,instituteid.instituteid,0)
              elif "grade" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     return grades_report(request,courseid.courseid,persid,instituteid.instituteid)
              elif "deactivate" in request.POST:
                     return teacherdeactivation(request,courseid.courseid,persid,instituteid.instituteid)
              elif "bulkmove" in request.POST:
                     if teacher == "All Teachers":
                        args['error_message'] = "Not valid  for all teacher option.Please select one teacher"
                        return render(request,error_,args)  
                     else:
                           return bulkmove(request,courseid.courseid,persid,instituteid.instituteid)
       else:
                    args['error_message']= "Person is not teacher for " +str(courseid.courseid)+" course for given RCID"
   
    
   else:
        return render(request,"uploaderinfo.html",args)


@login_required(login_url='/')
def adminupload(request,code,courseid,teacher,rcid):
     # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
   try:
             args =sessiondata(request)
             args.update(csrf(request))
   except Exception as e:
             print e.message  
             return sessionlogin(request) 
   args['courseid']=courseid
   args['uploaderrcid']=rcid
   args['teacher']=teacher
   try:      
     person=teacher 
     args['coursename']=edxcourses.objects.get(courseid=courseid).course
   
     if request.POST:
        form = UploadForms(request.POST, request.FILES)
        teacher_id = teacher
        fname=request.FILES['filename'].name        
        if form.is_valid():
           
            a = form.save()
            for p in uploadedfiles.objects.raw('SELECT * FROM SIP_uploadedfiles where uploadedby_id = 1 ORDER BY id DESC LIMIT 1 '):
                    changedfname = str(p.filename)
            args['fname']=fname
            uploadedfiles.objects.filter(filename = fname).update(uploadedby = teacher_id)
            extension = validate_file_extension(fname)
            if(extension):
                if code == "2":
                    context = validatefileinfo(request,courseid,changedfname,teacher_id)
                    if context['error']=='':
                       return render(request, fileupload_, context)
                    else:
                        form = UploadForms()
                        args.update(csrf(request))
                        args['form'] = form
                        args['message'] = context['error']+ " in "+fname
                        return render_to_response('adminupload.html', args)
            else:
                message = getErrorContent("upload_csvfile")
                form = UploadForms()
                #args = {}
                args.update(csrf(request))
    
                args['form'] = form
                args['message'] = message
                return render_to_response('adminupload.html', args)
           
     else:
        form = UploadForms() 
   except Exception as e:
           args['error_message'] = getErrorContent("upload_csv")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
             
   args['form'] = form
   
   return render_to_response('adminupload.html', args)


##################### End of admin upload  module  #############################################################################


##################### Begin of Error handler pages module  #############################################################################
def bmwcustom404(request):
                    args={"email":"bmwsoftwareteam@cse.iitb.ac.in"}
                    response= render_to_response('statictemplates/404.html',args)
                    response.status_code = 404
                    return response

def bmwcustom500(request):
                    response= render_to_response('statictemplates/500.html')
                    response.status_code = 500
                    return response

def bmwcustom403(request):
                    response= render_to_response('statictemplates/403.html')
                    response.status_code = 403
                    return response

##################### End of Error handler pages module  #############################################################################

######################## Begin of Teacher Deactivation module ########################################################################



@login_required(login_url='/')
def teacherdeactivation(request,courseid,pid,instituteidid):
     try:
             args =sessiondata(request)
             args.update(csrf(request))
     except Exception as e:
             print e.message  
             return sessionlogin(request) 
     
     try:
        courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,instituteid=instituteidid,roleid=5,startdate__lte=current,enddate__gte=current)
        courselevelid.roleid = int(-5)
        courselevelid.save()
        courselevelid=Courselevelusers.objects.filter(roleid=-5,startdate__lte=current,enddate__gte=current)
        args['inactteachers']=courselevelid
        return  render(request,"inactiveteacher.html",args)
        
     except Exception as e:
           args['error_message'] = "Not valid for All Teacher"
           return render(request,error_,args)
            


########################  End of Teacher Deactivation module ########################################################################


######################## Begin of admin registrationinterface ########################################################################
######################## Begin of admin registrationinterface ########################################################################

@login_required(login_url='/')
def registrationinterface(request,args={},role=0,redirectflag=0):
    
    try:
       try:
             args.update(sessiondata(request))
       except Exception as e:
             print e.message  
             return sessionlogin(request) 
       if redirectflag==0:
           args['error_message']=""
       if (request.session['usertype']==0 or 10) or (request.session['usertype']==1 and (role=="3" or role=="2") ) :
            approvinstitute=[]
            designationlist=[]
            qualificationlist=[]
            departmentlist=[]
            genderlist=[]
            rolelist=[]
            try:
               person=Personinformation.objects.get(email=args['email'])
               args['institute']=institute=args['institute']
               args['person']=person
            except Exception as e:
               args['error_message'] = getErrorContent("unique_person")
               args['error_message'] = "\n Error " + str(e.message) + str(type(e))
               return render(request,error_,args)
    
            args['institutename']=institute.institutename
            args['firstname']=person.firstname
            args['lastname']=person.lastname
            #args['email']=request.session['email_id']
            
            if role =="3" or  role=="2":
               if (args['role_id']==3 and role =="3") or (args['role_id']==2 and role=="2"): 
                 args['role']=role 
                 apprinstitute=T10KT_Approvedinstitute.objects.get(instituteid=args['institute'])
                 approvinstitute.append([apprinstitute.remotecenterid.remotecenterid,apprinstitute.instituteid.instituteid])
                 args['approvinstitute']=approvinstitute
                 lrole=Lookup.objects.filter(category = 'Role',code=5)
    
                 for i in lrole:
                     rolelist.append([i.code,i.comment])  
                 args['rolelist']=rolelist 
                 if args['courseid']:
                     sevenenddate=timezone.now()-timezone.timedelta(days=7)
                     courselist=edxcourses.objects.filter(blended_mode=1,courseid=args['courseid'])
                     if courselist[0].courseend >= sevenenddate:
                         args['courselist']=courselist
                     else:
                          args['error_message'] = "You have selected archived sourse .Please select some current course"
                          return render(request,error_,args)
                 else:
                      args['error_message'] = "Please select some course"
                      return render(request,error_,args)
                 
                    
               else:
                  args['error_message'] = "You do not have permission to view this page"
                  return render(request,error_,args)

            elif role=="0":
                # Added Org filter
                #apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
                apprinstitute=T10KT_Approvedinstitute.objects.filter(remotecenterid__in=T10KT_Remotecenter.objects.filter(org=args['org'])).order_by('remotecenterid__remotecenterid')
                for i in apprinstitute:
                     approvinstitute.append([i.remotecenterid.remotecenterid,i.instituteid.instituteid])  
                args['approvinstitute']=approvinstitute
                role=Lookup.objects.filter(category = 'Role',code__gte=2).exclude(code=4)
    
                for i in role:
                   rolelist.append([i.code,i.comment])  
                args['rolelist']=rolelist
                courselist=edxcourses.objects.filter(blended_mode=1,courseend__gte=datetime.now(),org=args['org'])
                args['courselist']=courselist
                args['role']=0
            else:
                  args['error_message'] = "You  have access wrong page"
                  return render(request,error_,args)
            designation=Lookup.objects.filter(category = 'Designation')
    
            for i in designation:
               designationlist.append([i.code,i.description])  
            args['designationlist']=designationlist
            
            qualification=Lookup.objects.filter(category = 'Qualification')
            
            for i in qualification:
               qualificationlist.append([i.code,i.description])  
            args['qualificationlist']=qualificationlist

            department=Lookup.objects.filter(category = 'Stream')
            
            for i in department:
               departmentlist.append([i.code,i.description])  
            args['departmentlist']=departmentlist
         
            genderlist=[["Female","Female"],["Male","Male"],["Others","Others"]]  
            args['genderlist']=genderlist
    
            return  render(request,"adminregister.html",args)
            
       else:
           args['error_message'] = "You do not have permission to view this page"
           return render(request,error_,args)
     
    except:
             args['error_message'] = "You are not logged-in or not selected role"
             return render(request,error_,args)



@login_required(login_url='/')
def register(request,role=0): 
   try:
      args=validateinterfacedata(request,role)
      if args['success_message']:
         return render(request,"registrationsuccessfull.html",args)
      if args['error_message']:
        return registrationinterface(request,args,role,1) 
      else:
           roleobj=Lookup.objects.get(category = 'Role',code=args['roleval'])
           args['roleobj']=roleobj
           # if else to check role appled by user.if courselevel else institutelevel        
           if int(args['roleval'])==5:# check and create courselevel
               cl_obj=Courselevelusers.objects.filter(personid=args['regperson'],courseid=args['course'],instituteid__instituteid=args['rcidval'],roleid=args['roleval'])
               if cl_obj.exists():#if exist prompt message
                   args['error_message']="Person is an existing teacher for "+str(args['course'].course) +" course."
                   return registrationinterface(request,args,role,1)
               else:#else create courseleveluser
                    return existperscourselevel(request,args,role)               
           else:#check and create institutelevel
                 il_obj=Institutelevelusers.objects.filter(instituteid__instituteid=args['rcidval'],roleid=args['roleval'])
                 if il_obj.exists():#if exist prompt message
                     #check if person is same with tat exist or not
                     
                     if il_obj[0].personid.email==args['regperson'].email:
                         args['error_message']="Person is an existing "+str(roleobj.comment)+ " for "+str(args['instinstance'].institutename)+"."
                     else:
                         args['error_message']=" Another  person is an existing "+str(roleobj.comment)+ " for "+str(args['instinstance'].institutename)+"."
                     return registrationinterface(request,args,role,1)
                 else:#else and create institutelevel
                     return existpersInstitutelevel(request,args,role) 
                          
        
   except:
           args={}
           return registrationinterface(request,args,role,1)


def existperscourselevel(request,args,pagerole):
               
                   Courselevelentry= Courselevelusers(personid=args['regperson'], courseid=args['course'], instituteid=args['instinstance'],roleid=args['roleval'],startdate= datetime.now(),enddate=default_end_date)
                   Courselevelentry.save()
                   successmessage = "Person is registered as teacher for  " +str(args['course'].courseid) +" for "+str(args['instinstance'].institutename)+"."                  
                   
                   args['success_message']=successmessage
                   ec_id = EmailContent.objects.get(systype = 'Registration', name = 'home').id
                   mail_obj = EmailContent.objects.get(id=ec_id)
                   subject=mail_obj.subject %(args['course'].courseid)
                 
                   message = mail_obj.message %(args['regperson'].firstname, args['instinstance'].institutename,args['course'].courseid,args['course'].courseid)  
                   send_mail(subject, message , DEFAULT_FROM_EMAIL ,[args['memailval']], fail_silently=False)


                   return render(request,"registrationsuccessfull.html",args)


def existpersInstitutelevel(request,args,pagerole):
                 
                          Institutelevel=Institutelevelusers(personid=args['regperson'], instituteid=args['instinstance'],roleid=args['roleval'],startdate= datetime.now(),enddate=default_end_date)
                          Institutelevel.save()
                          message = "Person is registered  as   "+str(args['roleobj'].comment)+"for"+str(args['instinstance'].institutename)+"."
                          subject="Registered successful for MIS"
                          send_mail(subject, message , DEFAULT_FROM_EMAIL ,[args['memailval']], fail_silently=False)
                          args['success_message']=message
                          return render(request,"registrationsuccessfull.html",args)       


def createnewuser(request,args,pagerole):
              if args['roleval']==3 or args['roleval']==2 :
                   if Institutelevelusers.objects.filter(instituteid__instituteid=args['rcidval'],roleid=args['roleval']).exists():
                         args['error_message']="Another Head or Pc already exist for given "+str(args['instinstance'].institutename)+"."
                         return args
                         
              instinstance=T10KT_Institute.objects.get(instituteid=args['rcidval'])
              authentry=User.objects.create_user(username=args['memailval'],email=args['memailval'],password="Welcome123")
              authentry.is_active=True  
              authentry.save()   
              userprofile=Userlogin(user=authentry,status=0)
              userprofile.save()
              
              person_obj=Personinformation(email=args['memailval'],firstname = args['mfirstname'],instituteid=instinstance,lastname =args['mlastname'],designation=args['designationval'],createdondate=datetime.now(),telephone1=args['mcontactno'],streamid=args['department'],gender=args['gender'],qualification=args['qualification'])
              person_obj.save() 
              
              if args['roleval']==5:
                                  
                 Courselevelentry= Courselevelusers(personid=person_obj, courseid=args['course'], instituteid=instinstance,roleid=args['roleval'],startdate= datetime.now(),enddate=default_end_date)
                 Courselevelentry.save()  
                 args['success_message']="User account  is successfully created as Teacher for "+str(instinstance.institutename)+"."             
                 
              
              else:
                   
                        Institute_level=Institutelevel=Institutelevelusers(personid=person_obj, instituteid=instinstance,roleid=args['roleval'],startdate= datetime.now(),enddate=default_end_date)
                        Institute_level.save() 
                        if args['roleval']==3:
                           args['success_message']="User account  is successfully created as Program Coordinator for "+str(instinstance.institutename)+"."
                        else:
                             args['success_message']="User account  is successfully created as Head for "+str(instinstance.institutename)+"."
                
              fname = person_obj.firstname
              email = person_obj.email
              per_id=signer.sign(person_obj.id)
              ecpass_id = EmailContent.objects.get(systype = 'Login', name = 'createpassword').id
              mailpass_obj = EmailContent.objects.get(id=ecpass_id)
              link = ROOT_URL + mailpass_obj.name + '/%s' %per_id
              message = mailpass_obj.message %(fname, link)  
              send_mail(mailpass_obj.subject, message , DEFAULT_FROM_EMAIL ,[email], fail_silently=False)
              
              if args['roleval']==5:
                 ec_id = EmailContent.objects.get(systype = 'Registration', name = 'home').id
                 mail_obj = EmailContent.objects.get(id=ec_id)
                 subject=mail_obj.subject %(args['course'].courseid)
                 
                 message = mail_obj.message %(fname, instinstance.institutename,args['course'].courseid,args['course'].courseid)  
                 send_mail(subject, message , DEFAULT_FROM_EMAIL ,[email], fail_silently=False)
              return args



def validateinterfacedata(request,pagerole):
    args={}
    args['mfirstname']=firstname=request.POST['firstname']
    args['mlastname']=lastname=request.POST['lastname']
    args['memailval']=emailval=request.POST['email'].replace(" ","")
    args['rcidval']=instituteid=int(request.POST['Institute'])
    args['designationval']=designationval=int(request.POST['designation'])
    args['roleval']=roleval=int(request.POST['role'])
    args['pagerole']=pagerole
    args['courseval']=courseval=int(request.POST['course'])
    args['gender']=gender=request.POST['gender']
    args['qualification']=qualification=int(request.POST['qualification'])
    args['department']=department=int(request.POST['department'])
    args['mcontactno']=contactno=request.POST['contactno']
    emailvalidate=validateEmail(emailval)
    fname=validateFname(firstname)
    lname=validateLname(lastname)
    personexist=ifblendedPersonExists(emailval,instituteid)
    contact=validateContact(contactno)
    
    args['personexist']=personexist
    
    args['error_message']=""
    args['success_message']=""
    if not emailval:
       args['error_message']="Enter valid Email."
    if emailvalidate == 0:
       args['error_message']="Enter valid Email."
       
    if fname==0:
       args['error_message']+="</br>Enter valid firstname."
    if lname==0:
       args['error_message'] +="</br>Enter valid lastname."
    if personexist==-1:
       args['error_message'] +="</br>Person belongs to different institute."
    if personexist==-2:
       args['error_message'] +="</br>Mutliple entries of person. Contact technical team with email and institutename."
    if instituteid==-1:
       args['error_message'] +="</br>Please select a Institute."
    if designationval==-1:
       args['error_message'] +="</br>Please select Designation."
    if roleval==-1:
       args['error_message'] +="</br>Please select Role."
    if gender==-1:
       args['error_message'] +="</br>Please select Gender."
    if qualification==-1:
       args['error_message'] +="</br>Please select Qualifications."
    if department==-1:
       args['error_message'] +="</br>Please select Department"
    if contact==0:
       args['error_message']+="</br>Enter valid Phone(Mobile should be 10 digit or Landline of 11 digit - include STD code)."
    

    if roleval==5:
             if courseval==-1:
                  args['error_message'] +="</br>Please select Course."
             elif courseval==-2:
                  args['error_message'] +="</br>You cannot create teacher account ,as there are no active courses."
    if args['error_message']:
                     return args
    if roleval==5:
 
                  courseenroll=IfCourseEnrolled(int(args['courseval']),instituteid)
                  course_instance=edxcourses.objects.get(id = int(args['courseval']))
                  if courseenroll ==0:
                        t10ktinstituteid=T10KT_Institute.objects.get(instituteid=instituteid)
                        apprinstitute=T10KT_Approvedinstitute.objects.get(instituteid=t10ktinstituteid)
         
                        courseenrollObj=courseenrollment(courseid=course_instance,instituteid=apprinstitute, enrollment_date=date.today(), status=1)
          
                        courseenrollObj.save()
                  args['course']=course_instance 
    args['instinstance']=T10KT_Institute.objects.get(instituteid=args['rcidval'])     
    if personexist==1:       
        persobj=Personinformation.objects.filter(email = args['memailval'],instituteid__instituteid=instituteid).update(firstname = args['mfirstname'],lastname =args['mlastname'],designation=args['designationval'],createdondate=datetime.now(),telephone1=args['mcontactno'],streamid=args['department'],gender=args['gender'],qualification=args['qualification']) 
        
        args['regperson']=Personinformation.objects.get(email = args['memailval'],instituteid__instituteid=instituteid)
    elif  personexist==0:    
        args= createnewuser(request,args,pagerole)
        
        return args
        
    return args


def instiname(request):
    instituteid=request.GET['id']
    args ={}
    institutename=T10KT_Approvedinstitute.objects.get(id=instituteid).instituteid.institutename
    
    return HttpResponse(json.dumps(institutename), content_type="application/json")

def reginstiname(request):
    instituteid=request.GET['id']
    args ={}
    institutename=T10KT_Institute.objects.get(instituteid=instituteid).institutename
    
    return HttpResponse(json.dumps(institutename), content_type="application/json")



########################  End of admin registrationinterface ########################################################################
########################  Begin of Bulkmove module           ########################################################################
@login_required(login_url='/')
def bulkmove(request,courseid,persid,instituteid):
    course_inst=edxcourses.objects.get(courseid=courseid) 
    pers_inst=Personinformation.objects.get(id=persid)
    course_filt_obj=Courselevelusers.objects.filter(instituteid__instituteid=instituteid,courseid=course_inst,roleid=5).exclude(personid=pers_inst)
    teacher_list=[]
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    args['selectedteacher']=pers_inst.firstname+" "+pers_inst.lastname
    args['selectedinstitute']=institutename=T10KT_Institute.objects.get(instituteid=instituteid).institutename
    args['selectedcourse']=course_inst.course
    args['courseid']=course_inst.courseid
    args['persid']=persid
    args['instituteid']=instituteid
    for i in course_filt_obj:
        teacher_list.append([i.id,i.personid.email])
    args['teacher_list']=teacher_list

    return render(request,"bulkmove.html",args)


@login_required(login_url='/')
def bulkmoveupdate(request,courseid,persid,instituteid):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    newteacher= request.POST['newteacher']
    pers_inst=Personinformation.objects.get(id=persid)
    updatedby=Personinformation.objects.get(id=request.session['person_id'])
    new_teacher=Courselevelusers.objects.get(id=newteacher)
    course_obj=edxcourses.objects.get(courseid=courseid) 
    old_teacher=Courselevelusers.objects.get(personid=pers_inst,instituteid__instituteid=instituteid,courseid=course_obj,roleid=5)
    args['oldteacher_initcount']=studentDetails.objects.filter(courseid=courseid,teacherid=old_teacher,edxis_active=1).count()
    studentDetails.objects.filter(courseid=courseid,teacherid=old_teacher,edxis_active=1).update(teacherid=new_teacher,last_update_on=datetime.now(),last_updated_by=updatedby)
    oldteachcount=studentDetails.objects.filter(courseid=courseid,teacherid=old_teacher,edxis_active=1)
    newteachcount=studentDetails.objects.filter(courseid=courseid,teacherid=new_teacher,edxis_active=1)
    args['studcountnewteach']= newteachcount.count()
    args['studcountoldteach']=oldteachcount.count()
    args['newteachemail']= new_teacher.personid.firstname+" "+new_teacher.personid.lastname
    args['oldteachemail']=pers_inst.firstname+" "+pers_inst.lastname
    rcidid=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=instituteid).id
    #return teacherstudentlist(request,rcidid,course_obj.course,new_teacher.personid.email)
    return render(request,"bulkmovesummary.html",args)   

########################  End of Bulkmove module           ########################################################################


########################  Begin of teacher unenroll module ########################################################################

@login_required(login_url='/')
def teacherunenroll(request,courseid,tid):
     
# args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    current_date=date.today()
    args.update(csrf(request))
    try:
      if int(tid)==-1:
           args['teachername']="All Teachers"
      else:
           person=Personinformation.objects.get(id=tid)
           args['teachername']=person.firstname+" "+person.lastname
           courselevelid=Courselevelusers.objects.get(personid=person,courseid__courseid=courseid,instituteid=args['institute'],roleid=5,startdate__lte=current,enddate__gte=current)
           if studentDetails.objects.filter(teacherid=courselevelid).exists():
              args['error_message'] =  "You can unenroll teacher only if no student exist for teacher."
              return render(request,error_,args)
           else:
              courselevelid.roleid = int(-5)
              courselevelid.save()
           courselevelid=Courselevelusers.objects.filter(roleid=-5,courseid__courseid=courseid,instituteid=args['institute'],startdate__lte=current,enddate__gte=current)
           args['inactteachers']=courselevelid
    except Exception as e:
           args['error_message'] =  getErrorContent("session_not_active")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['pid']=tid
    
    return render_to_response("inactiveteacher.html",args, context_instance=RequestContext(request))



########################  End of teacher unenroll module ########################################################################

########################  Begin of manual upload module ########################################################################  
@login_required(login_url='/')
def courseadminhome(request):

    return manualupload(request)



def updatepdf(request,key):
    args={}
    args.update(csrf(request))
    try:   
      
         if "usermanual" == key:
             value=request.FILES['usermanual']
             if not value.name.endswith('.pdf'):
                output =  "Please upload valid pdf only"
             
             else:
                  savenewfile(request.FILES['usermanual'],0)
                  output = str(request.FILES['usermanual'])+ " is uploaded successfully. Please refresh the page. "
             return HttpResponse(json.dumps(output), content_type="application/json")
         if "bmadminmanual" == key:
             value=request.FILES['bmadminmanual']
             if not value.name.endswith('.pdf'):
                output =  "Please upload valid pdf only"
             else:
                  savenewfile(request.FILES['bmadminmanual'],1)
                  output= str(request.FILES['bmadminmanual'])+ " is uploaded successfully. Please refresh the page. "
             return HttpResponse(json.dumps(output), content_type="application/json")
         if "bmcoursemanagermanual" == key:
             value=request.FILES['bmcoursemanagermanual']
             if not value.name.endswith('.pdf'):
                output =  "Please upload valid pdf only"
             else:
                  savenewfile(request.FILES['bmcoursemanagermanual'],2)
                  output= str(request.FILES['bmcoursemanagermanual'])+ " is uploaded successfully. Please refresh the page. "
             return HttpResponse(json.dumps(output), content_type="application/json")
    except Exception as e:
          args['error_message'] =  "Please select a file."
    return render_to_response("manualupload.html",args,context_instance=RequestContext(request))
def sendmanual(request):
    args={}
    args.update(csrf(request))
    try:
      if len(request.FILES.values()) == 0:
          output =  "Please select some file."
          return HttpResponse(json.dumps(output), content_type="application/json")
      if  (request.is_ajax()) and (request.method == 'POST'):
         for i,v in request.FILES.iteritems():
             return updatepdf(request,i)
         
    except Exception as e:
          args['error_message'] =  "Please select file."
    return render_to_response("manualupload.html",args,context_instance=RequestContext(request))

def manualupload(request):
    
    args={}
    try:
       args['email']=request.session['email_id']
       person=Personinformation.objects.get(email=request.session['email_id'])
       #start of org changes       
       #institute=institute=T10KT_Institute.objects.get(instituteid=0)      
       institute=T10KT_Institute.objects.get(instituteid=person.instituteid_id)      
       #end of org changes
       args['firstname']=request.session['firstname']=person.firstname
       args['lastname']=request.session['lastname']=person.lastname        
       args['institutename']=request.session['institutename']=institute.institutename     
       #Start of org changes  
       #args['rcid']=request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       args['rcid']=request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=institute.instituteid).remotecenterid.remotecenterid
       #end of org changes
    except:
         input_list['error_message'] = getErrorContent("no_person_info")
         return render(request,error_,input_list)

   
    return render_to_response("manualupload.html",args,context_instance=RequestContext(request))


def savenewfile(filed,fileuser):
   
    filename = filed._get_name()
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    if fileuser == 0:
      dirpath=os.path.join(full_path,'static/manualuploaddir/BM_User_Manual.pdf')
      newname=os.path.join(full_path,'static/manualuploaddir/BM_User_Manual'+str(currenttime)+'.pdf')
    elif fileuser ==1:
          dirpath=os.path.join(full_path,'static/manualuploaddir/Blended Course Administrator.pdf')
          newname=os.path.join(full_path,'static/manualuploaddir/Blended Course Administrator'+str(currenttime)+'.pdf')
    elif fileuser ==2:
          dirpath=os.path.join(full_path,'static/manualuploaddir/Blended course manager.pdf')
          newname=os.path.join(full_path,'static/manualuploaddir/Blended course manager'+str(currenttime)+'.pdf')
    if os.path.exists(dirpath):
                os.rename(dirpath,newname)
    
    destination = open('%s' % (dirpath), 'wb')
    
    for chunk in filed.chunks():
        destination.write(chunk)
    destination.close()
    command = "python "+full_path+"/manage.py collectstatic  --noinput"
    subprocess.call(command, shell=True)
 
    
########################  End of manual upload module ########################################################################    
  

########################  Begin of faculty generic interface module ##################################################################   

@login_required(login_url='/')
def facultygenericinterface(request,courseid):
   try:
             args =sessiondata(request)
             args.update(csrf(request))
   except Exception as e:
             print e.message  
             return sessionlogin(request) 
   apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
   approvinstitute=[]
   for i in apprinstitute:
       approvinstitute.append([i.instituteid.institutename,i.id]) 
   approvinstitute=sorted(approvinstitute,key = operator.itemgetter(0)) 
   args['approvinstitute']=approvinstitute
   args['course']=course=edxcourses.objects.get(courseid=courseid).course
   args['courseid']=courseid
   if request.POST: 
       #rcid=request.POST['rcid']
       teacher=request.POST['Teacher']
       
             
       rcidid=request.POST['Institute']
       if teacher == "noteacher":
          args['error_message'] = "Please select Teacher"
          return render(request,"facultygeneric.html",args)
       
       
       elif rcidid == "noinstitute":
          args['error_message'] = "Please select RCID"
          return render(request,"facultygeneric.html",args)
       else:
            
            
           try:     
                   courseinst=edxcourses.objects.get(courseid=courseid)
                   apinstituteid=T10KT_Approvedinstitute.objects.get(id=rcidid)
                   instituteid=apinstituteid.instituteid  
                   args['institute']=apinstituteid.instituteid     
                   if teacher == "All Teachers":
                      persid=-1
                      couselevel=Courselevelusers.objects.filter(courseid=courseinst,instituteid=instituteid)
                   else:
                      person=Personinformation.objects.get(email=teacher)
                      args['teacher']=person.id
                      persid=person.id
                      couselevel=Courselevelusers.objects.filter(personid=person,courseid=courseinst,instituteid=instituteid)
                           
           except:
                      args['error_message'] = "Enter valid Uploader Info"
                      return render(request,"facultygeneric.html",args)
       
       if couselevel.exists():
            
              if "teacherstudent" in request.POST:
                 return teacherstudentlist(request,rcidid,courseid,teacher)
              elif "evaluation" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     return evaluation(request,courseid,persid,instituteid.instituteid,0)
              elif "evaluationstatus" in request.POST:
                     return evalstatus(request,courseid,persid,instituteid.instituteid,0)
              elif "grade" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     return grades_report(request,courseid,persid,instituteid.instituteid)
              
              
       else:
                    args['error_message']= "Person is not teacher for " +str(courseid)+" course for given RCID"
   
    
   else:
        return render(request,"facultygeneric.html",args)

########################  End of faculty generic interface module   ##################################################################### 

"""
def studentdetails(request,courseid,pid):
      email=request.user
      args={}
      student_list=AuthUser.objects.raw('''select "1" id ,au.email email,au.username username from student_courseenrollment sce , auth_user au where sce.course_id=%s and sce.user_id not in (select user_id from student_courseaccessrole scr where course_id =%s) and sce.user_id =au.id''',[courseid,courseid])
      #student_list=mysql_csr.fetchall()
      student_detail=[]
      args['email']=request.user
      args['institutename']=request.session['institutename']
      course=edxcourses.objects.get(courseid=courseid).course
      args['course']=course
      for i in student_list:
           student_detail.append([i.email,i.username])
      args['studentdetail']=student_detail
      return render_to_response('iitbx/participantdetails.html',args)

def coursedetails(request,courseid,pid):
    args={}
    args['email']=request.user
    args['institutename']=request.session['org']
    course=edxcourses.objects.get(courseid=courseid)
    args['coursenm']=course.coursename
    args['course']=course.course
    args['coursestart']=course.coursestart.date()
    args['courseend']=course.courseend.date()
    args['enrollstart']=course.enrollstart.date()
    args['enrollend']=course.enrollend.date()
    policy=[["Assignment","Total","Mandatory","Weight(%)","Comments"]]
    criteria=[["Grade","Min %","Max %"]]
    evaluate=[["Assignment","Assignment Type","Due Date"]]
    try:
        grpolicy=gradepolicy.objects.filter(courseid__courseid=courseid)
        for gp in grpolicy:
            if gp.drop_count==0:
                policy.append([gp.type+' ('+ gp.short_label +')',gp.min_count,gp.min_count-gp.drop_count,(gp.weight *100),""])
            else:
                 policy.append([gp.type+' ('+ gp.short_label +')',gp.min_count,gp.min_count-gp.drop_count,(gp.weight * 100),"Best of "+str((gp.min_count-gp.drop_count))])
        grcriteria=gradescriteria.objects.filter(courseid__courseid=courseid).values('cutoffs','grade').order_by('cutoffs').reverse().distinct()
        l=len(grcriteria)
        for  gc in range(0,len(grcriteria)):
             # print grcriteria,gc
              if gc==0:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs']*100,100])
              else:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs']*100,grcriteria[gc-1]['cutoffs']*100])
        evaluat=evaluations.objects.filter(course__courseid=courseid).values('sectionid','sec_name','type','due_date').order_by('sectionid').distinct()
        for eva in evaluat:
            evaluate.append([eva['sec_name'],eva['type'],eva['due_date']])

    except Exception as e:
           args['error_message'] ="my name is khan"
           return render(request,error_,args)

    args['evaluate']=evaluate
    args['criteria']=criteria
    args['policy']=policy
    args['id'] = pid
    return render_to_response('iitbx/coursedetails.html',args)

"""


############################ Begin of   Evaluation option selected module #########################################################
@login_required(login_url='/')
def evaluationoption(request,courseid,pid,instituteidid,evalflag):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
       args['selectedinstitute']=t10kt_obj.institutename
       args['instituteidid']=instituteidid
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    person=Personinformation.objects.get(id=pid)    
    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name','due_date').distinct().order_by('-due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,"evaluationoption.html",args)




@login_required(login_url='/')
def quizanswers(request,courseid,pid,instituteidid):

    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    report=[]
    header=[]
    try:
       secid=request.POST['quiz']

       evalu=evaluations.objects.filter(sectionid=secid,course__courseid=courseid).values('sec_name').distinct()
       args['secname']=evalu[0]['sec_name']
    except Exception as e:
           return evaluationoption(request,courseid,pid,instituteidid,1)


    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       t10kt_obj=T10KT_Institute.objects.get(instituteid=instituteidid)
       args['selectedinstitute']=t10kt_obj.institutename
       args['instituteidid']=instituteidid
       args['pid']=pid
       currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
       report_name="Evaluation Report of "+"_"+str(courseid)+" _ "+currenttime
       person=Personinformation.objects.get(id=pid)
       args['teacher']= str(person.firstname)+' '+str(person.lastname)
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)

    try:
      head_str=headings.objects.get(section=secid).heading
      heading=map(str,head_str.split(","))
      del heading[3]

    except Exception as e:
      print str(e.message),str(type(e))
    sqlmod=""
    ques_dict={}
    qidslist=[]
    count=0
    totalweight=0
    evaluation_obj=questions.objects.filter(course=courseobj,eval__sectionid=secid ).exclude(q_weight=0 ).order_by('eval_id','id')
    for evaluate in evaluation_obj:
           if evaluate.q_weight != 0:
              sqlmod= sqlmod +'"'+evaluate.qid+'",'
              qidslist.append(evaluate.qid)
           count=count+1
           totalweight=totalweight+evaluate.q_weight
    sqlmod=sqlmod[:-1]
    if len(sqlmod) == 0:
         stud_rec=[]
    else:
         sqlstmt= '''SELECT "1" id,student_id,username,email,module_id, case prob_count when 0 then '' when 1 then t1 when 2 then concat(t1,'~',t2) when 3 then concat(t1,'~',t2,'~',t3) when 4 then concat(t1,'~',t2,'~',t3, '~',t4) when 5 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5) when  6 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6) when  7 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7) when  8 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7,'~',t8) when  9 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7,'~',t8,'~',t9) when  10 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7,'~',t8,'~',t9,'~',t10) end as answer  FROM
 (SELECT module_id,student_id,if(ans1 LIKE '["choi%%%%',concat(substring_index(ans1,']',1),']'),if( ans1 like '"choi%%%%',concat(substring_index(ans1,'"',2),'"'),'')) t1
,if(ans2 LIKE '["choi%%%%',concat(substring_index(ans2,']',1),']'),if( ans2 like '"choi%%%%',concat(substring_index(ans2,'"',2),'"'),'')) t2
,if(ans3 LIKE '["choi%%%%',concat(substring_index(ans3,']',1),']'),if( ans3 like '"choi%%%%',concat(substring_index(ans3,'"',2),'"'),'')) t3
,if(ans4 LIKE '["choi%%%%',concat(substring_index(ans4,']',1),']'),if( ans4 like '"choi%%%%',concat(substring_index(ans4,'"',2),'"'),'')) t4
,if(ans5 LIKE '["choi%%%%',concat(substring_index(ans5,']',1),']'),if( ans5 like '"choi%%%%',concat(substring_index(ans5,'"',2),'"'),'')) t5
,if(ans6 LIKE '["choi%%%%',concat(substring_index(ans6,']',1),']'),if( ans6 like '"choi%%%%',concat(substring_index(ans6,'"',2),'"'),'')) t6
,if(ans7 LIKE '["choi%%%%',concat(substring_index(ans7,']',1),']'),if( ans7 like '"choi%%%%',concat(substring_index(ans7,'"',2),'"'),'')) t7
,if(ans8 LIKE '["choi%%%%',concat(substring_index(ans8,']',1),']'),if( ans8 like '"choi%%%%',concat(substring_index(ans8,'"',2),'"'),'')) t8
,if(ans9 LIKE '["choi%%%%',concat(substring_index(ans9,']',1),']'),if( ans9 like '"choi%%%%',concat(substring_index(ans9,'"',2),'"'),'')) t9
,if(ans10 LIKE '["choi%%%%',concat(substring_index(ans10,']',1),']'),if( ans10 like '"choi%%%%',concat(substring_index(ans10,'"',2),'"'),'')) t10
,prob_count
FROM (SELECT module_id, student_id,substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_4_1": ') ,-1),'}}',1),'", "i4x',1)  ans3,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_5_1": ') ,-1),'}}',1),'", "i4x',1)  ans4,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_6_1": ') ,-1),'}}',1),'", "i4x',1)  ans5,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_7_1": ') ,-1),'}}',1),'", "i4x',1)  ans6,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_8_1": ') ,-1),'}}',1),'", "i4x',1)  ans7,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_9_1": ') ,-1),'}}',1),'", "i4x',1)  ans8,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_10_1": ') ,-1),'}}',1),'", "i4x',1)  ans9,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_11_1": ') ,-1),'}}',1),'", "i4x',1)  ans10  
 FROM edxapp.courseware_studentmodule where module_type=%s and module_id in (%s) and course_id=%s and grade is not null and instr(state,'"done": true')!=0 ) a,iitbxblended.SIP_questions b where a.module_id=b.qid) X,
  auth_user b where   student_id=b.id order by student_id''' %('"'+"problem"+'"',sqlmod,'"'+str(courseobj.courseid)+'"')
         answersheets=AuthUser.objects.raw(sqlstmt)
         #answersheets=AuthUser.objects.raw('''SELECT "1" id,student_id,username,email,module_id,if(state LIKE "%%choice_0%%","A",if(state LIKE "%%choice_1%%","B",if(state LIKE "%%choice_2%%","C",if(state LIKE "%%choice_3%%","D",if(state LIKE "%%choice_4%%","E","DN"))))) answer FROM edxapp.courseware_studentmodule a, auth_user b where  module_type="problem" and module_id in ('''+(sqlmod)+''') and a.student_id=b.id  and a.course_id=" '''+str(courseobj.courseid)+'''" order by student_id ''')
         oldstudent=-1; anslist={};replist=[];stud_rec=[]
         for answer in answersheets:
           #print "hello"
           if oldstudent == -1:
               replist=[answer.student_id,answer.username,answer.email]
               oldstudent=answer.student_id
           #print oldstudent, answer.student_id
           if answer.student_id == oldstudent:
               anslist[answer.module_id]=answer.answer
           else:
               for qid in qidslist:
                     if (anslist.has_key(qid)):
                        replist.append(anslist[qid])
                     else:
                        replist.append('')
               stud_rec.append(replist)
               replist=[];anslist={}
               oldstudent=answer.student_id
               anslist[answer.module_id]=answer.answer
               replist=[answer.student_id,answer.username,answer.email]

         for qid in qidslist:
            if (anslist.has_key(qid)):
                  replist.append(anslist[qid])
            else:
                 replist.append('')
         stud_rec.append(replist)
    args['stud_rec']=stud_rec
    args['headings']=heading
    args["report_name"]=report_name
    return render(request,"answer.html",args)


############################ End of option selected module   ######################################################################


######################Begin of old course report module      ######################################################################

def display_instructor_oldreport(request,course):
    
    args ={}
    course_obj=edxcourses.objects.get(courseid=course)  
    args['email']=request.session['email_id']
    if (course_obj.blended_mode==1): 
      args['blended_mode']=1
      args['institute_id']=request.session['institute_id']           
    else:
       args['blended_mode']=0 
    args['firstname']=request.session['firstname']
    args['lastname']=request.session['lastname']
    args['pid']=request.session['pid']
    #args['institute_id']=request.session['institute_id']

    args['institutename']=request.session['institutename']
    args['rcid']=request.session['rcid']
    args['courselist_flag']=request.session['courselist_flag']
    args['course']=course
    args['coursename']=course_obj.coursename 
       
    return render(request,"course_faculty_oldreport.html",args)

##################### Begin of inactive course evaluation module  ####################################################################
@login_required(login_url='/')
def geninactiveevaluation(request,courseid,pid,evalflag):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request)     
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid       
       args['selectedinstitute']="IITBombay"       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    
    person=Personinformation.objects.get(id=pid)    
    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    evaluation_obj=gen_evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    elif evalflag==2:
        args['error_message'] = "Email Send successfully"
    
    args['evaluation']=evaluation_obj
    return render(request,"inactivecoursereports/geninactiveevaluation.html",args)


@login_required(login_url='/')
def inactivequizdata(request,courseid,pid):    
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    header=[]
    csvfile = StringIO.StringIO()
    
          
    try:
       secid=request.POST['quiz']
       evalu=gen_evaluations.objects.filter(sectionid=secid,course__courseid=courseid).values('sec_name').distinct()
       args['secname']=secname=evalu[0]['sec_name']
       print secname
    except Exception as e:
           return geninactiveevaluation(request,courseid,pid,1)
     
    args['selectedinstitute']="IITBombay"    
     
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
       person=Personinformation.objects.get(id=pid)
       args['teacher']= str(person.firstname)+' '+str(person.lastname)
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    filename="ed_"+str(courseobj.course)+"_"+secname+".csv"
    selectedfile=os.path.join('static/closed_courses/',courseobj.course,"eval_details/",filename)
    realpath=open(selectedfile)#for prooviding existing file and also use content=realpath.read()
    response = HttpResponse(content=realpath.read(),content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(selectedfile)
    if "email" in request.POST:
          emailfile=os.path.join(full_path,selectedfile)
          message = EmailMessage("Evaluation report of %s"%(courseobj.course),"PFA csv of %s"%(courseobj.course),"tushars@cse.iitb.ac.in",["tushars@cse.iitb.ac.in"])#need to change to person.email
          message.attach(emailfile, csvfile.getvalue(), 'text/csv')
          message.send()
          return geninactiveevaluation(request,courseid,pid,2)
   
    return response

#################################### Start of grades Report ############################################################################

@login_required(login_url='/')
def geninactivegrades_report(request,courseid,pid,mailflag):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request)    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid       
       args['selectedinstitute']="IITBombay"       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    
    person=Personinformation.objects.get(id=pid)    
    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    
    if mailflag==1:
        args['error_message'] = "Email Send successfully"
    
    return render(request,"inactivecoursereports/geninactivegrades.html",args)



@login_required(login_url='/')
def marksheetdownloademail(request,courseid,pid):
    faculty=request.session['faculty']
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    
    try:
        courseobj = edxcourses.objects.get(courseid = courseid)
    except Exception as e:
        print "ERROR occured",str(e.message),str(type(e))  
        return [-1,-1]

   
    try:      
         if int(pid) == -1:
           args['teacher']="All Teachers"
         else:
           person=Personinformation.objects.get(id=pid)
           args['teacher']= str(person.firstname)+' '+str(person.lastname)          
    except Exception as e:
        print "Error occured",str(e.message),str(type(e))

    csvfile = StringIO.StringIO()
    args['course']=courseobj.course
    args['pid']=pid
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    filename=str(courseobj.course)+"_grade_details.csv"
    selectedfile=os.path.join('static/closed_courses/',courseobj.course,filename)
    realpath=open(selectedfile)#for prooviding existing file and also use content=realpath.read()
    response = HttpResponse(content=realpath.read(),content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(selectedfile)
    if "email" in request.POST:
          emailfile=os.path.join(full_path,selectedfile)
          message = EmailMessage("Evaluation report of %s"%(courseobj.course),"PFA csv of %s"%(courseobj.course),"tushars@cse.iitb.ac.in",["bmwsoftwareteam@cse.iitb.ac.in"])#need to change to person.email
          message.attach(emailfile, csvfile.getvalue(), 'text/csv')
          message.send()
          return geninactivegrades_report(request,courseid,pid,1)
   
    return response

# end grades_report
#################################### End of grades Report ############################################################################
##################### Begin of Institute list evaluation wise  ####################################################################

@login_required(login_url='/')
def instilistforevalwise(request,courseid,pid,instituteidid):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['instituteidid']=instituteidid
       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    if int(pid) == -1:
          args['teacher']="All Teachers"
    else:
          person=Personinformation.objects.get(id=pid)
          args['teacher']= str(person.firstname)+' '+str(person.lastname) 
    
    courseenollobj=courseenrollment.objects.filter(courseid=courseobj)
    args['courseenollobj']=courseenollobj    
    if request.method=="POST":
         instituteselected=request.POST['Institute']
         if not instituteselected:
            args['error_message']="Please select some institute"
            return render(request,"evalwiseinstiselect.html",args)
         t10kt_obj=T10KT_Remotecenter.objects.filter(instituteid__instituteid=instituteselected)
         args['selectedinstitute']=t10kt_obj[0].instituteid.institutename
         args['selectedrcid']=t10kt_obj[0].remotecenterid
         evalstatus_list=[]
         evalstatusrawobj=Courselevelusers.objects.raw('''SELECT "1" id ,sec_name,sum(if(value='PA',1,0)) "PA",sum(if(value='FA',1,0)) "FA",sum(if(value='NA',1,0)) "NA",count(*) Total,B.due_date "due_date"
FROM
(SELECT c.id,s.edxuserid_id ,if(total='NA',"NA", if(instr(eval,"NA")>0,"PA","FA")) Value , section FROM SIP_courselevelusers  c,SIP_studentdetails s,SIP_markstable m
where c.instituteid_id=%s
and c.courseid_id=%s 
and s.teacherid_id=c.id
and s.id=m.stud_id ) A,(SELECT distinct sec_name,sectionid,due_date from SIP_evaluations e where course_id=%s ) B
where A.section=B.sectionid
group by sec_name ORDER BY due_date DESC ''',[instituteselected,courseobj.id,courseobj.id]) 
         for i in evalstatusrawobj:
              evalstatus_list.append([i.sec_name,i.PA,i.NA,i.FA,i.Total])
         args['evalstatus_list']=evalstatus_list
    
    return render(request,"evalwiseinstiselect.html",args)
##################### End of Institute list evaluation wise  ####################################################################

  
##################### Begin of Evaluation  list Institute wise  ####################################################################

@login_required(login_url='/')
def evallistforinstiwise(request,courseid,pid,instituteidid):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['instituteidid']=instituteidid
       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    if int(pid) == -1:
          args['teacher']="All Teachers"
    else:
          person=Personinformation.objects.get(id=pid)
          args['teacher']= str(person.firstname)+' '+str(person.lastname) 
    
    evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')
    args['evaluation_obj']=evaluation_obj   
    if request.method=="POST":
         section=request.POST['sectionid']
         if not section:
            args['error_message']="Please select some evaluation"
            return render(request,"instiwiseevalselect.html",args)
         evaluation_inst=evaluations.objects.filter(course=courseobj,sectionid=section)
         args['selectedeval']=evaluation_inst[0].sec_name
         
         evalstatus_list=[]
         evalstatusrawobj=Courselevelusers.objects.raw('''SELECT "1" id ,r.remotecenterid "rcid",A.instituteid_id "instiid",remotecentername "rcname",sum(if(value='PA',1,0)) "PA",sum(if(value='FA',1,0)) "FA",sum(if(value='NA',1,0)) "NA",count(*) Total FROM  (SELECT c.id,s.edxuserid_id ,if(total='NA',"NA", if(instr(eval,"NA")>0,"PA","FA")) Value , c.instituteid_id FROM SIP_courselevelusers  c,SIP_studentdetails s,SIP_markstable m where courseid_id= %s  and section= %s and s.id=m.stud_id and c.id=s.teacherid_id ORDER BY `m`.`total` ASC) A, SIP_t10kt_remotecenter r  where A.instituteid_id=r.instituteid_id and A.instituteid_id !=0 group by r.remotecenterid,A.instituteid_id,remotecentername ''',[courseobj.id,section]) 
         for i in evalstatusrawobj:
              evalstatus_list.append([i.rcid,i.rcname,i.PA,i.NA,i.FA,i.Total])
         args['evalstatus_list']=evalstatus_list
    
    return render(request,"instiwiseevalselect.html",args)
##################### End of Evaluation  list Institute wise  ####################################################################
@login_required(login_url='/')
def commonhome(request):
    args={}
    args.update(csrf(request))
    try:
       
       args['email_id']= request.session['email_id']
       person=Personinformation.objects.get(email=request.session['email_id'])
       args['institute']=institute=T10KT_Institute.objects.get(instituteid=person.instituteid_id)
       args['person']=person
       args['institutename']=institute.institutename
       args['firstname']=person.firstname
       args['lastname']=person.lastname
       request.session['lastname']=person.lastname
       request.session['institutename']=institute.institutename
       request.session['firstname']=person.firstname
       request.session['role_id'] =0
       request.session['rolename']="Super User"
       args['role_id'] =0
       args['rolename']="Super User"
       args['email']=request.session['email_id']
       #srart of org changes
       #request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=person.instituteid_id).remotecenterid.remotecenterid
       #end of org changes
       args['rcid']= request.session['rcid'] 
       args['usertype']= request.session['usertype']
    except Exception as e:
          args['error_message'] = getErrorContent("person_not_exit")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)
    
    multirole=0
    if Institutelevelusers.objects.filter(personid=person).exists():
        multirole=1
    elif Courselevelusers.objects.filter(personid=person).exists():
        multirole=1
    else:
        multirole=0
        if args['usertype']==2:               
            return HttpResponseRedirect(facultyreport_) 
        elif args['usertype']==3:                     
            multirole=0 
    args['multirole']=multirole
    #request.session['faculty']=1
    if request.POST:        
        
        institute_id = request.POST.get('institute_id')
        request.session['institute_id']=request.POST.get('institute_id')#institute id set
        
        args['institutename']=institute.institutename
    return render_to_response("commonhome.html",args)

##################### Begin of Head-Pc Deactivation module  ####################################################################      

def instituteheadpc(request):
    instituteid=request.GET['id']
    args ={}
    t10ktinstitute=T10KT_Institute.objects.get(instituteid=instituteid)
    instiheadpc=collections.defaultdict(int)
    instiheadpc_obj=Institutelevelusers.objects.filter(Q(roleid=3,instituteid=t10ktinstitute)|Q(roleid=2,instituteid=t10ktinstitute))
    
    for i in instiheadpc_obj:
        instiheadpc[int(i.roleid)]=str(i.personid.email)
    output=[t10ktinstitute.institutename,instiheadpc] 
    
    #data = serializers.serialize('json',institutecourseenroll)
    return HttpResponse(json.dumps(output), content_type="application/json")

def userinfo(request):
    t10ktinstituteid=request.GET['iid']
    headpcemail=request.GET['hepcid']
    role_id=request.GET['role_id']
    t10ktinstitute=T10KT_Institute.objects.get(instituteid=t10ktinstituteid)
    try:
       instileveleobj=Institutelevelusers.objects.get(instituteid=t10ktinstitute,personid__email=headpcemail,startdate__lte=current,enddate__gte=current,roleid=role_id)
       name=instileveleobj.personid.firstname+" "+instileveleobj.personid.lastname
       roleobj=Lookup.objects.get(category='role', code=instileveleobj.roleid)
       output=[name,roleobj.comment]
    except:
          person=Personinformation.objects.get(email=headpcemail)
          name=person.firstname+" "+person.lastname
          output=[name,"Teacher"] 
    return HttpResponse(json.dumps(output), content_type="application/json")


@login_required(login_url='/')
def pcheadmanager(request):
    args ={}
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    #apprinstitute=T10KT_Approvedinstitute.objects.all().exclude(remotecenterid__remotecenterid=0).order_by('remotecenterid__remotecenterid')
    #apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
    apprinstitute=T10KT_Approvedinstitute.objects.filter(remotecenterid__in=T10KT_Remotecenter.objects.filter(org=args['org'])).order_by('remotecenterid__remotecenterid')
    approvinstitute=[]
    for i in apprinstitute:
         approvinstitute.append([i.remotecenterid.remotecenterid,i.instituteid.instituteid])  
    args['approvinstitute']=approvinstitute
    if request.POST: 
       #rcid=request.POST['rcid']
       role_id= request.POST['headpc']
       headpcemail=request.POST['headpc_name']
       t10ktinstituteid=request.POST['Institute']

       if headpcemail == "noheadpc":
          args['error_message'] = "Please select Head or Pc"
          return render(request,"pcheadinfo.html",args)
       
       
       elif t10ktinstituteid == "noinstitute":
          args['error_message'] = "Please select RCID"
          return render(request,"pcheadinfo.html",args)
       else:
           t10ktinstitute=T10KT_Institute.objects.get(instituteid=t10ktinstituteid)
           instilevelobj=Institutelevelusers.objects.get(instituteid=t10ktinstitute,personid__email=headpcemail,startdate__lte=current,enddate__gte=current,roleid=role_id)

           if int(instilevelobj.roleid) == 3:
              instilevelobj.roleid=int(-3)
              instilevelobj.save()  
              args['success_message']=instilevelobj.personid.firstname+ " "+instilevelobj.personid.lastname+" is successfully Deactivated"
           elif int(instilevelobj.roleid)== 2:
                instilevelobj.roleid = int(-2)
                instilevelobj.save()
                args['success_message']= instilevelobj.personid.firstname+ " "+instilevelobj.personid.lastname+" is successfully Deactivated"
           else:
                print "Error"
                args['error_message']="Error Occured"
           
    return render_to_response("pcheadinfo.html",args)
##################### End of Head-Pc Deactivation module  ####################################################################     

############################## Begin of Edit Profile module  ####################################################################      
@login_required(login_url='/')
def editprofile(request,userpid=0):
    
    #try:
            args={}   
            args['rooturl']=ROOT_URL    
            approvinstitute=[]
            designationlist=[]
            qualificationlist=[]
            departmentlist=[]
            genderlist=[]
            rolelist=[]
            try:
               if userpid != 0:
                  person=Personinformation.objects.get(id=userpid)
               else:
                  person=Personinformation.objects.get(email=request.session['email_id'])
               args['person']=person
            except Exception as e:
               args['error_message'] = getErrorContent("unique_person")
               args['error_message'] = "\n Error " + str(e.message) + str(type(e))
               return render(request,error_,args)
            loginperson=Personinformation.objects.get(email=request.session['email_id'])
            try:
               aproinst=T10KT_Approvedinstitute.objects.get(instituteid=person.instituteid)
               args['rcid']=aproinst.remotecenterid.remotecenterid
            except:
                  args['rcid']=""
            args['firstname']=loginperson.firstname
            args['lastname']=loginperson.lastname
            args['mfirstname']=person.firstname
            args['mlastname']=person.lastname
            args['memailval']=person.email
            args['gender']=person.gender
            args['qualification']=int(person.qualification)
            args['designationval']=person.designation
            args['department']=person.streamid
            args['mcontactno']=person.telephone1
            designation=Lookup.objects.filter(category = 'Designation')
    
            for i in designation:
               designationlist.append([i.code,i.description])  
            args['designationlist']=designationlist
            
            qualification=Lookup.objects.filter(category = 'Qualification')
            
            for i in qualification:
               qualificationlist.append([i.code,i.description])  
            args['qualificationlist']=qualificationlist

            department=Lookup.objects.filter(category = 'Stream')
            
            for i in department:
               departmentlist.append([i.code,i.description])  
            args['departmentlist']=departmentlist
         
            genderlist=[["Female","Female"],["Male","Male"],["Others","Others"]]  
            args['genderlist']=genderlist
            if request.POST:
                 args.update(validateeditprofiledata(request))
                 if args['error_message']:
                     return  render(request,"editprofile.html",args) 
                 else:
                     Personinformation.objects.filter(email = args['memailval']).update(firstname = args['mfirstname'],lastname =args['mlastname'],designation=args['designationval'],createdondate=datetime.now(),telephone1=args['mcontactno'],streamid=args['department'],gender=args['gender'],qualification=args['qualification'])
                     args['module']="editprofile" 
                     #args['success_message']="Profile updated successfully."
                     args['rooturl']=ROOT_URL
                     return  render(request,"registrationsuccessfull.html",args)
            return  render(request,"editprofile.html",args)
            
def validateeditprofiledata(request):
    args={}
    args['mfirstname']=firstname=request.POST['firstname']
    args['mlastname']=lastname=request.POST['lastname']
    args['memailval']=emailval=request.POST['email'].replace(" ","")
    args['designationval']=designationval=int(request.POST['designation'])
    args['gender']=gender=request.POST['gender']
    args['qualification']=qualification=int(request.POST['qualification'])
    args['department']=department=int(request.POST['department'])
    args['mcontactno']=contactno=request.POST['contactno']
    args['rcid']=request.POST['rcid']
    emailvalidate=validateEmail(emailval)
    fname=validateFname(firstname)
    lname=validateLname(lastname)
    personexist=ifPersonExists(emailval)
    contact=validateContact(contactno)    
    args['personexist']=personexist    
    args['error_message']=""
    if not emailval:
       args['error_message']="Enter valid Email."
    if emailvalidate == 0:
       args['error_message']="Enter valid Email."
       
    if fname==0:
       args['error_message']+="</br>Enter valid firstname."
    if lname==0:
       args['error_message'] +="</br>Enter valid lastname."
    if personexist==0:
       args['error_message'] +="</br>Person does not exists."
    if designationval==-1:
       args['error_message'] +="</br>Please select Designation."
    if not gender:
       args['error_message'] +="</br>Please select Gender."
    if qualification==-1:
       args['error_message'] +="</br>Please select Qualifications."
    if department==-1:
       args['error_message'] +="</br>Please select Department"
    if contact==0:
       args['error_message']+="</br>Enter valid Phone(Mobile should be 10 digit or Landline of 11 digit - include STD code)."
    
    return args
############################## End of Edit Profile module  ####################################################################  

############################## Begin of Admin Edit Profile Module #############################################################

@login_required(login_url='/')
def admineditprofile(request):
    args ={}
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    args['error_message']=""
    #apprinstitute=T10KT_Approvedinstitute.objects.all().exclude(remotecenterid__remotecenterid=0).order_by('remotecenterid__remotecenterid')
    #apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
    apprinstitute=T10KT_Approvedinstitute.objects.filter(remotecenterid__in=T10KT_Remotecenter.objects.filter(org=args['org'])).order_by('remotecenterid__remotecenterid')
    approvinstitute=[]

    for i in apprinstitute:
         approvinstitute.append([i.remotecenterid.remotecenterid,i.instituteid.instituteid])  

    
    args['approvinstitute']=approvinstitute
    if request.GET:
       if request.GET['Institute'] =="noinstitute":
            args['error_message'] +="</br>Please select Institute."
       else:
            instiuseremail=request.GET['Institute']
       if request.GET['role']=="norole":
            args['error_message'] +="</br>Please select Role."
       else:
            instiuseremail=request.GET['role']
            
       if request.GET['instiuser']=="nouser":
            args['error_message'] +="</br>Please select Email."
            
       else:
            instiuseremail=request.GET['instiuser']
            
       if  args['error_message']:
          return render_to_response("editprofileuser.html",args)
       person=Personinformation.objects.get(email=instiuseremail)
       return editprofile(request,person.id)
    return render_to_response("editprofileuser.html",args)

def ajaxrole(request):
    instituteid=request.GET['id']
    rolelist=[]
    t10ktinstitute=T10KT_Institute.objects.get(instituteid=instituteid)
    roleobj=Lookup.objects.filter(category = 'Role',code__gte=2).exclude(code=4)
    for i in roleobj:
                   rolelist.append([i.code,i.comment]) 
    output=[rolelist,t10ktinstitute.institutename] 
    return HttpResponse(json.dumps(output), content_type="application/json")

def institutebmuser(request):
    instituteid=request.GET['id']
    role=int(request.GET['rid'])
    args ={}
    t10ktinstitute=T10KT_Institute.objects.get(instituteid=instituteid)
    #t10ktinstituteid=selectapinrinfo.instituteid
    instibmuser=[]
    if role == 2 or role ==3:
         instiuser=Institutelevelusers.objects.filter(roleid=role,instituteid=t10ktinstitute)
    else:
         instiuser=Courselevelusers.objects.filter(roleid=role,instituteid=t10ktinstitute)
    for i in instiuser:
        instibmuser.append(i.personid.email) 
    instibmuser= list(set(instibmuser))
    output=[t10ktinstitute.institutename,instibmuser] 
    
    #data = serializers.serialize('json',institutecourseenroll)
    return HttpResponse(json.dumps(output), content_type="application/json")
############################## End of Admin Edit Profile Module ############################################################# 

############################## Begin of AllStudent Info Module #################################################################    
@login_required(login_url='/')
def allstudentinfo(request): 
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    sevenenddate=timezone.now()-timezone.timedelta(days=7)
    currentedxcourse=edxcourses.objects.filter(blended_mode=1,org=args['org'],courseend__gte=sevenenddate).order_by("-courseend")   
    args['courselist']=currentedxcourse
    if request.POST: 
       #rcid=request.POST['rcid']
       course=request.POST['Course']
       if course == "nocourse":
          args['error_message'] = "Please select Course"
          return render_to_response("allstudentinfo.html",args)
       
       else:
              courseobj=edxcourses.objects.get(id=course)
              if "coursestudentdetail" in request.POST:
                 return coursestudentdetail(request,courseobj.courseid)
              elif "courseallevaluation" in request.POST:
                     
                     return courseallevaluation(request,courseobj.courseid,0)
              
              elif "courseallgrade" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     return courseallgrade(request,courseobj.courseid)
              
    return render_to_response("allstudentinfo.html",args)

@login_required(login_url='/')
def coursestudentdetail(request,courseid):
    courselevelid=Courselevelusers.objects.filter(courseid__courseid=courseid,roleid=5,startdate__lte=current,enddate__gte=current)
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    course=edxcourses.objects.get(courseid=courseid).course

    name=course+"  student_details"+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)     
    writer.writerow(["RollNumber", "Teacher","UserName","Email"])
    students = studentDetails.objects.filter(teacherid__courseid__courseid=courseid,teacherid__roleid=5,teacherid__startdate__lte=current,teacherid__enddate__gte=current,courseid=courseid,edxis_active=1)
    for student in students:   
                      writer.writerow([student.roll_no,student.teacherid.personid.email,student.edxuserid.username,student.edxuserid.email])
    
    return response

@login_required(login_url='/')
def courseallevaluation(request,courseid,evalflag=0):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    
    
    evaluation_obj=evaluations.objects.raw('''SELECT a.id, a.sec_name "sec_name " ,a.sectionid "sectionid" ,release_date,due_date,type FROM `SIP_evaluations` a, `SIP_course_modlist` b where a.course_id=b.course and a.sectionid=b.module_id and a.course_id=%s and a.release_date <= current_date() order by b.order ASC    ''',[courseobj.id])
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,"courseallevaluation.html",args)


@login_required(login_url='/')
def courseallevaluationdata(request,courseid):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    
    header=[]
    ques_dict={}
    stud_rec=[]
    try:
       secid=request.POST['quiz']

       evalu=evaluations.objects.filter(sectionid=secid,course__courseid=courseid).values('sec_name').distinct()
       args['secname']=secname=evalu[0]['sec_name']
    except Exception as e:
           return courseallevaluation(request,courseid,1)
    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=course=courseobj.course
       args['courseid']=courseid
      
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    
    try:
      head_str=headings.objects.get(section=secid).heading
      heading=map(str,head_str.split(","))     

    except Exception as e:
      print str(e.message),str(type(e))
      if not head_str:
         return render(request,quizdata_,args)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    name=  str(course)+"_"+str(secname)+"_report_"+str(args['refreshdate'])+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    count=0
    heading = [h.replace('<br>', '\n') for h in heading]
    teacherheader=[]
    for i in heading:
           count = count +1
           if count == 2:
              teacherheader.append("Teacher")
              teacherheader.append(i)
           else:
               teacherheader.append(i)
    writer.writerow(teacherheader)
    marks_obj=markstable.objects.filter(section=secid,stud__teacherid__courseid__courseid=courseid,stud__teacherid__roleid=5,stud__teacherid__startdate__lte=current,stud__teacherid__enddate__gte=current,stud__edxis_active=1)  
    for studvalue in marks_obj:
            marks=studvalue.eval.split(",")
            total=studvalue.total
            writer.writerow([str(studvalue.stud.roll_no),str(studvalue.stud.teacherid.personid.email),str(studvalue.stud.edxuserid.username),str(studvalue.stud.edxuserid.email), total]+marks) 
           
    return response


@login_required(login_url='/')
def courseallgrade(request,courseid):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    try:
        courseobj = edxcourses.objects.get(courseid = courseid)       
    except Exception as e:
        print "ERROR occured",str(e.message),str(type(e))  
        return [-1,-1]
    currenttime = datetime.now().strftime("%d-%m-%Y_%H%M")   
    
    name= str(courseobj.course)+"-Progress Report"+currenttime+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    header=[] 
    ttheader=[]
    dwnldttheader=[]
    headerwithtt=[]
    try: 
       header=headings.objects.get(section=courseobj.courseid).heading
       header_data=map(str,header.split(","))           
    except Exception as e:
       print "1 Header does not exists"
       #Error code#
       print "Header does not exists",str(e.message),str(type(e))
       args['error_message'] = "Header does not exists"
       return render(request,error_,args)

    try :
       ttheader=headings.objects.get(section="TT"+courseobj.courseid).heading
       ttheader=",,,,,"+ttheader
       dwnldttheader=map(str,ttheader.split(","))
       ttheader_data=map(str,ttheader.split(","))
       
       for i in range(0,len(header_data)):
            headerwithtt.append([header_data[i],ttheader_data[i]])
    except Exception as e:
       dwnldttheader=[]
       for i in range(0,len(header_data)):
            headerwithtt.append([header_data[i],""])
       print "TTHeader does not exists",str(e.message),str(type(e))
    header = [h.replace('<br>', '\n') for h in header_data]
    #ttheader=[""]+dwnldttheader
    #ttheader_data=dwnldttheader
    count=0
    teacherheader=[]
    for i in header:
           count = count +1
           if count == 2:
              teacherheader.append("Edx User Id")
              teacherheader.append(i)
           else:
               teacherheader.append(i)
    writer.writerow(dwnldttheader)
    writer.writerow(teacherheader)

    student_details=studentDetails.objects.filter(teacherid__courseid__courseid=courseid,teacherid__roleid=5,teacherid__startdate__lte=current,teacherid__enddate__gte=current,courseid=courseid,edxis_active=1).order_by('edxuserid__edxuserid')    
    for student_detail in student_details:
           try:
              gradestable_obj=gradestable.objects.get(course=courseobj.courseid,stud=student_detail)
           except Exception as e:               
              print "grade does not exist",str(e.message),str(type(e))             
              #return render(request,coursegrades_,args)
           marks=(gradestable_obj.eval).split(",")
           grade=gradestable_obj.grade
           writer.writerow([str(gradestable_obj.stud.roll_no), str(gradestable_obj.stud.edxuserid.edxuserid), str(gradestable_obj.stud.edxuserid.username),str(gradestable_obj.stud.edxuserid.email),grade]+marks)
    
    return response  

############################## End of AllStudent Info Module #################################################################
@login_required(login_url='/')
def facultyuploaderinfo(request,courseid):  
   args={}
   
   try:
       if request.session['usertype']==2 or 1:
              try:
                   args =sessiondata(request)
                   args.update(csrf(request))
              except Exception as e:
                  print e.message  
                  return sessionlogin(request) 
       else:
           args['error_message'] = "You do not have permission to view this page"
           return render(request,error_,args)
     
   except:
             args['error_message'] = "You are not logged-in"
             return render(request,error_,args)
   args['courseid']=courseid
   #apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
   apprinstitute=T10KT_Approvedinstitute.objects.filter(remotecenterid__in=T10KT_Remotecenter.objects.filter(org=args['org'])).order_by('remotecenterid__remotecenterid')
   approvinstitute=[]
   for i in apprinstitute:
       approvinstitute.append([i.remotecenterid.remotecenterid,i.id])  
   args['approvinstitute']=approvinstitute
   if request.POST: 
       #rcid=request.POST['rcid']
       teacher=request.POST['Teacher']
       course=request.POST['Course']
             
       rcidid=request.POST['Institute']
       if teacher == "noteacher":
          args['error_message'] = "Please select Teacher"
          return render(request,"facultyuploaderinfo.html",args)
       elif teacher == "noteacherexist":
          args['error_message'] = "Selected Institute has no Teacher Enrolled for this Courses !!!"
          return render(request,"facultyuploaderinfo.html",args)
       
       
       elif rcidid == "noinstitute":
          args['error_message'] = "Please select RCID"
          return render(request,"facultyuploaderinfo.html",args)
       else:
            
            
           try:     
                   courseid=edxcourses.objects.get(courseid=course)
                   sevenenddate=timezone.now()-timezone.timedelta(days=7)
                   apinstituteid=T10KT_Approvedinstitute.objects.get(id=rcidid)
                   instituteid=apinstituteid.instituteid  
                   args['institute']=apinstituteid.instituteid     
                   if teacher == "All Teachers":
                      persid=-1
                      couselevel=Courselevelusers.objects.filter(courseid=courseid,instituteid=instituteid)
                   else:
                      person=Personinformation.objects.get(email=teacher)
                      args['teacher']=person.id
                      persid=person.id
                      couselevel=Courselevelusers.objects.filter(personid=person,courseid=courseid,instituteid=instituteid)
                           
           except:
                      args['error_message'] = "Enter valid Uploader Info"
                      return render(request,"facultyuploaderinfo.html",args)
       
       if couselevel.exists():
              if "studentupload" in request.POST:
                  if teacher == "All Teachers":
                     args['error_message'] = "Not valid  for all teacher option"
                     return render(request,error_,args)  
                  
                  if courseid.courseend < sevenenddate:
                         args['error_message'] = "This functionalty is not for archived courses. Please select current course."
                  args['uploaderrcid']=apinstituteid.remotecenterid.remotecenterid
                  args['courseid']=courseid.courseid
                  form = UploadForms() 
                  args['form'] = form
                  return render_to_response('adminupload.html', args)
              elif "teacherstudent" in request.POST:
                 return teacherstudentlist(request,rcidid,courseid.courseid,teacher)
              elif "evaluation" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     if courseid.courseend < sevenenddate:
                         args['error_message'] = "This functionalty is not for archived courses. Please select current course."
                         return render(request,"facultyuploaderinfo.html",args) 
                     return evaluation(request,courseid.courseid,persid,instituteid.instituteid,0)
              elif "evaluationstatus" in request.POST:
                     if courseid.courseend < sevenenddate:
                         args['error_message'] = "This functionalty is not for archived courses. Please select current course."
                         return render(request,"facultyuploaderinfo.html",args) 
                     return evalstatus(request,courseid.courseid,persid,instituteid.instituteid,0)
              elif "grade" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     return grades_report(request,courseid.courseid,persid,instituteid.instituteid)
              elif "deactivate" in request.POST:
                     return teacherdeactivation(request,courseid.courseid,persid,instituteid.instituteid)
              elif "bulkmove" in request.POST:
                     if teacher == "All Teachers":
                        args['error_message'] = "Not valid  for all teacher option.Please select one teacher"
                        return render(request,error_,args)  
                     else:
                           return bulkmove(request,courseid.courseid,persid,instituteid.instituteid)
       else:
                    args['error_message']= "Person is not teacher for " +str(courseid.courseid)+" course for given RCID"
   
    
   else:
        return render(request,"facultyuploaderinfo.html",args)

@login_required(login_url='/')
def facultyallstudentinfo(request,courseid): 
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message  
             return sessionlogin(request) 
    args['courseid']=courseid
    if request.POST: 
       #rcid=request.POST['rcid']
       course=request.POST['Course']
       if course == "nocourse":
          args['error_message'] = "Please select Course"
          return render_to_response("allstudentinfo.html",args)
       
       else:
              
              if "coursestudentdetail" in request.POST:
                 return coursestudentdetail(request,courseid)
              elif "courseallevaluation" in request.POST:
                     
                     return courseallevaluation(request,courseid,0)
              
              elif "courseallgrade" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     return courseallgrade(request,courseid)
              
    return render_to_response("facultyallstudentinfo.html",args)

################################################# Invited Participant report ########################################################
@login_required(login_url='/')
def invited_userlist(request,courseflag):
    info=[]
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    courseobj =edxcourses.objects.filter(blended_mode=1,org=args['org']).order_by("-courseend")
    args['courseobj']=courseobj
   
    if int(courseflag)==1:
        courseid=request.POST['courseid']
        courseobj =edxcourses.objects.get(courseid=courseid)
        if courseid !="Select":
          registrationinfo=AuthUser.objects.raw('''SELECT a.email,convert_tz(a.created,'+00:00','+05:30') invited ,b.username,b.id, convert_tz(b.date_joined, '+00:00','+05:30') date_joined,date_format(convert_tz(c.created ,'+00:00','+05:30'),"%%b. %%d,%%Y")  "enrolled" ,if (c.is_active=1,"Enrolled","Unenrolled") is_active FROM `student_courseenrollmentallowed` a ,  auth_user b,student_courseenrollment c where a.course_id=%s and c.course_id=a.course_id and a.email=b.email and b.id=c.user_id union SELECT a.email,convert_tz(a.created,'+00:00','+05:30') invited ,NULL,NULL, NULL date_joined,NULL  "enrolled" ,NULL FROM `student_courseenrollmentallowed` a where a.course_id=%s  and a.email not in (select email from auth_user b, student_courseenrollment c  where c.user_id=b.id and b.email=a.email and c.course_id=%s) ''',[courseid,courseid,courseid])
        for i in  registrationinfo:
           info.append([i.email,(i.invited).date(),i.enrolled,i.username,i.is_active])
        else:
           args['error_message'] = getErrorContent("select_course")+"<br>"
           args['info']=info
           args['courseid']=courseid
           args['coursedisplayname']=courseobj.coursename
           args['coursestart']=courseobj.coursestart.date()
           args['courseend']=courseobj.courseend.date()
        return render(request,'participant_list.html',args)
    
    
    return render(request,'invited_userlist.html',args)
############################################# End of Invited Participant report ##########################################################

def userweeklysession(request):
    try:
             args =sessiondata(request)
             args.update(csrf(request))
    except Exception as e:
             print e.message
             return sessionlogin(request)
    from django.contrib.sessions.models import Session
    from django.contrib.auth.models import User
    from tracking.models import Visitor
   
    session_obj = Session.objects.all().order_by('expire_date')
    wksessdata=[]
    currentday=datetime(2015, 12, 18, 0, 0,0)
    
    seventhday=datetime(2015, 12, 18, 0, 0,0)

    while (seventhday<=timezone.now().replace(tzinfo=None)):

        c=0
        n=0
        cluser=0
        iluser=0
        faculty=0
        staff=0
        #useremail=[]
        seventhday=(currentday+timezone.timedelta(days=7))
        
        for session in session_obj:
           if  currentday<=session.expire_date.replace(tzinfo=None)<seventhday:
                uid = session.get_decoded().get('_auth_user_id')
                if uid is not None:
                   c=c+1
                   user = User.objects.get(pk=uid)
                   user_info=Userlogin.objects.get(user=user)
                   #useremail.append(user.email)
                   
                   if user_info.usertypeid==1:
                       if Institutelevelusers.objects.filter(personid__email=user.email).exists():
                           iluser=iluser+1
                       elif Courselevelusers.objects.filter(personid__email=user.email).exists():
                           cluser=cluser+1
                   elif user_info.usertypeid==2:
                      faculty=faculty+1
                   else:
                      staff=staff+1
                       
                  
                else:
                    n=n+1
        #useremail=len(set(useremail))
        wksessdata.append([currentday.strftime("%d-%m-%Y"),seventhday.strftime("%d-%m-%Y"),c,iluser,cluser,faculty,staff,n])
        currentday=seventhday
        
    args['wksessarg']=wksessdata
    return render(request,'weeklysession.html',args)


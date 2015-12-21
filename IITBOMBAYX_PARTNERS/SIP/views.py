from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
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
#############################end of import statements by student management#######################################
current=timezone.now
default_password="Welcome123"
default_end_date="4712-12-31"

########################views Starts from Here ###################################


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def get_multi_roles(request):    
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
        rolelist,args= roleselect(request,institute_id,person,args)

        if len(rolelist)==1:
            return onerole(request,rolelist,args)
        elif len(rolelist)==0:
            args['norole']="You currently have no roles"
            return render(request,selectrole_,args)
        args.update(csrf(request)) 
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
def roleselect(request,institute_id,person,args):
    args['rolename']="Super User"
    try:
        rolelist=[]
        obj = Institutelevelusers.objects.filter(instituteid=institute_id,roleid__gte=0).filter(personid=request.session['person_id']).values("roleid").distinct()
        for row in obj:
            obj=Lookup.objects.get(category='role', code=row['roleid'])
            
            rolelist.append([obj.comment,row['roleid'],0])

        cobj = Courselevelusers.objects.filter(instituteid__instituteid=institute_id,roleid__gte=0).filter(personid=request.session['person_id'])
        for row in cobj:
            obj=Lookup.objects.get(category='role', code=row.roleid)
           # print row.courseid.id,row.roleid,obj.comment
            rolelist.append([obj.comment,row.roleid,row.courseid])       
        
        args['flag']=False
        args['rolelist']=rolelist  
        args['firstname']=person.firstname
        args['lastname']=person.lastname
        args['institutename']=T10KT_Institute.objects.get(instituteid=request.session['institute_id']).institutename
        args['email']=request.session['email_id']
        
        return rolelist,args
    except Exception as e:
          args['error_message'] = getErrorContent("roleid_not_exit")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)


###################Set institue directly in session if only one institute is present for logged in user#################
def oneinstitute(request,person):
    args={}
    if Institutelevelusers.objects.filter(personid=person.id).exists():
        institute_id=Institutelevelusers.objects.filter(personid=person.id)[0].instituteid.instituteid
    else:
        institute_id=Courselevelusers.objects.filter(personid=person.id)[0].instituteid.instituteid
    request.session['institute_id']=institute_id#institute id set
    try:
       request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=institute_id).remotecenterid.remotecenterid
    
    except:
       request.session['rcid']="   "   
    #insti_x=T10KT_Institute.objects.filter(instituteid=institute_id)
    #x= insti_x[0].institutename
    args['rcid']=request.session['rcid']
    
    rolelist,args=roleselect(request,institute_id,person,args)
   
    if len(rolelist)==1:
            return onerole(request,rolelist,args)
    elif len(rolelist)==0:
         args['norole']="You currently have no roles"
         return render(request,selectrole_,args)
    args.update(csrf(request)) 
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
def set_single_role(request,role,courseid,cid):
    try:    
        request.session['role_id']=int(role)
        request.session['rolename']=Lookup.objects.get(category="Role",code=role).comment
        request.session['courseid']=courseid#role id set
        request.session['edxcourseid']=cid#role id set
        args=sessiondata(request)
        return ccourse(request)
    
    except Exception as e:
          args['error_message'] = getErrorContent("category_not_exit")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)

#Return dictionary with default data of session institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid
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
    try:
       args['rolename']=request.session['rolename']
    except:
       pass
    args['rcid']=request.session['rcid'] 
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
               
               if user_info.usertypeid==0:
                   
                   return HttpResponseRedirect(iitbxhome_)
               elif user_info.usertypeid==2:
                    
                   return HttpResponseRedirect(facultyreport_)
               elif user_info.usertypeid==3:
                    
                   return HttpResponseRedirect(courseadminhome_)
               else:
                   return HttpResponseRedirect(get_multi_roles_)
            else:               
                return loginn(request)
    except:
                    
            return loginn(request)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def iitbxhome(request):
    args={}
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
       request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       args['rcid']= request.session['rcid'] 
    except Exception as e:
          args['error_message'] = getErrorContent("person_not_exit")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)
    

    if request.POST:        
        
        institute_id = request.POST.get('institute_id')
        print institute_id,"insti"
        #print request.POST.get('institute_id')
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
        args = emailid_validate(request,args)
        if args['error_message']:
            return render_to_response(login_,args)            
        loginlist = validate_login(request) 
## If the emailid exists, then call the page according to the role
        if (loginlist==1):      
            return HttpResponseRedirect(get_multi_roles_)
## If the emailid does not exist,display error message
        elif (loginlist == 0):
             print "hello"
             return HttpResponseRedirect(iitbxhome_)
        elif (loginlist == 2):
             return HttpResponseRedirect(facultyreport_)
        elif (loginlist == 3):
             return HttpResponseRedirect(courseadminhome_)
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
            #print ec_id
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
    print emailid
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
                       # print "ec_id =", ec_id
		        send_email(request,ec_id, per_id, per_id)
		        return render_to_response(createpasswordsuccess_,args)            
	  
		  #return render_to_response(createpassword_,args)
       return  render_to_response(passwordalreadycreated_,args)

    except Exception as e:
           args['error_message'] = getErrorContent("no_person")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)



#################### Delete session and redirect to login page on logout click#######################################
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
		del request.session['person_id']
		del request.session['email_id']
		del request.session['institute_id']
		if request.session['result']:
		    del request.session['result']
		del request.session['stud_rec']
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

def ccourse(request):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
    args =sessiondata(request)
    input_list={}
    
    input_list.update(args)
    input_list.update(csrf(request))
    input_list['roleid']=args['role_id']
        
    if input_list['roleid']==4:
		return HttpResponse('/coordinatorhome/')
    if input_list['roleid']==5:
		
		return teacherhome(request,args['person'].id)
    input_list['viewer'] = args['person'].id

    enrolled_courses=courseenrollment.objects.filter(status=1, instituteid__instituteid=request.session['institute_id'])

    edx_enrolled_courses=[]
    edx_unenrolled_courses=[]
    unenrolledxcourse=edxcourses.objects.exclude(courseid__in=enrolled_courses.values_list('courseid__courseid', flat=True))
    try:
       for index in enrolled_courses:
		  edx_enrolled_courses.append(edxcourses.objects.get(courseid=index.courseid.courseid))
    except Exception as e:
           args['error_message'] = getErrorcontent("no_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

    input_list['courselist'] = edx_enrolled_courses
    input_list['cid']=args['edxcourseid']
    input_list['unenrolledxcourse']=unenrolledxcourse
    return render(request,enrolled_course_, input_list)




################ Display list of Teacher's of  particular course and institute from Courselevelusers based on session #############################.

def teacherlist(request,courseid):
        # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
        args =sessiondata(request)
        args.update(csrf(request))
        teacherlist = []    
             
        users = Courselevelusers.objects.filter(instituteid__instituteid = request.session['institute_id'],roleid = 5).filter(courseid__courseid = courseid)
        for user in users:
                teacherlist.append(user)  
                args['coursename'] = user.courseid.coursename

        args['teacherlist'] = teacherlist
        args['courseid']=request.session['courseid'] = courseid
        request.session['edxcourseid']=edxcourses.objects.get(courseid=request.session['courseid']).id
        try:
            args['course']=edxcourses.objects.get(courseid=courseid).course
        except Exception as e:
           args['error_message'] = getErrorContent("course_not_present")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
        return render_to_response(teacherlist_,args, context_instance=RequestContext(request))



def courselist(request):
    #args = {}
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
    args =sessiondata(request) 
    args.update(csrf(request))   
    obj = Courselevelusers.objects.filter(personid_id = request.session['person_id'],courseid__courseid = request.session['courseid'],instituteid__instituteid=request.session['institute_id'],roleid = request.session['role_id'])     
    args['courses'] = obj
    for i in obj:
        args['coursename'] = i.courseid.coursename        
    return render_to_response(coordinatorhome_,args,context_instance=RequestContext(request))

    

  
###############Display details of student of logged-in teacher for selected institute for selected course from Student Tables#############

def studentdetails(request,courseid,pid):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
    args =sessiondata(request)
    args.update(csrf(request))
    faculty=request.session['faculty']
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
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
                header=["S.No","Roll Number","Teacher","UserName","Email","Select","Unenroll"]
            else:
                header=["S.No","Roll Number","Teacher","UserName","Email"]
            if faculty != 1:
               courselevelid=Courselevelusers.objects.filter(courseid__courseid=courseid,instituteid=args['institute'],roleid=5,startdate__lte=current,enddate__gte=current)
            
        else:
             if args['role_id']==5:
                header=["S.No","Roll Number","UserName","Email","Select","Unenroll"]
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
                students = studentDetails.objects.filter(courseid=courseid)
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


def downloadcsv(request,course,id):
    
    args=sessiondata(request)
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
             print courselevelid.count()
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
        students = studentDetails.objects.filter(teacherid__id=clid.id,courseid=course)
        #print clid   
        for student in students:   
		    try:
		       if int(id)==-1:
		            writer.writerow([student.roll_no,teachername,student.edxuserid.username,student.edxuserid.email])
		       else:
		             writer.writerow([student.roll_no,student.edxuserid.username,student.edxuserid.email])
		    except :
				     continue
    else:
        students = studentDetails.objects.filter(courseid=course_id)
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
def Update(request,pid,courseid,t_id):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html 
    args =sessiondata(request)
    #args = {}
    args.update(csrf(request))
    try:
       args.update(csrf(request))
       args['course']=edxcourses.objects.get(courseid=courseid).course
       courselevel=Courselevelusers.objects.get(personid=Personinformation.objects.get(id=t_id),courseid=edxcourses.objects.get(courseid=courseid),instituteid=args['institute'])
    except Exception as e:
           args['error_message'] = getErrorContent("no_unique_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    if request.method == 'POST':        
        studentDetails.objects.filter(edxuserid__username = request.POST['username'],courseid=courseid,teacherid=courselevel).update(roll_no = request.POST['roll_no'])  
        try:      
           user = iitbx_auth_user.objects.get(edxuserid = pid)
        except Exception as e:
           args['error_message'] = getErrorContent("no_pid")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
              
        return HttpResponseRedirect(students_information+courseid+'/'+t_id)
    else:
        try:
           student = studentDetails.objects.get(edxuserid__edxuserid=pid,courseid=courseid,teacherid=courselevel)
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
def upload(request,code,courseid):

   # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
   args =sessiondata(request)

   args.update(csrf(request))
   try:      
     person=Personinformation.objects.get(email=request.session['email_id'])   
     args['coursename']=edxcourses.objects.get(courseid=courseid).course
   
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
            if(extension):
                if code == "2":
                    context = validatefileinfo(request,courseid,changedfname,teacher_id)
                    context.update(args)
                    print context
                    return render(request, fileupload_, context)
            else:
                message = getErrorContent("upload_csvfile")
                form = UploadForms()
                args = {}
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

def teacherhome(request,tid):
     
# args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
    args =sessiondata(request)
    current_date=date.today()
    args.update(csrf(request))
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
        course=edxcourses.objects.get(id=request.session['edxcourseid'])
    except Exception as e:
           args['error_message'] = getErrorContent("no_edxcourse_present")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    a.append(course)
    #Context = {'courses_list': a} #send the context to the html page to display the courses
    args['courses_list'] = a
    return render_to_response(teacherhome_,args, context_instance=RequestContext(request))



############## unenroll student by updating teacher id to default teacherid =1 in studentDetails Teacher###############

def unenrollstudent(request,pid,courseid,t_id):
	# args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
	args =sessiondata(request) 
        
        try:
           edxcourses_obj=edxcourses.objects.get(courseid=courseid)
           personalinformation_obj=Personinformation.objects.get(id=1) 
           courselevelusers_obj=Courselevelusers.objects.get(personid=personalinformation_obj,courseid=edxcourses_obj).id 

        except Exception as e:
           args['error_message'] = getErrorContent("no_default_teacher"),courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
 
	studentDetails.objects.filter(edxuserid__edxuserid = pid).filter(courseid = courseid).update(teacherid =courselevelusers_obj )
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
def blendedadmin_home(request):
     input_list={}
     request.session['faculty']=0
     print "request.session['email_id']=" ,request.session['email_id']     
       #Set session parameters
     try:
       request.session['institute_id']=0
       person=Personinformation.objects.get(email=request.session['email_id'])
       print "after person object"
       institute=institute=T10KT_Institute.objects.get(instituteid=request.session['institute_id'])
       print "after institute object"
       request.session['firstname']=person.firstname
       request.session['lastname']=person.lastname 
       request.session['role_id']=1
       print "before role"
       request.session['rolename']=Lookup.objects.get(category="Role",code=1).comment
       print "after role"
       request.session['institutename']=institute.institutename
       print "after institutename"
       try:
         request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       except:
         request.session['rcid']="   " 
     except:
         input_list['error_message'] = getErrorContent("no_person_info")
         return render(request,error_,input_list)
     report_name_list=[]
     report_list=Reports.objects.filter(usertype=0).order_by("category")   #fetching all reports from database whose usertype =0
     input_list['report_list']=report_list        #names of all reports to be displayed 
     request.session['courseid']=""
     request.session['edxcourseid']=""
     print "request.session['rcid']=",request.session['rcid']
     input_list['rcid']=request.session['rcid']
     
     args=sessiondata(request)
     
     input_list.update(args)
     return render(request,admin_home_,input_list)


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



def instructoradmin(request,report_id,courseid,param_id=0):
 
        input_list={}
        flag=0
        errors=[]
        input_list['errors']=errors
        report_obj=Reports.objects.get(reportid=report_id)
        last_reportid=0
        input_list['report_name']=report_obj.report_title
        if report_obj.usertype==2:
           
             #print report,"this is report"
             subreport=report_obj.reportid.split("_")[2]
             title=report_obj.report_title
             report_id=report_obj.reportid
             course=courseid
             #print subreport,"this is subreport"
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
                print query
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

#################################### Start of grades Report ############################################################################
def grades_report(request,courseid,pid,instituteidid):
    faculty=request.session['faculty']
    args =sessiondata(request)
    args.update(csrf(request))
    try:
        course = edxcourses.objects.get(courseid = courseid).course
    except Exception as e:
        print "ERROR occured",str(e.message),str(type(e))  
        return [-1,-1]

    header=[] 
    try: 
       header=headings.objects.get(section=course).heading
    except Exception as e:
       print "Header does not exists",str(e.message),str(type(e))
    header_data=map(str,header.split(","))
    try:
      if faculty != 1:
         if int(pid)==-1:
            courselevelid=Courselevelusers.objects.filter(courseid__courseid=courseid,instituteid=instituteidid,roleid=5,startdate__lte=current,enddate__gte=current)
           
         else:
           courselevelid=Courselevelusers.objects.filter(personid__id=pid,courseid__courseid=courseid,instituteid=instituteidid,roleid=5,startdate__lte=current,enddate__gte=current)        
           teacher=str(courselevelid[0].personid.firstname)+str(courselevelid[0].personid.lastname)
        #courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,instituteid=args['institute'])
        
        #print teacher,"teacher"
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
        student_details=studentDetails.objects.filter(teacherid=clid,courseid=courseid).order_by('edxuserid__edxuserid')
        for student_detail in student_details:
           try:
              gradestable_obj=gradestable.objects.get(course=course,stud=student_detail)
           except Exception as e:
              print "grade does not exist",str(e.message),str(type(e))
           marks=(gradestable_obj.eval).split(",")
           grade=gradestable_obj.grade
           if int(pid)==-1:
               student_record.append([str(gradestable_obj.stud.roll_no),str(gradestable_obj.stud.teacherid.personid.email), str(gradestable_obj.stud.edxuserid.username),str(gradestable_obj.stud.edxuserid.email),grade,marks])
           else:
                student_record.append([str(gradestable_obj.stud.roll_no), str(gradestable_obj.stud.edxuserid.username),str(gradestable_obj.stud.edxuserid.email),grade,marks])
    else:
       try:
        student_details=studentDetails.objects.filter(courseid=courseid)
        for student_detail in student_details:
           try:
              gradestable_obj=gradestable.objects.get(course=course,stud=student_detail)
           except Exception as e:
              print "grade does not exist",str(e.message),str(type(e))
           marks=(gradestable_obj.eval).split(",")
           grade=gradestable_obj.grade
           student_record.append([str(gradestable_obj.stud.roll_no), str(gradestable_obj.stud.edxuserid.username),str(gradestable_obj.stud.edxuserid.email),grade,marks])
       except Exception as e:
         print "Error ocurred",str(e.message),str(type(e))

    request.session['grade_heading']= header_data  
    args['headings']=header_data             
    request.session['student_record']= student_record         
    args['student_record']=student_record
    args['course']=course
    args['pid']=pid
    args['instituteidid']=instituteidid
    return render(request,coursegrades_,args) 

# end grades_report
#################################### End of grades Report ############################################################################

##################################### Beginning of download grade Report #############################################################

def downloadgradecsv(request,courseid,pid):
    args =sessiondata(request)
    args.update(csrf(request))
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(course = courseid)
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
    header = [h.replace('<br>', '\n') for h in header_data]
    result=request.session['student_record']
   
    name=  "grade"+"_"+str(courseobj.id)+"_"+str(pid)+"_"+currenttime+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    
    
    if int(pid)==-1:
       count=0
       teacherheader=[]
       for i in header:
           count = count +1
           if count == 2:
              teacherheader.append("Teacher")
              teacherheader.append(i)
           else:
               teacherheader.append(i)
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
def course_faculty(request):
    args={}
    list_of_courses=[]
    faculty=1
    request.session['faculty']=faculty

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
    coursefaculty_obj=coursefaculty.objects.filter(person=person)
    no_of_courses=len(coursefaculty_obj)
    for course in coursefaculty_obj:
         
         list_of_courses.append([course.course.courseid,course.course.coursename,course.course.coursestart.date(),course.course.courseend.date()])
    if no_of_courses > 1: 
       list_of_courses.sort(key=operator.itemgetter(1),reverse=False)
       args['list_of_courses']=list_of_courses 
       args['email']= request.session['email_id']
       args['firstname']=request.session['firstname']
       args['lastname']=request.session['lastname']
       args['institutename']=request.session['institutename']
       args['rcid']=request.session['rcid']
       args['institute_id']=request.session['institute_id']
       request.session['courselist_flag']=1
       
       return render(request,facultycourseparticipation_,args)
    elif no_of_courses == 1: 
       request.session['courselist_flag']=0
       return display_instructor_report(request,course.course.courseid)    
    else:
       args['error_message'] = getErrorContent("not_valid_faculty")
       return render(request,error_,args)
    

def display_instructor_report(request,course):
    
    args ={}
    #args['course']=course
    
    #request.session['course']=course
    course_obj=edxcourses.objects.get(courseid=course)  

    args['email']=request.session['email_id']
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
    args['firstname']=request.session['firstname']
    args['lastname']=request.session['lastname']
    args['pid']=request.session['pid']
    #args['institute_id']=request.session['institute_id']

    args['institutename']=request.session['institutename']
    args['rcid']=request.session['rcid']
    args['courselist_flag']=request.session['courselist_flag']
    args['course']=course
    args['record']=record_list
    args['coursename']=course_obj.coursename 
       
    return render(request,coursefacultyreport_,args)
################################ Begin Teachers Student Report module  #################################################################
def approvedinstitute(request):
    args ={}
    args =sessiondata(request)
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
    institutecourseenroll=courseenrollment.objects.filter(instituteid=institute).order_by('courseid__course')
    for i in institutecourseenroll:
         courseenroll.append(i.courseid.course) 
    
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
    print courseid
    courseteacher=Courselevelusers.objects.filter(courseid=edxcourses.objects.get(course=courseid),instituteid=instituteid,roleid=5)
    for i in courseteacher:
        teachers.append(i.personid.email)   
    
    combineddata=[teachers,selectapinrinfo.remotecenterid.remotecenterid]
    
    #data = serializers.serialize('json',institutecourseenroll)
   
    return HttpResponse(json.dumps(combineddata), content_type="application/json")

def teacherstudent(request):
    args =sessiondata(request)
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
                 edxcourse_obj=edxcourses.objects.get(course=course)
                 if  teacher=="All Teachers":
                     student=[['Rollno','Email Id','Username',"Teacher"]]
                     args['teacher']="All Teachers"
               
                     courselevel_obj=Courselevelusers.objects.filter(courseid=edxcourse_obj,instituteid=instituteid,roleid=5) 
                     for j in courselevel_obj:
                       
                       teacherstudent=studentDetails.objects.filter(courseid=edxcourse_obj.courseid,teacherid=j,edxis_active=1)
                       for i in teacherstudent:
                             student.append([i.roll_no,i.edxuserid.email,i.edxuserid.username,i.teacherid.personid.firstname+" "+i.teacherid.personid.lastname])
                 else:
                     student=[['Rollno','Email Id','Username']]
                     person=Personinformation.objects.get(email=teacher)
                     args['teacher']=person.firstname +" "+person.lastname
                     courselevel_obj=Courselevelusers.objects.filter(courseid=edxcourse_obj,personid=person,instituteid=instituteid,roleid=5)
                     for j in courselevel_obj:
                       
                       teacherstudent=studentDetails.objects.filter(courseid=edxcourse_obj.courseid,teacherid=j,edxis_active=1)
                       for i in teacherstudent:
                             student.append([i.roll_no,i.edxuserid.email,i.edxuserid.username])
              
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
def evaluation(request,courseid,pid,instituteidid,evalflag):
    args =sessiondata(request)
    args.update(csrf(request))
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
    evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,evaluation_,args)

def quizdata(request,courseid,pid,instituteidid):
    faculty= request.session['faculty']
    args =sessiondata(request)
    args.update(csrf(request))
    header=[]
    try:
       secid=request.POST['quiz']

       evalu=evaluations.objects.filter(sectionid=secid).values('sec_name').distinct()
       args['secname']=evalu[0]['sec_name']
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
    
    ques_dict={}
    stud_rec=[]
    if faculty !=1:

      for clid in courselevelid:
    
        marks_obj=markstable.objects.filter(section=secid,stud__teacherid=clid)  #.values_list(stud.roll_no,stud.edxuserid.email,stud.edxuserid.username,eval).order_by(stud.roll_no)
        for studvalue in marks_obj:
            marks=studvalue.eval.split(",")
            total=studvalue.total
            if int(pid) == -1:
               stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.teacherid.personid.email), str(studvalue.stud.edxuserid.username),str(studvalue.stud.edxuserid.email), total,marks]) 
            else:
               stud_rec.append([str(studvalue.stud.roll_no), str(studvalue.stud.edxuserid.username),str(studvalue.stud.edxuserid.email), total,marks]) 
    else:
      try:
        stud_obj=  studentDetails.objects.filter(courseid=courseid) 
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
  





def downloadquizcsv(request,courseid,pid):
    args =sessiondata(request)
    args.update(csrf(request))
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    if int(pid) == -1:
          args['teacher']="All Teachers"
    else:
          person=Personinformation.objects.get(id=pid)
          args['teacher']= str(person.firstname)+' '+str(person.lastname)
    
    result=request.session['stud_rec']
    
    name=  "quizreport"+"_"+str(courseobj.id)+"_"+str(pid)+"_"+currenttime+'.csv'
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
def coursedescription(request,courseid,pid):
    # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid ,institute instance and person instance and use args to add your  data and send  in html
    args =sessiondata(request)
    args.update(csrf(request))
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['coursestart']=courseobj.coursestart.date()

       args['courseend']=courseobj.courseend.date()
       args['enrollstart']=courseobj.enrollstart.date()
       args['enrollend']=courseobj.enrollend.date()
    except Exception as e:
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
        evaluat=evaluations.objects.filter(course__courseid=courseid).values('sectionid','sec_name','type','due_date').order_by('sectionid').distinct()
        for eva in evaluat:
            evaluate.append([eva['sec_name'],eva['type'],eva['due_date']])

    except Exception as e:
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
def allcourses(request,courseflag):
    args =sessiondata(request)
    args.update(csrf(request))
    courseobj = edxcourses.objects.all()
    args['courseobj']=courseobj
   
    if int(courseflag)==1:
        courseid=request.POST['courseid']
        if courseid !="Select":
            return coursedescription(request,courseid,0)
        else:
              print "aa"
              args['error_message'] = getErrorContent("select_course")+"<br>"
              return render(request,'allcourses.html',args)
    
    
    return render(request,'allcourses.html',args)



##################### End admin CourseDesciption page ###############################################################################

##################### Begin of evaluation Status  module  ###########################################################################
def evalstatus(request,courseid,pid,instituteidid,evalflag):
    args =sessiondata(request)
    args.update(csrf(request))
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
  
    evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')

    if evalflag==1:
        args['error_message'] = "Please select any quiz"
    
    args['evaluation']=evaluation_obj
    return render(request,'evalstatus.html',args)

def studentstatus(request,courseid,pid,instituteidid,report):
    if request.POST:
           if request.POST['status']=="Select":
              return evalstatus(request,courseid,pid,instituteidid,1)
           request.session['secid']=request.POST['status']
    args =sessiondata(request)
    args.update(csrf(request))
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
            
            marks=markstable.objects.filter(section=secid,stud__teacherid=clid)
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
    args['secname']=evaluations.objects.filter(sectionid=secid)[0].sec_name
    ques_dict={}
    NA_stud_rec=[]; PA_stud_rec=[]; AA_stud_rec=[]
    NA_count=0; PA_count=0; AA_count=0
    
    for studvalue in marks_obj:            
            if studvalue.total=="NA":               
               NA_count=NA_count+1
               if int(pid)==-1:
                   NA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.teacherid.personid.email),str(studvalue.stud.edxuserid.email)])
               else:
                   NA_stud_rec.append([str(studvalue.stud.roll_no),str(studvalue.stud.edxuserid.email)])
            elif  studvalue.total!="NA" and "NA" in studvalue.eval:                  
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
               
    
    args['NA_count']= NA_count; args['PA_count']= PA_count ; args['AA_count']= AA_count

    if int(report) == 0:
         return render(request,'studentstatus.html',args) 
    elif int(report) == 5:
          args['stud_rec']= NA_stud_rec          
    elif int(report) == 6:          
          args['stud_rec']= PA_stud_rec           
    else:
          args['stud_rec']= AA_stud_rec 

    args['filename']='tmp/'+downloadstatucsv(request,courseid,pid,report,args['stud_rec'])    
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    request.session['stud_rec']=args['stud_rec']           
    args['heading']= heading
    command = "python "+full_path+"/manage.py collectstatic  --noinput"
    subprocess.call(command, shell=True)
    return render(request,'studentstatus.html',args)
  

def downloadstatucsv(request,courseid,pid,report,stud_rec):
    args =sessiondata(request)
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
    print name
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
def teacherstudentlist(request,institute,course,teacher):
          args =sessiondata(request)       
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
                 edxcourse_obj=edxcourses.objects.get(course=course)
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




def adminuploaderinfo(request):
   args =sessiondata(request)
   apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
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
                   courseid=edxcourses.objects.get(course=course)
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
                  args['uploaderrcid']=apinstituteid.remotecenterid.remotecenterid
                  args['courseid']=courseid.courseid
                  form = UploadForms() 
                  args['form'] = form
                  return render_to_response('adminupload.html', args)
              elif "teacherstudent" in request.POST:
                 return teacherstudentlist(request,rcidid,course,teacher)
              elif "evaluation" in request.POST:
                     faculty=0
                     request.session['faculty']=faculty
                     return evaluation(request,courseid.courseid,persid,instituteid.instituteid,0)
              elif "evaluationstatus" in request.POST:
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
                    args['error_message']= "Person is not teacher for " +str(course)+" course for given RCID"
   
    
   else:
        return render(request,"uploaderinfo.html",args)

def adminupload(request,code,courseid,teacher,rcid):
     # args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
   args =sessiondata(request)
   args.update(csrf(request))
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
                    print context
                    context.update(args)
                    
                    return render(request, fileupload_, context)
            else:
                message = getErrorContent("upload_csvfile")
                form = UploadForms()
                args = {}
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
   args['courseid']=courseid
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
def teacherdeactivation(request,courseid,pid,instituteidid):
     args =sessiondata(request)
     
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
def registrationinterface(request,args={},role=0):
    approvinstitute=[]
    designationlist=[]
    rolelist=[]
    if int(role) ==3:
       args.update(sessiondata(request))  
       apprinstitute=T10KT_Approvedinstitute.objects.get(instituteid=args['institute'])
       approvinstitute.append([apprinstitute.remotecenterid.remotecenterid,apprinstitute.id])
       args['approvinstitute']=approvinstitute
       role=Lookup.objects.filter(category = 'Role',code=5)
    
       for i in role:
           rolelist.append([i.code,i.comment])  
       args['rolelist']=rolelist  
       courselist=edxcourses.objects.filter(courseid=args['courseid'])
       args['courselist']=courselist
       args['role']=3

    else:
        apprinstitute=T10KT_Approvedinstitute.objects.all().order_by('remotecenterid__remotecenterid')
    
        for i in apprinstitute:
           approvinstitute.append([i.remotecenterid.remotecenterid,i.id])  
        args['approvinstitute']=approvinstitute
        role=Lookup.objects.filter(category = 'Role',code__gte=2).exclude(code=4)
    
        for i in role:
           rolelist.append([i.code,i.comment])  
        args['rolelist']=rolelist
        courselist=edxcourses.objects.all()
        args['courselist']=courselist
        args['role']=0
    designation=Lookup.objects.filter(category = 'Designation')
    
    for i in designation:
       designationlist.append([i.code,i.description])  
    args['designationlist']=designationlist
    
    return  render(request,"adminregister.html",args)

def register(request,role=0): 
   try:
      args=validateinterfacedata(request)
    
      if args['error_message']:
        return registrationinterface(request,args,role) 
      else:
         personexist=ifPersonExists(args['emailval'])
         if personexist==1:
            if int(args['roleval'])==5:
               return existperscourselevel(request,args)               
            else:
                return existpersInstitutelevel(request,args) 
                          
         else:
              apprvinstinstance=T10KT_Approvedinstitute.objects.get(id=args['rcidval']).instituteid
              if Institutelevelusers.objects.filter(instituteid=apprvinstinstance,roleid=args['roleval']).exists():
                  if int(args['roleval'])==2:
                     rolestring="Head"
                  else:
                      rolestring="Program Coordinator"
                  args['error_message']="Another "+str(rolestring)+ "  already exist for given "+str(apprvinstinstance.institutename)
                  return registrationinterface(request,args,role)
              else:
                   per_obj=createnewuser(args)
                   ec_id = EmailContent.objects.get(systype = 'Login', name = 'createpassword').id
                   mail_obj = EmailContent.objects.get(id=ec_id)
                   fname = per_obj.firstname
                   email = per_obj.email
                   per_id=signer.sign(per_obj.id)
                   link = ROOT_URL + mail_obj.name + '/%s' %per_id
                   message = mail_obj.message %(fname, link)  
                   send_mail(mail_obj.subject, message , DEFAULT_FROM_EMAIL ,[email], fail_silently=False)
                   args['success_message']="User account  is successfully created at http://bmwinfo.iitbombayx.in/"
                   return registrationinterface(request,args,role)
   except:
           return registrationinterface(request)

def existperscourselevel(request,args):
               apprvinstinstance=T10KT_Approvedinstitute.objects.get(id=args['rcidval']).instituteid
               pers_instance=Personinformation.objects.get(email=args['emailval'])
               course_instance=edxcourses.objects.get(id = int(args['courseval']))
               cl_obj=Courselevelusers.objects.filter(personid=pers_instance, courseid=course_instance,instituteid=apprvinstinstance)
               if cl_obj.exists():
                    if cl_obj[0].roleid==5:
                       args['error_message']="You are already teacher for "+str(course_instance.course) +" this course"
                       return registrationinterface(request,args)
                    elif cl_obj[0].roleid== -5:
                         cl_obj.update(roleid=5)   
                         args['success_message']="Activated  account of given existing user."
                         return registrationinterface(request,args)                      
               else:
                   Courselevelentry= Courselevelusers(personid=pers_instance, courseid=course_instance, instituteid=apprvinstinstance,roleid=args['roleval'],startdate= datetime.now(),enddate=default_end_date)
                   Courselevelentry.save()
                   message = "You are registered as teacher for  " +str(course_instance.course) +" for "+apprvinstinstance.institutename 
                   subject="Registered successfull for BMWinfoiitbombay"
                   send_mail(subject, message , DEFAULT_FROM_EMAIL ,[args['emailval']], fail_silently=False)
                   args['success_message']="Person is successfully created in Courseleveleveluser"
                   return registrationinterface(request,args)


def existpersInstitutelevel(request,args):
                 apprvinstinstance=T10KT_Approvedinstitute.objects.get(id=args['rcidval']).instituteid
                 pers_instance=Personinformation.objects.get(email=args['emailval'])
                 il_obj=Institutelevelusers.objects.filter(personid=pers_instance, instituteid=apprvinstinstance)
                 
                 if il_obj.exists():
                    if (il_obj[0].roleid==3 and args['roleval']==3) or (il_obj[0].roleid==2 and args['roleval']==2):
                       args['error_message']="Person for the given role  in instituteleveluser already exist"
                       return registrationinterface(request,args) 
                    elif (il_obj[0].roleid==-3 and args['roleval']==3) or (il_obj[0].roleid==-2 and args['roleval']==2):
                         if Institutelevelusers.objects.filter(instituteid=apprvinstinstance,roleid=args['roleval']).exists():
                              args['error_message']="Another person already exist for this role in this institute"
                              return registrationinterface(request,args)
                         else:
                             il_obj.update(roleid=args['roleval'])
                             args['success_message']="Activated  account of given existing user."
                             return registrationinterface(request,args)
                    else:
                         args['error_message']="You cannot create another entry for existing person in institutelevel user"
                         return registrationinterface(request,args)
                 else:
                     if Institutelevelusers.objects.filter(personid=pers_instance).exists():
                          args['error_message']="Person is already Head or Pc in some other institute"
                          return registrationinterface(request,args)
                     else:
                          Institutelevel=Institutelevelusers(personid=pers_instance, instituteid=apprvinstinstance,roleid=args['roleval'])
                          Institutelevel.save()
                          message = "You are registered  as Head or PC  "+str(args['rcidval'])
                          subject="Registered successfull for BMWinfoiitbombay"
                          args['success_message']="Person is successfully updated in Instituteleveluser"
                          return registrationinterface(request,args)         


def createnewuser(args):
              apprvinstinstance=T10KT_Approvedinstitute.objects.get(id=args['rcidval']).instituteid
              authentry=User.objects.create_user(username=args['emailval'],email=args['emailval'],password="Welcome123")
              authentry.is_active=True  
              authentry.save()   
              userprofile=Userlogin(user=authentry,status=0)
              userprofile.save()
              person_obj=Personinformation(email=args['emailval'],firstname = args['firstname'], instituteid=apprvinstinstance,lastname =args['lastname'],designation=args['designationval'],createdondate=datetime.now(),telephone1=0)
     
              person_obj.save() 
              if args['roleval']==5:
                 Courselevelentry= Courselevelusers(personid=person_obj, courseid=edxcourses.objects.get(id = int(args['courseval'])),instituteid=apprvinstinstance,roleid=args['roleval'],startdate= datetime.now(),enddate=default_end_date)
                 Courselevelentry.save()
              else:
                   Institute_level=Institutelevelusers(personid=person_obj,instituteid = apprvinstinstance,roleid =args['roleval'],startdate= datetime.now(),enddate=default_end_date)
                   Institute_level.save() 
                
              print "New user registration done"
              return person_obj

def validateinterfacedata(request):
    args={}
    args['firstname']=firstname=request.POST['firstname']
    args['lastname']=lastname=request.POST['lastname']
    args['emailval']=emailval=request.POST['email']
    args['rcidval']=rcidval=int(request.POST['Institute'])
    args['designationval']=designationval=int(request.POST['designation'])
    args['roleval']=roleval=int(request.POST['role'])
    args['courseval']=courseval=int(request.POST['course'])
    fname=validateFname(firstname)
    lname=validateLname(lastname)
    personexist=ifPersonExists(emailval)
    args['error_message']=""
    if fname==0:
       args['error_message']="Enter valid firstname."
    if lname==0:
       args['error_message'] +="</br>Enter valid firstname."
    #if personexist==1:
       #args['error_message'] +="</br>Person already exists"
    if rcidval==-1:
       args['error_message'] +="</br>Please select Institute."
    if designationval==-1:
       args['error_message'] +="</br>Please select Designation."
    if roleval==-1:
       args['error_message'] +="</br>Please select Role."
    else:
         if roleval==5:
             if courseval==-1:
                  args['error_message'] +="</br>Please select Course."
         
    return args


def instiname(request):
    instituteid=request.GET['id']
    args ={}
    institutename=T10KT_Approvedinstitute.objects.get(id=instituteid).instituteid.institutename
    
    return HttpResponse(json.dumps(institutename), content_type="application/json")



########################  End of admin registrationinterface ########################################################################
########################  Begin of Bulkmove module           ########################################################################

def bulkmove(request,courseid,persid,instituteid):
    course_inst=edxcourses.objects.get(courseid=courseid) 
    pers_inst=Personinformation.objects.get(id=persid)
    course_filt_obj=Courselevelusers.objects.filter(instituteid__instituteid=instituteid,courseid=course_inst,roleid=5).exclude(personid=pers_inst)
    teacher_list=[]
    args=sessiondata(request)
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

def bulkmoveupdate(request,courseid,persid,instituteid):
    args=sessiondata(request)
    newteacher= request.POST['newteacher']
    pers_inst=Personinformation.objects.get(id=persid)
    updatedby=Personinformation.objects.get(id=request.session['person_id'])
    new_teacher=Courselevelusers.objects.get(id=newteacher)
    course_obj=edxcourses.objects.get(courseid=courseid) 
    old_teacher=Courselevelusers.objects.get(personid=pers_inst,instituteid__instituteid=instituteid,courseid=course_obj,roleid=5)
    args['oldteacher_initcount']=studentDetails.objects.filter(courseid=courseid,teacherid=old_teacher).count()
    studentDetails.objects.filter(courseid=courseid,teacherid=old_teacher).update(teacherid=new_teacher,last_update_on=datetime.now(),last_updated_by=updatedby)
    oldteachcount=studentDetails.objects.filter(courseid=courseid,teacherid=old_teacher)
    newteachcount=studentDetails.objects.filter(courseid=courseid,teacherid=new_teacher)
    args['studcountnewteach']= newteachcount.count()
    args['studcountoldteach']=oldteachcount.count()
    args['newteachemail']= new_teacher.personid.firstname+" "+new_teacher.personid.lastname
    args['oldteachemail']=pers_inst.firstname+" "+pers_inst.lastname
    rcidid=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=instituteid).id
    #return teacherstudentlist(request,rcidid,course_obj.course,new_teacher.personid.email)
    return render(request,"bulkmovesummary.html",args)   

########################  End of Bulkmove module           ########################################################################


########################  Begin of teacher unenroll module ########################################################################

def teacherunenroll(request,courseid,tid):
     
# args contain  default data of session with  these parameter institutename,firstname,lastname,email,role_id,rolename,rcid,courseid,edxcourseid and use args to add your  data and send  in html 
    args =sessiondata(request)
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

def courseadminhome(request):

    return manualupload(request)



def manualupload(request):
    args={}
    try:
       args['email']=request.session['email_id']
       person=Personinformation.objects.get(email=request.session['email_id'])       
       institute=institute=T10KT_Institute.objects.get(instituteid=0)      
       args['firstname']=request.session['firstname']=person.firstname
       args['lastname']=request.session['lastname']=person.lastname        
       args['institutename']=request.session['institutename']=institute.institutename       
       args['rcid']=request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       
    except:
         input_list['error_message'] = getErrorContent("no_person_info")
         return render(request,error_,input_list)

    args.update(csrf(request))
    try:
      if request.POST:
         value=request.FILES['usermanual']
         if not value.name.endswith('.pdf'):
            args['error_message'] =  "Please upload valid pdf only"
         elif str(value) != "BM_User_Manual.pdf":
              args['error_message'] =  "Please upload file with file name BM_User_Manaual"
         else:
              savenewfile(request.FILES['usermanual'])
              args['successmsg'] =  "File uploaded successfully"
    except:
          args['error_message'] =  "Please select file."
    return render_to_response("manualupload.html",args,context_instance=RequestContext(request))


def savenewfile(filed):
   
    filename = filed._get_name()
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    dirpath=os.path.join(full_path,'static/BM_User_Manual.pdf')
    newname=os.path.join(full_path,'static/BM_User_Manual'+str(currenttime)+'.pdf',)
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
def facultygenericinterface(request,courseid):
   args =sessiondata(request)
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
                 return teacherstudentlist(request,rcidid,course,teacher)
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
                    args['error_message']= "Person is not teacher for " +str(course)+" course for given RCID"
   
    
   else:
        return render(request,"facultygeneric.html",args)

########################  End of faculty generic interface module   ##################################################################### 


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




############################ Begin of   Evaluation option selected module #########################################################


def evaluationoption(request,courseid,pid,instituteidid,evalflag):
    args =sessiondata(request)
    
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
    evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,"evaluationoption.html",args)




def quizanswers(request,courseid,pid,instituteidid):

    args =sessiondata(request)
    report=[]
    header=[]
    try:
       secid=request.POST['quiz']

       evalu=evaluations.objects.filter(sectionid=secid).values('sec_name').distinct()
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
         sqlstmt= '''SELECT "1" id,student_id,username,email,module_id,concat(replace(if(ans1 like '"{%%%%',"",if(ans1 like '"i4x-%%%%' ,"",if( ans1 like '%%%%"[[%%%%',"",if(ans1 like '%%%%[{%%%%',"",ans1)))),'"',''),'\n',
         replace(if(ans2 like '%%%%{%%%%',"",if(ans2 like 'i4x-%%%%' ,"",if( ans2 like '%%%%[[%%%%',"",if(ans2 like '%%%%[{%%%%',"",ans2)))),'"','')) answer FROM
          (SELECT module_id, student_id,  substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2
 FROM edxapp.courseware_studentmodule where module_type=%s and module_id in (%s) and course_id=%s and grade is not null ) a,
  auth_user b where   a.student_id=b.id order by student_id''' %('"'+"problem"+'"',sqlmod,'"'+str(courseobj.courseid)+'"')
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
    #print stud_rec
    args['headings']=heading
    args["report_name"]=report_name
    return render(request,"answer.html",args)


############################ End of option selected module   ######################################################################
      

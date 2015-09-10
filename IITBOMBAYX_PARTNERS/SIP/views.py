'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''
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
from SIP.validations import *
from django.utils import timezone
import glob 
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
#############################end of import statements by student management#######################################
current=timezone.now
default_password="Welcome123"

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
    args['rolename']=request.session['rolename']
    args['rcid']=request.session['rcid']  
    args['courseid']= request.session['courseid']
    
    args['edxcourseid']=request.session['edxcourseid']
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
                   
                   return HttpResponseRedirect(blendedadminhome_)
               elif user_info.usertypeid==2:
                    
                   return HttpResponseRedirect(facultyreport_)
               else:
                   return HttpResponseRedirect(get_multi_roles_)
            else:               
                return loginn(request)
    except:
                    
            return loginn(request)

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
             return HttpResponseRedirect(blendedadminhome_)
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
    #print emailid
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
		del request.session['person_id']
		del request.session['email_id']
		del request.session['institute_id']
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
    try:
       for index in enrolled_courses:
		  edx_enrolled_courses.append(edxcourses.objects.get(courseid=index.courseid.courseid))
    except Exception as e:
           args['error_message'] = getErrorcontent("no_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

    input_list['courselist'] = edx_enrolled_courses
    input_list['cid']=args['edxcourseid']
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
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
    except Exception as e:
           args['error_message'] = getErrorContent("no_course_entry")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['personid']=request.session['person_id']

    try:
        courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,startdate__lte=current,enddate__gte=current)
    except Exception as e:
           args['error_message'] = getErrorContent("not_valid_teacher")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    students = studentDetails.objects.filter(teacherid__id=courselevelid.id,courseid=courseid)
    data=[]    
    for student in students:   
		try:

			data.append([student.edxuserid.pk,student.roll_no,student.edxuserid.username,student.edxuserid.email])
		except :
				continue
                
    data.sort()  
    args['info']=data
    args['id'] = pid
    return render_to_response(studentdetails_,args,RequestContext(request))


def downloadcsv(request,course,id):
   
    args=sessiondata(request)
    name=args['person'].firstname+"_"+course+"  student_details"+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    writer.writerow(["RollNumber", "UserName","Email"])     
     
    try:
        courselevelid=Courselevelusers.objects.get(personid__id=id,courseid__courseid=course,startdate__lte=current,enddate__gte=current)
    except Exception as e:
           args['error_message'] = getErrorContent("not_valid_teacher")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    students = studentDetails.objects.filter(teacherid__id=courselevelid.id,courseid=course)
    data=[]    
    for student in students:   
		try:

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
                    #print context
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
    try:
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
     #print "request.session['email_id']=" ,request.session['email_id']     
       #Set session parameters
     try:
       request.session['institute_id']=0
       person=Personinformation.objects.get(email=request.session['email_id'])
       #print "after person object"
       institute=institute=T10KT_Institute.objects.get(instituteid=request.session['institute_id'])
       #print "after institute object"
       request.session['firstname']=person.firstname
       request.session['lastname']=person.lastname 
       request.session['role_id']=1
       #print "before role"
       request.session['rolename']=Lookup.objects.get(category="Role",code=1).comment
       #print "after role"
       request.session['institutename']=institute.institutename
       #print "after institutename"
       try:
         request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       except:
         request.session['rcid']="   " 
     except:
         input_list['error_message'] = getErrorContent("no_person_info")
         return render(request,error_,input_list)
     report_name_list=[]
     report_list=Reports.objects.filter(usertype=0).order_by("report_title")   #fetching all reports from database whose usertype =0
     input_list['report_list']=report_list        #names of all reports to be displayed 
     request.session['courseid']=""
     request.session['edxcourseid']=""
     #print "request.session['rcid']=",request.session['rcid']
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
              reports.append(record)   
        input_list['heading']=reports.pop(0)
        input_list['reports']=reports
        

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
               query=report_obj.sqlquery %(course,course) 
               flag=2 
             elif subreport == "C" :
               query=report_obj.sqlquery %(course,course)
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
               # print query
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
def grades_report(request,courseid,pid):
    args =sessiondata(request)
    args.update(csrf(request))
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    args['teacher']= str(args['firstname'])+' '+str(args['lastname'])
    
    #print "institute =",args['institutename']
    try:
        courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,startdate__lte=current,enddate__gte=current)
    except Exception as e:
           args['error_message'] = getErrorContent("teacher_not_valid"),courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    result=get_grades_report(courseobj,courselevelid)
    request.session['result']=result
    if (result[0][0] != -1):
         args['heading']=result[0]
         args['grade_data']=result[1]
         
         args['error_message'] =' '.join(map(str, result[0]))
         #print args['error_message']
         return render(request,coursegrades_,args) 
    else:
         args['error_message'] =str(result[1][0])+"\n"+ str(result[1][1])
         return render(request,error_,args)  
    

# end grades_report
#################################### End of grades Report ############################################################################

##################################### Beginning of download grade Report #############################################################

def downloadgradecsv(request,courseid,pid):
    args =sessiondata(request)
    args.update(csrf(request))
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['teacher']= str(args['firstname'])+' '+str(args['lastname'])
    
    result=request.session['result']

    name=  "grade"+"_"+str(courseobj.id)+"_"+str(pid)+"_"+currenttime+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    count=1
    for data in result:
            if count==1:
                count = count +1
                writer.writerow(data)
                
            else:
                for row in data:
                    writer.writerow(row)   
    return response
##################### End of download grade report ####################################################################################
def course_faculty(request):
    args={}
    list_of_courses=[]
    try:
        person=Personinformation.objects.get(email=request.session['email_id'])
        request.session['firstname']=person.firstname
        request.session['lastname']= person.lastname
        request.session['role_id']=1
        remote_center=T10KT_Remotecenter.objects.get(instituteid=person.instituteid)
        request.session['rcid']=remote_center.remotecenterid
        
        institute=T10KT_Institute.objects.get(instituteid=person.instituteid_id)
        request.session['institutename']=institute.institutename

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
    args['course']=course
    
    #request.session['course']=course
    

    args['email']=request.session['email_id']
    
    report_list=Reports.objects.filter(usertype=2).order_by("reportid")
    record=[]
    for report in report_list:
       record.append(report.reportid)
       args['title']=report.report_title
    args['firstname']=request.session['firstname']
    args['lastname']=request.session['lastname']
    #args['institute_id']=request.session['institute_id']
    args['institutename']=request.session['institutename']
    args['rcid']=request.session['rcid']
    args['courselist_flag']=request.session['courselist_flag']
    args['course']=course
    args['record']=record
       
    return render(request,coursefacultyreport_,args)
################################ Begin Teachers Student Report module  #################################################################
def approvedinstitute(request):
    args ={}
    args =sessiondata(request)
    apprinstitute=T10KT_Approvedinstitute.objects.all().exclude(remotecenterid__remotecenterid=0).order_by('remotecenterid__remotecenterid')
    approvinstitute=[]
    for i in apprinstitute:
         approvinstitute.append([i.remotecenterid.remotecenterid,i.id])  
    args['approvinstitute']=approvinstitute
    return render(request,listofinstitute_,args)  
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
    instituteid=T10KT_Approvedinstitute.objects.get(id=instituteid).instituteid
    #print courseid
    courseteacher=Courselevelusers.objects.filter(courseid=edxcourses.objects.get(course=courseid),instituteid=instituteid)
    for i in courseteacher:
        teachers.append(i.personid.email)   
    
    
    
    #data = serializers.serialize('json',institutecourseenroll)
   
    return HttpResponse(json.dumps(teachers), content_type="application/json")


def teacherstudent(request):
    args =sessiondata(request)
    if request.method == 'POST':
       try:
          institute=request.POST['Institute']
          course=request.POST['Course']
          teacher=request.POST['Teacher']
    
          
          apprinstitute=T10KT_Approvedinstitute.objects.all().exclude(remotecenterid__remotecenterid=0).order_by('remotecenterid__remotecenterid')
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
                     student=[['Rollno','Email','Username',"Teacher"]]
                     args['teacher']="All Teachers"
               
                     courselevel_obj=Courselevelusers.objects.filter(courseid=edxcourse_obj,instituteid=instituteid) 
                     for j in courselevel_obj:
                       
                       teacherstudent=studentDetails.objects.filter(courseid=edxcourse_obj.courseid,teacherid=j,edxis_active=1)
                       for i in teacherstudent:
                             student.append([i.roll_no,i.edxuserid.email,i.edxuserid.username,i.teacherid.personid.firstname+" "+i.teacherid.personid.lastname])
                 else:
                     student=[['Rollno','Email','Username']]
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
          return render(request,listofinstitute_, args)
       except Exception as e:
           
           args['error_message'] = getErrorContent("select_all")+"\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    else:
         return approvedinstitute(request)
################################ End Teachers Student Report module   #########################################################

##################### Begin of evaluation module   ####################################################################################
def evaluation(request,courseid,pid,evalflag):
    args =sessiondata(request)
    args.update(csrf(request))
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    args['teacher']= str(args['firstname'])+' '+str(args['lastname'])    
    try:
        courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,startdate__lte=current,enddate__gte=current)
    except Exception as e:
           args['error_message'] = getErrorContent("teacher_not_valid"),courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    evaluation_obj=evaluations.objects.filter(course=courseobj,due_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,evaluation_,args)

def quizdata(request,courseid,pid):
    args =sessiondata(request)
    args.update(csrf(request))
    try:
       secid=request.POST['quiz']
       evalu=evaluations.objects.filter(sectionid=secid).values('sec_name').distinct()
       args['secname']=evalu[0]['sec_name']
    except Exception as e:
           return evaluation(request,courseid,pid,1)
    try:
        courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,startdate__lte=current,enddate__gte=current)
    except Exception as e:
           args['error_message'] = getErrorContent("teacher_not_valid"),courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
       args['teacher']= str(args['firstname'])+' '+str(args['lastname'])
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    heading = ["Rollno","Username","Email","Avg <br>M.M:1.0","Total"]
    ques_dict={}
    evaluation_obj=questions.objects.filter(course=courseobj,eval__sectionid=secid).exclude(q_weight=0 ).order_by('id')
    count=0
    totalweight=0
    not_attempt=[]
    for evaluate in evaluation_obj:
         count=count+1
         totalweight=totalweight+evaluate.q_weight
         quesname="Q"+str(count).zfill(2)+"<br>MM:"+str(evaluate.q_weight)
         heading.append(quesname)
         ques_dict[evaluate.qid]=count-1
        
         not_attempt.append("NA")
         
    heading[4]=heading[4]+"<br>MM:"+str(totalweight)
  
    data=[]
    #print heading
    request.session['heading']= heading
    args['heading']=heading
    stud_list = studentDetails.objects.filter(teacherid=courselevelid,courseid=courseid)
    grade_list=[]
    stud_rec=[]
    for studvalue in stud_list:
                totalmark=0.0
                avgmarks=0.0                
                quiz_res=result.objects.filter(edxuserid=studvalue.edxuserid.edxuserid,question__eval__sectionid=secid).exclude(question__q_weight=0 ).order_by('question__id')
                quizdata=[]
                for res in quiz_res:
                     
                     quizmark=(res.grade/res.maxgrade)*res.question.q_weight
                     totalmark=totalmark+quizmark
                     while (len(quizdata)<ques_dict[res.question.qid]):
                       quizdata.append("NA")
                     quizdata.append(round(quizmark,2))
                #print quizmark,studvalue.edxuserid.edxuserid
                total=str(round(totalmark,2)) 
                try:
                   avgmarks=totalmark/totalweight
                except:
                       avgmarks=0.0
                if quizdata == []:
                     quizdata=not_attempt
                     total="NA"
                while len(quizdata)<count:
                     quizdata.append("NA")
                     
                	 	
                stud_rec.append([str(studvalue.roll_no), str(studvalue.edxuserid.username),str(studvalue.edxuserid.email), round(avgmarks,2),total,quizdata])
                
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
    args['teacher']= str(args['firstname'])+' '+str(args['lastname'])
    
    result=request.session['stud_rec']

    name=  "quizreport"+"_"+str(courseobj.id)+"_"+str(pid)+"_"+currenttime+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    heading=request.session['heading']
    heading = [h.replace('<br>', '\n') for h in heading]
    
    writer.writerow(heading)
    for data in result:
                count=0
                createrow=[]
                for row in data:
                    count=count+1
                    if count<=5:
                       createrow.append(row)
                    else:
                         for r in row: 
                           
                           createrow.append(r)
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
       args['coursestart']=courseobj.coursestart
       args['courseend']=courseobj.courseend
       args['enrollstart']=courseobj.enrollstart
       args['enrollend']=courseobj.enrollend
    except Exception as e:
           args['error_message'] ="cannot get entry for course"
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    policy=[["Type","Abbreviation","Drop-Count","Total","Weight","Comment"]]
    criteria=[["Grade","Min","Max"]]
    evaluate=[["Assignment","Assignment Type","Due Date"]]
    try:
        grpolicy=gradepolicy.objects.filter(courseid__courseid=courseid)
        for gp in grpolicy:
            if gp.drop_count==0:
                policy.append([gp.type,gp.short_label,gp.drop_count,gp.min_count,(gp.weight),""])
            else:
                 policy.append([gp.type,gp.short_label,gp.drop_count,gp.min_count,(gp.weight),"Best of "+str((gp.min_count-gp.drop_count))])
        grcriteria=gradescriteria.objects.filter(courseid__courseid=courseid).values('cutoffs','grade').order_by('cutoffs').reverse().distinct()
        l=len(grcriteria)
        for  gc in range(0,len(grcriteria)):
             # print grcriteria,gc
              if gc==0:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs'],1])
              else:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs'],grcriteria[gc-1]['cutoffs']])
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
              #print "aa"
              args['error_message'] = getErrorContent("select_course")+"<br>"
              return render(request,'allcourses.html',args)
    
    
    return render(request,'allcourses.html',args)



##################### End admin CourseDesciption page ###############################################################################


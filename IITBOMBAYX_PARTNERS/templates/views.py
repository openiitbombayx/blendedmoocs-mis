from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.core.mail import send_mail
import datetime
from django.db import transaction
from django.contrib import auth
from django.template import Context
##ketaki
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User
#from SIP.models import Userlogin,ErrorContent
from SIP.validations import retrieve_error_message,validate_login,validate_email,password_reset
from django.core.mail import send_mail

#importing the PersonInformation Class from models.py
from .models import *


#importing the validations from validations.py
from .validations import *
############## Login by Ketaki###################################

@csrf_protect

def loginn(request):
    page = 'Login'
    module = 'Registration'
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        
	
        list1 = validate_login(request)
        
        if (list1!=-1):      
            
            args['institutename']=list1[1]            
            args['firstname']=list1[2]
            args['lastname']=list1[3]
            #return render_to_response('login/login_success.html',args)
            return ccourse(request)
        else:
            error_message=retrieve_error_message (module,page,'LN_INV')
            args = {}
            args.update(csrf(request))
            args['error_message']=error_message
            return render_to_response('login/tologin.html',args)            

            #return HttpResponseRedirect('/login_success/')
    args = {}
    args.update(csrf(request))        
    return render_to_response('login/tologin.html',args)
           
   
def forgot_pass(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        email = request.POST['email']
        emailid= validate_email(email)
        if emailid != -1:            
            link = 'http://127.0.0.1:9005/resetpass/%d' %emailid
            email_subject = 'Reset Password'
            email_body = "Hey %s,  To Reset your Password, click this link within \
            48hours http://127.0.0.1:9005/resetpass/%d"
            send_mail(email_subject, email_body, 'myemail@example.com',[email], fail_silently=False)
            print link
            args['message']=  "We've mailed you the instructions"
            return render_to_response('login/forgot_pass.html',args)                
            #return HttpResponseRedirect('/homepage/')
        else:
            args['message']="Unregistered email"
            return render_to_response('login/forgot_pass.html',args)                
    
    return render_to_response('login/forgot_pass.html',args)
    
 
def home(request):
    
    args = {}
    args.update(csrf(request))
    return render_to_response('login/home.html',args)


def resetpass(request,emailid):
    if request.method == 'POST':
        args = {}
        args.update(csrf(request))
        pwd1 = request.POST.get('new_password1','')
        pwd2 = request.POST.get('new_password2','')
        if pwd1!=pwd2:
            args = {}
            args.update(csrf(request))
            args['message']= "Password didn't match. Please enter again!!"
            return render_to_response('login/resetpass.html',args)
        else:
            password_reset(emailid,pwd1)
            args = {}
            args.update(csrf(request))
            args['message']= "Password changed successfully!!!"
            return render_to_response('login/home.html',args)            
    args = {}
    args.update(csrf(request))
    return render_to_response('login/resetpass.html',args)
    

    
def logout(request):
    del request.session['person_id']
    del request.session['email_id']
    del request.session['institute_id']
    args = {}
    args.update(csrf(request))
    return HttpResponseRedirect('/homepage/')





####################End Ketaki module############################



#################	Apoorva		Agrawal		########################################################
################################################################################################################

def headhome(request, hoi_pid = 5):
	args = {}
	args.update(csrf(request))
	hoi_obj = Personinformation.objects.get(id = hoi_pid)
	args['viewer'] = hoi_obj
	return render(request, 'head/home.html', args)

#########################################################################################################################################################
###############		Program Coordinator Delegation Page 	#########################################################################

@transaction.atomic
def pc(request):				#right now the only hoi in my database has the id = 5, change to match yours
	error = []
	if request.method == 'POST':
		getemail = request.POST.get('email', '')
		getfirstname = request.POST.get('firstname', '')
		getlastname = request.POST.get('lastname', '')
		getstartdate = request.POST.get('startdate','')
		getenddate = request.POST.get('enddate', '')

		hoi_obj = Personinformation.objects.get(id = hoi_pid)

		args = {'error_message': error,'firstname': getfirstname, 'lastname' : getlastname, 'email' : getemail, 'hoi_pid' : hoi_pid, 'hoi':hoi_obj, 'startdate':getstartdate, 'enddate':getenddate}

		args.update(csrf(request))
		
		if not validateEmail(getemail):
			error.append(ErrorContent.objects.get(errorcode = 'email').error_message)
			return render_to_response('head/programcoordinator.html', args)

		if Personinformation.objects.filter(email = getemail):
			error.append(ErrorContent.objects.get(errorcode = 'regemail').error_message)
			return render_to_response('head/programcoordinator.html', args)
		if not getfirstname:
			error.append(ErrorContent.objects.get(errorcode = 'firstname').error_message)
			return render_to_response('head/programcoordinator.html', args)
	
		if not getlastname:
			error.append(ErrorContent.objects.get(errorcode = 'lastname').error_message)
			return render_to_response('head/programcoordinator.html', args)
	
		if not getstartdate:
			error.append(ErrorContent.objects.get(errorcode = 'invsdate').error_message)
			return render_to_response('head/programcoordinator.html', args)

		if not getenddate:
			error.append(ErrorContent.objects.get(errorcode = 'invedate').error_message)
			return render_to_response('head/programcoordinator.html', args)

		if getstartdate >= getlastdate:
			error.append(ErrorContent.objects.get(errorcode = 'invdur').error_message)
			return render_to_response('head/programcoordinator.html', args)
		
		
				
	
		inst_obj = T10KT_Approvedinstitute.objects.get(id = 2)
		
		x = Personinformation(firstname = getfirstname, lastname = getlastname, email = getemail, instituteid = inst_obj)
		x.save()
		
		lookup_obj = T10KT_Lookup.objects.get(code = 4, category='Designation')
		y = Institutelevelusers(personid=x, instituteid=inst_obj, roleid=lookup_obj, startdate=getenddate, enddate=getenddate)
		y.save()

		args = {}
		args.update(csrf(request))

		return thanks(request, inst_obj, hoi_obj)


	args = {}
	hoi_obj = Personinformation.objects.get(id = hoi_pid)
	args['hoi'] = hoi_obj
	args.update(csrf(request))
	return render_to_response('head/programcoordinator.html', args)

######################################################################################################################################################


####################Temporary Function ############################ Should be replaced #####################

def thanks(request, inst_obj, hoi_obj):
	data = Institutelevelusers.objects.filter(instituteid = inst_obj).order_by('startdate')
	return render(request, 'head/thanks.html', {'pc_data':data, 'hoi':hoi_obj})

############################################################################################################




########################################################################################################################

def team(request):
        viewer_pid= request.session['person_id']   		#right now the i'm assuming to be logged with id=5 in personinformation, change to match yours
	args = {}
	args.update(csrf(request))

	teammembersclu = Courselevelusers.objects.all().order_by('roleid')
	teammembersilu = Institutelevelusers.objects.all().order_by('roleid')
	viewer = Personinformation.objects.get(id = viewer_pid)
	
	#teammembersclu = Courselevelusers.objects.filter(instituteid = 1).order_by('roleid')
	#teammembersilu = Institutelevelusers.objects.filter(instituteid = 1).order_by('roleid')
	
	args['team1']= teammembersilu
	args['team2'] =  teammembersclu
	args['viewer_pid'] = viewer_pid
	args['viewer'] = viewer
	return render_to_response('head/team.html', args)



##############################################	Email 	Utility	###################################################################

def sendmail(request, sender_pid = 0, receiver_pid = 0):
	args = {}
	args.update(csrf(request))
	
	try:
		args['viewer'] = Personinformation.objects.get(id = sender_pid)
	except:
		args['viewer'] = Personinformation.objects.get(id = 5)			#dummy 
	
	if request.method == 'POST':
		args['sender'] = request.POST.get('sender', '')
		args['receiver'] = request.POST.get('receiver', '')
		args['subject'] = request.POST.get('subject', '')
		args['body'] = request.POST.get('body', '')

		if not validateEmail(args['sender']):
			args['error_message'] = ErrorContent.objects.get(errorcode = 'incsemail').error_message
			return render(request, 'head/sendmail.html', args)

		if not validateEmail(args['receiver']):
			args['error_message'] = ErrorContent.objects.get(errorcode = 'incremail').error_message
			return render(request, 'head/sendmail.html', args)

		if not args['subject']:
			args['error_message'] = ErrorContent.objects.get(errorcode = 'submis').error_message
			return render(request, 'head/sendmail.html', args)

		if not args['body']:
			args['error_message'] = ErrorContent.objects.get(errorcode = 'bodymis').error_message
			return render(request, 'head/sendmail.html', args)

		
		send_mail(args['subject'], args['body'], args['sender'], [args['receiver']])
		return HttpResponse('Your Email has been sent')
	
	else:
		if sender_pid and receiver_pid:
					
			try:
				sender = Personinformation.objects.get(id = sender_pid)
				receiver = Personinformation.objects.get(id = receiver_pid)
				args['sender'] = sender.email
				args['receiver'] = receiver.email
		
				return render(request, 'head/sendmail.html', args)
			
			except:
				args['sender'] = ErrorContent.objects.get(errorcode = 'invemail').error_message
				args['receiver'] = ErrorContent.objects.get(errorcode = 'invemail').error_message
				
				return render(request, 'head/sendmail.html', args)
	
		return render(request, 'head/sendmail.html', args)
	return render(request, 'head/sendmail.html', args)
	
	
###################################### Apoorva Code End #####################################################################






########################################### Deepak Code ######################################################################

def home(request):
	return render(request,'base2.html')

##############################################################################################################################################
def enrollfinal(request,course,years):
	errors = []	
	if request.method=='POST':
		args = {}
		args.update(csrf(request))
		args['errors'] = errors
		args['coursename'] = request.POST.get('coursename','')
		args['startdate'] = request.POST.get('startdate','')
		args['enddate'] = request.POST.get('enddate','')
		args['astud'] = request.POST.get('astud','')
		args['astudp'] = request.POST.get('astudp','')
		args['program'] = request.POST.get('program','')
		args['year'] = request.POST.get('year','')
		args['comments'] = request.POST.get('comments','')
		enrollformvalidation(args)		
		
		if not args['errors']:
			#cid=request.POST.get('cid','')
			ccname=args['coursename']
			start=args['startdate']
			end=args['enddate']
			prog=args['program']
			year=args['year']
			stud=args['astud']
			studp=args['astudp']
			comment=args['comments']
			x=courseenrollment(corresponding_course_name=ccname, start_date=start, end_date=end, program=prog, year=year, total_moocs_students=stud, total_course_students=studp, status="1", comments=comment, courseid='IITBombayX/course/years', instituteid = request.session['instituteid'],enrolledby=request.session['personid'])
			x.save()
			return render(request,'/SIP/enrolled/course',args)
	args = {}
	args.update(csrf(request))
	args['institutename']=T10KT_Institute.objects.get(instituteid=request.session['instituteid']).institutename
	args['name']=edxcourses.objects.get(course=course,year=years).name
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	return render(request,'course/enrollfinal2.html', args)

##############################################################################################################################################


def unenroll(request,course,year):
	errors=[]
	args = {}
	args.update(csrf(request))
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	if request.method=='POST':
		args['reason']=request.POST.get('reason','')
		unenrollvalidation(errors)
		args['errors'] = errors
		if not args['errors']:
			courseenrollment.objects.get(course=course,year=year,status="1",instituteid=request.session['instituteid']).update(reason_of_cancelation=reason,status="0",cancelled_date=date.today(),cancelledby=request.session['person_id'])
			return HttpResponseRedirect('/SIP/unenrolled/')
	return render(request,'course/unenroll/course/year.html', args)


def enrolled(request,course):
	args = {}
	args.update(csrf(request))
	args['institutename']=T10KT_Institute.objects.get(instituteid=request.session['institute_id']).institutename
	args['coursename']=course
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	return render(request,'course/enrolled.html', args)


def unenrolled(request):
	args = {}
	args.update(csrf(request))
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	return render(request,'course/unenrolled.html', args)


def ccourse(request):
	args = {}
	args.update(csrf(request))
	a=courseenrollment.objects.filter(status='1', instituteid=request.session['institute_id'])
	p=[]
	for i in a:
		p.append(edxcourses.objects.get(courseid=i.courseid))
	args['courselist'] = p
	x=Personinformation.objects.get(email=request.session['email_id'])
	args['firstname']=x.firstname
	args['lastname']=x.lastname
	args['institutename']=T10KT_Institute.objects.get(instituteid=request.session['institute_id']).institutename
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	'''if args['roleid']==4:
		return to cc page
	if args['roleid']==5:
		return to ta page'''
	return render(request,'course/enrolledcoursesfinal.html', args)

def allcourses(request):
	args = {}
	args.update(csrf(request))
	args['allcourses'] = edxcourses.objects.all()
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	return render(request,'course/allcourses.html',args)

def updatecourses(request,course,year):
	errors = []	
	if request.method=='POST':
		args = {}
		args.update(csrf(request))
		args['errors'] = errors
		args['coursename'] = request.POST.get('coursename','')
		args['startdate'] = request.POST.get('startdate','')
		args['enddate'] = request.POST.get('enddate','')
		args['astud'] = request.POST.get('astud','')
		args['astudp'] = request.POST.get('astudp','')
		args['program'] = request.POST.get('program','')
		args['year'] = request.POST.get('year','')
		args['comments'] = request.POST.get('comments','')
		enrollformvalidation(args)		
		
		if not args['errors']:
			#cid=request.POST.get('cid','')
			ccname=args['coursename']
			start=args['startdate']
			end=args['enddate']
			prog=args['program']
			year=args['year']
			stud=args['astud']
			studp=args['astudp']
			comment=args['comments']
			x=courseenrollment.objects.get(courseid='IITBombayX/course/year',instituteid=request.session['institute_id']).update(corresponding_course_name=ccname, start_date=start, end_date=end, program=prog, year=year, total_moocs_students=stud, total_course_students=studp, status="1", comments=comment, courseid='IITBombayX/course/years', instituteid = request.session['instituteid'],enrolledby=request.session['personid'])
			x.save()
			return render(request,'/SIP/updated/course',args)
	args = {}
	args.update(csrf(request))
	x=courseenrollment.objects.get(courseid='IITBombayX/course/year',instituteid=request.session['institute_id'])
	args['coursename'] = x.corresponding_course_name
	args['startdate'] = x.start_date
	args['enddate'] = x.end_date
	args['astud'] = x.total_moocs_students
	args['astudp'] = x.total_course_students
	args['program'] = x.program
	args['year'] = x.year
	args['comments'] = x.comments
	args['coursename']=edxcourses.objects.get(course=course,year=years).coursename
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	return render(request,'course/updatefinal.html', args)

def updated(request,course):
	args={}
	args.update(csrf(request))
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	args['course']=course
	return render(request,'course/updated.html',args)

def course(request,course,year):
	args = {}
	args.update(csrf(request))
	ccourseid="IITBombayX/course/year"
	args['course'] = edxcourses.objects.get(courseid=ccourseid)
	args['gradelist']=gradecriteria.objects.get(courseid=ccourseid)
	args['typelist']=gradepolicy.objects.get(courseid=ccourseid)
	args['roleid']=int(Institutelevelusers.objects.get(personid=request.session['person_id']).roleid)
	return render(request,'course/enrollmentcourse.html', args)




###########################	Deepak Code End #######################################################


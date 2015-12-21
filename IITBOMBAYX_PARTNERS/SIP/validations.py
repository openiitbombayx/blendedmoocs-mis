from .models import *
from django.shortcuts import render_to_response, render, redirect
from django.core.exceptions import *
import re
from django.core.signing import Signer
from SIP.models import ErrorContent
from django.http import HttpResponseRedirect
from datetime import datetime 
from SIP.models import Userlogin,Institutelevelusers,T10KT_Approvedinstitute,T10KT_Institute,Personinformation
from SIP.models import *
from datetime import *
from django.contrib import auth
import csv
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from globalss import *
from django.http import HttpResponse
from IITBOMBAYX_PARTNERS.settings import *
from fetch_student_info import *
from django.db.models import Q
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
import string
signer = Signer(sep="$",salt='as12')

###########################################

def validate_auth_user(email,user):
    
    userlogin_obj=iitbx_auth_user.objects.filter(Q(email=email) | Q(username=user))
# For correct email address verify username

    for row in userlogin_obj:
       uid=row.edxuserid
       username=row.username
       emailid=row.email.lower()
       
       if( username == user) and (emailid==email):
    	  return [int(uid),email,username,1,'01-01-2005']
       elif  ( username != user) and (emailid==email):
    	  return [-1,email,"",1,'01-01-2005']
       elif  ( username == user) and (emailid !=email):
    	  return [-1,"",username,1,'01-01-2005']
    return [-1 ,"","",-1,-1]





###################Return error message from ErrorContent Tables based errorcode as input for table #########################
def getErrorContent(errorcode):
  try:
     return ErrorContent.objects.get(errorcode=errorcode).error_message
  except:
     return "Error Message not defined"




################# Return  error messages for invalid input based on systype,name,errorcode as input to function ###################
def retrieve_error_message(systype,name,errorcode):
    x = ErrorContent.objects.get(systype=systype,name=name,errorcode=errorcode)        
    error_message=x.error_message
    return error_message

      
## This function validates the email id and password of the user
## Returns a list and updates userlogin table if valid email id
## Returns an integer value if invalid
def validate_login(request):
  try: 
    
## If email exists, returns a row containing details for that id           
    
    user_auth=auth.authenticate(username=request.POST['email'], password=request.POST['password'])
    

## Checks if the password entered by the user matches with the password in the userlogin table
    #print user_info.password,"passwords", request.POST['password']
    #if check_password(request.POST['password'],user_info.password):
    if user_auth is not None and user_auth.is_active:
        auth.login(request,user_auth)
        userdetail = User.objects.get(username=request.POST['email'])
        user_info=Userlogin.objects.get(user=userdetail)
        if user_info.usertypeid == 0:
           
           request.session['email_id'] =userdetail.email
           pson=Personinformation.objects.get(email=userdetail.email)
           request.session['person_id']=pson.id

           return  0
        elif user_info.usertypeid == 2:
           
           request.session['email_id'] =userdetail.email
           pson=Personinformation.objects.get(email=userdetail.email)
           request.session['person_id']=pson.id

           return  2
        elif user_info.usertypeid == 3:
           
           request.session['email_id'] =userdetail.email
           pson=Personinformation.objects.get(email=userdetail.email)
           request.session['person_id']=pson.id
           
           return  3
        
        request.session['email_id'] =userdetail.email
        user_info.nooflogins +=1
        user_info.last_login=datetime.now()
        user_info.status=1
        user_info.save()
        return 1   

    else:
## If password not valid, then returns -1
        return -1
        
  except:
## If email id does not exist, then returns -1
        return -1


###################### check if email exist in Personinformation tables ####################
def validate_email(email):
    try:
        email_obj = Personinformation.objects.get(email=email)
        if email_obj:
		
                return email_obj.id
                
        else:
                return -1
    except:
            return -1


################## Check format of email#################
def emailid_validate(request,args):
    module = LOGIN_
    ck_email = r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$"
## Checks if email is blank
    if not args['email']: 
        args['error_message']=retrieve_error_message(module,'Email_empty','EML_EMPTY')
## Check for regex validation
    elif not re.match(ck_email,args['email']):
        args['error_message']=retrieve_error_message(module,'Email_invalid','INV_EML')
    return args
   

################# Check if password is empty ################### 
def pwd_field_empty(request,args,value):
    #ck_password =  r"^[A-Za-z0-9!@#$%^&*()_]{6,20}$"	
    module = 'Login'
    if value == 'Change_Pass':
        
        if not args['old_password']:
           
            args['message']=retrieve_error_message(module,'Pwd_empty','PASS_EMPTY')
## Checks if Field is Blank
    if not args['password1'] or not args['password2'] :	
        args['message']=retrieve_error_message(module,'Pwd_empty','PASS_EMPTY')
    elif  args['password1'] != args['password2']:
            args['message']= retrieve_error_message(module,value,'PWD_NO_MTCH')
    elif filter(lambda x: x  in string.printable and  x  not in string.whitespace, args['password1']) !=args['password1']:
        args['message']= retrieve_error_message(module,value,'INV_CHAR')
    elif len(args['password1'])<6 or len(args['password1'])>30:
         args['message']= retrieve_error_message(module,value,'INV_LEN')
## Checks if Field is Blank
    
    return args
            

################################ Check email format for Automate registration script input email ###################################
def validateEmail(email):
    if len(email) > 4:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0


# Return
def validate_file_extension(fname):
    if not fname.endswith('.csv'):
        return 0
    return 1


#This function is used to validate the records-------#
#This function detects following errors--------------#
#1)invalid username----------------------------------#
#2)invalid email-id----------------------------------#
#3)student not enrolled for the course---------------#


def valid_stud_record(request,rollnum,user,email,courseid,currentfile,defaultteacher,teacher_id):

    message=""
    error_code=0
    ignore=0 # Added for already marked records 1308/M
    user_details= validate_auth_user(email.lower(),user)
    
    if user_details[1] == "" and user_details[2] == "" :  
        message = getErrorContent("not_registered")   
        error_code=1

    else:
         if user_details[1] != email.lower():             
             message = getErrorContent("invalidemail")
             error_code=1

         if user_details[2] != user:
            
             message = message+'\n'+ getErrorContent("invaliduser")
             error_code=1

         if user_details[3] != 1:
             
             message = message+'\n'+ getErrorContent("inactive_user")   
             error_code=1

    if (error_code != 1):
        
       try:  
          student_det = studentDetails.objects.get(edxuserid=iitbx_auth_user.objects.get(edxuserid=user_details[0]),courseid=courseid)
          if not student_det:    
           
             message = message + '\n'+getErrorContent("not_enroll")#check error code        
             error_code=1
          else:
             if student_det.teacherid == teacher_id and student_det.teacherid != defaultteacher :
                ignore=1  #Added for already marked records to be ignored 1308/M
                message = message + '\n'+getErrorContent("dup_entry")#check error code        
                error_code=1
  
             elif student_det.teacherid != defaultteacher :
              
                message = message + '\n'+getErrorContent("already_assigned")#check error code        
                error_code=1
             if student_det.edxis_active == 0:
                
                  message = message + '\n'+getErrorContent("cancelled_enrollment")#check error code       
                  error_code=1
       except:
           message ="Student Does not exist"
           #return render(request,'geterror.html',args)
    #return [user_details[0],message]
    return [user_details[0],message,ignore]   #Added for already marked records to be ignored 1308/M

################ validate uploaded file fields and store message and status in student interface table and return studentinterface table object  and valirecord and invalid record count
def validatefileinfo(request,courseid,fname,teacher_id):


    validcount = 0
    invalidcount = 0
    ignorecount=0  #Added 1308/M
    recordno= 0    
    rollnum=0
    user=""
    email=""
    VALID="Valid"
    ERROR="Error"

    try:
       
       currentfile = uploadedfiles.objects.get(filename = fname)
    except DoesNotExist:
       message = getErrorContent("invalidfilename")
       
       return
   
    fo=open(fname,'rb')    
    reader = csv.reader(fo)
    heading= next(reader)
    heading[0]=heading[0].replace(" ","")
    heading[1]=heading[1].replace(" ","")
    heading[2]=heading[2].replace(" ","")
    
    if (heading[0]== "RollNumber") and  heading[1] == "UserName" and heading[2]== "Email" :  
       try:
           
           courseobj= edxcourses.objects.get(courseid = courseid)
       except DoesNotExist:
           message = getErrorContent("invalidcourse")
           
           return
       try:
           courselevelobj=Courselevelusers.objects.get(personid=Personinformation.objects.get(id=teacher_id),courseid=edxcourses.objects.get(courseid = courseid))
           default_teacher=Courselevelusers.objects.get(personid=Personinformation.objects.get(id=1),courseid=edxcourses.objects.get(courseid = courseid)) 
       except Exception as e:
           args={}
           args['error_message'] = getErrorContent("not_valid_teacher")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,'geterror.html',args)
    else:
      
       message = getErrorContent("invalidheading")
       return;
    #Check if the records are correct
    for line in reader:
        recordno+=1
        message=""
        status=VALID
        
        rollnum=""
        user=""
        email=""
        #Check if the file has empty record
        
        if not line:
            message = message + getErrorContent("blankline")       
            status=ERROR
            
        #Check if none of the fields is blank
        elif len(line)!= 3:
            message = message + getErrorContent("inv_rec")        
            status=ERROR
            rollnum = line[0].replace(" ","")
            user = line[1].replace(" ","")
            email = line[2].replace(" ","")
            invalidcount+=1
             
        #Record is complete in file.Check values exists
       
        else:
             #Remove trailing and leading blanks                   
             rollnum = line[0].replace(" ","")
             user = line[1].replace(" ","")
             email = line[2].replace(" ","")  
              
             if  len(rollnum) == 0 or len(user) == 0 or len(email) == 0:
                message = message + getErrorContent("fields_empty")       
                status=ERROR
                invalidcount+=1
                 
        #Record is complete in file.Check contents
             else:
                 result=valid_stud_record(request,rollnum,user,email,courseid,currentfile,default_teacher,courselevelobj)
                
                 message = message + result[1]
              #print "nbye das ",valid_stud_record(request,rollnum,user,email,courseid,currentfile,courselevelobj.id) ," message"
                 
                 if (message != "" or status== ERROR) and  result[2]==0:
                  invalidcount+=1
                  status= ERROR
                 elif (result[2] == 1):
                  ignorecount+=1
                  status = "Ignore"
                 else:   
                   validcount+=1
                   try:
                    stud_obj=studentDetails.objects.get(edxuserid__edxuserid=result[0],courseid=courseid)
                    stud_obj.teacherid= courselevelobj
                    stud_obj.roll_no=rollnum
                    stud_obj.save()    
                   except:
                       message ="Student dos not exist"
                       #return render(request,'geterror.html',args)       
        
        interface_obj = student_interface(fileid = currentfile ,recordno = recordno,roll_no = rollnum,email = email , username = user , error_message = message,status=status) 
        interface_obj.save()
        line=[]  
    context = {'validcount':validcount,'invalidcount':invalidcount,'ignorecount':ignorecount,'totalrecords':recordno}    
    errorreport = student_interface.objects.filter(fileid = currentfile).exclude(error_message="")
    context.update({'errorreport':errorreport})
    return context




############################## Send mail by fetching content of mail from EmailContent table ###################################
def send_email(request,ec_id, req_id, per_id):
    try:
	    ec_id = int(ec_id)
	    req_id = int(req_id)  
	    
	    per_id = int(per_id)
	    mail_obj = EmailContent.objects.filter(id=ec_id)
	    #req_obj = RequestedUsers.objects.filter(id = req_id)
            #print "mail obj",mail_obj
	    '''if req_obj:
		    fname = req_obj[0].firstname
		    lname = req_obj[0].lastname
		    email = req_obj[0].email
		    code = req_obj[0].roleid
		    role = Lookup.objects.filter( category = 'Role', code = code)
		    role = role[0].comment
		    if not ((role == 'Program Coordinator') or (role == 'Head')):
		    	cname = edxcourses.objects.filter(id = req_obj[0].courseid_id)
		    	cname= cname[0].coursename 
			iname = T10KT_Institute.objects.get(instituteid = req_obj[0].instituteid.instituteid).institutename 
		    link = ROOT_URL + mail_obj[0].name + '/%d' %req_id
	      '''
            #print "before if"
            if ec_id == 1: # Email verification -> user
		message = mail_obj[0].message %(fname, link, email)
	    elif ec_id == 2: # request for approval -> higher authorities
		message = mail_obj[0].message %(role, cname, email, fname)
	    elif ec_id ==3: # request submitted mail -> user
		message = mail_obj[0].message %(fname, role, cname)
	    elif ec_id == 4: # accepted, register link -> user
		message = mail_obj[0].message %(fname, role, cname, link)
	    elif ec_id == 5: # rejected by authorities mail to user
		message = mail_obj[0].message %(fname, role)
	    elif ec_id == 6: # request register to HOI's
		cname = edxcourses.objects.filter(id = req_obj[0].courseid_id)
		cname= cname[0].coursenam
		message = mail_obj[0].message %(fname,cname,link)
	    elif ec_id == 8: # successful registration to user(CC AND TA)
		message = mail_obj[0].message %(fname,role,cname)
	    elif ec_id == 9: #Invite Program Coordinator /2 for the roles of PC, CC, TA
		link = ROOT_URL + mail_obj[0].name + '/%d/2' %req_id 
		message = mail_obj[0].message %(fname, role,link)
	    elif ec_id == 10: # Reset password of a user
		per_obj = Personinformation.objects.filter(id = per_id)
		fname = per_obj[0].firstname
		email = per_obj[0].email
   #encrypting link
		
		per_id=signer.sign(per_id)
        
		link = ROOT_URL + mail_obj[0].name + '/%s' %per_id
		message = mail_obj[0].message %(fname, link)
	    elif ec_id == 11 or ec_id==31: # Reset password of a user
		#print "inside if"
                per_obj = Personinformation.objects.filter(id = per_id)
		fname = per_obj[0].firstname
		email = per_obj[0].email
		link = ROOT_URL + mail_obj[0].name + '/%d' %per_id
		#print ec_id , mail_obj[0].message
                message = mail_obj[0].message %(fname)
                #print message
	    elif ec_id == 12: #Invite Program Coordinator /2 for the roles of PC, CC, TA
		linked = mail_obj[0].name.split(',')
		#per_obj = Personinformation.objects.filter(id = 9)
		#fname = per_obj[0].firstname
		link1 = ROOT_URL + linked[0] + '/%d' %req_id 
		link2 = ROOT_URL + linked[1] + '/%d' %req_id 
		message = mail_obj[0].message %(fname,role,link1,link2)
	    elif ec_id == 13: #Invite Program Coordinator /2 for the roles of PC, CC, TA
		link = ROOT_URL + mail_obj[0].name + '/%d/2' %req_id 
		cname = edxcourses.objects.filter(id = req_obj[0].courseid_id)
		cname= cname[0].coursename
		message = mail_obj[0].message %(fname, role,cname,link)
	    elif ec_id == 14: #Invite Program Coordinator /2 for the roles of PC, CC, TA
		cname = edxcourses.objects.filter(id = req_obj[0].courseid_id)
		cname= cname[0].coursename
		linked = mail_obj[0].name.split(',')
		link1 = ROOT_URL + linked[0] + '/%d' %req_id 
		link2 = ROOT_URL + linked[1] + '/%d' %req_id 
		message = mail_obj[0].message %(fname, role,cname,link1, link2)    
	    elif ec_id == 15: #Email to acknowledge approval 
		cname = edxcourses.objects.filter(id = req_obj[0].courseid_id)
		cname= cname[0].coursename 
		message = mail_obj[0].message %(fname, role,cname)    
	    elif ec_id == 16: #Email to acknowledge rejection
		cname = edxcourses.objects.filter(id = req_obj[0].courseid_id)
		cname= cname[0].coursename 
		message = mail_obj[0].message %(fname, role,cname)    
	    elif ec_id == 17: #Email to acknowledge cancellation
		message = mail_obj[0].message %(fname, role)  
	    elif ec_id == 19: #Email to inviter that his invite has been declined by invitee
		cname = edxcourses.objects.filter(id = req_obj[0].courseid_id)
		cname= cname[0].coursename 
		
		hname = Personinformation.objects.get(id = per_id).firstname
	#	hname = per_id.objects.get(id = per_id)
		message = mail_obj[0].message %(hname, role,cname, fname)    
	    elif ec_id == 23: #Email to acknowledge change of password
		  message = mail_obj[0].message %(fname)    
          #for createpassword
	    elif ec_id == 30: #Email to acknowledge change of password
		    per_obj = Personinformation.objects.filter(id = per_id)
		    fname = per_obj[0].firstname
		    email = per_obj[0].email
		    link = ROOT_URL + mail_obj[0].name + '/%d' %per_id
		    message = mail_obj[0].message %(fname, link)  
	    test=send_mail(mail_obj[0].subject, message , DEFAULT_FROM_EMAIL ,[email], fail_silently=False)      
            #print test
    except Exception as e:
          args={}
          args['error_message'] = getErrorContent("unique_person")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,'geterror.html',args)



 

############### Return 1 if firstname is validate by given regular expression #######################

def validateFname(fname):
    if len(fname) >=1:
        if re.match("^[A-Za-z][\.\]?[a-zA-Z]+$", fname) != None:
            return 1
    return 0

############### Return 1 if lastname is validate by given regular expression #######################

def validateLname(lname):
    if len(lname) >= 1:
        if re.match("^[A-Za-z][\.\]?[a-zA-Z]+$", lname) != None:
            return 1
    return 0


################# Check if PC exist for given instituteid
def validatePC(email, role,instituteid):##modifiaction based on institute also
    try:
        #per_obj = Personinformation.objects.get(email = email)
        institute_obj=T10KT_Institute.objects.get(instituteid=instituteid)
        if Personinformation.objects.filter(email = email).exists():
            per_obj = Personinformation.objects.get(email = email)
            if Institutelevelusers.objects.filter(personid = per_obj, roleid = role,instituteid=institute_obj).exists():
                return 0
            else :
                return 1
        else:
             return 2
    except:
        return 1
        
#################### check if email exist in auth_user table for login #####################
def ifLoginExists(email):
    if User.objects.filter(email = email).exists():
        return 1
    else:
        return 0

#################### check if email exist in Personinformation table for login #####################

def ifPersonExists(email):
    if Personinformation.objects.filter(email = email).exists():
        return 1
    else:
        return 0

#################### check if institute exist in T10KT_Institute table for login .True return institute object #####################
def validateInstitute(institutename):
    
    try:
        insti_obj =T10KT_Institute.objects.get(institutename = institutename)
        return insti_obj
    except ObjectDoesNotExist:
        return None

#################### check if Remotecenter exists in T10KT_Remotecenter table for login .True return institute object #####################

def validateRemotecenter(rcid):
     
    try:
        rc_obj =T10KT_Remotecenter.objects.get(remotecenterid=rcid)
        return rc_obj
    except ObjectDoesNotExist:
        return None
    
#################### check if role exists in Lookup table .True return look code #####################
def validateRole(role):
     try:
        look_obj = Lookup.objects.get(category = 'Role', comment = role)
        return look_obj.code
     except ObjectDoesNotExist:
        return 0
    
#################### check if role Course exists in edxcourses table .True return look id of edxcourse #####################
def validateCourse(course):
    try:
        edx_obj = edxcourses.objects.get(course = course)
        return edx_obj.id
    except ObjectDoesNotExist:
        return 0


#################### check if role Course is enrolled by given institute  .True return if enrolled #####################
def IfCourseEnrolled(courseid,instituteid):
    try:
       edxcourseid= edxcourses.objects.get(id=courseid)
       if courseenrollment.objects.filter(courseid=edxcourseid,instituteid__instituteid=instituteid).exists():
          return 1

       else :
          return 0

    except:
           return 0
#################### check if Designationexists in Lookup table .True return if exists#####################

def validateLookup(comment,category):
     
     if Lookup.objects.filter(category = 'Designation', description = comment).exists():
            
            return 1
     return 0
        
#############################################################

def get_grades_report(courseobj,courselevelid):
   try:
      grades_obj=gradepolicy.objects.filter(courseid=courseobj).order_by('id')
      heading = ["RollNumber","Username","Email","Grade"]
      avg={}
      gradelist=[]
      stud_rec =["" ,"" ,"",""]
      #Heading for the report
      for gradetype in grades_obj:
           grade_value=gradetype.min_count-gradetype.drop_count
           gradelist.append(gradetype) 
           
           
           for i in range(1,gradetype.min_count+1):
               value=gradetype.short_label +" "+ str(i).zfill(2)
               stud_rec.append("0.0") 
               heading =heading+ [str(value)]
           if (grade_value > 1):    
               heading =heading+ [str(gradetype.short_label +" Avg")] 
               avg[gradetype.type]=len(heading)-5
           #print avg    
      stud_list = studentDetails.objects.raw('''SELECT d.id, d.roll_no,d.edxuserid_id ,a.username,a.email
FROM SIP_studentdetails d,SIP_iitbx_auth_user a
WHERE d.courseid = %s and d.teacherid_id=%s and d.edxis_active=1
and d.edxuserid_id=a.edxuserid 
ORDER BY d.edxuserid_id''',(str(courseobj.courseid),str(courselevelid.id)))  
      grade_list=[]
      for studvalue in stud_list:
                stud_rec=[str(studvalue.roll_no), str(studvalue.username),str(studvalue.email)]   
                gradelist=result.objects.raw('''select id1 "id", type ,sec_name, due_date, sum((ifnull(grade,0)/ifnull(maxgrade,1))*q_weight)/sum(q_weight) res,weight,value
from (
select g.id "id1",e.type,q.id,e.sec_name,e.due_date,q_weight,r.grade,r.maxgrade ,g.weight,g.min_count-g.drop_count value from SIP_evaluations e,SIP_questions q 
, SIP_result r ,SIP_gradepolicy g where e.course_id=%s and q.eval_id=e.id and r.question_id=q.id and g.type=e.type and g.courseid_id=%s
and r.edxuserid=%s 
union
select g.id "id1",e.type, q.id,e.sec_name,e.due_date,q_weight,0,1,g.weight,g.min_count-g.drop_count value from SIP_evaluations e,SIP_questions q,SIP_gradepolicy g
 where e.course_id=%s and q.eval_id=e.id and g.type=e.type and g.courseid_id=%s
 and not exists (select * from SIP_result r where r.question_id=q.id and r.edxuserid=%s)
)  t group by id1,type,sec_name,due_date,weight,value order by id1,due_date asc''',(str(courseobj.id),str(courseobj.courseid),str(studvalue.edxuserid_id),str(courseobj.id),str(courseobj.courseid),str(studvalue.edxuserid_id)))
                grade=0.0
                typ=""
                count=0
                weight=0
                marks_list=[]
                grade_rec=[]
                for grades in gradelist:
                   if (typ != grades.type):
                      if count != 1 and marks_list != []:
                        marks_list=sorted(marks_list,reverse=True)[:count]
                        average=sum(marks_list)/float(count)
                        grade=grade+average*weight 
                        while (len(grade_rec) < avg[grades.type]):
                          grade_rec.append("0.00")
                         
                        grade_rec = grade_rec +[round(average,2)]
                        #print grade_rec
                      elif count == 1 and marks_list != []:
                        grade=grade+marks_list[0]*weight    
                      typ=grades.type
                      count=grades.value
                      marks_list=[grades.res]
                      weight =grades.weight
                   else:
                      marks_list+=  [grades.res] 
                   grade_rec= grade_rec +[str(round(grades.res,2))] 
                   #grade=grades.res*grades.grade_weight
                #Last type
                if count != 1 and marks_list != []:
                        marks_list=sorted(marks_list,reverse=True)[:count]
                        average=sum(marks_list)/float(count)
                        grade=grade+average*weight 
                        while (len(grade_rec) < avg[grades.type]):
                          grade_rec.append("0.00")
                         
                        grade_rec = grade_rec +[round(average,2)]
                        #print grade_rec
                       ## grade_rec[avg[grades.type]] = [round(average,2)]
                elif count == 1 and marks_list != []:
                        grade=grade+marks_list[0]*weight    
                   
                grade_list=grade_list +[stud_rec+[round(grade,2)] +grade_rec]
      return [heading,grade_list]
   except Exception as e:
      #print [[-1],[e.message,type(e)]]
      return [[-1],[e.message,type(e)]]      
#end get_grades_report

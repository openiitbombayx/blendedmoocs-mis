'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


# VERSION 2.1
# DATED 20 JUNE 2015
# TIME 10:00 AM
# models.py includes all the classes corresponding to database tables
# This file contains foreign key dependency
'''
Change log prepared by PARTH(19/06/2015: 10:30PM)
-renamed table filestatus to student_interface
-removed table studentcourseenrollment as it was a replica of IITBX_studentcourseenrollment
-removed validators in uploadedfiles class
-added columns status, createdon, createdby, updatedon, updatedby in Requestedusers class
-renamed thumbnail to filename in uploadedfiles class
-renamed column lastupdatedon by uploadedon in uploadedfiles class
-corrected foreign key dependencies
-renamed column name with personid  in Responsibility class
-added foreign key arg to verticalid in problemid class
-added foreign key arg to studentid in coursewarestudentmodule
-added foreign key arg to last_updated_by in studentdetails
-added foreign key arg to enrolledby, cancelledby in courseenrollment
-changed loginname to email in userlogin class
-changed loginstatus to status and changed it to booleanfield
-changed createdby, updatedby to foreignkey with Personinformation
-added id column to IITBX_authuser
 '''


#Final Database Modules

from django.db import models
from datetime import datetime,time
from datetime import date
from django.utils import timezone
from time import time
from django.core.exceptions import ValidationError
from django.utils.timezone import *
from django.contrib.auth.models import User

#def validate_file_extension(value):
 #   if not value.endswith('.csv'):
  #      raise ValidationError('Error : Extension should be .csv only')
def validate_image_extension(value):
    img=['.jpeg','.png']
    if not value.endswith(img):
        raise ValidationError('Error : Extension should be .jpeg or .png only')


def get_upload_file_name(instance,filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)

def get_upload_image(instance,filename):
	return "static/upload/upload_images/%s" % filename


class Api_call(models.Model):
    api_name = models.CharField(max_length=200)
    last_run = models.DateTimeField("2005-01-01 00:00:00") 

class Lookup(models.Model): # remove T10KT , make it just Lookup 
	category=models.CharField(max_length=75,null=False)
	code=models.IntegerField(null=False)
	description=models.CharField(max_length=100, null=False)
	comment=models.CharField(max_length=100,null=True)
	is_active = models.BooleanField(default=1)
        @classmethod
        def updatedate(cls):
             return cls.objects.get(category = 'RefreshDate',code=1).description

class  iitbx_auth_user(models.Model):   
    edxuserid = models.IntegerField(primary_key=True)
    username =  models.CharField(max_length=100,null=True)
    email =  models.CharField(max_length=100,null=True)



class edxcourses(models.Model):   
    tag =  models.CharField(max_length=100,null=True)
    org =  models.CharField(max_length=100,null=True)
    course =  models.CharField(max_length=100,null=True)
    name =  models.CharField(max_length=100,null=True)
    courseid =  models.CharField(max_length=100,null=True, unique=True)
    coursename=models.CharField(max_length=100, null=True)
    enrollstart =  models.DateTimeField(null=True)
    enrollend =  models.DateTimeField(null=True)
    coursestart =  models.DateTimeField(null=True)
    courseend =  models.DateTimeField(null=True)
    image=models.ImageField(upload_to=get_upload_image)
    instructor=models.CharField(max_length=50)
    coursesubtitle=models.TextField()
    blended_mode=models.IntegerField(null=True)

class gradepolicy(models.Model):
    	courseid =  models.ForeignKey(edxcourses, to_field='courseid')  #foreign key with edxcourses
    	min_count=models.IntegerField(null=True)
    	weight=models.FloatField(null=True)
    	type=models.CharField(max_length=100,null=True)
    	drop_count=models.IntegerField(null=True)
    	short_label=models.CharField(max_length=10,null=True)

class gradescriteria(models.Model):
    	courseid =  models.ForeignKey(edxcourses, to_field='courseid')  #foreign key with edxcourses
    	grade=models.CharField(max_length=5,null=True)
    	cutoffs=models.FloatField(null=True)
    
# Configuration tables interfaced from IITB-NMEICT T10KT website

#Start

class T10KT_Institute(models.Model):
     instituteid=models.IntegerField(primary_key=True)
     institutename=models.CharField(max_length=100,null=False)
     state=models.CharField(max_length=50)
     city=models.CharField(max_length=100)
     pincode=models.IntegerField(null=True) # null is true because in csv many rows have null pincode
     address=models.CharField(max_length=250,null=True) # null is true because in csv many rows have null address
           
class T10KT_Remotecenter(models.Model):
	remotecenterid=models.IntegerField(primary_key=True)
	remotecentername=models.CharField(max_length=100,null=False)
	state=models.CharField(max_length=50)
	city=models.CharField(max_length=100)
	instituteid=models.ForeignKey(T10KT_Institute) #changes made here
	autonomous=models.BooleanField(default=1)

class T10KT_Approvedinstitute(models.Model):
	remotecenterid=models.ForeignKey(T10KT_Remotecenter,null=True)
	instituteid=models.ForeignKey(T10KT_Institute,null=True, unique=False)


class Personinformation(models.Model):
    GENDER_CHOICES = ( 
     ('MALE', 'Male'),
     ('FEMALE', 'Female'),
	)
    email=models.EmailField(max_length=100,null=False)
    titleid=models.IntegerField(null=True)
    firstname=models.CharField(max_length=45,null=True)
    lastname=models.CharField(max_length=45,null=True)
    designation=models.IntegerField(null=True)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES, null='TRUE')
    streamid=models.IntegerField(null=True)
    instituteid=models.ForeignKey(T10KT_Institute)    #can be modified later 'do not remove'
    experience=models.CharField(max_length=45,null=True)
    qualification=models.CharField(max_length=45,null=True)
    telephone1=models.CharField(null=False, max_length=12, default=0)
    telephone2=models.CharField(default=0, max_length=12, null=True)
    createdondate=models.DateField(default=timezone.now,null=False)
    isactive=models.BooleanField(default=1) #added this to know whether the person is currently attached with the system    

class courseenrollment(models.Model):
	courseid =  models.ForeignKey(edxcourses, to_field='courseid')  #foreign key with edxcourses
	instituteid=models.ForeignKey(T10KT_Approvedinstitute,unique=False)  #foreign key with T10KT_Approvedinstitute.instituteid
	corresponding_course_name=models.CharField(max_length=100)
	start_date=models.DateField(default=timezone.now)
	end_date=models.DateField(4712-12-31)
	year=models.IntegerField()
	program=models.CharField(max_length=50)
	total_moocs_students=models.IntegerField()
	total_course_students=models.IntegerField()
	enrollment_date=models.DateField(default=timezone.now)
	enrolledby=models.ForeignKey(Personinformation, related_name='enrollid')
	comments=models.TextField(null=True)
	cancelled_date=models.DateField(null=True)
	cancelledby=models.ForeignKey(Personinformation, related_name='coordinatorid',null=True)
	reason_of_cancellation=models.TextField(null=True)
	status=models.BooleanField(default=1)

             
class Responsibility(models.Model):#personid
    '''ROLE_PERMISSIONS = ( 
        ('Y', 'Yes'),
        ('N', 'No'),
    )'''
    systype=models.CharField(max_length=30)
    admin=models.BooleanField(default=0)
    hoi = models.BooleanField(default=0)
    pc = models.BooleanField(default=0)
    cc=models.BooleanField(default=0)
    ta=models.BooleanField(default=0)
    comments=models.TextField(null=True)
 
class Userlogin(models.Model):
    user = models.OneToOneField(User, unique=True,related_name='login')
    #email=models.CharField(max_length=75,null=False)
    #password=models.CharField(max_length=75,null=False)
    usertypeid=models.IntegerField(default=1)
    status=models.BooleanField(default=0)
    last_login=models.DateTimeField(default=timezone.now,null=False)
    nooflogins=models.IntegerField(null=True,default=0)

class Institutelevelusers(models.Model):
    personid=models.ForeignKey(Personinformation)
    instituteid=models.ForeignKey(T10KT_Institute)
    roleid=models.IntegerField()
    startdate=models.DateField(default=timezone.now,null=False)
    enddate=models.DateField(4712-12-31)           #Give a fix date 31/Dec/4712
        	      
class Courselevelusers(models.Model):
    personid=models.ForeignKey(Personinformation, unique=False) # remove unique from here
    instituteid=models.ForeignKey(T10KT_Institute) 
    courseid=models.ForeignKey(edxcourses)
    roleid=models.IntegerField()
    startdate=models.DateField(default=timezone.now,null=False)
    enddate=models.DateField(4712-12-31)     #Give a fix date 31/Dec/4712
        
# Upload students

class studentDetails(models.Model):
     edxuserid = models.ForeignKey(iitbx_auth_user,unique=False)              
     courseid = models.CharField(max_length=250,null=True) 
     teacherid = models.ForeignKey(Courselevelusers, to_field='id',unique=False)# replaced Courseleveluser with Personinformation
     roll_no = models.CharField(max_length=30,default="0")
     last_update_on = models.DateTimeField()
     last_updated_by = models.ForeignKey(Personinformation,related_name="lastupdatedby") # replaced Courseleveluser with Personinformation
     edxcreatedon =  models.CharField(max_length=100,null=True)
     edxis_active =  models.BooleanField()
     edxmode =  models.CharField(max_length=100,null=True)  

class coursefaculty(models.Model):
    person = models.ForeignKey(Personinformation)
    course = models.ForeignKey(edxcourses) 

class uploadedfiles(models.Model):
	filename = models.FileField(upload_to=get_upload_file_name, null=True)
	is_read = models.BooleanField(default = 0)
	errorocccur = models.BooleanField(default=0)
	uploadedby = models.ForeignKey(Personinformation,default=1)  # replaced Courseleveluser with Personinformation
	uploadedon = models.DateField(default=timezone.now)


class PageContent(models.Model):
	systype=models.CharField(max_length=30)
	name=models.CharField(max_length=100)
	html_text=models.TextField()

class EmailContent(models.Model):
	systype=models.CharField(max_length=30)
	name=models.CharField(max_length=100)
	subject=models.CharField(max_length=100)
	message=models.TextField()

class ErrorContent(models.Model):
	systype=models.CharField(max_length=30)
	name=models.CharField(max_length=100)
	errorcode=models.CharField(max_length=20, unique=True, default='null')
	error_message=models.TextField()

class student_interface(models.Model):
	fileid = models.ForeignKey(uploadedfiles)  #foreign key with uploadedfiles
	recordno = models.IntegerField()
	roll_no = models.CharField(max_length = 100, null=True)
	username = models.CharField(max_length = 100, null=True)
	email = models.CharField(max_length = 100, null=True)
	error_message =  models.TextField(null=True) #foreign key with ErrorContent
	status=models.CharField(max_length=20)

class RequestedUsers(models.Model):
    courseid = models.ForeignKey(edxcourses,null=True)
    state = models.CharField(max_length=255)
    instituteid = models.ForeignKey(T10KT_Institute)
    remotecenterid = models.ForeignKey(T10KT_Remotecenter)
    firstname=models.CharField(max_length=45,null=True)
    lastname=models.CharField(max_length=45,null=True)	
    email=models.EmailField(max_length=100,null=False)
    roleid=models.IntegerField()
    designation=models.IntegerField(null=True)
    status=models.CharField(max_length=50)
    createdon=models.DateTimeField(0001-01-01) 
    createdby=models.ForeignKey(Personinformation, related_name='user',null=True)
    updatedon=models.DateTimeField() 
    updatedby=models.ForeignKey(Personinformation, related_name='higherauthority',null=True)
    
    
#end of System table      
#  performance table
class performance_interface(models.Model):
	stud = models.ForeignKey(studentDetails)
        grade = models.CharField(max_length=2, null=True)
        eval = models.TextField(null=True)

class markstable(models.Model):
	stud = models.ForeignKey(studentDetails)
        section= models.CharField(max_length=250)
        total=models.CharField(max_length=25)
        eval = models.TextField(null=True)


class gradestable(models.Model):
	stud = models.ForeignKey(studentDetails)
        course = models.CharField(max_length=250)
        grade =models.CharField(max_length=25)
        eval = models.TextField(null=True)   



class evaluations(models.Model):
     course =models.ForeignKey(edxcourses)
     sectionid =models.CharField(max_length=250) 
     sec_name  =models.CharField(max_length=250)
     subsec_id =models.CharField(max_length=250)
     subsec_name =models.CharField(max_length=250)
     type =models.CharField(max_length=150)
     release_date =models.DateTimeField()
     due_date =models.DateTimeField()
     total_weight =models.FloatField()
     grade_weight =models.FloatField()    
     total_marks=models.IntegerField()  
     
class questions(models.Model):
      course =models.ForeignKey(edxcourses)
      eval =models.ForeignKey(evaluations)
      qid =models.CharField(max_length=250) 
      q_name = models.CharField(max_length=250)    
      q_weight= models.FloatField()
      prob_count=models.IntegerField()

class headings(models.Model):
      section=models.CharField(max_length=200)
      heading=models.TextField()


class result(models.Model):
       question =models.ForeignKey(questions)
       edxuserid =models.IntegerField()
       grade =models.FloatField()
       maxgrade =models.FloatField()


class Reports(models.Model):
	reportid=models.CharField(max_length=20,primary_key=True)
	usertype=models.IntegerField()
	sqlquery=models.CharField(max_length=200)
	report_title=models.CharField(max_length=100)
	num_cols=models.IntegerField()
	comments=models.CharField(max_length=200)
	category=models.CharField(max_length=30)
	rel_rep_id=models.IntegerField()
	


class mail_interface(models.Model):
    fname = models.CharField(max_length=75)
    lname = models.CharField(max_length=75)
    email = models.CharField(max_length=75)
    institutename=models.CharField(max_length=250)
    instituteid = models.ForeignKey(T10KT_Institute,null = True)
    designation=models.CharField(max_length=100)
    role = models.CharField(max_length=30)
    role_id=models.IntegerField()
    rcid=models.IntegerField()
    courseid =models.IntegerField()
    course = models.CharField(max_length = 50, null = True)
    status = models.CharField(max_length=30)
    error_message = models.CharField(max_length = 300, null = True)
    filename=models.CharField(max_length = 300, null = True)


class interfaces(models.Model):
    type=models.CharField(max_length=200)
    date=models.DateTimeField()

class course_modlist(models.Model):
    display_name= models.CharField(max_length=200)
    module_type= models.CharField(max_length=200)
    module_id= models.CharField(max_length=200)
    startdate=models.DateTimeField()
    duedate=models.DateTimeField()
    long_name=models.CharField(max_length=300)
    course =models.IntegerField()
    related_id= models.IntegerField()
    order=models.IntegerField()
    visible_to_staff_only=models.IntegerField() 
    graded=models.IntegerField() 
    questions=models.IntegerField()
    maxmarks=models.IntegerField()
    hasproblems=models.IntegerField()
    gradetype=models.CharField(max_length=100)





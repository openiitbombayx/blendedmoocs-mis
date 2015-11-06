'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''

# There are three parts of the interface LOAD,VALIDATE and SEND REGISTRATION LINK
import sys,os
#Global Variable 

SCRIPT_DIR_PATH=os.path.dirname(__file__)
SCRIPT_DIR_PARENT=os.path.join(SCRIPT_DIR_PATH,os.pardir)
SCRIPT_ABS_PATH = os.path.abspath(SCRIPT_DIR_PARENT)
project_dir=SCRIPT_ABS_PATH

debug_mode=1
default_password=""
member=1
VALID ="Valid"
INVALID="Invalid"
EXISTS="Exists"
CREATED="Created"
SENDMAIL="sendmail"
ERROR="ERROR"
default_end_date="4712-12-31"



sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='IITBOMBAYX_PARTNERS.settings'
import csv
import django
django.setup()

from django.db import models
from SIP.models import *
from SIP.validations import *
from SIP.views import *
from django.db import transaction 
from django.contrib.auth.models import User 

#Prints on the console
def print_debug(str):
   if debug_mode == 1:
     print str

#Checks the csv file and returns the python list of content
def read_file(csvfile):    
   #Checks whether the csv file can be open or not
   try:   
      reader = csv.reader(open(csvfile,'rb'))
      print_debug("Reading CSV..")
      return reader
   except:
      sys.exit("Cannot open CSV file!")
# End read_file    

def from_file_to_interface(reader,filename):
     csvrecordc=0
     # Defines the current executing section
     #This function gets each row from csv file, validates the format of email, institutename and insert into mail_interface table; in case data is not acceptable, it adds an error into the error_message field
     #Check head record 
     heading = next(reader, None) 
     if(len(heading)<8):
          sys.exit("Please upload data in correct template format")
     print heading
        
     
     if heading[0]== "RCID" and heading[1]=="InstituteName" and heading[2]=="First Name" and heading[3]=="Last Name" and heading[4] =="Email" and heading[5] == "Designation" and heading[6] == "Role" and heading[7] == "Course" : 
        pass
        
     else:
          sys.exit("Please upload data in correct template format")
     # Check for user data
     for line in reader:
         csvrecordc+=1
         err_message = ''
         status=VALID
         
         #checks that a email format is acceptable or not; returns 0 if not
         if validateEmail(line[4].replace(" ","")) == 0:
              err_message += 'Email format not valid!'+'\n'
              status=INVALID 

         #First name is mandatory 
         #checks that a first name format is acceptable or not; returns 0 if not 
         if validateFname(line[2].replace(" ","")) == 0: 
              err_message += 'First name format not valid!'+'\n'
              status=INVALID 
         #Last name is not mandatory 
         #checks if last name exists and if exists, format is acceptable or not; returns 0 if not
         if len(line[3])>0:    
              if validateLname(line[3].replace(" ","")) == 0: 
                   err_message += 'Last name format not valid!'+'\n'
                   status=INVALID 
         if  validateLookup(line[5],"Designation")==0:    
               err_message += 'Designation not Exist! '+"\n"
               status=INVALID 
         
         
         #checks that a Institutename present into database or not;  returns 0 if not else instituteid
         instituteid=validateInstitute(line[1])
         if not instituteid : 
                err_message += 'Institute name not valid!'+'\n'
                status=INVALID
         #checks that a remotecenterid present into database or not;  returns 0 if not else instituteid
         remotecenterid=validateRemotecenter(line[0].replace(" ",""))
         if not remotecenterid: 
                err_message += 'rcid  does not exist in remotecenter table!'+'\n'
                status=INVALID  
         
         #checks that a role is valid or not; returns 0 if not   
        
         role_id=validateRole(line[6])
         if role_id == 0: 
               err_message += 'Role is  not valid!'+'\n'
               status=INVALID 
         
         #Head and Program Coordinator should not be assigned to a Course   
         #print type(line[7]),len(line[7]),line[2]
         if (line[6] =='Head' or line[6] =='Program Coordinator') and len(line[7]) > 0:
               err_message += line[6]+ " should not have course assigned"+"\n" 
               status=INVALID 
        
         #Teacher should  be assigned to a valid Course
         courseid=validateCourse(line[7].replace(" ",""))   
         if  line[6] == 'Teacher' and courseid== 0:    
               err_message += 'Course format not valid! '+"\n"
               status=INVALID 
         
         
         # checking that mail interface table should not duplicate
         if mail_interface.objects.filter(email=line[4],role = line[6],instituteid = instituteid,course = line[7],status =SENDMAIL).exists():
               err_message += "Entry for "+ line[4]+"   for  " +line[6]+"  in "+line[1]+"  already exist" +"\n"
               status=INVALID
         
         mail_obj= mail_interface(rcid=line[0],role_id=role_id,courseid=courseid,institutename=line[1],instituteid = instituteid,fname = line[2], lname = line[3], email = line[4], designation=line[5], role = line[6], course = line[7],status=status, error_message = err_message,filename=filename)
         mail_obj.save()
     return csvrecordc
            
     #end for         
#end from_file_to_interface

def createusers(filename):   
    
    #accesing email content for reset password 
   
    encyrypt_pwd = make_password(default_password,salt=None,hasher='pbkdf2_sha256')
    current_date=date.today()
    #Select Valid Records inserted in the file
    for row in mail_interface.objects.filter(status="Valid",filename=filename):
        #ifLoginExists return 1 means  Login exist in user table and ifPersonExists return 1 means  Personinformation has entry of this user
        LoginExist=ifLoginExists(row.email)
        PersonExist=ifPersonExists(row.email)
        
         
        
        if LoginExist == 0 and PersonExist == 0:
                     
                person_obj = createsingleuser(row)
               
           
           
        elif (LoginExist == 0 and PersonExist == 1) or (LoginExist == 1 and PersonExist == 0):
            row.message = "User Data inconsistent in system Error"                   
            row.status=ERROR
            row.save()
            continue 
        else :
            person_obj=Personinformation.objects.get(email=row.email) 
        if row.course:
               
                CourseEnrollExist=IfCourseEnrolled(row.courseid,row.instituteid)
                print CourseEnrollExist
                
                if CourseEnrollExist==0:
                   print row.instituteid
                   edxcourseid= edxcourses.objects.get(id=row.courseid)
                   print edxcourseid
                   institute=T10KT_Approvedinstitute.objects.get(instituteid=row.instituteid)
                   print institute
                   courseObj=courseenrollment(courseid=edxcourseid, instituteid=institute, enrollment_date=date.today(), status=1)
                   courseObj.save()
                   print "course enrolled"
                else:
                    print "course already enrolled"

                if Courselevelusers.objects.filter(personid=person_obj,instituteid = row.instituteid,courseid =edxcourses.objects.get(course = row.course),roleid = row.role_id).exists():
                    row.error_message += 'The person already has the same role in the same institute teaching the same course'
                    row.status = EXISTS
                    row.save()
                else:
                    req_obj=createcourseleveluser(edxcourses.objects.get(course = row.course),row.instituteid,T10KT_Remotecenter.objects.get(remotecenterid=row.rcid),row.fname,row.lname,row.email,row.role,row.status,row.designation,person_obj,row.role_id) 
                    row.status = CREATED
                    row.save()
                              
        else: 
                      
                if Institutelevelusers.objects.filter(personid=person_obj,instituteid = row.instituteid,roleid =row.role_id,startdate__lte=current_date,enddate__gt=current_date).exists():
                     row.error_message += 'The person already has the same role in the same institute teaching the same course'
                     row.status = EXISTS
                     row.save()
                else:
                      
                      req_obj=createinstituteleveluser(row.instituteid,T10KT_Remotecenter.objects.get(remotecenterid=row.rcid),row.fname,row.lname,row.email,row.role,row.status,row.designation,person_obj, row.role_id)
                      row.status = CREATED
                      row.save()
@transaction.atomic
def createsingleuser(row): 
    
   singleuser=User.objects.create_user(username=row.email,email=row.email,password=default_password)
   singleuser.is_active=True  
   singleuser.save()   
   userprofile=Userlogin(user=singleuser,status=0)
   userprofile.save()

   person_obj=createpersoninformation(row.email,row.fname,row.lname,row.designation,row.instituteid)
   return  person_obj
                                     
                
#function to create institutelevel user                
def createinstituteleveluser(instituteid,rcid,fname,lname,email,role,status,designation,person_obj,role_id) : 

    req_obj  = RequestedUsers(state = instituteid.state, instituteid = instituteid, remotecenterid = rcid, firstname = fname, lastname = lname, email = email, roleid = role_id, status = status, createdon = timezone.now(), updatedon = timezone.now(),designation=Lookup.objects.get(category = 'Designation', description = designation).code)
    req_obj.save()

    Institute_level=Institutelevelusers(personid=person_obj,instituteid = instituteid,roleid =role_id,startdate= datetime.now(),enddate=default_end_date)
    Institute_level.save() 
    return req_obj


#function to create courselevel user
def createcourseleveluser(courseid,instituteid,rcid,fname,lname,email,role,status,designation,person_obj,role_id) : 
    req_obj  = RequestedUsers(courseid = courseid,  state = instituteid.state, instituteid = instituteid, remotecenterid =rcid, firstname = fname, lastname = lname, email = email, roleid = role_id, status = status, createdon = timezone.now(), updatedon = timezone.now(),designation=Lookup.objects.get(category = 'Designation', description = designation).code)
    req_obj.save()
    Course_level=Courselevelusers(personid=person_obj,instituteid = instituteid,courseid =courseid,roleid = role_id,startdate= datetime.now(),enddate=default_end_date)
    Course_level.save() 
    return req_obj


# create Personinformation entry
def createpersoninformation(email,fname,lname,designation,instituteid):
    
    person_obj=Personinformation(email=email,firstname = fname, instituteid=instituteid,lastname =lname,designation=Lookup.objects.get(category = 'Designation', description = designation).code,createdondate=datetime.now(),telephone1=0)
     
    person_obj.save()
   
    return person_obj

def emailusers(filename):  
     ec_id = EmailContent.objects.get(systype = 'Login', name = 'createpassword').id
     mail_obj = EmailContent.objects.get(id=ec_id)
     emailsendc=0
     for row in mail_interface.objects.filter(status=CREATED,filename=filename).values('email','status').distinct():
        
        #person_obj=Personinformation.objects.get(email=row['email'])
        #req_obj=RequestedUsers.objects.filter(email=row.email,instituteid = row.instituteid,roleid=row.role_id).latest('createdon')
        #if req_obj.status == "Valid":
        per_obj = Personinformation.objects.get(email=row['email'])
        fname = per_obj.firstname
        email = per_obj.email
        per_id=signer.sign(per_obj.id)
        link = ROOT_URL + mail_obj.name + '/%s' %per_id
        message = mail_obj.message %(fname, link)  
        send_mail(mail_obj.subject, message , DEFAULT_FROM_EMAIL ,[email], fail_silently=False)  
        row['status']=SENDMAIL
        mail_interface.objects.filter(status=CREATED,filename=filename,email=row['email']).update(status=SENDMAIL)
        
        
        emailsendc+=1
          
     return (emailsendc)

def report(filename,csvrecordc,emailsendc):  
     
     validrecordc=0
     invalidrecordc=0
     errorrecordc=0
     rolecreated=0
     personcreated=0
     courselevelc=0
     institutelevelc=0
     totalcount=0
     existsrecordc=0
     for row in mail_interface.objects.filter(filename=filename):
        totalcount +=1
        if row.status==VALID:
           validrecordc+=1
        if row.status==INVALID:
           invalidrecordc+=1
        if row.status=='ERROR':
           errorrecordc+=1
        if row.status==EXISTS:
           existsrecordc+=1
        if row.status==EXISTS or row.status==SENDMAIL :
           rolecreated+=1
           personcreated+=1
           if row.courseid==0:
              institutelevelc+=1
           else:
              courselevelc+=1
     print "Report for ",filename
     print "" 
     print "Total number of records  :",totalcount
     print "Total number of records read :" , csvrecordc
     print "Total number of person created:" , personcreated
     #print "Total number of roles created:" , rolecreated
     print "Total number of InstituteLevelUsers:" , institutelevelc
     print "Total number of CourseLevelUsers:" , courselevelc
     print "Total number of mails send:" ,     emailsendc
     print "Total number of Exists Record:" ,     existsrecordc
    #
     print "" 
     print "Error Record Details"
     print "Total number of valid records which was not created :", validrecordc
     print "Total number of invalid records :", invalidrecordc
     print "Total number of error records in csv file: ", errorrecordc 
     print "Total number of mails not send:" ,     rolecreated      
     for row in mail_interface.objects.filter(filename=filename).exclude(status = SENDMAIL): 
          print "Instituteid=",row.instituteid," Email=",row.email, " Status=",row.status," ErrorMessage=",row.error_message
                
def main():
  
   csvfile=sys.argv[1]
   reader=read_file(csvfile)
   csvfile=csvfile+str(timezone.now())
   csvrecordc=from_file_to_interface(reader,csvfile)
   createusers(csvfile)
   emailsendc  =emailusers(csvfile)
   report(csvfile,csvrecordc,emailsendc)
if __name__ == "__main__":
    main()
   

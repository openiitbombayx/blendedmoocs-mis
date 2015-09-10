'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''

'''
This file contains apis to fetch mysql student information from IITBombayX
'''
from models import *
from datetime import datetime
import MySQLdb

# Connection information 
def db_openconnection(usr,password,host_name,database):
     cnx = MySQLdb.connect(user=usr,passwd=password,host=host_name,db=database)
     return cnx

# Initialize the connection
def init(usr,password,host_name,database):

    cnx=db_openconnection(usr,password,host_name,database)
    #cnx=db_openconnection("root","root","localhost","edxapp")
    return cnx
# Validates the student information received from teacher in iitbombayx
# Returns list of edxuserid , email, username,isActive and date joined infromation from iitbombayX
# if error the strings are empty and numbers are negative
# check for email - if correct then validate username , if incorrect username is empty.
#                   if incorrect then check username, if exist return the information that email is empty. 
#                                                     if username doesnot exist return error list.

# Validates student course enrollment information received from teacher in iitbombayx

def validate_course_enrollment(email,course_id):
     course_enrollment_csr=mysql_csr
     course_enrollment_csr.execute("select sce.user_id,sce.is_active,au.is_active from auth_user au,student_courseenrollment sce where sce.user_id=au.id and au.email=%s and sce.course_id=%s",(email,course_id))
     for sce_user_id,sce_is_active,au_is_active in auth_user_csr:
       return [sce_user_id,sce_is_active,au_is_active]
     return [0,0,0]



def get_last_run(api_name):
    
    last_run_date=Api_call.objects.get(api_name=api_name).last_run
    return last_run_date



# Gets all the users from iitbx enrolled to a course in studentDetails table.

def fetch_course_enrollment(course_id,edxcourseid,by,course_level_det):
    mysql_csr=init("root","root","localhost","edxapp").cursor()
    # Get apis last run date 
    runtime = datetime.now()
    api_name="fetch_course_enrollment"
    last_run_date = get_last_run(api_name)
   
    # query to fetch new users enrolled to the course after the last run and insert into student details
    mysql_csr.execute("select user_id,created,is_active,mode from student_courseenrollment where created >= %s and course_id=%s",(last_run_date,edxcourseid))
    for usr_id,created,is_active,mode in mysql_csr :
        stud_det=studentDetails(edxuserid=usr_id, courseid=edxcourseid, edxcreatedon=created, edxis_active=is_active, edxmode=mode,teacherid=course_level_det,roll_no=0,last_update_on=runtime,last_updated_by=by)
        stud_det.save()
    
    #query to fetch users who have changed their enrollment option
    mysql_csr.execute("select user_id,is_active,mode from student_courseenrollment where created < %s and is_active=0 and course_id=%s", (last_run_date,edxcourseid))     
    for usr_id,is_active,mode in mysql_csr :
        update_stud_det=studentDetails.objects.get(edxuserid=usr_id,courseid=edxcourseid)
        update_stud_det.edxis_active=is_active
        update_stud_det.edxmode=mode
        update_stud_det.save() 
   
    #update the api last run
    api=Api_call.objects.get(api_name=api_name)
    api.last_run=runtime
    api.save()


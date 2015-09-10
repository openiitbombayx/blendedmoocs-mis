'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''
#!/usr/bin/env python

import pymongo
import MySQLdb
from pymongo import MongoClient
#from optparse import OptionParser
import argparse
import sys, getopt
project_dir="/home/asl/blended14_07/IITBOMBAYX_PARTNERS"

import sys,os
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='IITBOMBAYX_PARTNERS.settings'
import csv
import django
from django.db import models
from SIP.models import *
from django.db import transaction
import django
django.setup()

prefix_url="https://iitbombayx.in/c4x/IITBombayX/"
infix_url ="/asset/"


def db_openconnection():
	
	cnx = MySQLdb.connect(user='root',passwd='iitb@3dx#2015',host='localhost',db='edxapp')
        return cnx


def mongo_openconnection():
	global client
        print "instide"
	client = MongoClient('mongodb://localhost:27017/')
        print "instide"
	global db 
        print "instide"
	db= client.edxapp
        print "instide"
	global collection
        print "instide" 
	collection = db.modulestore
        print "instide"
        return collection

#@transaction.atomic
def truncate_tables():

        query = ("truncate table edx_grade_policy")
        cursor.execute(query)
        cnx.commit()	
        query = ("truncate table edx_course_gradecriteria")
        cursor.execute(query)
        cnx.commit()
        cursor=cnx.cursor()
        query = ("truncate table edx_courses") 
        cursor.execute(query)
        cnx.commit()
   
#@transaction.atomic
def get_courses(course_name):
  
       collection=mongo_openconnection()
       course_id=""
    #try:
       print "before for",course_name, collection
       for course_det in collection.find({"_id.course":course_name,"_id.category":"course"},{"metadata.start":1,"metadata.end":1,"metadata.enrollment_start":1,"metadata.enrollment_end":1,"metadata.course_image":1,"metadata.display_name":1,"definition.data.grading_policy":1}):
                print("test")
		course_tag=course_det["_id"]["tag"]
		course_org= course_det["_id"]["org"]
		course= course_det["_id"]["course"]
		course_name= course_det["_id"]["name"]
		course_id =course_org+'/'+course+'/'+course_name
		course_disp_name=course_det["metadata"]["display_name"]
		course_enroll_start=course_det["metadata"]["enrollment_start"]
		course_enroll_end=course_det["metadata"]["enrollment_end"]
		course_start=course_det["metadata"]["start"]
		course_end=course_det["metadata"]["end"]
		course_image=course_det["metadata"]["course_image"]
		image_url=prefix_url+course+infix_url+course_image
                print "test"
		course_obj=edxcourses(tag=course_tag, org=course_org, course=course, name=course_name, courseid=course_id, coursename=course_disp_name, enrollstart=course_enroll_start, enrollend=course_enroll_end, coursestart=course_start, courseend=course_end,image=image_url)
		print "test2"
                course_obj.save()
                print "test3"
		get_grade_policy_criteria(course_obj)
                insert_admin_courseleveluser(course_id)
                return course_id
    #except:
    #print "Error Occured while fetching Course data from mongodb"
  
  


#@transaction.atomic
def get_grade_policy_criteria(course_obj):
  collection=mongo_openconnection()
  course=course_obj.courseid.split('/')[1]
  try:
     for course_det in collection.find({"$and": [{"_id.category":"course"},{"_id.course":course }]}):
        course_grading_policy= course_det["definition"]["data"]["grading_policy"]["GRADER"]
        for coursepolicy in course_grading_policy :
            min_count=coursepolicy["min_count"]
            weight=coursepolicy["weight"]
            type=coursepolicy["type"]
            drop_count=coursepolicy["drop_count"]
            short_label=coursepolicy["short_label"]
            print "before grade policy"
            grade_policy_obj=gradepolicy(courseid=course_obj, min_count=min_count, weight=weight ,type=type, drop_count=drop_count, short_label=short_label)
            print "after grade policy"
            grade_policy_obj.save()
        cutoffs=course_det["definition"]["data"]["grading_policy"]["GRADE_CUTOFFS"]
    	for key,value in cutoffs.iteritems():
             	grade_criteria_obj=gradescriteria(courseid=course_obj,grade=key,cutoffs=value)
                grade_criteria_obj.save()
  except:
     print "Error Ocurred:while fetching data grade data from mongodb"

@transaction.atomic
def insert_admin_courseleveluser(courseid):
    try:
      edx_course_obj=edxcourses.objects.get(courseid=courseid)
      instituteid=T10KT_Institute.objects.get(instituteid=0)
      course_level_obj=Courselevelusers(personid_id=1,instituteid=instituteid,courseid_id=edx_course_obj.id,roleid=5,startdate="2005-01-01",enddate="4712-12-31")
      course_level_obj.save()
    except:
     print "Error Occured in inserting data to courseleveluser table"



#@transaction.atomic
def fetch_auth_user(courseid):
    cnx=db_openconnection()
    mysql_csr_insert = cnx.cursor()

    # Get apis last run date 
    runtime = datetime.now()
    api_name="fetch_auth_user"
    last_run_date = get_last_run(api_name)
    print last_run_date,"coursessssssssssssssssssssss",courseid   
    
    
    mysql_csr_insert.execute("select au.id,au.username,au.email,au.date_joined from auth_user au INNER JOIN student_courseenrollment sce ON au.id=sce.user_id where sce.course_id=%s and date(au.date_joined) >= %s",(courseid,last_run_date))
    for edx_id,edx_user,edx_email,date in mysql_csr_insert:
       #print "inside for", edx_user 
       auth_usr_obj=iitbx_auth_user(edxuserid=edx_id,username=edx_user,email=edx_email)
       #print edx_id
       auth_usr_obj.save()
                
    #update the api last run
    api=Api_call.objects.get(api_name=api_name)
    api.last_run=runtime
    #api.save()
    print "Successssssssssssssssssssssss"
     


#@transaction.atomic
def get_student_course_enrollment(course):
        edx_course_obj=edxcourses.objects.get(courseid=course)  
        person_info_obj=Personinformation.objects.get(id=1)
        course_level_obj=Courselevelusers.objects.get(courseid=edx_course_obj,personid=person_info_obj)        
        print course_level_obj.id ,   person_info_obj.id
        fetch_course_enrollment(edx_course_obj.courseid,person_info_obj,course_level_obj)




 
# Gets all the users from iitbx enrolled to a course in studentDetails table.
#@transaction.atomic
def fetch_course_enrollment(edxcourseid,by,course_level_det):

    # Get apis last run date 
    runtime = datetime.now()
    api_name="fetch_course_enrollment"
    last_run_date = get_last_run(api_name)
    print last_run_date,"#################################################################"
    cnx=db_openconnection()
    mysql_csr=cnx.cursor()
    print "select user_id,created,is_active,mode from student_courseenrollment where date(created) >= '%s' and course_id='%s'"%(last_run_date,edxcourseid)   
    # query to fetch new users enrolled to the course after the last run and insert into student details
    mysql_csr.execute("select user_id,created,is_active,mode from student_courseenrollment where date(created) >= %s and course_id=%s",(last_run_date,edxcourseid))
    for usr_id,created,is_active,mode in mysql_csr :
        print "inside for ",usr_id
        stud_det=studentDetails(edxuserid=iitbx_auth_user.objects.get(edxuserid=usr_id), courseid=edxcourseid, edxcreatedon=created, edxis_active=is_active, edxmode=mode,teacherid=course_level_det,roll_no=0,last_update_on=runtime,last_updated_by=by)
        stud_det.save()
  
    
    #query to fetch users who have changed their enrollment option
    mysql_csr.execute("select user_id,is_active,mode from student_courseenrollment where date(created) < %s and is_active=0 and course_id=%s", (last_run_date,edxcourseid))
    if mysql_csr:     
      for usr_id,is_active,mode in mysql_csr :
        update_stud_det=studentDetails.objects.get(edxuserid=iitbx_auth_user.objects.get(edxuserid=usr_id),courseid=edxcourseid)
        update_stud_det.edxis_active=is_active
        update_stud_det.edxmode=mode
        update_stud_det.save() 
   
    #update the api last run
    api=Api_call.objects.get(api_name=api_name)
    api.last_run=runtime
    #api.save()
    




  
def get_last_run(api_name):
    
    last_run_date=Api_call.objects.get(api_name=api_name).last_run
    return last_run_date 
 

@transaction.atomic
def main(argv):
		
	try:
			
		opts, args = getopt.getopt(argv,"hi:",["ifile="])
		print opts,args # opt stores option and args stores arguments of that option 
			
   	except getopt.GetoptError:
		print 'test.py -i <course> '
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <course>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
	db_openconnection()
	#truncate_tables()
	for course in args:
                print course
		course_id=get_courses(course)
                print "***************************************************",course_id
                fetch_auth_user(course_id)
                get_student_course_enrollment(course_id)


if __name__ == "__main__":
	main(sys.argv[1:])






'''
def db_closeconnection(cnx):
	cnx.close()

def fetch_courselist():
'''

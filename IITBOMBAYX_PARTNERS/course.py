'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


#!/usr/bin/env python
from iitbx_settings import *


'''
Input parameter : --
Output Generated: --

Sets the prefix and postfix url for course image
'''
def init():

       global prefix_url
       prefix_url="https://iitbombayx.in/c4x/IITBombayX/"
       global infix_url 
       infix_url="/asset/" 

'''
Input parameter : --
Output Generated: -- return collection point to modulestore

Establishes connection to mongo
'''

def mongo_openconnection():
     global client
     client = MongoClient(mongodb)
     global db 
     db= client.edxapp
     global collection
     collection = db.modulestore
     return collection


'''
Input parameter : csr (Course short name i.e. "CS101.1x")
Output generated: dictionary with key and value 

Fetches alll relevant fields of a course from mongo
'''
def get_course_detail(csr):
     init()
     collection=mongo_openconnection()
     curtime = datetime.now()
     course_id=""
     category_about={}
     category_course={}
 
     for course_det in collection.find({"_id.course":csr,"_id.category":"course"},{"metadata.start":1,"metadata.end":1,"metadata.enrollment_start":1,"metadata.enrollment_end":1,"metadata.course_image":1,"metadata.display_name":1}):               
           category_course["course_tag"] = str(course_det["_id"]["tag"])
           category_course["course_org"] = str(course_det["_id"]["org"])
           category_course["course"] = str(course_det["_id"]["course"])
           category_course["course_name"] = str(course_det["_id"]["name"])
           category_course["course_id"] = str(course_det["_id"]["org"]+'/'+course_det["_id"]["course"]+'/'+course_det["_id"]["name"])
           category_course["course_disp_name"] = str(course_det["metadata"]["display_name"])
           try:
                   temp=course_det["metadata"]["end"]
                   category_course["course_end"] = datetime.strptime(str(temp),'%Y-%m-%dT%S:%M:%HZ')
           except:
                   category_course["course_end"]=date_format("9999-12-31 00:00:00","%Y-%m-%d %H:%M:%S")
          
           try:
                   course_enroll_end=course_det["metadata"]["enrollment_end"]
                   category_course["course_enroll_end"]=str(datetime.strptime(str(course_enroll_end), '%Y-%m-%dT%S:%M:%HZ'))

           except:
                   category_course["course_enroll_end"]=course_end
           try: 
                   course_start=course_det["metadata"]["start"]
                   category_course["course_start"]=datetime.strptime(str(course_start), '%Y-%m-%dT%S:%M:%HZ')
           except:
                   category_course["course_start"]= course_end + timedelta(days=-1)
           try: 
                   course_enroll_start=course_det["metadata"]["enrollment_start"]
                   category_course["course_enroll_start"]=datetime.strptime(str(course_enroll_start), '%Y-%m-%dT%S:%M:%HZ')
           except:
                   category_course["course_enroll_start"]= course_end + timedelta(days=-1)      

           try:
                   category_course["course_image"]=str(course_det["metadata"]["course_image"])
           except:
                   category_course["course_image"]="No Image"
     list_of_names=["short_description","overview","video","effort"]
     
     for course_det in collection.find({"_id.course":csr,"_id.category":"about"},{"definition.data.data":1}):
         if course_det["_id"]["name"] in list_of_names :
            category_about[str(course_det["_id"]["name"])]=course_det["definition"]["data"]["data"]
     return (category_about,category_course)

"""
Input Parameter: --
Output generated : returns list of dictionary, containing required field for https://iitbombayx.in/all_courses/all (i.e. overview) and list of courses(i.e. all_courses),past courses,current courses and new courses

Fetches required field and course based on type (i.e all,past,current and new) for https://iitbombayx.in/all_courses/all
"""


def course_category():

    collection=mongo_openconnection()
    all_courses=[];past_courses=[];new_courses=[];current_courses=[]
    curtime = datetime.now() 
    overview=[]
    for course_det in collection.find({"_id.category":"course"}, {"metadata.start":1,"metadata.end":1,"metadata.course_image":1,"metadata.display_name":1,"metadata.course_image":1}): 
           course_overview={}
           course_overview["course_name"]= course_det["_id"]["course"] 
           course_overview["org"] = course_det["_id"]["org"]
           try: 
                   temp=course_det["metadata"]["end"] 
                   course_overview["course_end"]= datetime.strptime(str(temp),'%Y-%m-%dT%S:%M:%HZ') 
           except: 
                   course_overview["course_end"]=date_format("9999-12-31 00:00:00","%Y-%m-%d %H:%M:%S") 
           try: 
                   course_start=course_det["metadata"]["start"] 
                   course_overview["course_start"]=datetime.strptime(str(course_start), '%Y-%m-%dT%S:%M:%HZ') 
           except: 
                   course_overview["course_start"] = course_end + timedelta(days=-1)
           try:
                   course_overview["course_image"]=str(course_det["metadata"]["course_image"])
           except:
                   course_overview["course_image"]="No Image"
           # For all course 
           all_courses.append(str(course_overview["course_name"]))
           # For past course
           if str(course_overview["course_end"]) < str(curtime): 
              past_courses.append(str(course_overview["course_name"])) 
           #For new course
           elif str(curtime) < str(course_overview["course_start"]): 
              new_courses.append(str(course_overview["course_name"])) 
           #For current course
           elif str(course_overview["course_start"]) <= str(curtime) <= str(course_overview["course_end"]): 
              current_courses.append(str(course_overview["course_name"]))
           course_name = course_overview["course_name"]
           for course_about_det in collection.find({"_id.category":"about","_id.name":"short_description","_id.course":course_name}, {"definition.data.data":1}) :
               course_overview['short_decription']=course_about_det["definition"]["data"]["data"]
           overview.append(course_overview)
           
    return (overview,all_courses,past_courses,current_courses,new_courses)

    



def main(argv):
    #get_course_detail("BMWME209.x")
    #get_course_detail("CS101.1x")
    course_category()

  
if __name__ == "__main__":
    main(sys.argv[1:])




         
           

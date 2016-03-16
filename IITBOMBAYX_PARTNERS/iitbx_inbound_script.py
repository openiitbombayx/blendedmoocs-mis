'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


#!/usr/bin/env python

from iitbx_settings import *
question_types=["<choiceresponse>","<optionresponse>","<multiplechoiceresponse>","<numericalresponse ","<stringresponse ","<drag_and_drop_input","<imageresponse","<formularesponse","<customresponse","<jsmeresponse>","<schematicresponse>"]
def init():

       global prefix_url
       prefix_url="https://iitbombayx.in/c4x/IITBombayX/"
       global infix_url 
       infix_url="/asset/"
  

def dbedxapp_openconnection():
     cnxedxapp = MySQLdb.connect(user=user,passwd=passwd,host=mysql_host,db=mysql_schema)
     return cnxedxapp

def mongo_openconnection():
     global client
     client = MongoClient(mongodb)
     global db 
     db= client.edxapp
     global collection
     collection = db.modulestore
     return collection

@transaction.atomic
def delete_grade_information(cid):
       gradepolicy.objects.filter(courseid=cid).delete()
       gradescriteria.objects.filter(courseid=cid).delete()

@transaction.atomic

def get_course_detail(csr):
     collection=mongo_openconnection()
     curtime = datetime.now()
     course_id=""
     blended = 0
     if str(csr) in courses:
        blended=1
     else:
        blended=0
     for course_det in collection.find({"_id.course":csr,"_id.category":"course"},{"metadata.start":1,"metadata.end":1,"metadata.enrollment_start":1,"metadata.enrollment_end":1,"metadata.course_image":1,"metadata.display_name":1,"definition.data.grading_policy":1}):
                
           course_tag=course_det["_id"]["tag"]
           course_org= course_det["_id"]["org"]
           course= course_det["_id"]["course"]
           course_name= course_det["_id"]["name"]
           course_id =course_org+'/'+course+'/'+course_name
           course_disp_name=course_det["metadata"]["display_name"]
           try:
                   temp=course_det["metadata"]["end"]
                   course_end= datetime.strptime(str(temp),'%Y-%m-%dT%S:%M:%HZ')
           except:
                   course_end=date_format("9999-12-31 00:00:00","%Y-%m-%d %H:%M:%S")
          
           try:
                   course_enroll_end=course_det["metadata"]["enrollment_end"]
                   course_enroll_end=datetime.strptime(str(course_enrol_end), '%Y-%m-%dT%S:%M:%HZ')

           except:
                   course_enroll_end=course_end
           try: 
                   course_start=course_det["metadata"]["start"]
                   course_start=datetime.strptime(str(course_start), '%Y-%m-%dT%S:%M:%HZ')
           except:
                   course_start= course_end + timedelta(days=-1)
           try: 
                   course_enroll_start=course_det["metadata"]["enrollment_start"]
                   course_enroll_start=datetime.strptime(str(course_enroll_start), '%Y-%m-%dT%S:%M:%HZ')
           except:
                   course_enroll_start= course_end + timedelta(days=-1)      

           ahead_date=course_end+ timedelta(days=num_days)
           delta= ahead_date-course_end
           if  ( ahead_date-curtime ).days > 0:
                try:
                   course_image=course_det["metadata"]["course_image"]
                except:
                   course_image="No Image"
                image_url=prefix_url+course+infix_url+course_image
                try:  # if course is there update it
                      course_obj=edxcourses.objects.get(course=course)
                      courseid=course_obj.id
                      course_obj=edxcourses.objects.get(course=csr)
                      course_obj.tag=course_tag
                      course_obj.org=course_org
                      course_obj.course=course
                      course_obj.name=str(course_name)
                      course_obj.courseid=course_id
                      course_obj.coursename=course_disp_name
                      course_obj.enrollstart=course_enroll_start      
                      course_obj.enrollend=course_enroll_end
                      course_obj.coursestart=course_start
                      course_obj.courseend=course_end
                      course_obj.image=image_url
                      course_obj.blended_mode=blended
                        
                      try:
                        course_obj.save()
                      except Exception as e:
                         print "Error %s,(%s) - Insert on %s. Contact Software team."%(e.message,str(type(e)),course_id) 
                      try:
                         delete_grade_information(course_id)
                         if (get_grade_policy_criteria(course_obj) == -1) :
                             print "Issue in getting grade policy and criteria"
                      except Exception as e:
                          print "Error %s,(%s) - Update on %s. Contact Software team."%(e.message,str(type(e)),course_id)
                          return "-1"
                except Exception as e: # else insert the courses 
                    course_obj=edxcourses(tag=course_tag, org=course_org, course=course, name=course_name, courseid=course_id, coursename=course_disp_name, enrollstart=course_enroll_start, enrollend=course_enroll_end, coursestart=course_start, courseend=course_end,image=image_url,blended_mode=blended)
                    
                    course_obj.save()
                    if( get_grade_policy_criteria(course_obj) == -1):
                        print "Issue in getting grade policy and criteria"
                if blended == "1":
                   try:       
                       if (insert_admin_courseleveluser(course_id) == -1):
                          print "Issue in inserting admin courseleveluser"
                   except Exception as e:
                       print "Error %s,(%s) insert of course level users on %s. Contact Software team."%(e.message,str(type(e)),course_id)
                       return "-1"
     return course_id

@transaction.atomic
def get_grade_policy_criteria(course_obj):
  
  collection=mongo_openconnection()
 
  course=course_obj.courseid.split('/')[1]
  try:
     for course_det in collection.find({"$and": [{"_id.category":"course"},{"_id.course":course }]}):
        course_grading_policy= course_det["definition"]["data"]["grading_policy"]["GRADER"]
        for coursepolicy in course_grading_policy :
            min_count=coursepolicy["min_count"]
            weight=coursepolicy["weight"]
            ptype=coursepolicy["type"]
            drop_count=coursepolicy["drop_count"]
            short_label=coursepolicy["short_label"]
            grade_policy_obj=gradepolicy(courseid=course_obj, min_count=min_count, weight=weight ,type=ptype, drop_count=drop_count, short_label=short_label)
            grade_policy_obj.save()

            cutoffs=course_det["definition"]["data"]["grading_policy"]["GRADE_CUTOFFS"]
            for key,value in cutoffs.iteritems():
                grade_criteria_obj=gradescriteria(courseid=course_obj,grade=key,cutoffs=value)
                grade_criteria_obj.save()

     return 0
  except Exception as e:
     print "Error %s - Fetching grade criteria and Policy from mongodb for course %s "%(e.message,course_obj.courseid)
     return -1

@transaction.atomic
def insert_admin_courseleveluser(courseid):
    
    try:
      try:
         course_obj=edxcourses.objects.get(courseid=courseid)
      except Exception as e:
         print "Error %s,(%s) - Fetching course object for " %(e.message,str(type(e)),courseid)
         return -1
      try:
         instituteid=T10KT_Institute.objects.get(instituteid=0)
      except Exception as e:
         print "Error %s,(%s) -Fetching Institute object for " %(e.message,str(type(e)),courseid)
         return -1
      
      if Courselevelusers.objects.filter(personid_id=1,instituteid=instituteid,courseid_id=course_obj.id,roleid=5).exists():
         pass # No modification required for courselevelusers
      else:   #insert default teacher with personid=1 and instituteid=0 in courselevelusers table
        person_obj=Personinformation.objects.get(id=1)
        print instituteid, person_obj.email
        course_level_obj=Courselevelusers(personid=person_obj,instituteid=instituteid,courseid=course_obj,roleid=5,startdate="2005-01-01",enddate="4712-12-31")
        course_level_obj.save()
        return 0
    except Exception as e:
     print "Error  %s,(%s) - Insert of courseleveluser for " %(e.message,str(type(e)),courseid)
     return -1
      



@transaction.atomic
def get_student_course_enrollment(course):
    try:
        edx_course_obj=edxcourses.objects.get(courseid=course)

    except Exception as e:
         print "Error  %s,(%s) - EdxCourse object for course %s doesnot exists"%(e.message,str(type(e)),course)
         return   [-1]
    try:
        person_info_obj=Personinformation.objects.get(id=1)
    except Exception as e:
         print "Error  %s,(%s) -Personinformation object for default user doesnot exist while finding enrollments for %s"%(e.message,str(type(e)),course)
         return  [-1] 
    try:   
           course_level_obj=Courselevelusers.objects.get(courseid=edx_course_obj,personid=person_info_obj)
    except Exception as e:
          print "Error  %s,(%s) -Courselevel default user is not present for %s "%(e.message,str(type(e)),course)
          return [-1]   
   
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error  %s,(%s) -Establishing mysql connection"%(e.message,str(type(e)))
      return [-1]

    insertuser=0
    insertstudent=0
    updatestudent=0
    erroruser=0
    errorstudent=0    
    errorupdate=0
    runtime = datetime.now()
    
    # query to fetch new users enrolled to the course after the last run and insert into student details
    mysql_csr.execute("select b.user_id,a.username,a.email ,b.created,b.is_active,b.mode from auth_user a,student_courseenrollment b where  b.course_id= %s and b.user_id=a.id and not exists (select * from iitbxblended.SIP_studentdetails  s where s.courseid=b.course_id and b.user_id=s.edxuserid_id)",(course,))

    
    studrecords=mysql_csr.fetchall()
    for record in studrecords :
       try:
         auth_usr_obj=iitbx_auth_userobjects.get(edxuserid=record[0])
       except Exception as e:
           try:
             auth_usr_obj=iitbx_auth_user(edxuserid=record[0],username=record[1],email=record[2])
             auth_usr_obj.save()
             insertuser=insertuser+1 
           except Exception as e:
             print" Error  %s,(%s) -Inserting new user %s" %(e.message,str(type(e)),record) 
             erroruser=erroruser+1
             continue
       try:  
         stud_det=studentDetails(edxuserid=auth_usr_obj, courseid=course,edxcreatedon=record[3],edxis_active=record[4], edxmode=record[5],teacherid=course_level_obj,roll_no=0,last_update_on=runtime,last_updated_by=person_info_obj)
         stud_det.save()
         insertstudent=insertstudent+1
       except Exception as e: 
         print "Error  %s,(%s) -Inserting studentdetails %s "%(e.message,str(type(e)), record[0])
         errorstudent=errorstudent+1
         continue
      
    #query to fetch users who have changed their enrollment option
    mysql_csr.execute("select b.user_id,a.username,a.email ,b.created,b.is_active,b.mode from auth_user a,student_courseenrollment b where  b.course_id=%s and b.user_id=a.id and exists (select * from iitbxblended.SIP_studentdetails  s where s.courseid=b.course_id and b.user_id=s.edxuserid_id and b.is_active != s.edxis_active)",(course,))
    updated_student_enroll=mysql_csr.fetchall()     
    for record in updated_student_enroll :
       try:
          edxuser=iitbx_auth_user.objects.get(edxuserid=record[0])  
       except Exception as e:
          print" Error  %s,(%s) -Get existing user %s"%(e.message,str(type(e)), record) 
          erroruser=erroruser+1
          continue
       try: 
          update_stud_det=studentDetails.objects.get(edxuserid=edxuser,courseid=edx_course_obj.courseid)
          update_stud_det.edxis_active=record[4]
          update_stud_det.save()
          updatestudent=updatestudent+1 
       except Exception as e:
          print"Error  %s,(%s) -Updating studentdetails %s"%(e.message,str(type(e)), record)
          errorupdate=errorupdate+1
          continue 
    return [insertuser,insertstudent,updatestudent,erroruser,errorstudent,errorupdate]  

@transaction.atomic
def fetch_evaluations(course_id):
     collection=mongo_openconnection()
     inserted_vertical_count=0
     inserted_problem_count =0
     updated_problem_count =0 
     error_vertical_count=0
     error_problem_count=0
     error_updated_count=0  
     runtime = datetime.now() 
     status=[]
     course=course_id.split('/')[1]
     try:   
          edx_course_obj=edxcourses.objects.get(courseid=course_id)
     except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(e.message,str(type(e)), course_id)
          return [-1]
     try:    
          grades_obj=gradepolicy.objects.filter(courseid_id=course_id).exclude(weight=0)
     except Exception as e:
          print "Error - %s,(%s) ,Grading Policy for %s doesnot exists"%(e.message,str(type(e)), course_id)
          return [-1]
     for grade_type in grades_obj:
         try:
            grade_weight=grade_type.weight/(grade_type.min_count -grade_type.drop_count)     
         except:
            grade_weight=grade_type.weight
         for sequential in collection.find({"_id.category":"sequential", "_id.course":course, "metadata.graded":True, "metadata.format":grade_type.type}, {"metadata.display_name":1, "metadata.format":1,  "metadata.start":1,  "metadata.due":1, "definition.children":1,"_id.name":1}):
                        sequential_id=sequential["_id"]["name"]    #sectionid
                        seq_name=sequential["metadata"]["display_name"].encode('utf-8')    #sec_name
                        try:
                          
                                                    
                          due_date=datetime(*map(int, re.split('[^\d]', sequential["metadata"]["due"])[:-1]))
                          
                          
                        except:
                          due_date=runtime

                       
                        try:
                          
                          release_date=datetime(*map(int, re.split('[^\d]', sequential["metadata"]["start"])[:-1]))
                          
                        except Exception as e :
                          
                          release_date=due_date
                        
                           
                        for verticals in  sequential["definition"]["children"]:
                            if "vertical" in verticals:
                                 total_weight =0
                                 vertical_id = verticals.split('/')[5]
                                 vertical_det=collection.find({"_id.category":"vertical","_id.name":vertical_id,"_id.course":course },{"metadata.display_name":1,"definition.children":1}).limit(1)
                                 for vdetails in vertical_det:
                                    vertical_name= vdetails["metadata"]["display_name"] 
                                    
                                    try:
                                         evaluations_obj=evaluations.objects.get(subsec_id=vertical_id,course=edx_course_obj)
                                         evaluations_obj.sec_name=seq_name
                                         evaluations_obj.release_date=release_date
                                         evaluations_obj.due_date=due_date=due_date
                                         evaluations_obj.subsec_name=vertical_name
                                         evaluations_obj.grade_weight=grade_weight
                                         evaluations_obj.save()
                                    except Exception as e:
                                         try:
                                           evaluations_obj=evaluations(course=edx_course_obj, sectionid=sequential_id,sec_name=seq_name, subsec_id=vertical_id, subsec_name=vertical_name,type=grade_type.type ,release_date=release_date, due_date=due_date, total_weight=0 ,grade_weight=grade_weight)
                                           evaluations_obj.save()
                                           inserted_vertical_count=inserted_vertical_count+1
                                         except Exception as e:
                                           print "Insert Error - %s,(%s)- Vertical Entry failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,str(type(e)),course_id,grade_type,vertical_id,vertical_name,seq_name)
                                           error_vertical_count=error_vertical_count+1
                                           continue

                                    
                                    result=fetch_questions(vertical_id,course,course_id,edx_course_obj,grade_type.type,vdetails["definition"]["children"],evaluations_obj)
                                    
                                    inserted_problem_count+=result[0]
                                    updated_problem_count+=result[1]
                                    error_problem_count+=result[2]
                                    error_updated_count+=result[3]
                                    total_weight =total_weight + result[4]
                                    try:
                                      evaluations_obj.total_weight=total_weight
                                      evaluations_obj.save()
                                    except:
                                      print "Error - %s,(%s)- Vertical Entry weight update failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,str(type(e)),course_id,grade_type,vertical_id,vertical_name,seq_name)

     del_list=update_deleted_evaluations(edx_course_obj)
     return [inserted_vertical_count,inserted_problem_count,updated_problem_count,error_vertical_count,error_problem_count,    error_updated_count,del_list[1],del_list[0]] 

@transaction.atomic
def fetch_gen_evaluations(course_id):
     collection=mongo_openconnection()
     inserted_vertical_count=0
     inserted_problem_count =0
     updated_problem_count =0 
     error_vertical_count=0
     error_problem_count=0
     error_updated_count=0  
     runtime = datetime.now() 
     status=[]
     course=course_id.split('/')[1]
     try:   
          edx_course_obj=edxcourses.objects.get(courseid=course_id)
     except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(e.message,str(type(e)), course_id)
          return [-1]
     try:    
          grades_obj=gradepolicy.objects.filter(courseid_id=course_id).exclude(weight=0)
     except Exception as e:
          print "Error - %s,(%s) ,Grading Policy for %s doesnot exists"%(e.message,str(type(e)), course_id)
          return [-1]
     grade_weight=0.0
     for grade_type in grades_obj:
         try:
            grade_weight=grade_type.weight/(grade_type.min_count -grade_type.drop_count)     
         except:
            grade_weight=grade_type.weight
         for sequential in collection.find({"_id.category":"sequential", "_id.course":course, "metadata.graded":True, "metadata.format":grade_type.type}, {"metadata.display_name":1, "metadata.format":1,  "metadata.start":1,  "metadata.due":1, "definition.children":1,"_id.name":1}):
                        sequential_id=sequential["_id"]["name"]    #sectionid
                        seq_name=sequential["metadata"]["display_name"].encode('utf-8')    #sec_name
                        try:
                          
                          #release_date=datetime(*map(int, re.split('[^\d]', sequential["metadata"]["start"].getdate())[:-1]))
                          release_date= sequential["metadata"]["start"]
                          release_date=datetime.strptime(str(release_date), '%Y-%m-%dT%S:%M:%HZ')
                        except Exception as e :
                          
                          release_date=runtime
                        try:
                          
                          due_date= sequential["metadata"]["due"]
                          due_date=datetime.strptime(str(due_date), '%Y-%m-%dT%S:%M:%HZ')                          
                        except Exception as e:
                          
                          due_date=runtime
                        
                           
                        for verticals in  sequential["definition"]["children"]:
                            if "vertical" in verticals:
                                 total_weight =0
                                 vertical_id = verticals.split('/')[5]
                                 vertical_det=collection.find({"_id.category":"vertical","_id.name":vertical_id,"_id.course":course },{"metadata.display_name":1,"definition.children":1}).limit(1)
                                 for vdetails in vertical_det:
                                    vertical_name= vdetails["metadata"]["display_name"].encode('utf-8')
                                    
                                    try:
                                         evaluations_obj=gen_evaluations.objects.get(subsec_id=vertical_id,course=edx_course_obj)
                                         evaluations_obj.sec_name=str(seq_name)
                                         evaluations_obj.release_date=release_date
                                         evaluations_obj.due_date=due_date=due_date
                                         evaluations_obj.subsec_name=str(vertical_name)
                                         evaluations_obj.grade_weight=grade_weight
                                         evaluations_obj.save()
                                    except Exception as e:
                                      try:
                                          evaluations_obj=gen_evaluations(course=edx_course_obj, sectionid=sequential_id,sec_name=str(seq_name), subsec_id=vertical_id, subsec_name=str(vertical_name),type=grade_type.type ,release_date=release_date, due_date=due_date, total_weight=0 ,grade_weight=grade_weight)
                                          evaluations_obj.save()
                                          inserted_vertical_count=inserted_vertical_count+1
                                      except Exception as e:
                                           
                                           print "InsertError - %s,(%s)- Vertical Entry failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,str(type(e)),course_id,grade_type.type,vertical_id,vertical_name,seq_name)
                                           #error_vertical_count=error_vertical_count+1
                                           #continue
      
                                    result=fetch_gen_questions(vertical_id,course,course_id,edx_course_obj,grade_type.type,vdetails["definition"]["children"],evaluations_obj)
                                    
                                    inserted_problem_count+=result[0]
                                    updated_problem_count+=result[1]
                                    error_problem_count+=result[2]
                                    error_updated_count+=result[3]
                                    total_weight =total_weight + result[4]
                                    try:
                                      evaluations_obj=gen_evaluations.objects.get(subsec_id=vertical_id)   
                                      evaluations_obj.total_weight=total_weight
                                      evaluations_obj.save()
                                    except:
                                      print "Error - %s,(%s)- Vertical Entry weight update failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,str(type(e)),course_id,grade_type,vertical_id,vertical_name,seq_name)

     del_list=update_deleted_gen_evaluations(edx_course_obj)
     return [inserted_vertical_count,inserted_problem_count,updated_problem_count,error_vertical_count,error_problem_count,    error_updated_count,del_list[1],del_list[0]] 


@transaction.atomic   
def update_deleted_evaluations(edx_course_obj):
    del_ques =0
    del_eval =0
    eval_list=evaluations.objects.filter(course=edx_course_obj)
    for eval in eval_list:
       tobedeleted=True

       vertical_det=collection.find({"_id.category":"vertical","_id.name":eval.subsec_id,"_id.course":edx_course_obj.course },{"metadata.display_name":1,"definition.children":1,"metadata.visible_to_staff_only":1})
       for vertical in vertical_det:

           tobedeleted =False
           try:
              if vertical['metadata']['visible_to_staff_only'] == True:
                 tobedeleted=True
           except:
                 tobedeleted =False

       long_seq_name="i4x://IITBombayX/"+ edx_course_obj.course +"/sequential/"+eval.sectionid
       for ch in collection.find({"_id.category":"chapter","definition.children":long_seq_name,"_id.course":edx_course_obj.course},{"metadata.visible_to_staff_only" : 1,"metadata.display_name":1}):
          try:
              if(ch['metadata']['visible_to_staff_only'] ==True):
                tobedeleted =True
          except:
              None
       ques_list = questions.objects.filter(eval=eval)   
              
       for ques in ques_list:
           
           delprob=True
           quesid=ques.qid.split('/')[5]
           for problem in collection.find({"_id.category":"problem","_id.name":quesid,"_id.course":edx_course_obj.course},{"metadata.display_name":1,"metadata.weight":1,"edit_info.published_date":1,"edit_info.edited_on":1,"metadata.visible_to_staff_only":1}): 

               delprob =False

               try:
                  if vertical['metadata']['visible_to_staff_only'] == True:
                  
                      delprob=True
               except:
                      delprob =False


           if delprob == True:
                 result.objects.filter(question=ques).delete()
                 ques.delete()
                 del_ques=del_ques+1
       if tobedeleted == True:
              result.objects.filter(question=questions.objects.filter(eval=eval)).delete()
              questions.objects.filter(eval=eval).delete()
              eval.delete()
              del_eval=del_eval+1
       evaluation_objs=evaluations.objects.exclude(id__in=[ques.eval_id for ques in questions.objects.all()])
       for eval in evaluation_objs:
           eval.delete()
           del_eval=del_eval+1
    return [del_ques,del_eval]



@transaction.atomic
def update_deleted_gen_evaluations(edx_course_obj):
    del_ques =0
    del_eval =0
    eval_list=gen_evaluations.objects.filter(course=edx_course_obj)
    for eval in eval_list:
       tobedeleted=True

       vertical_det=collection.find({"_id.category":"vertical","_id.name":eval.subsec_id,"_id.course":edx_course_obj.course },{"metadata.display_name":1,"definition.children":1,"metadata.visible_to_staff_only":1})
       for vertical in vertical_det:

           tobedeleted =False
           try:
              if vertical['metadata']['visible_to_staff_only'] == True:
                 tobedeleted=True
           except:
                 tobedeleted =False

       long_seq_name="i4x://IITBombayX/"+ edx_course_obj.course +"/sequential/"+eval.sectionid
       for ch in collection.find({"_id.category":"chapter","definition.children":long_seq_name,"_id.course":edx_course_obj.course},{"metadata.visible_to_staff_only" : 1,"metadata.display_name":1}):
          try:
              if(ch['metadata']['visible_to_staff_only'] ==True):
                tobedeleted =True
          except:
              None
       ques_list = gen_questions.objects.filter(eval=eval)   
              
       for ques in ques_list:
           
           delprob=True
           quesid=ques.qid.split('/')[5]
           for problem in collection.find({"_id.category":"problem","_id.name":quesid,"_id.course":edx_course_obj.course},{"metadata.display_name":1,"metadata.weight":1,"edit_info.published_date":1,"edit_info.edited_on":1,"metadata.visible_to_staff_only":1}): 

               delprob =False

               try:
                  if vertical['metadata']['visible_to_staff_only'] == True:
                  
                      delprob=True
               except:
                      delprob =False


           if delprob == True:
                 ques.delete()
                 del_ques=del_ques+1
       if tobedeleted == True:
              gen_questions.objects.filter(eval=eval).delete()
              eval.delete()
              del_eval=del_eval+1
       evaluation_objs=gen_evaluations.objects.exclude(id__in=[ques.eval_id for ques in gen_questions.objects.all()])
       for eval in evaluation_objs:
           eval.delete()
           del_eval=del_eval+1
    return [del_ques,del_eval]

@transaction.atomic
def fetch_questions(vertical_id,course,course_id,edx_course_obj,gtype,problist,evaluations):
     inserted_problem_count =0
     updated_problem_count =0 
     error_problem_count=0
     error_updated_count=0 
     weight=0   
     runtime = datetime.now()  
     for problemlist in problist:
         if "problem" in problemlist:
                weight=0
                problem_id=problemlist.split('/')[5]
                p_id=problemlist
                problem_details= collection.find({"_id.category":"problem","_id.name":problem_id,"_id.course":course},{"metadata.display_name":1,"metadata.weight":1,"edit_info.published_date":1,"edit_info.edited_on":1,"definition.data.data":1})
                
                for problemdet in  problem_details:
                            
                            try:
                                edited_on=problemdet["edit_info"]["edited_on"]
                            except:
                                edited_on=runtime
                            try:
                                published_on=problemdet["edit_info"]["published_date"]
                            except:
                                published_on=datetime.strptime("1900-01-01 00:00:01.78200", "%Y-%m-%d %H:%M:%S.%f")
                            if (edited_on > published_on):
                               
                               continue;                   
                            try: 
                                problem_name=problemdet["metadata"]["display_name"]
                            except:
                                problem_name=""
                            definition_data=problemdet['definition']['data']['data'].encode('utf-8')
                            try:
                                weight=problemdet["metadata"]["weight"]
                                
                            except Exception as e:
                                for type in question_types:
                                    weight+=definition_data.count(type)
                            count=0
                            for type in question_types:
                                    count+=definition_data.count(type)
                                
                            try:
                                problem_obj=questions.objects.get( qid=p_id)
                                try: 
                                  problem_obj.q_weight=weight
                                  problem_obj.q_name=problem_name
                                  problem_obj.prob_count=count
                                  problem_obj.save()
                       
                                  updated_problem_count=updated_problem_count+1
                                except Exception as e:
                                  print "Error - %s,(%s) while updating  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, str(type(e)),problem_id,problem_name,vertical_id,vertical_name,gtype,course_id)
                                  error_updated_count=error_updated_count+1                          
                            except Exception as e:
                                 try:
                                      questions_obj=questions(course=edx_course_obj, eval=evaluations, qid=p_id, q_name=problem_name, q_weight=weight,prob_count=count)
                                      questions_obj.save()
                                      inserted_problem_count=inserted_problem_count+1
                                 except Exception as e:                  
                                     print "Error- %s,(%s) while insert  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, str(type(e)),problem_id,problem_name,vertical_id,vertical_name,gtype,course_id)
                                     error_problem_count=error_problem_count+1
 
     return [inserted_problem_count,updated_problem_count,error_problem_count,error_updated_count,weight]

@transaction.atomic
def fetch_gen_questions(vertical_id,course,course_id,edx_course_obj,gtype,problist,evaluations):
     inserted_problem_count =0
     updated_problem_count =0 
     error_problem_count=0
     error_updated_count=0 
     weight=0   
     runtime = datetime.now()  
     for problemlist in problist:
         if "problem" in problemlist:
                weight=0
                problem_id=problemlist.split('/')[5]
                p_id=problemlist
                problem_details= collection.find({"_id.category":"problem","_id.name":problem_id,"_id.course":course},{"metadata.display_name":1,"metadata.weight":1,"edit_info.published_date":1,"edit_info.edited_on":1,"definition.data.data":1})
                
                for problemdet in  problem_details:
                            weight=0
                            try:
                                edited_on=problemdet["edit_info"]["edited_on"]
                            except:
                                edited_on=runtime
                            try:
                                published_on=problemdet["edit_info"]["published_date"]
                            except:
                                published_on=datetime.strptime("1900-01-01 00:00:01.78200", "%Y-%m-%d %H:%M:%S.%f")
                            if (edited_on > published_on):
                               
                               continue;                   
                            try: 
                                problem_name=problemdet["metadata"]["display_name"]
                            except:
                                problem_name=""
                            definition_data=problemdet['definition']['data']['data'].encode('utf-8')
                            try:
                                weight=problemdet["metadata"]["weight"]
                                
                            except Exception as e:
                                for type in question_types:
                                    weight+=definition_data.count(type)
                            count=0
                            for type in question_types:
                                    count+=definition_data.count(type)
                            try:
                                problem_obj=gen_questions.objects.get( qid=p_id)
                                try: 
                                  problem_obj.q_weight=weight
                                  problem_obj.q_name=problem_name
                                  problem_obj.prob_count=count
                                  problem_obj.save()
                                  updated_problem_count=updated_problem_count+1
                                except Exception as e:
                                  
                                  print "Error - %s,(%s) while updating  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, str(type(e)),problem_id,problem_name,vertical_id,vertical_name,gtype,course_id)
                                  error_updated_count=error_updated_count+1  
                                                         
                            except Exception as e:
                                 try:
                                      questions_obj=gen_questions(course=edx_course_obj, eval=evaluations, qid=p_id, q_name=problem_name, q_weight=weight,prob_count=count)
                                      questions_obj.save()
                                      inserted_problem_count=inserted_problem_count+1
                                 except Exception as e:                  
                                     print "Error- %s,(%s) while insert  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, str(type(e)),problem_id,problem_name,vertical_id,vertical_name,gtype,course_id)
                                     error_problem_count=error_problem_count+1
                                      
 
     return [inserted_problem_count,updated_problem_count,error_problem_count,error_updated_count,weight]

@transaction.atomic

def get_student_grades(course_id):
    insert_count=0
    update_count=0
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error-%s,(%s) -Establishing mysql connection for %s" %(e.message,str(type(e)),course_id)
      return [-1] 
    try:
      mysql_csr.execute("insert into iitbxblended.SIP_result(question_id,edxuserid,grade,maxgrade) SELECT a.id,b.student_id,b.grade,b.max_grade FROM `courseware_studentmodule`b,iitbxblended.SIP_questions a where b.module_id =a.qid  and b.course_id='%s'and b.grade is not null and not exists (select * from iitbxblended.SIP_result r where r.question_id = a.id and r.edxuserid=b.student_id)" %(course_id))
      insert_count=mysql_csr.rowcount
      cnx.commit()
    except Exception as e:
       print "Error-%s,(%s) -Insert Grades for %s" %(e.message,str(type(e)),course_id)
       return [-1]
    try:
       mysql_csr.execute('''UPDATE iitbxblended.SIP_result r,
`courseware_studentmodule` b,
iitbxblended.SIP_questions a SET r.grade = b.grade,
r.maxgrade = b.max_grade WHERE b.module_id = a.qid AND b.course_id='%s' AND b.grade IS NOT NULL AND r.question_id = a.id AND r.edxuserid = b.student_id AND r.grade != b.grade ''' %(course_id))
       update_count=mysql_csr.rowcount
       cnx.commit()
    except Exception as e:
       print "Error-%s,(%s) -Update Grades for %s" %(e.message,str(type(e)),course_id)
       return [-1]
    
    return [insert_count,update_count]

@transaction.atomic
def evaldata(course_id):
     
     runtime = datetime.now()
     inserteval=0
     updateeval=0
     course=course_id.split('/')[1]
     try:   
          courseobj=edxcourses.objects.get(courseid=course_id)
          
     except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(e.message,str(type(e)), course_id)
          return [-1]
     evals=evaluations.objects.filter(course=courseobj,release_date__lte=runtime).values('sectionid').distinct()
     for eval in evals:
         ques_dict={}
         secid=str(eval['sectionid'])
         evaluation_obj=questions.objects.filter(course=courseobj,eval__sectionid=secid ).exclude(q_weight=0 ).order_by('eval_id','id')
         heading = ["Rollno","Username","Email Id"]
         count=0
         totalweight=0
         not_attempt=[]
         qlist=[]
         for evaluate in evaluation_obj:
           count=count+1
           totalweight=totalweight+evaluate.q_weight
           quesname="Q"+str(count).zfill(2)+"<br>MM:"+str(evaluate.q_weight)
           ques_dict[evaluate.qid]=count-1
           not_attempt.append("NA")
           qlist.append(quesname)
         heading.append("Total <br>MM:"+str(totalweight))
         heading=heading+qlist
         
         try:
            headers=headings.objects.get(section=evaluate.eval.sectionid)   
            headers.heading=",".join(map(str,heading))
            headers.save()
         except Exception as e:
            heading_obj=headings(heading=",".join(map(str,heading)),section=evaluate.eval.sectionid)
            heading_obj.save()
         stud_list = studentDetails.objects.filter(courseid=course_id)
         grade_list=[]
         stud_rec=[]
         for studvalue in stud_list:
                totalmark=0.0
                avgmarks=0.0 
                quiz_res=result.objects.filter(edxuserid=studvalue.edxuserid.edxuserid,question__eval__sectionid=secid).exclude(question__q_weight=0 ).order_by('question__id')
                quizdata=[]
                for res in quiz_res:
                     quizmark=round((res.grade/res.maxgrade)*res.question.q_weight,2) ###check it 
                     totalmark=totalmark+quizmark
                     while (len(quizdata) < ques_dict[res.question.qid]):
                       quizdata.append("NA")
                     quizdata.append(round(quizmark,2))
                     try:
                       avgmarks=totalmark/totalweight
                       total=round(totalmark,2)
                     except:
                       avgmarks=0.0
                if quizdata != []:
                   while len(quizdata) <= max(value for (key,value) in ques_dict.items()):
                      quizdata.append("NA")
                elif quizdata == []:
                     quizdata=not_attempt
                     total="NA"
                     while len(quizdata) < count:
                        quizdata.append("NA")
    
                res=",".join(map(str, quizdata))
                
                
                try:
                   marks_obj=markstable.objects.get(stud=studvalue,section=secid)
                   marks_obj.eval=res
                   marks_obj.total=total
                   marks_obj.save()
                   updateeval = updateeval +1
                except Exception as e:
                   marks_obj=markstable(stud=studvalue,section=secid,eval=res,total=total)
                   marks_obj.save() 
                   inserteval=inserteval+1
           
     return [inserteval,updateeval]
#end evaldata()



@transaction.atomic
def gen_evaldata(course_id):
     
     runtime = datetime.now()
     inserteval=0
     updateeval=0
     try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
     except Exception as e:
      print "Error  %s,(%s) -Establishing mysql connection"%(e.message,str(type(e)))
      return [-1]
     course=course_id.split('/')[1]
     try:   
          courseobj=edxcourses.objects.get(courseid=course_id)
     except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(e.message,str(type(e)), course_id)
          return [-1]
     
     evals=gen_evaluations.objects.filter(course=courseobj.id,release_date__lte=runtime).values('sectionid').distinct()
     sqlmod=""
     for eval in evals:
         ques_dict={}
         secid=str(eval['sectionid'])
         
         sqlmod=""
         evaluation_obj=gen_questions.objects.filter(course=courseobj.id,eval__sectionid=secid ).exclude(q_weight=0 ).order_by('eval_id','id')
         
         heading = ["UserId","Username","Email Id"]
         count=0
         totalweight=0
         not_attempt=[]
         qlist=[]
         qidslist=[]
         for evaluate in evaluation_obj:
           if evaluate.q_weight != 0:
              sqlmod= sqlmod +'"'+evaluate.qid+'",'
              qidslist.append(evaluate.qid) 
           
           count=count+1
           totalweight=totalweight+evaluate.q_weight
           
           quesname="Q"+str(count).zfill(2)+"<br>MM:"+str(evaluate.q_weight)
           ques_dict[evaluate.qid]=count-1
           not_attempt.append("NA")
           qlist.append(quesname)
         heading.append("Total <br>MM:"+str(totalweight))
         heading=heading+qlist
         na=",".join(map(str, not_attempt)) 
         pheading=""
         pheading=",".join(map(str,heading))
         
         try:
            headers=gen_headings.objects.get(section=secid)   
            headers.heading=pheading
            headers.save()
         except Exception as e:
            heading_obj=gen_headings(heading=pheading,section=secid)
            heading_obj.save()
         
         sqlmod=sqlmod[:-1]
         if len(sqlmod) == 0:
            continue
         sqlstmt= "SELECT q.qid,q.q_name,c.student_id,round(c.grade/c.max_grade*q.q_weight,2)  FROM iitbxblended.iitbx_gen_evaluations e, iitbxblended.iitbx_gen_questions q ,edxapp.courseware_studentmodule c WHERE e.`course_id` = %s and q.eval_id = e.id and c.course_id= %s and q.qid in (%s) and c.module_type= %s and c.module_id = q.qid and c.grade is not NULL  order by c.student_id, q.id" %(str(courseobj.id),'"'+str(courseobj.courseid)+'"',(sqlmod),'"'+"problem"+'"')
         
         mysql_csr.execute(sqlstmt)
         studrecords=mysql_csr.fetchall()
         total=len(studrecords)
        
         if (total != 0):
             ctr=0
             studrec=[0,0,0,0]
             oldstud=0
             total_grade=0.0
             marks={}
             questions_marks=[]
             t=0
             while(ctr< total) :
               studrec=studrecords[ctr]
               if oldstud == 0:
                 oldstud=studrec[2]
               if studrec[2] == oldstud: 
                      total_grade=total_grade+studrec[3]
                      marks[studrec[0]]=studrec[3] 
                      ctr=ctr+1
               else: 
                  for qid in qidslist:
                     if (marks.has_key(qid)):
                        questions_marks.append(marks[qid])
                        t=t+marks[qid]
                     else:  
                        questions_marks.append('NA')
                  res=",".join(map(str,questions_marks))
                  try:
                   
                     marks_obj=gen_markstable.objects.get(edxuserid=oldstud,section=secid)
                     marks_obj.eval=res
                     marks_obj.total=t
                     marks_obj.save()
                     updateeval = updateeval +1
                  except Exception as e:
                     marks_obj=gen_markstable(edxuserid=oldstud,section=secid,eval=res,total=t)
                     marks_obj.save() 
                     inserteval=inserteval+1      
                  marks={};total_grade=0.0;questions_marks=[];t=0
                  total_grade=total_grade+studrec[3]
                  marks[studrec[0]]=studrec[3] 
                  oldstud=studrec[2]
                  ctr=ctr+1
             if oldstud !=0:
                  for qid in qidslist:
                     if (marks.has_key(qid)):
                        questions_marks.append(marks[qid])
                        t=t+marks[qid]
                     else:  
                        questions_marks.append('NA')
                  res=",".join(map(str,questions_marks))
                  try:
                   
                     marks_obj=gen_markstable.objects.get(edxuserid=oldstud,section=secid)
                     marks_obj.eval=res
                     marks_obj.total=t
                     marks_obj.save()
                     updateeval = updateeval +1
                  except Exception as e:
                     marks_obj=gen_markstable(edxuserid=oldstud,section=secid,eval=res,total=t)
                     marks_obj.save() 
                     inserteval=inserteval+1      
                  
         else:
            ctr=0
            studrec = [0,0,0,0]
              #return [inserteval,updateeval]
     return [0,0]
     
#end evaldata()

def print_report(status,course_id, result):
    print "Status Report for ",course_id
    print ""
    if (status[0] !=-1):
        print "Total Number of iitbx_auth_user Inserted ",status[0]
        print "Total Number of studentDetails Inserted ",status[1]
        print "Total Number of studentDetails Updated ",status[2]
        print "Total Number of iitbx_auth_user Error ",status[3]
        print "Total Number of studentDetails Insert Error ",status[4]
        print "Total Number of studentDetails Update Error ",status[5]
    if (result[0]!= -1):
        print "Total Number of Verticals Inserted ",result[0]
        print "Total Number of Verticals Deleted ",result[6]
  
        print "Total Number of Problems Inserted ",result[1]
        print "Total Number of Problems Updated ",result[2]
        print "Total Number of Problems Deleted ",result[7]
 
        print "Total Number of Verticals Insert Error ",result[3]
        print "Total Number of Problems Insert Error ",result[4]
        print "Total Number of Problems Update Error ",result[5]
        
def print_student_grade_status(result,outlist):
    if (result[0]!= -1):
       print "Total inserted student grades records are",result[0]
       print "Total updated student grades records are",result[1]
    if (outlist[0]!= -1):
       print "Total inserted student marks records are",outlist[0]
       print "Total updated student marks records are",outlist[1]      

@transaction.atomic    
def insert_modlist(disnm,motype,moid,rel_id):
    try:
       mod_obj = course_modlist.objects.get(module_id=moid)
       mod_obj.display_name = disnm
       mod_obj.module_type = motype
       mod_obj.module_id = moid
       mod_obj.related_id = rel_id
       mod_obj.save()
       return mod_obj.id
    except Exception as e:
       #print str(e.message)
       coursemod = course_modlist(display_name=disnm,module_type=motype,module_id=moid,related_id=rel_id)
       coursemod.save()
       return coursemod.id
 
@transaction.atomic
def deleted_module(module):
    try:
          module_detail=collection.find({"_id.name":module.module_id})
          try:
              for module in module_detail:
                 try:
                    if module['metadata']['visible_to_staff_only'] == True:
                          module.delete() 
                          return 1            
                 except:
                          return 0
          except:
            module.delete()
            return 1
          return 0
    except:
      return 0

@transaction.atomic    
def update_deleted_modules():
    modules_deleted =0
    modules_list=course_modlist.objects.exclude(module_type__in=["course","chapter","sequential","vertical"])
    for module in modules_list:
           modules_deleted +=deleted_module(module)
    
    vertical_list=course_modlist.objects.filter(module_type="vertical")
    for vertical in vertical_list:
           modules_deleted +=deleted_module(vertical)
 
    sequential_list=course_modlist.objects.filter(module_type="sequential")
    for sequential in sequential_list:
           modules_deleted +=deleted_module(sequential)
 
    chapter_list=course_modlist.objects.filter(module_type="chapter")
    for chapter in chapter_list:
           modules_deleted +=deleted_module(chapter)

    course_list=course_modlist.objects.filter(module_type="course")  
    for course in course_list:
           modules_deleted +=deleted_module(course)
    print "Number of modules deleted=",modules_deleted

@transaction.atomic   
def course_modules(csr):
    for csr_name in collection.find({"_id.course":csr,"_id.category":"course"} ,{"metadata.display_name":1, "metadata.visible_to_staff_only":1}):
        try:
           if csr_name['metadata']['visible_to_staff_only'] == True:
             continue 
        except:
             pass
        csr_id=insert_modlist((csr_name["metadata"]["display_name"].encode('utf-8')),"course",csr,"0")

        for chp_name in collection.find({"_id.course":csr,"_id.category":"chapter"},{"metadata.display_name":1,"definition.children":1,"metadata.start":1,"_id.name":1, "metadata.visible_to_staff_only":1}).sort([("metadata.start",1)]):
           try:
             if vertical['metadata']['visible_to_staff_only'] == True:
                continue 
           except:
             pass
   
             chp_id=insert_modlist((chp_name["metadata"]["display_name"].encode('utf-8')),"chapter",chp_name["_id"]["name"],csr_id)

             for sequential in  chp_name["definition"]["children"]:

                  stype= sequential.split('/')[4]
                  seq_id = sequential.split('/')[5]


                  if (stype== "sequential"):
                        for seq_name in collection.find({ "_id.course":csr,"_id.name":seq_id}, {"metadata.display_name":1,  "metadata.start":1,  "metadata.due":1, "definition.children":1,"_id.name":1, "metadata.visible_to_staff_only":1}):
                                 try:
                                        if seq_name['metadata']['visible_to_staff_only'] == True:
                                            continue 
                                 except:
                                         pass
  
                                 seq_id=insert_modlist((seq_name["metadata"]["display_name"].encode('utf-8')),stype,seq_id,chp_id)
                                 for vertical in seq_name["definition"]["children"]:
                                       vtype= vertical.split('/')[4]
                                       vert_id = vertical.split('/')[5]

                                       if (vtype== "vertical"):
                                        for vert_name in collection.find({ "_id.course":csr,"_id.name":vert_id},{"metadata.display_name":1,  "metadata.start":1,  "metadata.due":1, "definition.children":1,"_id.name":1, "metadata.visible_to_staff_only":1}):
                                           try:
                                                  if vert_name['metadata']['visible_to_staff_only'] == True:
                                                      continue 
                                           except:
                                                  pass
  
                                           vert_id=insert_modlist((vert_name["metadata"]["display_name"].encode('utf-8')),vtype,vert_id,seq_id)
                                           for module in vert_name["definition"]["children"]:
                                                mtype= module.split('/')[4]
                                                mod_id = module.split('/')[5]
                                                for mod_name in collection.find({ "_id.course":csr,"_id.name":mod_id},{"metadata.display_name":1,  "metadata.start":1,  "metadata.due":1, "_id.name":1, "metadata.visible_to_staff_only":1}):
                                                    try:
                                                        if mod_name['metadata']['visible_to_staff_only'] == True:
                                                                  continue 
                                                    except:
                                                        pass
  
                                                    try:
                                                         mod_id=insert_modlist((mod_name["metadata"]["display_name"].encode('utf-8')),mtype,mod_id,vert_id)
                                                    except:
                                                         None
                                                         #print "                   4",mod_id,mtype



####### start of get_grades_report() #########
@transaction.atomic
def get_grades_report(course_id):
 print course_id
 try:
      courseobj = edxcourses.objects.get(courseid = course_id)
 except Exception as e:
      print "ERROR occured",str(e.message),str(type(e))  
      return [-1,-1]
 count=0
 sections=[];update_gradestable=0;insert_gradestable=0;dropcount_dict={};gradetype_weight={}
 heading=["RollNumber","Username","Email Id","Progress <br>in %"]
 tooltip=[]
 try:  
   grades_obj=gradepolicy.objects.filter(courseid=courseobj).order_by('id')
   for gradetype in grades_obj:
      count=0

      dropcount_dict[gradetype.type]=gradetype.min_count-gradetype.drop_count
      gradetype_weight[gradetype.type]=gradetype.weight
      evaluation_objs=evaluations.objects.filter(course_id=courseobj.id,type=gradetype.type).values('sectionid','grade_weight','total_marks','type','sec_name').distinct().order_by("type","due_date")
      for evaluation_obj in evaluation_objs:
       
        count=count+1
        try:
           header=headings.objects.get(section=evaluation_obj['sectionid'])
        except Exception as e:
           print "Error :Missing Evaluation",str(e.message),str(type(e)),"evaluation",evaluation_obj['sectionid']

        headings_short_label=header.heading.split(',')[3].strip('Total <br>')  
        total_marks=float(headings_short_label.strip('MM:'))
        evaluation_obj['total_marks']=total_marks
        sections.append([evaluation_obj['sectionid'],evaluation_obj['grade_weight'],evaluation_obj['type'],total_marks])
        evaluation_objs=evaluations.objects.filter(course_id=courseobj.id,type=gradetype.type).update(total_marks=total_marks)
        heading.append(str(gradetype.short_label+str(count).zfill(2))+"<br>"+str(headings_short_label))
        tooltip.append(evaluation_obj['sec_name'])
   heading=",".join(map(str,heading))
   tooltip=",".join(map(str,tooltip))
   tt='TT'+str(courseobj.course)
   
   try:
      header_objs=headings.objects.get(section=courseobj.course)
      header_objs.heading=heading
      header_objs.save()
   except:
      header_objs=headings(section=courseobj.course,heading=heading)  
      header_objs.save()
   
   try:
      header_objs=headings.objects.get(section=tt)
      header_objs.heading=tooltip
      header_objs.save()
   except:
      header_objs=headings(section=tt,heading=tooltip)  
      header_objs.save()
   #iitbx_auth_user_objs=iitbx_auth_user.objects.get(edxuserid="589") #for CS101.1xA15 589,3033
   #iitbx_auth_user_objs=iitbx_auth_user.objects.get(edxuserid="77764") # for EE210.1xA15
   #studentdetails_obj=studentDetails.objects.filter(courseid=courseobj.courseid,edxuserid=iitbx_auth_user_objs)
   studentdetails_obj=studentDetails.objects.filter(courseid=courseobj.courseid)
   for studentdetails in studentdetails_obj:
     grade=0;total=[];sublist=[];old_grade_type="";grade=0.0;total_grade=[]
     for section in sections:
        new_grade_type=section[2]
        total_marks=section[3]
        # First Record .No type already exist
        if old_grade_type=="":
           old_grade_type=new_grade_type
        if new_grade_type==old_grade_type :
           markstable_obj=markstable.objects.get(section=str(section[0]),stud=studentdetails.id)  
           if markstable_obj.total =="NA":
              total.append(str(markstable_obj.total))
              sublist.append(0)
           else:
              grade=float(float(markstable_obj.total)/total_marks)*100
              total.append(str(markstable_obj.total))
              sublist.append(grade)
        else:
              drop_count= dropcount_dict[old_grade_type]
              if drop_count <= len(sublist):
                 sublist=sorted(sublist,reverse=True)[:drop_count]
                 sum_var=sum(sublist)
                 avg=(sum_var/drop_count)*gradetype_weight[old_grade_type]
                 total_grade.append(avg)
                 sublist=[]
              else:
                 sublist=sorted(sublist,reverse=True)
                 sum_var=sum(sublist)
                 avg=(sum_var/drop_count)*gradetype_weight[old_grade_type]
                 total_grade.append(avg)
                 sublist=[]
              markstable_obj=markstable.objects.get(section=str(section[0]),stud=studentdetails.id)  
              if markstable_obj.total =="NA":
                 total.append(str(markstable_obj.total))
                 sublist.append(0)
              else:
                 grade=float(float(markstable_obj.total)/total_marks)*100
                 total.append(str(markstable_obj.total))
                 sublist.append(grade)
              old_grade_type=new_grade_type
     
     drop_count=dropcount_dict[old_grade_type]
     if drop_count <= len(sublist):
         sublist=sorted(sublist,reverse=True)[:drop_count]
     else:
         sublist=sorted(sublist,reverse=True)
     sum_var=sum(sublist)
     avg=(sum_var/drop_count)*gradetype_weight[old_grade_type]
     total_grade.append(avg)
     final_grade=sum(total_grade)
     
     #Quizzes

     res=",".join(map(str, total))  
     
     try:
        gradestable_obj=gradestable.objects.get(stud=studentdetails,course=courseobj.course)
        gradestable_obj.stud=studentdetails
        gradestable_obj.course=courseobj.course
        gradestable_obj.grade=final_grade
        gradestable_obj.eval=res
        gradestable_obj.save() 
        update_gradestable+=1 
     except:
        gradestable_obj=gradestable(stud=studentdetails,course=courseobj.course,grade=avg,eval=res)
        gradestable_obj.save()
        insert_gradestable+=1 
   return [insert_gradestable,update_gradestable]
 except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(str(e.message),str(type(e)), courseobj.courseid)
          return [-1,-1]    
     
     

########### end of get_grades_report() #############
     

########### end of get_grades_report() #############

def print_get_gradestable_status(grades_table_status):
   if grades_table_status[0]!=-1:
       print "Total inserted student grades records are",grades_table_status[0]
       print "Total updated student grades records are",grades_table_status[1]

def generate_emails():
      
       FROM = "bmwsupport@iitbombayx.in"
       TO = ["bmwsoftwareteam@cse.iitb.ac.in","workshopmanagers@cse.iitb.ac.in","sheweta@cse.iitb.ac.in"] # must be a list
       #CC = ["bmwsoftwareteam@cse.iitb.ac.in"] # email id as CC
       SUBJECT = "Bmwinfo Sync Script Status"
       runtime = datetime.now()
       TEXT = """The script ran sucessfully on %s. Please note this doesnot mean that IITBombayX data was refreshed.""" %(runtime)
             
       # Prepare actual message

       message = """\
       From: %s
       To: %s
       Subject: %s

       %s
       """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
       #msg = EmailMultiAlternatives(SUBJECT, message, FROM, TO, cc=CC) # if cc is required
       msg = EmailMultiAlternatives(SUBJECT, message, FROM, TO)
       msg.send(fail_silently=False)



@transaction.atomic
def gen_grades(course_id):
####### start of get_grades_report() #########
 curtime = datetime.now()
 try:
      courseobj = edxcourses.objects.get(courseid = course_id)
 except Exception as e:
      print "ERROR occured",str(e.message),str(type(e))  
      return [-1,-1]
 count=0
 sections=[];update_gradestable=0;insert_gradestable=0;dropcount_dict={};gradetype_weight={}
 heading=["UserId","Username","Email Id","Progress <br>in %"]
 sectionl=[]
 try:  
   grades_obj=gradepolicy.objects.filter(courseid=courseobj).exclude(weight=0).order_by('id')
   for gradetype in grades_obj:
      count=0
      
      dropcount_dict[gradetype.type]=gradetype.min_count-gradetype.drop_count
      gradetype_weight[gradetype.type]=gradetype.weight
      evaluation_objs=gen_evaluations.objects.filter(course_id=courseobj.id,type=gradetype.type,release_date__lte=curtime).exclude(total_marks=0).values('sectionid','grade_weight','total_marks','type').distinct().order_by("type","due_date")
      for evaluation_obj in evaluation_objs:
        count=count+1
        sectionl.append(evaluation_obj['sectionid'])
        try:
           header=gen_headings.objects.get(section=evaluation_obj['sectionid'])
        except Exception as e:
           print "Error :Missing Evaluation",str(e.message),str(type(e)),"evaluation",evaluation_obj['sectionid']

        headings_short_label=header.heading.split(',')[3].strip('Total <br>')  
        total_marks=float(headings_short_label.strip('MM:'))
        evaluation_obj['total_marks']=total_marks
        if total_marks == 0.0:
         continue 
        sections.append([evaluation_obj['sectionid'],evaluation_obj['grade_weight'],evaluation_obj['type'],total_marks])
        evaluation_objs=gen_evaluations.objects.filter(course_id=courseobj.id,type=gradetype.type).update(total_marks=total_marks)
        heading.append(str(gradetype.short_label+str(count).zfill(2))+"<br>"+str(headings_short_label))
   heading=",".join(map(str,heading))
   
   try:
      header_objs=gen_headings.objects.get(section=courseobj.courseid)
      header_objs.heading=heading
      header_objs.save()
   except:
      header_objs=gen_headings(section=courseobj.course,heading=heading)  
      header_objs.save()
   
   #iitbx_auth_user_objs=iitbx_auth_user.objects.get(edxuserid="589") #for CS101.1xA15 589,3033
   #iitbx_auth_user_objs=iitbx_auth_user.objects.get(edxuserid="34630") # for EE210.1xA15
   #studentdetails_obj=studentDetails.objects.filter(courseid=courseobj.courseid,edxuserid=iitbx_auth_user_objs)
   #studentdetails_obj=studentDetails.objects.filter(courseid=courseobj.courseid)
   studentdetails_obj=gen_markstable.objects.filter(section__in=sectionl).values("edxuserid").distinct()
   for studentdetails in studentdetails_obj:
     
     grade=0;total=[];sublist=[];old_grade_type="";grade=0.0;total_grade=[]
     for section in sections:
        new_grade_type=section[2]
        total_marks=section[3]
        # First Record .No type already exist
        if old_grade_type=="":
           old_grade_type=new_grade_type
        if new_grade_type==old_grade_type :
           try:
              markstable_obj=gen_markstable.objects.get(section=str(section[0]),edxuserid=studentdetails['edxuserid'])
              temp=markstable_obj.total
           except:
              temp="NA"
           if temp =="NA":
              total.append(str(temp))
              sublist.append(0)
           else:
              grade=float(float(temp)/total_marks)*100
              total.append(str(temp))
              sublist.append(grade)
        else:
              drop_count= dropcount_dict[old_grade_type]
              if drop_count <= len(sublist):
                 sublist=sorted(sublist,reverse=True)[:drop_count]
                 sum_var=sum(sublist)
                 avg=(sum_var/drop_count)*gradetype_weight[old_grade_type]
                 total_grade.append(avg)
                 sublist=[]
              else:
                 sublist=sorted(sublist,reverse=True)
                 sum_var=sum(sublist)
                 avg=(sum_var/drop_count)*gradetype_weight[old_grade_type]
                 total_grade.append(avg)
                 sublist=[]
              try:
                  markstable_obj=gen_markstable.objects.get(section=str(section[0]),edxuserid=studentdetails['edxuserid'])  
                  temp=markstable_obj.total
              except:
                  temp="NA"
              if temp =="NA":
                 total.append(str(temp))
                 sublist.append(0)
              else:
                 grade=float(float(temp)/total_marks)*100
                 total.append(str(temp))
                 sublist.append(grade)
              old_grade_type=new_grade_type
        drop_count=dropcount_dict[old_grade_type]
        if drop_count <= len(sublist):
            sublist=sorted(sublist,reverse=True)[:drop_count]
        else:
            sublist=sorted(sublist,reverse=True)
        sum_var=sum(sublist)
     avg=(sum_var/drop_count)*gradetype_weight[old_grade_type]
     total_grade.append(avg)
     final_grade=sum(total_grade)
     res=",".join(map(str, total))  
     
     try:
        gradestable_obj=gen_gradestable.objects.get(edxuserid=studentdetails['edxuserid'],course=courseobj.course)
        
        gradestable_obj.grade=final_grade
        gradestable_obj.eval=res
        gradestable_obj.save() 
        update_gradestable+=1 
     except:
        gradestable_obj=gen_gradestable(edxuserid=studentdetails['edxuserid'],course=courseobj.course,grade=avg,eval=res)
        gradestable_obj.save()
        insert_gradestable+=1 
   return [insert_gradestable,update_gradestable]
 except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(str(e.message),str(type(e)), courseobj.courseid)
          return [-1,-1]    
  
       

########### end of get_grades_report() #############

##################################################start of iitbxactivity############################################################
@transaction.atomic
def iitbxactivity():
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error  %s,(%s) -Establishing mysql connection"%(e.message,str(type(e)))
      return [-1]
    
    mysql_csr.execute('''SELECT " " id ,months,DATE_FORMAT(maxdate,"%b.%d,%Y") mxdate,lastday, DATE_FORMAT(lastday,"%b-%y") mname,CONCAT(DATE_FORMAT( MAKEDATE(YEAR(lastday), 1) + INTERVAL QUARTER(lastday) QUARTER  - INTERVAL    1 QUARTER,"%b")  ," to ",
  DATE_FORMAT(MAKEDATE(YEAR(lastday), 1) + INTERVAL QUARTER(lastday) QUARTER - INTERVAL 1 DAY ,"%b-%y")) "quartername",DATE_ADD(DATE_FORMAT(lastday,"%Y-%m-%d"),interval -7 day ) week, week(lastday) weekno, month(lastday) monthno, quarter(lastday)  quarterno,
 MAKEDATE(YEAR(lastday), 1) + INTERVAL QUARTER(lastday) QUARTER  
                                       - INTERVAL    1 QUARTER  firstday
   from
(SELECT  PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM max(modified) ),
EXTRACT(YEAR_MONTH FROM date_format('2015-01-26', "%Y%m%d"))) AS months, date(max(modified)) "maxdate" ,DATE(date_add(max(modified),INTERVAL -1 day)) "lastday"
from courseware_studentmodule ) d
''')
    dta=mysql_csr.fetchall()
    for i in dta:
         heading=str(i[1])+","+str(i[2])
         lday=i[3]
         fday=i[10]
         week=i[6]
         weekno=i[7]
         month=i[8]
         quarter=i[9]
         monthnm=i[4]
         quarternm=i[5]
    try:
             report_obj=gen_repout.objects.get(B="Last days")
             report_obj.reportid=1
             report_obj.num_cols=5
             report_obj.A=heading
             report_obj.C="Last 7 days"
             report_obj.D=monthnm
             report_obj.E=quarternm
             report_obj.save()
    except:
             report_obj=gen_repout(reportid=1,num_cols=5,A=heading,B="Last days",C="Last 7 days",D=monthnm,E=quarternm)
             report_obj.save()   
            
    mysql_csr.execute('''SELECT " " id,sum(lusers) "clusers",sum(wusers) "cwusers",sum(musers) "cmusers",sum(qusers) "cqusers",
       sum(lausers) "clausers",sum(wausers) "cwausers",sum(mausers) "cmausers",sum(qausers) "cqausers",
         sum(llusers) "cllusers",sum(wlusers) "cwlusers",sum(mlusers) "cmlusers",sum(qusers) "cqlusers"
FROM(
SELECT if(date(date_joined)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),1,0) "lusers"
       ,if(week(date_joined)=%s,1,0) "wusers"
       ,if(month(date_joined)=%s,1,0) "musers"
       ,if(quarter(date_joined)=%s,1,0) "qusers"
       ,if(date(date_joined)=DATE_FORMAT(%s,"%%Y-%%m-%%d") and is_active=1,1,0) "lausers"
       ,if(week(date_joined)=%s and is_active=1,1,0) "wausers"
       ,if(month(date_joined)=%s and is_active=1,1,0) "mausers"
       ,if(quarter(date_joined)=%s and is_active=1,1,0) "qausers"
       , if(last_login=DATE_FORMAT(%s,"%%Y-%%m-%%d"),1,0) "llusers"
       ,if(week(last_login)=%s,1,0) "wlusers"
       ,if(month(last_login)=%s,1,0) "mlusers"
       ,if(quarter(last_login)=%s,1,0) "qlusers"
  FROM auth_user where date_joined >= DATE_FORMAT(%s,"%%Y-%%m-%%d") ) A 
 ''',(lday,weekno,month,quarter,lday,weekno,month,quarter,lday,weekno,month,quarter,fday))
    user=mysql_csr.fetchall()
    for j in user:
        try:
            report_obj=gen_repout.objects.get(A="New Users")
            report_obj.reportid=1
            report_obj.num_cols=5
            report_obj.B=j[1]
            report_obj.C=j[2]
            report_obj.D=j[3]
            report_obj.E=j[4]
            report_obj.save()
        except:
            totaluser_obj=gen_repout(reportid=1,num_cols=5,A="New Users",B=j[1],C=j[2],D=j[3],E=j[4]) 
            totaluser_obj.save()
        try:
            report_obj=gen_repout.objects.get(A="New Activated Users")
            report_obj.reportid=1
            report_obj.num_cols=5
            report_obj.B=j[5]
            report_obj.C=j[6]
            report_obj.D=j[7]
            report_obj.E=j[8]
            report_obj.save()
        except:
            totalusers_obj=gen_repout(reportid=1,num_cols=5,A="New Activated Users",B=j[5],C=j[6],D=j[7],E=j[8])
            totalusers_obj.save()
        try:
            report_obj=gen_repout.objects.get(A="Logged-in Users")
            report_obj.reportid=1
            report_obj.num_cols=5
            report_obj.B=j[9]
            report_obj.C=j[10]
            report_obj.D=j[11]
            report_obj.E=j[12]
            report_obj.save()
        except:
           totaluse_obj=gen_repout(reportid=1,num_cols=5,A="Logged-in Users",B=j[9],C=j[10],D=j[11],E=j[12])  
           totaluse_obj.save()

    mysql_csr.execute('''SELECT " " id, sum(estu) "cestu",sum(westu) "cwestu",sum(mestu) "cmestu",sum(qestu) "cqestu" , count(distinct enrolcou) -1 "cenrolcou",count(distinct wenrolcou)-1 "cwenrolcou",count(distinct menrolcou)-1 "cmenrolcou",count(distinct qenrolcou)-1 "cqenrolcou"
FROM(
SELECT course_id, if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),1,0) "estu"
       ,if(week(created)=%s,1,0) "westu"
       ,if(month(created)=%s,1,0) "mestu"
       ,if(quarter(created)=%s,1,0) "qestu"
       ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),course_id,"") "enrolcou"
       ,if(week(created)=%s,course_id,"") "wenrolcou"
       ,if(month(created)=%s,course_id,"") "menrolcou"
       ,if(quarter(created)=%s,course_id,"") "qenrolcou"
from  student_courseenrollment where created >= DATE_FORMAT(%s,"%%Y-%%m-%%d") ) S ''',(lday,weekno,month,quarter,lday,weekno,month,quarter,fday))
    estud=mysql_csr.fetchall()
    for k in estud:
            try:
               report_obj=gen_repout.objects.get(A="Enrolled Users")
               report_obj.reportid=1
               report_obj.num_cols=5
               report_obj.B=k[1]
               report_obj.C=k[2]
               report_obj.D=k[3]
               report_obj.E=k[4]
               report_obj.save()
            except:
               totaluser_obj=gen_repout(reportid=1,num_cols=5,A="Enrolled Users",B=k[1],C=k[2],D=k[3],E=k[4]) 
               totaluser_obj.save()
            try:
               report_obj=gen_repout.objects.get(A="Courses where users enrolled")
               report_obj.reportid=1
               report_obj.num_cols=5
               report_obj.B=k[5]
               report_obj.C=k[6]
               report_obj.D=k[7]
               report_obj.E=k[8]
               report_obj.save()
            except:
               totaluser_obj=gen_repout(reportid=1,num_cols=5,A="Courses where users enrolled",B=k[5],C=k[6],D=k[7],E=k[8]) 
               totaluser_obj.save()

    mysql_csr.execute('''select " " id, count(distinct lactstud) -1 "clactstud", count(distinct wactstud)-1 "cwactstud", count(distinct mactstud)-1 "cmactstud", count(distinct qactstud)-1 "cqactstud",count(distinct lactcour)-1 "clactcour", count(distinct wactcour)-1 "cwactcour", count(distinct mactcour)-1 "cmactcour", count( distinct qactcour)-1 "cqactcour", count(distinct lvideo)-1 "clvideo",count(distinct wvideo)-1 "cwvideo", count(distinct mvideo)-1 "cmvideo", count(distinct qvideo)-1 "cqvideo", count(distinct lstudprob)-1 "clstudprob", count(distinct wstudprob)-1 "cwstudprob", count(distinct mstudprob)-1 "cmstudprob", count(distinct qstudprob)-1 "cqstudprob", count(distinct lstudgrade)-1 "clstudgrade",count(distinct wstudgrade)-1 "cwstudgrade", count(distinct mstudgrade)-1 "cmstudgrade", count(distinct qstudgrade)-1 "cqstudgrade"
from(
select student_id, course_id,
          if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),student_id,0)  "lactstud"
          ,if(week(created)=%s,student_id,0)  "wactstud"
          ,if(month(created)=%s,student_id,0) "mactstud"
          ,if(quarter(created)=%s,student_id,0) "qactstud"
          ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),course_id,"") "lactcour"
          ,if(week(created)=%s,course_id,"")  "wactcour"
          ,if(month(created)=%s,course_id,"") "mactcour"
          ,if(quarter(created)=%s,course_id,"") "qactcour"
          ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d") and module_type="video",student_id,0)  "lvideo"
          ,if(week(created)=%s and module_type="video",student_id,0)  "wvideo"
          ,if(month(created)=%s and module_type="video",student_id,0) "mvideo"
          ,if(quarter(created)=%s and module_type="video",student_id,0) "qvideo"
          ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d") and module_type="problem",student_id,0) "lstudprob"
          ,if(week(created)=%s and module_type="problem",student_id,0) "wstudprob"
          ,if(month(created)=%s and module_type="problem",student_id,0) "mstudprob"
          ,if(quarter(created)=%s and module_type="problem",student_id,0) "qstudprob"
          ,if(created=DATE_FORMAT(%s,"%%Y-%%m-%%d") and module_type="problem" and grade is not null,student_id,0) "lstudgrade"
          ,if(week(created)=%s and module_type="problem" and grade is not null,student_id,0) "wstudgrade"
          ,if(month(created)=%s and module_type="problem" and grade is not null,student_id,0) "mstudgrade"
          ,if(quarter(created)=%s and module_type="problem" and grade is not null,student_id,0) "qstudgrade"
          from  courseware_studentmodule where created >= DATE_FORMAT(%s,"%%Y-%%m-%%d")) C
''',(lday,weekno,month,quarter,lday,weekno,month,quarter,lday,weekno,month,quarter,lday,weekno,month,quarter,lday,weekno,month,quarter,fday))
    courseact=mysql_csr.fetchall()
    for l in courseact:
           try:
               report_obj=gen_repout.objects.get(A="Active Students")
               report_obj.reportid=1
               report_obj.num_cols=5
               report_obj.B=l[1]
               report_obj.C=l[2]
               report_obj.D=l[3]
               report_obj.E=l[4]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=5,A="Active Students",B=l[1],C=l[2],D=l[3],E=l[4]) 
               totaluser_obj.save()

           try:
               report_obj=gen_repout.objects.get(A="Active Courses")
               report_obj.reportid=1
               report_obj.num_cols=5
               report_obj.B=l[5]
               report_obj.C=l[6]
               report_obj.D=l[7]
               report_obj.E=l[8]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=5,A="Active Courses",B=l[5],C=l[6],D=l[7],E=l[8]) 
               totaluser_obj.save()

           try:
               report_obj=gen_repout.objects.get(A="Students who watched videos")
               report_obj.reportid=1
               report_obj.num_cols=5
               report_obj.B=l[9]
               report_obj.C=l[10]
               report_obj.D=l[11]
               report_obj.E=l[12]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=5,A="Students who watched videos",B=l[9],C=l[10],D=l[11],E=l[12]) 
               totaluser_obj.save()
  
           try:
               report_obj=gen_repout.objects.get(A="Students who attempted practice problems")
               report_obj.reportid=1
               report_obj.num_cols=5
               report_obj.B=l[13]
               report_obj.C=l[14]
               report_obj.D=l[15]
               report_obj.E=l[16]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=5,A="Students who attempted practice problems",B=l[13],C=l[14],D=l[15],E=l[16]) 
               totaluser_obj.save()
  
           try:
               report_obj=gen_repout.objects.get(A="Students who attempted graded problems")
               report_obj.reportid=1
               report_obj.num_cols=5
               report_obj.B=l[17]
               report_obj.C=l[18]
               report_obj.D=l[19]
               report_obj.E=l[20]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=5,A="Students who attempted graded problems",B=l[17],C=l[18],D=l[19],E=l[20]) 
               totaluser_obj.save()

    return 1  
###############################################end of iitbxactivity#################################################################


def main(argv):
        init()
        collection=mongo_openconnection()
        curtime = datetime.now()
        course_id=""
        
        for course in collection.distinct("_id.course"):
         print course
         course_id=get_course_detail(course)
         if (course_id != "-1") :
           try:
             course_obj=edxcourses.objects.get(course=course)
             try:
                ahead_date=course_obj.courseend + timedelta(days=num_days)
             except:
                ahead_date="9999-12-31 24:00:00"
             try:
                coursestart=str(course_obj.coursestart)
             except:
                coursestart="1111-01-01 24:00:00"
             try:
                enrollend=str(course_obj.enrollend)
             except:
                enrollend="9999-12-31 24:00:00" 
             
             if (coursestart < str(curtime)) and (str(curtime) < str(ahead_date)):
                if course_obj.blended_mode==1:
                    if str(curtime) < enrollend :
                        status=get_student_course_enrollment(course_id)
                    else:
                      print "Enrollment is closed"
                    result=fetch_evaluations(course_id) 
                    
                    grade=get_student_grades(course_id)
                    outlist=evaldata(course_id)
                    grades_table_status=get_grades_report(course_id)
                    module=course_modules(course)
                    print_report(course_id,result)
                    print_student_grade_status(grade,outlist)
                    print_get_gradestable_status(grades_table_status)
                    
                else:
                    blended_result= fetch_gen_evaluations(course_id)
                    gen_evaldata(course_id)
                    gen_grades(course_id)
             else:
                    print "Course has been closed"
           except:
                print "issue with course_obj",course_id
             #break
        #update_deleted_modules()
        iitbxactivity()
        generate_emails()
                                                   

'''
def main(argv):
         init()
         collection=mongo_openconnection()
         curtime = datetime.now()
         course_id=""
         #for course in collection.distinct("_id.course"):
         course_id=get_course_detail("ME209xA15")
         #print course_id
         result=fetch_evaluations(course_id)             
         grade=get_student_grades(course_id)
         outlist=evaldata("IITBombayX/ME209xA15/2015_T1")
         grade=get_grades_report("IITBombayX/ME209xA15/2015_T1")
'''
if __name__ == "__main__":
    main(sys.argv[1:])








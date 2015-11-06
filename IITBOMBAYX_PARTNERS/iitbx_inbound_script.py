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

def delete_grade_information(cid):
       gradepolicy.objects.filter(courseid=cid).delete()
       gradescriteria.objects.filter(courseid=cid).delete()

#@transaction.atomic

def get_course_detail(csr):
     collection=mongo_openconnection()
     course_id=""
     for course_det in collection.find({"_id.course":csr,"_id.category":"course"},{"metadata.start":1,"metadata.end":1,"metadata.enrollment_start":1,"metadata.enrollment_end":1,"metadata.course_image":1,"metadata.display_name":1,"definition.data.grading_policy":1}):
                
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
                
                try:  # if course is there update it
                      course_obj=edxcourses.objects.get(course=course)
                      courseid=course_obj.id
                      course_obj=edxcourses.objects.get(course=csr)
                      course_obj.tag=course_tag
                      course_obj.org=course_org
                      course_obj.course=course
                      course_obj.name=course_name
                      course_obj.courseid=course_id
                      course_obj.coursename=course_disp_name
                      course_obj.enrollstart=course_enroll_start      
                      course_obj.enrollend=course_enroll_end
                      course_obj.coursestart=course_start
                      course_obj.courseend=course_end
                      course_obj.image=image_url
                      try:
                         course_obj.save()
                         
                         delete_grade_information(course_id)
                         if (get_grade_policy_criteria(course_obj) == -1) :
                            return -1
                      except Exception as e:
                          print "Error %s,(%s) - Update on %s. Contact Software team."%(e.message,type(e),course_id)
                          return "-1"
                except Exception as e: # else insert the courses 
                    course_obj=edxcourses(tag=course_tag, org=course_org, course=course, name=course_name, courseid=course_id, coursename=course_disp_name, enrollstart=course_enroll_start, enrollend=course_enroll_end, coursestart=course_start, courseend=course_end,image=image_url)
                    course_obj.save()
                    if( get_grade_policy_criteria(course_obj) == -1):
                          return "-1"
                try:       
                     if (insert_admin_courseleveluser(course_id) == -1):
                          return "-1"     
                except Exception as e:
                       print "Error %s,(%s) insert of course level users on %s. Contact Software team."%(e.message,type(e),course_id)
                       return "-1"
     return course_id

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
            grade_policy_obj=gradepolicy(courseid=course_obj, min_count=min_count, weight=weight ,type=type, drop_count=drop_count, short_label=short_label)
            grade_policy_obj.save()

            cutoffs=course_det["definition"]["data"]["grading_policy"]["GRADE_CUTOFFS"]
            for key,value in cutoffs.iteritems():
                grade_criteria_obj=gradescriteria(courseid=course_obj,grade=key,cutoffs=value)
                grade_criteria_obj.save()

     return 0
  except Exception as e:
     print "Error %s,(%s) - Fetching grade criteria and Policy from mongodb for course "%(e.message,type(e),course_obj.courseid)
     return -1

def insert_admin_courseleveluser(courseid):
    
    try:
      try:
         course_obj=edxcourses.objects.get(courseid=courseid)
      except Exception as e:
         print "Error %s,(%s) - Fetching course object for " %(e.message,type(e),courseid)
         return -1
      try:
         instituteid=T10KT_Institute.objects.get(instituteid=0)
      except Exception as e:
         print "Error %s,(%s) -Fetching Institute object for " %(e.message,type(e),courseid)
         return -1
      
      if Courselevelusers.objects.filter(personid_id=1,instituteid=instituteid,courseid_id=course_obj.id,roleid=5).exists():
         pass # No modification required for courselevelusers
      else:   #insert default teacher with personid=1 and instituteid=0 in courselevelusers table
        person_obj=Personinformation.objects.get(id=1)
        course_level_obj=Courselevelusers(personid=person_obj,instituteid=instituteid,courseid=course_obj,roleid=5,startdate="2005-01-01",enddate="4712-12-31")
        course_level_obj.save()
        return 0
    except Exception as e:
     print "Error  %s,(%s) - Insert of courseleveluser for " %(e.message,type(e),courseid)
     return -1
      



#@transaction.atomic
def get_student_course_enrollment(course):
    try:
        edx_course_obj=edxcourses.objects.get(courseid=course)

    except Exception as e:
         print "Error  %s,(%s) - EdxCourse object for course %s doesnot exists"%(e.message,type(e),course)
         return   [-1]
    try:
        person_info_obj=Personinformation.objects.get(id=1)
    except Exception as e:
         print "Error  %s,(%s) -Personinformation object for default user doesnot exist while finding enrollments for %s"%(e.message,type(e),course)
         return  [-1] 
    try:   
           course_level_obj=Courselevelusers.objects.get(courseid=edx_course_obj,personid=person_info_obj)
    except Exception as e:
          print "Error  %s,(%s) -Courselevel default user is not present for %s "%(e.message,type(e),course)
          return [-1]   
   
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error  %s,(%s) -Establishing mysql connection"%(e.message,type(e))
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
             print" Error  %s,(%s) -Inserting new user %s" %(e.message,type(e),record) 
             erroruser=erroruser+1
             continue
       try:  
         stud_det=studentDetails(edxuserid=auth_usr_obj, courseid=course,edxcreatedon=record[3],edxis_active=record[4], edxmode=record[5],teacherid=course_level_obj,roll_no=0,last_update_on=runtime,last_updated_by=person_info_obj)
         stud_det.save()
         insertstudent=insertstudent+1
       except Exception as e: 
         print "Error  %s,(%s) -Inserting studentdetails %s "%(e.message,type(e), record[0])
         errorstudent=errorstudent+1
         continue
      
    #query to fetch users who have changed their enrollment option
    mysql_csr.execute("select b.user_id,a.username,a.email ,b.created,b.is_active,b.mode from auth_user a,student_courseenrollment b where  b.course_id=%s and b.user_id=a.id and exists (select * from iitbxblended.SIP_studentdetails  s where s.courseid=b.course_id and b.user_id=s.edxuserid_id and b.is_active != s.edxis_active)",(course,))
    updated_student_enroll=mysql_csr.fetchall()     
    for record in updated_student_enroll :
       try:
          edxuser=iitbx_auth_user.objects.get(edxuserid=record[0])  
       except Exception as e:
          print" Error  %s,(%s) -Get existing user %s"%(e.message,type(e), record) 
          erroruser=erroruser+1
          continue
       try: 
          update_stud_det=studentDetails.objects.get(edxuserid=edxuser,courseid=edx_course_obj.courseid)
          update_stud_det.edxis_active=record[4]
          update_stud_det.save()
          updatestudent=updatestudent+1 
       except Exception as e:
          print"Error  %s,(%s) -Updating studentdetails %s"%(e.message,type(e), record)
          errorupdate=errorupdate+1
          continue 
    return [insertuser,insertstudent,updatestudent,erroruser,errorstudent,errorupdate]  

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
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(e.message,type(e), course_id)
          return [-1]
     try:    
          grades_obj=gradepolicy.objects.filter(courseid_id=course_id)
     except Exception as e:
          print "Error - %s,(%s) ,Grading Policy for %s doesnot exists"%(e.message,type(e), course_id)
          return [-1]
     for grade_type in grades_obj:
         grade_weight=grade_type.weight/(grade_type.min_count -grade_type.drop_count)     
         for sequential in collection.find({"_id.category":"sequential", "_id.course":course, "metadata.graded":True, "metadata.format":grade_type.type}, {"metadata.display_name":1, "metadata.format":1,  "metadata.start":1,  "metadata.due":1, "definition.children":1,"_id.name":1}):
                        sequential_id=sequential["_id"]["name"]    #sectionid
                        seq_name=sequential["metadata"]["display_name"].encode('utf-8')    #sec_name
                        try:
                          
                          release_date=datetime(*map(int, re.split('[^\d]', sequential["metadata"]["start"])[:-1]))
                          
                        except Exception as e :
                          
                          release_date=runtime
                        try:
                          
                          due_date=datetime(*map(int, re.split('[^\d]', sequential["metadata"]["due"])[:-1]))
                          
                        except:
                          due_date=runtime
                        
                           
                        for verticals in  sequential["definition"]["children"]:
                            if "vertical" in verticals:
                                 total_weight =0
                                 vertical_id = verticals.split('/')[5]
                                 vertical_det=collection.find({"_id.category":"vertical","_id.name":vertical_id,"_id.course":course },{"metadata.display_name":1,"definition.children":1}).limit(1)
                                 for vdetails in vertical_det:
                                    vertical_name= vdetails["metadata"]["display_name"] 
                                    try:
      
                                         evaluations_obj=evaluations.objects.get(subsec_id=vertical_id)
                                          
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
                                           print "Error - %s,(%s)- Vertical Entry failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,type(e),course_id,grade_type,vertical_id,vertical_name,seq_name)
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
                                      print "Error - %s,(%s)- Vertical Entry weight update failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,type(e),course_id,grade_type,vertical_id,vertical_name,seq_name)

     del_list=update_deleted_evaluations(edx_course_obj)
     return [inserted_vertical_count,inserted_problem_count,updated_problem_count,error_vertical_count,error_problem_count,    error_updated_count,del_list[1],del_list[0]] 
   
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
                            try:
                                weight=problemdet["metadata"]["weight"]
                                
                            except Exception as e:
                                
                                definition_data=problemdet['definition']['data']['data'].encode('utf-8')
 
                                global question_types
                                for type in question_types:
                                    weight+=definition_data.count(type)
                                
                            try:

                                problem_obj=questions.objects.get( qid=p_id)

                                try: 
                                  problem_obj.q_weight=weight
                                  problem_obj.q_name=problem_name
                                  problem_obj.save()
                       
                                  updated_problem_count=updated_problem_count+1
                                except Exception as e:
                                  print "Error - %s,(%s) while updating  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, type(e),problem_id,problem_name,vertical_id,vertical_name,gtype,course_id)
                                  error_updated_count=error_updated_count+1                          
                            except Exception as e:
                                 try:
                                      questions_obj=questions(course=edx_course_obj, eval=evaluations, qid=p_id, q_name=problem_name, q_weight=weight)
                                      questions_obj.save()
                                      inserted_problem_count=inserted_problem_count+1
                                 except Exception as e:                  
                                     print "Error- %s,(%s) while insert  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, type(e),problem_id,problem_name,vertical_id,vertical_name,gtype,course_id)
                                     error_problem_count=error_problem_count+1
 
     return [inserted_problem_count,updated_problem_count,error_problem_count,error_updated_count,weight]

def get_student_grades(course_id):
    insert_count=0
    update_count=0
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error-%s,(%s) -Establishing mysql connection for %s" %(e.message,type(e),course_id)
      return [-1] 
    try:
      mysql_csr.execute("insert into iitbxblended.SIP_result(question_id,edxuserid,grade,maxgrade) SELECT a.id,b.student_id,b.grade,b.max_grade FROM `courseware_studentmodule`b,iitbxblended.SIP_questions a where b.module_id =a.qid  and b.course_id='%s'and b.grade is not null and not exists (select * from iitbxblended.SIP_result r where r.question_id = a.id and r.edxuserid=b.student_id)" %(course_id))
      insert_count=mysql_csr.rowcount
      cnx.commit()
    except Exception as e:
       print "Error-%s,(%s) -Insert Grades for %s" %(e.message,type(e),course_id)
       return [-1]
    try:
       mysql_csr.execute('''UPDATE iitbxblended.SIP_result r,
`courseware_studentmodule` b,
iitbxblended.SIP_questions a SET r.grade = b.grade,
r.maxgrade = b.max_grade WHERE b.module_id = a.qid AND b.course_id='%s' AND b.grade IS NOT NULL AND r.question_id = a.id AND r.edxuserid = b.student_id AND r.grade != b.grade ''' %(course_id))
       update_count=mysql_csr.rowcount
       cnx.commit()
    except Exception as e:
       print "Error-%s,(%s) -Update Grades for %s" %(e.message,type(e),course_id)
       return [-1]
    
    return [insert_count,update_count]


def evaldata(course_id):
     print course_id,"course_id"
     runtime = datetime.now()
     inserteval=0
     updateeval=0
     course=course_id.split('/')[1]
     try:   
          courseobj=edxcourses.objects.filter(courseid=course_id)
     except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(e.message,type(e), course_id)
          return [-1]
            
     evals=evaluations.objects.filter(course=courseobj,release_date__lte=runtime).values('sectionid').distinct()
     
     for eval in evals:
         ques_dict={}
         secid=str(eval['sectionid'])
         
         evaluation_obj=questions.objects.filter(course=courseobj,eval__sectionid=secid ).exclude(q_weight=0 ).order_by('eval_id','id')
         heading = ["Rollno","Username","Email"]
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
                     quizmark=round((res.grade/res.maxgrade)*res.question.q_weight,2)
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
     
def insert_modlist(disnm,motype,moid,rel_id):
    try:
       print moid
       mod_obj = course_modlist.objects.get(module_id=moid)
       mod_obj.display_name = disnm
       mod_obj.module_type = motype
       mod_obj.module_id = moid
       mod_obj.related_id = rel_id
       mod_obj.save()
       return mod_obj.id
    except Exception as e:
       print str(e.message)
       coursemod = course_modlist(display_name=disnm,module_type=motype,module_id=moid,related_id=rel_id)
       coursemod.save()
       return coursemod.id
 

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

def get_grades_report(course_id):
 try:
      courseobj = edxcourses.objects.get(courseid = course_id)
 except Exception as e:
      print "ERROR occured",str(e.message),str(type(e))  
      return [-1,-1]
 count=0
 sections=[];update_gradestable=0;insert_gradestable=0
 heading=["RollNumber","Username","Email","Grade <br>100%"]
 try:  
   grades_obj=gradepolicy.objects.filter(courseid=courseobj).order_by('id')
   for gradetype in grades_obj:
      count=0
      evaluation_objs=evaluations.objects.filter(course_id=courseobj.id,type=gradetype.type).values('sectionid','grade_weight','total_marks').distinct().order_by("type","due_date")
      for evaluation_obj in evaluation_objs:
        sections.append([evaluation_obj['sectionid'],evaluation_obj['grade_weight']])
        count=count+1
        try:
           header=headings.objects.get(section=evaluation_obj['sectionid'])
        except Exception as e:
           print "Error :Missing Evaluation",str(e.message),str(type(e)),"evaluation",evaluation_obj['sectionid']

        headings_short_label=header.heading.split(',')[3].strip('Total <br>')  
        total_mark=float(headings_short_label.strip('MM:'))
        evaluation_obj['total_marks']=total_mark
        evaluation_objs=evaluations.objects.filter(course_id=courseobj.id,type=gradetype.type).update(total_marks=total_mark)
        heading.append(str(gradetype.short_label+str(count).zfill(2))+"<br>"+str(headings_short_label))
   heading=",".join(map(str,heading))
   try:
      header_objs=headings.objects.get(section=courseobj.course)
      header_objs.heading=heading
      header_objs.save()
   except:
      header_objs=headings(section=courseobj.course,heading=heading)  
      header_objs.save()
   studentdetails_obj=studentDetails.objects.filter(courseid=courseobj.courseid)
   for studentdetails in studentdetails_obj:
     grade=0;total=[]
     for section in sections:
        markstable_obj=markstable.objects.get(section=str(section[0]),stud=studentdetails.id)  
        if markstable_obj.total =="NA":
           total.append(str(markstable_obj.total))
           grade=grade+0.0
        else:
            grade=grade+float(float(markstable_obj.total)/total_mark * float(section[1]))
            total.append(float(markstable_obj.total))
     rounded_grade=round((grade*100),2)
     res=",".join(map(str, total))
     try:
        gradestable_obj=gradestable.objects.get(stud=studentdetails,course=courseobj.course)
        gradestable_obj.stud=studentdetails
        gradestable_obj.course=courseobj.course
        gradestable_obj.grade=rounded_grade
        gradestable_obj.eval=res
        gradestable_obj.save() 
        update_gradestable+=1    
     except:
        gradestable_obj=gradestable(stud=studentdetails,course=courseobj.course,grade=rounded_grade,eval=res)
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
       TO = ["bmwsoftwareteam@cse.iitb.ac.in","workshopmanagers@cse.iitb.ac.in"] # must be a list
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



def main(argv):
        init()
        curtime = datetime.now()
        course_id=""
        
        for course in courses:
         try:
           course_obj=edxcourses.objects.get(course=course)
         except Exception as e:
           print "Error occured",str(e.message),str(type(e))
         try:
           ahead_date=course_obj.courseend + timedelta(days=7)
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
         if coursestart < str(curtime):
            if str(curtime) < str(ahead_date):
                  course_id=get_course_detail(course)
                  if (course_id != "-1") :
                    if str(curtime) < enrollend :
                      status=get_student_course_enrollment(course_id)
                    else:
                      print "Enrollment is closed"
                    
                    result=fetch_evaluations(course_id) 
                    grade=get_student_grades(course_id)
                    outlist=evaldata(course_id)
                    grades_table_status=get_grades_report(course_id)
                    module=course_modules(course)
                    try:
                       print_report(status,course_id,result)
                    except Exception as e:
                      print "Enrollment has closed ",str(e.message),str(type(e))
                      
                    print_student_grade_status(grade,outlist)
                    print_get_gradestable_status(grades_table_status)
                    
            else:
                    print "Course has been closed"
        update_deleted_modules()
        generate_emails()

                 

if __name__ == "__main__":
    main(sys.argv[1:])








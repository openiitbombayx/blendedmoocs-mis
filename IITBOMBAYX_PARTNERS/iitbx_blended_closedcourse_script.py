#!/usr/bin/env python
from iitbx_settings import *
import csv
import glob
global question_types
question_types=["<choiceresponse>","<optionresponse>","<multiplechoiceresponse>","<numericalresponse ","<stringresponse ","<drag_and_drop_input","<imageresponse","<formularesponse","<customresponse","<jsmeresponse>","<schematicresponse>"]
def mongo_openconnection():
     global client
     client = MongoClient(mongodb)
     global db 
     db= client.edxapp
     global collection
     collection = db.modulestore
     return collection

def dbedxapp_openconnection():
     cnxedxapp = MySQLdb.connect(user=user,passwd=passwd,host=mysql_host,db=mysql_schema)
     return cnxedxapp

def init():

       global prefix_url
       prefix_url="https://iitbombayx.in/c4x/IITBombayX/"
       global infix_url 
       infix_url="/asset/"

def delete_grade_information(cid):
       gradepolicy.objects.filter(courseid=cid).delete()
       gradescriteria.objects.filter(courseid=cid).delete()

def get_course_detail(csr):
     collection=mongo_openconnection()
     curtime = datetime.now()
     course_id=""
 
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
                      course_obj.blended_mode=0
                        
                      try:
                        course_obj.save()
                      except Exception as e:
                         print "Error %s,(%s) - Insert on %s. Contact Software team."%(e.message,str(type(e)),course_id) 
                      try:
                         delete_grade_information(course_id)
                         if (get_grade_policy_criteria(course_obj) == -1) :
                            return -1
                      except Exception as e:
                          print "Error %s,(%s) - Update on %s. Contact Software team."%(e.message,str(type(e)),course_id)
                          return "-1"
           except Exception as e: # else insert the courses 
                    course_obj=edxcourses(tag=course_tag, org=course_org, course=course, name=course_name, courseid=course_id, coursename=course_disp_name, enrollstart=course_enroll_start, enrollend=course_enroll_end, coursestart=course_start, courseend=course_end,image=image_url,blended_mode=0)
                    
                    course_obj.save()
                    if( get_grade_policy_criteria(course_obj) == -1):
                          return "-1"

     return course_obj


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
     print "Error %s - Fetching grade criteria and Policy from mongodb for course %s "%(str(e.message),course_obj.courseid)
     return -1


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
                                         evaluations_obj=gen_evaluations.objects.get(subsec_id=vertical_id)
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
                                           print "InsertError - %s- Vertical Entry failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,course_id,grade_type.type,vertical_id,(vertical_name
).decode('utf-8'),(seq_name).decode('utf-8'))
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
                                      
                                    except Exception as e:
                                      print "Error - %s,(%s)- Vertical Entry weight update failed for course %s,type=%s,  verticalid= %s, displayname= %s, for %s"%(e.message,str(type(e)),course_id,grade_type,vertical_id,(vertical_name).decode('utf-8'),(seq_name).decode('utf-8'))

     del_list=update_deleted_gen_evaluations(edx_course_obj)
     return [inserted_vertical_count,inserted_problem_count,updated_problem_count,error_vertical_count,error_problem_count,    error_updated_count,del_list[1],del_list[0]] 



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
                                  print "Error - %s,(%s) while updating  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, str(type(e)),problem_id,(problem_name).decode('utf-8'),vertical_id,(vertical_name).decode('utf-8'),gtype,course_id)
                                  error_updated_count=error_updated_count+1  
                            except Exception as e:
                                 try:
                                      questions_obj=gen_questions(course=edx_course_obj, eval=evaluations, qid=p_id, q_name=problem_name, q_weight=weight,prob_count=count)
                                      questions_obj.save()
                                      inserted_problem_count=inserted_problem_count+1
                                     
                                 except Exception as e:                  
                                     print "Error- %s,(%s) while insert  problem (%s, %s) of vertical (%s ,%s) of  type %s of course %s"%(e.message, str(type(e)),problem_id,(problem_name).decode('utf-8'),vertical_id,(vertical_name).decode('utf-8'),gtype,course_id)
                                     error_problem_count=error_problem_count+1
                                      
 
     return [inserted_problem_count,updated_problem_count,error_problem_count,error_updated_count,weight]




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
     print course_id
     course=course_id.split('/')[1]
     try:   
          courseobj=edxcourses.objects.get(courseid=course_id)
     except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(e.message,str(type(e)), course_id)
          return [-1]
     
     evals=gen_evaluations.objects.filter(course=courseobj.id,release_date__lte=runtime).values('sectionid','sec_name').distinct()
     sqlmod=""
     for eval in evals:
       ques_dict={}
       #print eval
       secid=str(eval['sectionid'])
       sec_name=str(eval['sec_name'])
       sqlmod=""
       name='static/closed_courses/'+courseobj.course+'/eval_details/'+"ed_"+courseobj.course+"_"+sec_name+'.csv'
       with open(name,'w') as csvfile:
         wr = csv.writer(csvfile,delimiter=',')
         wr.writerow(["edxuserid","section","eval","total"])
         evaluation_obj=gen_questions.objects.filter(course=courseobj.id,eval__sectionid=secid ).exclude(q_weight=0 ).order_by('eval_id','id')
         
         heading = ["UserId","Username","Email"]
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
                  wr.writerow([oldstud,secid,res,t])
                  try:
                   
                     marks_obj=gen_temp.objects.get(edxuserid=oldstud,section=secid)
                     marks_obj.eval=res
                     marks_obj.total=t
                     marks_obj.save()
                     updateeval = updateeval +1
                  except Exception as e:
                     marks_obj=gen_temp(edxuserid=oldstud,section=secid,eval=res,total=t)
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
                  wr.writerow([oldstud,secid,res,t])
                  try:
                   
                     marks_obj=gen_temp.objects.get(edxuserid=oldstud,section=secid)
                     marks_obj.eval=res
                     marks_obj.total=t
                     marks_obj.save()
                     updateeval = updateeval +1
                  except Exception as e:
                     marks_obj=gen_temp(edxuserid=oldstud,section=secid,eval=res,total=t)
                     marks_obj.save() 
                     inserteval=inserteval+1      
         else:
            ctr=0
            studrec = [0,0,0,0]
              #return [inserteval,updateeval]
         
     return [0,0]

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
 heading=["UserId","Username","Email","Grade <br>100%"]
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
   name='static/closed_courses/'+courseobj.course+'/'+courseobj.course+'_grade_details.csv'
   with open(name,'w') as csvfile:
    wr = csv.writer(csvfile,delimiter=',')
    wr.writerow(["edxuserid","course","Grade","eval"])
    studentdetails_obj=gen_temp.objects.filter(section__in=sectionl).values("edxuserid").distinct()
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
              markstable_obj=gen_temp.objects.get(section=str(section[0]),edxuserid=studentdetails['edxuserid'])
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
                  markstable_obj=gen_temp.objects.get(section=str(section[0]),edxuserid=studentdetails['edxuserid'])  
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

     wr.writerow([studentdetails['edxuserid'],courseobj.course,avg,res])
     insert_gradestable+=1 
   return [insert_gradestable,update_gradestable]
 except Exception as e:
          print "Error - %s,(%s) edxcourse object for %s doesnot exists"%(str(e.message),str(type(e)), courseobj.courseid)
          return [-1,-1]    
     
     
def delete_temp_table():
   gen_temp.objects.all().delete()
          
def main(argv):
      init()
      course_id=""
      course_list=["CS101.1x","SKANI101x","PATH372.1x","WME209x","WEE210.2x","WEE210.1x","WCS101.1x","ME209x","EE210.2x","EE210.1x"]#list of closed course
      for course in course_list:
         try:
            course_obj=edxcourses.objects.get(course=course)
         except:
            course_obj=get_course_detail(course)
         if course_obj != -1 :
            #create a folder course as name under static folder i.e. static/closed_courses/CS101.1x
            newpath = 'static/closed_courses/'+course_obj.course
            if not os.path.exists(newpath):
               os.makedirs(newpath)
            result=fetch_gen_evaluations(course_obj.courseid)
            # create folder eval_details/
            newpath = 'static/closed_courses/'+course_obj.course+'/eval_details'
            if not os.path.exists(newpath):
               os.makedirs(newpath)
            gen_evaldata(course_obj.courseid)
            gen_grades(course_obj.courseid)
            delete_temp_table()




if __name__ == "__main__":
    main(sys.argv[1:])






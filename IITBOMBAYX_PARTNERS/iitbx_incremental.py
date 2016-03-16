'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


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

def get_course_detail(csr,org,longname):
     collection=mongo_openconnection()
     curtime = datetime.now()
     course_id=""
     blended = 0
     if str(longname) in courses:
        blended=1
     else:
        blended=0
     for course_det in collection.find({"_id.course":csr,"_id.org":org,"_id.category":"course"},{"metadata.start":1,"metadata.end":1,"metadata.enrollment_start":1,"metadata.enrollment_end":1,"metadata.course_image":1,"metadata.display_name":1,"definition.data.grading_policy":1}):
                
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
                      course_obj=edxcourses.objects.get(courseid=course_id)
                      courseid=course_obj.id
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
     for course_det in collection.find({"$and": [{"_id.category":"course"},{"_id.course":course_obj.course },{"_id.org":course_obj.org}]}):
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
def insert_modlist(disnm,motype,moid,rel_id,sort1,visible_to_staff_only,graded,long_name,weight1, count,release_date,due_date,cid,gradetype):
    
    try:
       
       mod_obj = course_modlist.objects.get(long_name=long_name)
       mod_obj.display_name = disnm
       mod_obj.module_type = motype
       mod_obj.module_id = moid
       mod_obj.long_name=long_name 
       mod_obj.related_id = rel_id
       
       mod_obj.order=sort1
       
       mod_obj.visible_to_staff_only=visible_to_staff_only
       mod_obj.graded=graded
       mod_obj.maxmarks=weight1
       mod_obj.questions=count
       mod_obj.startdate=release_date
       mod_obj.duedate=due_date
       mod_obj.hasproblems=0
       mod_obj.course=cid
       mod_obj.gradetype=gradetype
       mod_obj.save()
       return mod_obj.id
    except Exception as e:
       #print str(e.message)
       #print "insert"
       coursemod = course_modlist(display_name=disnm,module_type=motype,module_id=moid, related_id=rel_id,order=sort1, visible_to_staff_only=visible_to_staff_only, graded=graded, long_name=long_name, maxmarks=weight1, questions=count, startdate=release_date, duedate=due_date,hasproblems=0,course=cid,gradetype=gradetype)
       coursemod.save()
       return coursemod.id
 

@transaction.atomic      
def open_module(csr,org,csr_id,mlist,sortorder,start,end,cid):
  runtime = datetime.now()
  weight=0
  has_problem=0
  count=0
  totalques=0
  totalmarks=0
  dict={}
  count=0 
  weight=0
  childgraded=0
  for mod in mlist:
       mtype=mod.split('/')[4]
       mid=mod.split('/')[5]
       sortorder=sortorder+1
       #print sortorder
       for moddetails in collection.find({"_id.course":csr,"_id.org":org,"_id.category":mtype,"_id.name":mid},{"metadata.display_name":1,"definition.children":1,"_id.name":1, "metadata.graded":1,"metadata.visible_to_staff_only":1,"metadata.format":1,"metadata.start":1,"metadata.due":1,"definition.data.data":1,"metadata.weight":1}):
            try:
               dname=moddetails["metadata"]["display_name"].encode('utf-8')
            except:
               dname=""
            try:
               gradetype=moddetails["metadata"]["format"]
            except:
               gradetype=""
            try:
               
               due_date=moddetails["metadata"]["due"]
               due_date=datetime.strptime(str(due_date), '%Y-%m-%dT%S:%M:%HZ')
            except:
               due_date=end
            try:
               release_date= moddetails["metadata"]["start"]
               release_date=datetime.strptime(str(release_date), '%Y-%m-%dT%S:%M:%HZ')

            except Exception as e :
               release_date=start
            try:
               if moddetails['metadata']['visible_to_staff_only'] == True:
                      #print dname
                      visible_to_staff_only=1 
            except:
               visible_to_staff_only=0 
            try:
               if moddetails['metadata']['graded'] ==True:
                  graded=1
            except:
               graded=0 
            if mtype == 'problem':
             has_problem=1
             try:
               definition_data=moddetails['definition']['data']['data'].encode('utf-8')
               try:
                   weight=moddetails["metadata"]["weight"]
                   count=1
               except Exception as e:
                   count=0;weight=0
                   for type in question_types:
                      weight+=definition_data.count(type)
                      count+=definition_data.count(type)
               totalques=totalques+1
               totalmarks=totalmarks+weight
             except Exception as ex:
                   print ex.__class__.__name__,str(ex.message)
            else:
                    weight=0
                    count =0
            
            #insert_id=insert_modlist(dname,mtype,mod_details["_id"]["name"],csr_id,sortby,visible_to_staff_only,graded,mod)
            insert_id=insert_modlist(dname,mtype,moddetails["_id"]["name"],csr_id,sortorder,visible_to_staff_only,graded,mod,weight, count,release_date,due_date,cid,gradetype) 
            try:
               clist=moddetails["definition"]["children"]
            except:
               clist=[]
            if len(clist) !=0:
                result=open_module(csr,org,insert_id,clist,sortorder,start,end,cid)
                
                sortorder=result['sortorder'] 
                #print result, clist
                # Update Verticals and  Sequentials that have graded problems with maxmarks and number of questions
                # update verticals with number of  
  dict['graded']=graded
  dict['questions']=totalques
  dict['maxmarks']=totalmarks
  dict['sortorder']=sortorder
  dict['has_problem']=has_problem
  return dict        



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
def course_modules(course_id,org,cid):
    csr=edxcourses.objects.get(courseid=course_id).course
    result={}
    sortby=0   
    for csr_name in collection.find({"_id.course":csr,"_id.org":org,"_id.category":"course"} ,{"metadata.display_name":1, "metadata.visible_to_staff_only":1,"definition.children":1,"metadata.start":1,"metadata.end":1}): 
         sortby=sortby+1
         try:
            temp=csr_name["metadata"]["end"]
            course_end= datetime.strptime(str(temp),'%Y-%m-%dT%S:%M:%HZ')
         except:
            course_end=date_format("9999-12-31 00:00:00","%Y-%m-%d %H:%M:%S")
         try: 
                   course_start=csr_name["metadata"]["start"]
                   course_start=datetime.strptime(str(course_start), '%Y-%m-%dT%S:%M:%HZ')
         except:
                   course_start= course_end + timedelta(days=-1)
         csr_id=insert_modlist((csr_name["metadata"]["display_name"].encode('utf-8')),"course",course_id,"0",sortby,0,0,csr,0,0,course_start,course_end,cid,"")
         if len(csr_name["definition"]["children"]) !=0:
                result=open_module(csr,org,csr_id,csr_name["definition"]["children"],sortby,course_start,course_end,cid,)

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
def print_courseware(csr,org,cid):
    evallist=[];qlist=[]
    grades_dict={}
    updated_problem_count=0
    inserted_problem_count=0
    error_updated_count=0
    dict={}
    evaluation_dict=collections.OrderedDict()
    
    try:
       course_obj=edxcourses.objects.get(id=cid)
    except:
       return -1
    gradedprob=0
    curtime = datetime.now() 
    ques_dict={} 
    modlist=course_modlist.objects.get(module_id= csr,course=cid,visible_to_staff_only=0)
    chlist=course_modlist.objects.filter(related_id= modlist.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id')
         
    for chap in chlist:
       ecount=0  # keep track on evaluation order
       seqlist=course_modlist.objects.filter(related_id= chap.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id') 
       for seq in seqlist:
           gradedprob=0 
           qlist=[]
           count=0
           heading = ["Rollno","Username","Email"]
           headlist=[]
           total=0
           not_attempt={}
           quest=[]
           q_dict={}
           tcount=0
           ecount=ecount+1
           na=[]  
           vertlist=course_modlist.objects.filter(related_id=seq.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id')
           evaluations_type={}
           grade_total=0
           for vert in vertlist:
            if (seq.graded==1) or (vert.graded==1) :
               
               problist=course_modlist.objects.filter(related_id=vert.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime,module_type='problem').exclude(maxmarks=0).order_by('order','related_id')
               
               for prob in problist:
                    gradedprob=1
                    count=count+1 
                    total=total+prob.maxmarks                               
                    quesname="Q"+str(count).zfill(2)+"<br>"+str(prob.maxmarks)+" Pts"
                    headlist.append(quesname)
                    qlist.append([prob.maxmarks,prob.long_name,prob.display_name.encode('utf-8'),prob.questions])
                  
                    not_attempt[prob.long_name]=tcount
                    tcount=tcount+1
                    quest.append(prob.long_name)
                    q_dict[prob.long_name]=prob.maxmarks    
               grade_total=grade_total+total         # To get the total grade for a particular evaluation
            else:
              # Search for Non graded Problems
              problist=course_modlist.objects.filter(related_id=vert.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime,module_type='problem').order_by('order','related_id')
              for prob in problist:
                    gradedprob=-1
                    count=count+1 
                    total=total+prob.maxmarks                               
                    qlist.append([prob.maxmarks,prob.long_name,prob.display_name.encode('utf-8'),prob.questions])
                  
                    quest.append(prob.long_name)
                    q_dict[prob.long_name]=prob.maxmarks    
               
           if(gradedprob==1):

               #print "Evaluation -->", seq.display_name.encode('utf-8'), seq.startdate,seq.duedate, seq.gradetype,total
               heading=heading+["Total <br>"+str(total)+" Pts"]+headlist 
               dict[str(seq.id)]=qlist
               evallist.append(dict)
               na=["NA"]*count
               try:
                   evaluations_obj=evaluations.objects.get(course=course_obj, sectionid=seq.module_id)
                   evaluations_obj.sec_name=seq.display_name.encode('utf-8')
                   evaluations_obj.release_date=seq.startdate
                   evaluations_obj.due_date=seq.duedate
                   total_marks=total
                   evaluations_obj.save()
               except Exception as e:
                
                   evaluations_obj=evaluations(course=course_obj, sectionid=seq.module_id,sec_name=seq.display_name.encode('utf-8') ,type=seq.gradetype ,release_date=seq.startdate, due_date=seq.duedate, total_weight=0,grade_weight=0,total_marks=total)
                   evaluations_obj.save()

               for qid in qlist:
                    try:
                       problem_obj=questions.objects.get( qid=qid[1])
                       try: 
                          problem_obj.q_weight=qid[0]
                          problem_obj.q_name=qid[2]
                          problem_obj.prob_count=qid[3]
                          problem_obj.save()
                          updated_problem_count=updated_problem_count+1
                       except Exception as e:
                               error_updated_count=error_updated_count+1                          
                    except Exception as e:
                           questions_obj=questions(course=course_obj, eval=evaluations_obj, qid=str(qid[1]), q_name=qid[2], q_weight=qid[0], prob_count=qid[3])
                           questions_obj.save()
                           inserted_problem_count=inserted_problem_count+1

               #creating dictionary for evaluation
               '''
                Graded Quiz:{'aa70ddd71a334da286ffdf248432e2aa': {'total': 10}},
                Graded Programming Assignment: {'d47b9626818e41dea3ba94cc1d076d72': {'total': 10}},
                Final Exam: {'a52581465469418bb9ae0666633b93bf': {'total': 15}}
               '''
               eval_dict=evaluation_dict.setdefault(str(seq.gradetype),OrderedDict({}))
               evl_dict=eval_dict.setdefault(str(seq.module_id),{})
               e_dict=evl_dict.setdefault("total",int(total))
               #o_dict=evl_dict.setdefault("order",int(ecount))
               dict={}
               
               try:
                  headers=headings.objects.get(section=evaluations_obj.sectionid)   
                  headers.heading=",".join(map(str,heading))
                  headers.save()
               except Exception as e:
                  heading_obj=headings(heading=",".join(map(str,heading)),section=evaluations_obj.sectionid)
                  heading_obj.save()
               if course_obj.blended_mode==1:
                  get_marks(course_obj,evaluations_obj,quest,q_dict,not_attempt,count,grades_dict)
           elif gradedprob==-1:
             #print "Non graded Evaluation -->", seq.display_name.encode('utf-8'), seq.startdate,seq.duedate, seq.gradetype,total 
             try:
                   evaluations_obj=gen_evaluations.objects.get(course=course_obj, sectionid=seq.module_id)
                   evaluations_obj.sec_name=seq.display_name.encode('utf-8')
                   evaluations_obj.release_date=seq.startdate
                   evaluations_obj.due_date=seq.duedate
                   total_marks=total
                   evaluations_obj.save()
             except Exception as e:
                   evaluations_obj=gen_evaluations(course=course_obj, sectionid=seq.module_id,sec_name=seq.display_name.encode('utf-8') ,type=seq.gradetype ,release_date=seq.startdate, due_date=seq.duedate, total_weight=0,grade_weight=0,total_marks=total)
                   evaluations_obj.save()
             for qid in qlist:
                    try:
                       problem_obj=gen_questions.objects.get( qid=qid[1])
                       problem_obj.q_weight=qid[0]
                       problem_obj.q_name=qid[2]
                       problem_obj.prob_count=qid[3]
                       problem_obj.save()
                       updated_problem_count=updated_problem_count+1
                    except Exception as e:
                       questions_obj=gen_questions(course=course_obj, eval=evaluations_obj, qid=str(qid[1]), q_name=qid[2], q_weight=qid[0], prob_count=qid[3])
                       questions_obj.save()   
    if course_obj.blended_mode==1:
       grades_policy_dict=create_headings(course_obj,evaluation_dict)  
       student_grades(course_obj,grades_dict,evaluation_dict,grades_policy_dict)

   
@transaction.atomic    
def create_headings(course_obj,eval_dict):
      headers=["RollNumber","Username","Email Id","Progress <br>in %"] ;tooltip=[];grades_policy_dict=collections.OrderedDict()
      for keys,values in eval_dict.iteritems():
          #Creating dictinary of grade policy
          '''
          'Graded Quiz':{'min_count': '6', 'drop_count': '2', 'weight': 0.4}, 
          'Graded Programming Assignment': 'min_count': '4', 'drop_count': '1', 'weight': 0.3},
          'Final Exam': {'min_count': '1', 'drop_count': '0', 'weight': 0.3}
          '''
          grade_types=gradepolicy.objects.get(courseid=course_obj,type=keys)
          grade_policy_dict=grades_policy_dict.setdefault(keys,OrderedDict({}))
          min_count_dict=grade_policy_dict.setdefault("min_count",str(grade_types.min_count))
          drop_count_dict=grade_policy_dict.setdefault("drop_count",str(grade_types.drop_count))
          weight_dict=grade_policy_dict.setdefault("weight",grade_types.weight)
          #print values.keys()
          for key,value in values.iteritems():
              total=value['total']
              # To get the order of individual sections
              key_order=(values.keys().index(key))+1
              headers.append(str(grade_types.short_label+str(key_order)+"<br>"+str(total)+"Pts"))
              tt='TT'+str(course_obj.courseid)
              evaluations_obj=evaluations.objects.filter(course_id=course_obj,sectionid=key).values("sec_name").distinct()
              section_name=evaluations_obj[0]["sec_name"]
              tooltip.append(str(section_name))
              #res=",".join(map(str,eval_out))
              header=",".join(map(str,headers))
              print "HEADER",header
              tooltip_header=",".join(map(str,tooltip))
         
      try:
          header_objs=headings.objects.get(section=course_obj.courseid)
          header_objs.heading=header
          header_objs.save()
      except:
          header_objs=headings(section=course_obj.courseid,heading=header)  
          header_objs.save()
      #For tooltip
      try:
         header_objs=headings.objects.get(section=tt)
         header_objs.heading=tooltip_header
         header_objs.save()
      except:
         header_objs=headings(section=tt,heading=tooltip_header)  
         header_objs.save()
      
      return grades_policy_dict
   


@transaction.atomic
def get_marks(course_obj,evaluations_obj,quest,q_dict,not_attempt,count,grades_dict):
    updateeval=1;inserteval=0;
    #students_obj=studentDetails.objects.filter(courseid=course_obj.courseid,edxuserid__edxuserid__in=[31982,31840,33625,113312,117634,105045])  # For testing
    students_obj=studentDetails.objects.filter(courseid=course_obj.courseid)
    #students_obj=studentDetails.objects.filter(courseid=course_obj.courseid,edxuserid__edxuserid=31982)
   
    for student in students_obj:
        eval_out=["NA"]*count
        total_marks=0
        marks_obtained=0
        marks_obj=CoursewareStudentmodule.objects.filter(student__id=student.edxuserid.edxuserid,course_id=course_obj.courseid,module_id__in=quest,grade__isnull=False)
        for marks in marks_obj:
            marks_obtained=marks.grade/marks.max_grade*q_dict[marks.module_id]
        
            eval_out[not_attempt[marks.module_id]]=marks_obtained
            total_marks=total_marks+marks_obtained
        #res=",".join(map(str, eval_out.values()))
        res=",".join(map(str,eval_out))
        try:
                   marks_obj=markstable.objects.get(stud=student,section=evaluations_obj.sectionid)
                   marks_obj.eval=res
                   marks_obj.total=total_marks
                   marks_obj.save()
                   updateeval = updateeval +1
        except Exception as e:
                   marks_obj=markstable(stud=student,section=evaluations_obj.sectionid,eval=res,total=total_marks)
                   marks_obj.save() 
                   inserteval=inserteval+1 
        #print evaluations_obj.type
        #Creating dictionary for student grades
        '''
         '17':{
               'Graded Quiz':{'aa70ddd71a334da286ffdf248432e2aa': {'obtained_marks': 9.0,'total_marks':10.0},
                              '0db4e13e3838441ca99f2763a422f2ab': {'obtained_marks': 0.0,'total_marks':10.0}}
               'Graded Programming Assignment':
                            {'d47b9626818e41dea3ba94cc1d076d72': {'obtained_marks': 0.0,'total_marks':10.0}, 
                             '5409d445cd954c2199a7b1d74376ff79': {'obtained_marks': 0.0,'total_marks':10.0}}
               'Final Exam':{'a52581465469418bb9ae0666633b93bf': {'obtained_marks': 0.0,'total_marks':15.0}, 
                             '41dd3824d6c24123bd977d805bb4a499': {'obtained_marks': 0.0,'total_marks':15.0}}
              }
        '''
        grade_dict=grades_dict.setdefault(str(student.edxuserid.edxuserid),OrderedDict({})) 
        g_dict=grade_dict.setdefault(str(evaluations_obj.type),OrderedDict({}))
        grd_dict=g_dict.setdefault(str(evaluations_obj.sectionid),{})
        g_dict=grd_dict.setdefault("obtained_mark",total_marks)
        total_dict=grd_dict.setdefault("total_mark",float(evaluations_obj.total_marks))

@transaction.atomic
def student_grades(course_obj,grades_dict,evaluation_dict,grades_policy_dict):
    #print grades_policy_dict
    drop_count=0;min_count=0
    for keys,values in grades_dict.iteritems():
      #print keys # student edxuserid
      res=[];marks_list=[];total=0.0
      for key, value in values.iteritems():
        grades_list=[]
        #print key  #grade type
        for i, j in grades_policy_dict.iteritems():
             if i == key:
                min_count= int(j["min_count"])
                drop_count= int(j["drop_count"])
                weight= float(j["weight"])
                
        for k,v in value.iteritems():
          studentdetails_obj=studentDetails.objects.get(courseid=course_obj.courseid,edxuserid=keys)
          total_grade=0.0
          marks_list.append(v['obtained_mark'])
          grades_list.append(float(v['obtained_mark']/v['total_mark']))
        if len(grades_list) > min_count:
           length=len(grades_list)
           q_count=length-drop_count
        else :
           q_count=min_count-drop_count
        grades_list=sorted(grades_list,reverse=True)[:q_count]
        sum_grade=sum(grades_list)
        avg_grade=sum_grade/q_count
        grade_weight=(sum(grades_list)/q_count)*weight
        total=total+grade_weight
      res=",".join(map(str,marks_list))
      try:
           gradestable_obj=gradestable.objects.get(stud=studentdetails_obj,course=course_obj.courseid)
           gradestable_obj.stud=studentdetails_obj
           gradestable_obj.course=course_obj.courseid
           gradestable_obj.grade=round(total*100+0.05)
           gradestable_obj.eval=res
           gradestable_obj.save() 
      except Exception as e:
           gradestable_obj=gradestable(stud=studentdetails_obj,course=course_obj.courseid,grade=round(total*100+0.05),eval=res)
           gradestable_obj.save()


def ObtainDate():
    isValid=False
    while not isValid:
        userIn = raw_input("Type Refresh Date in format(YYYY-MM-DD_HHhMIm). Example:2015-11-18_10h30m :")
        try:
            ref = datetime.strptime(userIn, "%Y-%m-%d_%Ih%Mm").strftime("%b %d, '%y %I:%M %p")
            print ref
            isValid=True
        except:
            print "Invalid Format!\n"
    return ref

def generate_emails(refreshdate,runtime):
      
       FROM = "bmwsupport@iitbombayx.in"
       TO = ["bmwsoftwareteam@cse.iitb.ac.in","workshopmanagers@cse.iitb.ac.in","sheweta@cse.iitb.ac.in"] # must be a list
       #CC = ["bmwsoftwareteam@cse.iitb.ac.in"] # email id as CC
       SUBJECT = "MIS Sync Script Status"
       text = """The script ran sucessfully on %s UTC. Please note the IITBombayX data was refreshed on %s IST.

Regards,
MIS Support
""" %(runtime,refreshdate)
             
       # Prepare actual message

       #msg = EmailMultiAlternatives(SUBJECT, message, FROM, TO, cc=CC) # if cc is required
       msg = EmailMultiAlternatives(SUBJECT, text, FROM, TO)
       msg.send(fail_silently=False)

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
 MAKEDATE(YEAR(lastday), 1) + INTERVAL QUARTER(lastday) QUARTER - INTERVAL    1 QUARTER  firstday,year(lastday) currentyear from
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
         currentyear=i[11]
    try:
             report_obj=gen_repout.objects.get(B="Date")
             report_obj.reportid=1
             report_obj.num_cols=6 
             report_obj.A=heading
             report_obj.C="WTD"
             report_obj.D="MTD"
             report_obj.E="QTD"
             report_obj.F="YTD"
             report_obj.G="Since inception"
             report_obj.save()
    except:
             report_obj=gen_repout(reportid=1,num_cols=6,A=heading,B="Date",C="WTD",D="MTD",E="QTD",F="YTD",G="Since inception")
             report_obj.save()   
            
    mysql_csr.execute('''SELECT " " id,sum(lusers) "clusers",sum(wusers) "cwusers",sum(musers) "cmusers",sum(qusers) "cqusers",sum(yusers) "cyusers",sum(iusers) "ciusers",sum(lausers) "clausers",sum(wausers) "cwausers",sum(mausers) "cmausers",sum(qausers) "cqausers",sum(yausers) "cyausers",sum(iausers) "ciausers",sum(llusers) "cllusers",sum(wlusers) "cwlusers",sum(mlusers) "cmlusers",sum(qlusers) "cqlusers",sum(ylusers) "cylusers",sum(ilusers) "cilusers"
FROM(
SELECT if(date(date_joined)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),1,0) "lusers"
       ,if(week(date_joined)=%s and year(date_joined)=%s,1,0) "wusers"
       ,if(month(date_joined)=%s and year(date_joined)=%s,1,0) "musers"
       ,if(quarter(date_joined)=%s and year(date_joined)=%s,1,0) "qusers"
       ,if(year(date_joined)=%s,1,0) "yusers"
       ,1 "iusers" 
       ,if(date(date_joined)=DATE_FORMAT(%s,"%%Y-%%m-%%d") and is_active=1,1,0) "lausers"
       ,if(week(date_joined)=%s and is_active=1 and year(date_joined)=%s,1,0) "wausers"
       ,if(month(date_joined)=%s and is_active=1 and year(date_joined)=%s,1,0) "mausers"
       ,if(quarter(date_joined)=%s and is_active=1 and year(date_joined)=%s,1,0) "qausers"
       ,if(year(date_joined)=%s and is_active=1,1,0) "yausers"
       ,if(is_active=1,1,0) "iausers"
       ,if(last_login=DATE_FORMAT(%s,"%%Y-%%m-%%d"),1,0) "llusers"
       ,if(week(last_login)=%s and year(last_login)=%s,1,0) "wlusers"
       ,if(month(last_login)=%s and year(last_login)=%s,1,0) "mlusers"
       ,if(quarter(last_login)=%s and year(last_login)=%s,1,0) "qlusers"
       ,if(year(last_login)=%s,1,0) "ylusers"
       ,1 "ilusers"
  FROM auth_user  ) A 
 ''',(lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear,lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear,lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear))
    user=mysql_csr.fetchall()
    for j in user:
        try:
            report_obj=gen_repout.objects.get(A="New Users")
            report_obj.reportid=1
            report_obj.num_cols=6
            report_obj.B=j[1]
            report_obj.C=j[2]
            report_obj.D=j[3]
            report_obj.E=j[4]
            report_obj.F=j[5]
            report_obj.G=j[6]
            report_obj.save()
        except:
            totaluser_obj=gen_repout(reportid=1,num_cols=6,A="New Users",B=j[1],C=j[2],D=j[3],E=j[4],F=j[5],G=j[6]) 
            totaluser_obj.save()
        try:
            report_obj=gen_repout.objects.get(A="New Activated Users")
            report_obj.reportid=1
            report_obj.num_cols=6
            report_obj.B=j[7]
            report_obj.C=j[8]
            report_obj.D=j[9]
            report_obj.E=j[10]
            report_obj.F=j[11]
            report_obj.G=j[12]
            report_obj.save()
        except:
            totalusers_obj=gen_repout(reportid=1,num_cols=6,A="New Activated Users",B=j[7],C=j[8],D=j[9],E=j[10],F=j[11],G=j[12])
            totalusers_obj.save()
        try:
            report_obj=gen_repout.objects.get(A="Logged-in Users")
            report_obj.reportid=1
            report_obj.num_cols=6
            report_obj.B=j[13]
            report_obj.C=j[14]
            report_obj.D=j[15]
            report_obj.E=j[16]
            report_obj.F=j[17]
            report_obj.G=j[18]
            report_obj.save()
        except:
           totaluse_obj=gen_repout(reportid=1,num_cols=6,A="Logged-in Users",B=j[13],C=j[14],D=j[15],E=j[16],F=j[17],G=j[18])  
           totaluse_obj.save()

    mysql_csr.execute('''SELECT " " id, sum(estu) "cestu",sum(westu) "cwestu",sum(mestu) "cmestu",sum(qestu) "cqestu" ,sum(yestu) "cyestu",sum(iestu) "ciestu", count(distinct enrolcou) -1 "cenrolcou",count(distinct wenrolcou)-1 "cwenrolcou",count(distinct menrolcou)-1 "cmenrolcou",count(distinct qenrolcou)-1 "cqenrolcou",count(distinct yenrolcou)-1 "cyenrolcou",count(distinct ienrolcou) "cienrolcou"
FROM(
SELECT course_id, if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),1,0) "estu"
       ,if(week(created)=%s and year(created)=%s,1,0) "westu"
       ,if(month(created)=%s and year(created)=%s,1,0) "mestu"
       ,if(quarter(created)=%s and year(created)=%s,1,0) "qestu"
       ,if(year(created)=%s,1,0) "yestu"
       ,1 "iestu" 
       ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),course_id,"") "enrolcou"
       ,if(week(created)=%s and year(created)=%s,course_id,"") "wenrolcou"
       ,if(month(created)=%s and year(created)=%s,course_id,"") "menrolcou"
       ,if(quarter(created)=%s and year(created)=%s,course_id,"") "qenrolcou"
       ,if(year(created)=%s,course_id,"") "yenrolcou"
       ,course_id "ienrolcou" 
FROM  student_courseenrollment ) S ''',(lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear,lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear))
    estud=mysql_csr.fetchall()
    for k in estud:
            try:
               report_obj=gen_repout.objects.get(A="Enrolled Users")
               report_obj.reportid=1
               report_obj.num_cols=6
               report_obj.B=k[1]
               report_obj.C=k[2]
               report_obj.D=k[3]
               report_obj.E=k[4]
               report_obj.F=k[5]
               report_obj.G=k[6]
               report_obj.save()
            except:
               totaluser_obj=gen_repout(reportid=1,num_cols=6,A="Enrolled Users",B=k[1],C=k[2],D=k[3],E=k[4],F=k[5],G=k[6]) 
               totaluser_obj.save()
            try:
               report_obj=gen_repout.objects.get(A="Courses where users enrolled")
               report_obj.reportid=1
               report_obj.num_cols=6
               report_obj.B=k[7]
               report_obj.C=k[8]
               report_obj.D=k[9]
               report_obj.E=k[10]
               report_obj.F=k[11]
               report_obj.G=k[12]
               report_obj.save()
            except:
               totaluser_obj=gen_repout(reportid=1,num_cols=6,A="Courses where users enrolled",B=k[7],C=k[8],D=k[9],E=k[10],F=k[11],G=k[12]) 
               totaluser_obj.save()
   

    mysql_csr.execute('''select " " id, count(distinct lactstud) -1 "clactstud", count(distinct wactstud)-1 "cwactstud", count(distinct mactstud)-1 "cmactstud", count(distinct qactstud)-1 "cqactstud",count(distinct yactstud)-1 "cyactstud",count(distinct iactstud)-1 "ciactstud",count(distinct lactcour) "clactcour", count(distinct wactcour)-1 "cwactcour", count(distinct mactcour)-1 "cmactcour", count( distinct qactcour)-1 "cqactcour",count( distinct yactcour)-1 "cyactcour",count( distinct iactcour) "ciactcour", count(distinct lvideo)-1 "clvideo",count(distinct wvideo)-1 "cwvideo", count(distinct mvideo)-1 "cmvideo", count(distinct qvideo)-1 "cqvideo",count(distinct yvideo)-1 "cyvideo",count(distinct ivideo)-1 "civideo",count(distinct lstudprob)-1 "clstudprob", count(distinct wstudprob)-1 "cwstudprob", count(distinct mstudprob)-1 "cmstudprob", count(distinct qstudprob)-1 "cqstudprob",count(distinct ystudprob)-1 "cystudprob",count(distinct istudprob)-1 "cistudprob", count(distinct lstudgrade)-1 "clstudgrade",count(distinct wstudgrade)-1 "cwstudgrade", count(distinct mstudgrade)-1 "cmstudgrade",count(distinct qstudgrade)-1 "cqstudgrade",count(distinct ystudgrade)-1 "cystudgrade",count(distinct istudgrade)-1 "cistudgrade"
from(
select student_id, course_id,
          if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),student_id,0)  "lactstud"
          ,if(week(created)=%s and year(created)=%s,student_id,0)  "wactstud"
          ,if(month(created)=%s and year(created)=%s,student_id,0) "mactstud"
          ,if(quarter(created)=%s and year(created)=%s,student_id,0) "qactstud"
          ,if(year(created)=%s ,student_id,0) "yactstud"
          ,student_id "iactstud"
          ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d"),course_id,"") "lactcour"
          ,if(week(created)=%s and year(created)=%s,course_id,"")  "wactcour"
          ,if(month(created)=%s and year(created)=%s,course_id,"") "mactcour"
          ,if(quarter(created)=%s and year(created)=%s,course_id,"") "qactcour"
          ,if(year(created)=%s,course_id,"") "yactcour"
          ,course_id "iactcour"
          ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d") and module_type="video",student_id,0)  "lvideo"
          ,if(week(created)=%s and module_type="video" and year(created)=%s,student_id,0)  "wvideo"
          ,if(month(created)=%s and module_type="video" and year(created)=%s,student_id,0) "mvideo"
          ,if(quarter(created)=%s and module_type="video" and year(created)=%s,student_id,0) "qvideo"
          ,if(year(created)=%s and module_type="video",student_id,0) "yvideo"
          ,if(module_type="video",student_id,0) "ivideo"
          ,if(date(created)=DATE_FORMAT(%s,"%%Y-%%m-%%d") and module_type="problem",student_id,0) "lstudprob"
          ,if(week(created)=%s and module_type="problem" and year(created)=%s,student_id,0) "wstudprob"
          ,if(month(created)=%s and module_type="problem" and year(created)=%s,student_id,0) "mstudprob"
          ,if(quarter(created)=%s and module_type="problem" and year(created)=%s,student_id,0) "qstudprob"
          ,if(year(created)=%s and module_type="problem" ,student_id,0) "ystudprob"
          ,if(module_type="problem",student_id,0) "istudprob"
          ,if(created=DATE_FORMAT(%s,"%%Y-%%m-%%d") and module_type="problem" and grade is not null,student_id,0) "lstudgrade"
          ,if(week(created)=%s and module_type="problem" and grade is not null and year(created)=%s,student_id,0) "wstudgrade"
          ,if(month(created)=%s and module_type="problem" and grade is not null and year(created)=%s,student_id,0) "mstudgrade"
          ,if(quarter(created)=%s and module_type="problem" and grade is not null and year(created)=%s,student_id,0) "qstudgrade"
          ,if(year(created)=%s and module_type="problem" and grade is not null,student_id,0) "ystudgrade"
          ,if(module_type="problem" and grade is not null,student_id,0) "istudgrade"
          from  courseware_studentmodule ) C
''',(lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear,lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear,lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear,lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear,lday,weekno,currentyear,month,currentyear,quarter,currentyear,currentyear))
    courseact=mysql_csr.fetchall()
    for l in courseact:
           try:
               report_obj=gen_repout.objects.get(A="Active Students")
               report_obj.reportid=1
               report_obj.num_cols=6
               report_obj.B=l[1]
               report_obj.C=l[2]
               report_obj.D=l[3]
               report_obj.E=l[4]
               report_obj.F=l[5]
               report_obj.G=l[6]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=6,A="Active Students",B=l[1],C=l[2],D=l[3],E=l[4],F=l[5],G=l[6]) 
               totaluser_obj.save()

           try:
               report_obj=gen_repout.objects.get(A="Active Courses")
               report_obj.reportid=1
               report_obj.num_cols=6
               report_obj.B=l[7]
               report_obj.C=l[8]
               report_obj.D=l[9]
               report_obj.E=l[10]
               report_obj.F=l[11]
               report_obj.G=l[12]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=6,A="Active Courses",B=l[7],C=l[8],D=l[9],E=l[10],F=l[11],G=l[12]) 
               totaluser_obj.save()

           try:
               report_obj=gen_repout.objects.get(A="Students who watched videos")
               report_obj.reportid=1
               report_obj.num_cols=6
               report_obj.B=l[13]
               report_obj.C=l[14]
               report_obj.D=l[15]
               report_obj.E=l[16]
               report_obj.F=l[17]
               report_obj.G=l[18]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=6,A="Students who watched videos",B=l[13],C=l[14],D=l[15],E=l[16],F=l[17],G=l[18]) 
               totaluser_obj.save()
  
           try:
               report_obj=gen_repout.objects.get(A="Students who attempted practice problems")
               report_obj.reportid=1
               report_obj.num_cols=6
               report_obj.B=l[19]
               report_obj.C=l[20]
               report_obj.D=l[21]
               report_obj.E=l[22]
               report_obj.F=l[23]
               report_obj.G=l[24]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=6,A="Students who attempted practice problems",B=l[19],C=l[20],D=l[21],E=l[22],F=l[23],G=l[24]) 
               totaluser_obj.save()
  
           try:
               report_obj=gen_repout.objects.get(A="Students who attempted graded problems")
               report_obj.reportid=1
               report_obj.num_cols=6
               report_obj.B=l[25]
               report_obj.C=l[26]
               report_obj.D=l[27]
               report_obj.E=l[28]
               report_obj.F=l[29]
               report_obj.G=l[30]
               report_obj.save()
           except:
               totaluser_obj=gen_repout(reportid=1,num_cols=6,A="Students who attempted graded problems",B=l[25],C=l[26],D=l[27],E=l[28],F=l[29],G=l[30]) 
               totaluser_obj.save()
    

    return 1
###############################################end of iitbxactivity#################################################################
def main(argv):
        refreshDate=ObtainDate() 
        init()
        collection=mongo_openconnection()
        curtime = datetime.now()
        course_id=""
        
        #for course in collection.distinct("_id.course"):
        for course in collection.find({"_id.category":"course"},{"_id.course":1,"_id.org":1,"_id.tag":1,"_id.name":1}):
         longname=course["_id"]["tag"]+"/"+course["_id"]["org"]+"/"+course["_id"]["course"]+"/"+course["_id"]["name"]
         course_id=get_course_detail(course["_id"]["course"],course["_id"]["org"],longname)
         print course_id
         if (course_id != "-1") :
           try:
             course_obj=edxcourses.objects.get(courseid=course_id)
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
                    course_modules(course_obj.courseid,course_obj.org,course_obj.id)
                    print_courseware(course_obj.courseid,course["_id"]["org"],course_obj.id)
                    #grade=get_student_grades(course_id) 
                    #outlist=evaldata(course_id)
                else:
                    course_modules(course_obj.courseid,course_obj.org,course_obj.id)
                    print_courseware(course_obj.courseid,course["_id"]["org"],course_obj.id)
             
             else:
               print course_id, " is closed."
             
           except:
             print course_id," doesnot exist in edxcourses."
         else:
             print "Failed Get_course_detail" 
         try:
            refresh=Lookup.objects.get(category='RefreshDate',code=1)
            refresh.description=refreshDate
            refresh.save()
         except:
            None  
        iitbxactivity()
        generate_emails(refreshDate,curtime)
        
'''
# For closed course,as per faculties demand

def main(argv):
        init()
        collection=mongo_openconnection()
        curtime = datetime.now()
        #for course in ["TISS/SKANI101x/2015-16","NVAforIA/PATH372.1x/2015-16"]:
        #for course in ["IITBombayX/CS101.1xA15/2015_T1","IITBombayX/ME209xA15/2015_T1","IITBombayX/EE210.1xA15/2015_T1"]:
        # To check for practice problem
        for course in ["IITBombayX/EE210xS16/2016_T1","IITBombayX/CS101.1xS16/2016_T1","IITBombayX/ME209xS16/2016_T1","IITBombayX/HS791xS16/2016_T1","IITBombayX/SKANI101x/2016_T1"]:
        #for course in ["IITBombayX/EE210xS16/2016_T1"]:
            print course
            course_obj=edxcourses.objects.get(courseid=course)
            course_modules(course_obj.courseid,course_obj.org,course_obj.id)
            print_courseware(course_obj.courseid,course_obj.org,course_obj.id)
        iitbxactivity()
'''

if __name__ == "__main__":
    main(sys.argv[1:])


#end main

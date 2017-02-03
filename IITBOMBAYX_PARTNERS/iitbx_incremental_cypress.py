'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


from iitbx_settings import *
default_iitbx="admin@workshop.com"

course_list=["IITBombay/DC101/2015_25"] # add course names here

question_types=["<choiceresponse>","<optionresponse>","<multiplechoiceresponse>","<numericalresponse ","<stringresponse ","<drag_and_drop_input","<imageresponse","<formularesponse","<customresponse","<jsmeresponse>","<schematicresponse>"]
def init():
       global prefix_url
       prefix_url="https://iitbombayx.in/asset-v1:"
       global infix_url 
       infix_url='''+type@asset+block@'''
  

def dbedxapp_openconnection():
     cnxedxapp = MySQLdb.connect(user=user,passwd=passwd,host=mysql_host,db=mysql_schema)
     return cnxedxapp

def mongo_openconnection():
     global client
     client = MongoClient(mongodb)
     global db 
     db= client.edxapp
     collections=[]
     global collection_definitions
     global collection_structures
     global collection_active_versions
     collection_definitions = db.modulestore.definitions
     collections.append(collection_definitions)
     collection_structures = db.modulestore.structures
     collections.append(collection_structures)
     collection_active_versions = db.modulestore.active_versions
     collections.append(collection_active_versions)
     return collections

@transaction.atomic
def delete_grade_information(cid):
       gradepolicy.objects.filter(courseid=cid).delete()
       gradescriteria.objects.filter(courseid=cid).delete()


def get_course_detail(collection,csr, org, run, published_version):
     #print "start"
     curtime=datetime.now()
     course_initial="course-v1:"; definition_id=""; course_start=""; course_end=""; course_enroll_start=""; course_enroll_end=""; course_image="";course_disp_name="";
     course_id=course_initial + org + "+" + csr + "+" + run
     course= org + "+" + csr + "+" + run
     old_course=1
     children_list=None
     course_obj=[]
     if course_id in course_list:
        blended_mode =1
     else: 
        blended_mode= 0
    
     print course_id
     collection_structures=collection[1] 
     blocklist=collection_structures.find({"_id":published_version},{"blocks":1})
     blist=[]
     for blocks in blocklist :
        blist.append(blocks) 
        block = next((blck for blck in  blocks["blocks"] if blck["block_type"] == "course"), None)     
        try:
            course_disp_name=block["fields"]["display_name"]
        except :
            course_disp_name=""
        try:
            course_end=block["fields"]["end"]
            if course_end==None:
               course_end= curtime + timedelta(days=10000)
            
        except :
            #course_end=dateutil.parser.parse("4712-11-31T00:00:00Z")
            course_end= curtime + timedelta(days=10000)
        try:
            course_enroll_end=block["fields"]["enrollment_end"]
        except :
            course_enroll_end=course_end
        try:
            course_start=block["fields"]["start"]
        except :
            course_start=course_end + timedelta(days=-1)
          
        try:
            course_enroll_start=block["fields"]["enrollment_start"]
        except :
            course_enroll_start=course_start
        #print course_enroll_start,course_start,course_end,course_enroll_end,"dates"    
        ahead_date=course_end+ timedelta(days=num_days)
        delta= ahead_date-course_end
        if  ( ahead_date-curtime ).days > 0:
          old_course=0
          try:
              course_image=prefix_url+course+infix_url+block["fields"]["course_image"]
          except :
            course_image=""
          try:
            definition_id=block["definition"]
          except :
            definition_id=None
          try:
            children_list=block["fields"]["children"]
          except:
            None
          try:
             course_obj=edxcourses.objects.get(courseid=course_id)
             #course_obj.tag=course_tag
             course_obj.org=org
             course_obj.course=csr
             course_obj.name=str(run)
             course_obj.courseid=course_id
             course_obj.coursename=course_disp_name
             course_obj.enrollstart=course_enroll_start      
             course_obj.enrollend=course_enroll_end
             course_obj.coursestart=course_start
             course_obj.courseend=course_end
             course_obj.image=course_image
             course_obj.blended_mode=blended_mode
             course_obj.save()
          except Exception as e:
             course_obj=edxcourses( org=org, course=csr, name=run, courseid=course_id, coursename=course_disp_name, enrollstart=course_enroll_start, enrollend=course_enroll_end, coursestart=course_start, courseend=course_end,image=course_image,blended_mode=blended_mode)
             course_obj.save()
          #print definition_id        
          if definition_id  != None:        
             delete_grade_information(course_id)
             get_grade_policy_criteria(collection,course_obj,definition_id)
             if blended_mode ==1:
                 insert_admin_courseleveluser(course_id)
     return (course_id,children_list,blist,course_obj,old_course)
     
@transaction.atomic
def insert_admin_courseleveluser(courseid):
    
      try:
         course_obj=edxcourses.objects.get(courseid=courseid)
      except Exception as e:
         print "Error %s,(%s) - Fetching course object for " %(e.message,str(type(e)),courseid)
         return -1

      #Added by Sheweta for default org
      if course_obj.org == 'IITBombayX':
           default_user=default_iitbx
           default_org=0
      else:
           default_user=default_iimbx
           default_org=10
      try:
         instituteid=T10KT_Institute.objects.get(instituteid=default_org)
      except Exception as e:
         print "Error %s,(%s) -Fetching Institute object for " %(e.message,str(type(e)),courseid)
         return -1
      
      if Courselevelusers.objects.filter(personid__email=default_user,instituteid=instituteid,courseid_id=course_obj.id,roleid=5).exists():
         pass # No modification required for courselevelusers
      else:   #insert default teacher with personid=1 and instituteid=0 in courselevelusers table
        person_obj=Personinformation.objects.get(email=default_user)
        course_level_obj=Courselevelusers(personid=person_obj,instituteid=instituteid,courseid=course_obj,roleid=5,startdate="2005-01-01",enddate="4712-12-31")
        course_level_obj.save()
        return 0




def get_grade_policy_criteria(collection,course_obj ,definition_id):
     collection_definition=collection[0]
     cutoffs=None
     for policies in collection_definition.find({"_id":definition_id}):
       try:
         for policy in policies["fields"]["grading_policy"]["GRADER"]:
             try:
                min_count = policy["min_count"]
             except:
                min_count=0
             try:
                weight = policy["weight"]
             except:
                weight=0
             try:
                ptype = policy["type"]
             except:
                ptype=""
             try:
                drop_count = policy["drop_count"]
             except:
                drop_count=0
             try:
               short_label = policy["short_label"]
             except:
               short_label=""
             try:
                cutoffs = policies["fields"]["grading_policy"]["GRADE_CUTOFFS"]
             except:
                cutoffs=None
             #print cutoffs, "cutoffs"
             grade_policy_obj=gradepolicy(courseid=course_obj, min_count=min_count, weight=weight, type=ptype, drop_count=drop_count, short_label=short_label)
             grade_policy_obj.save()
       except:
         pass
         
     if cutoffs :
       for key,value in cutoffs.iteritems():
                grade_criteria_obj=gradescriteria(courseid=course_obj,grade=key,cutoffs=value)
                grade_criteria_obj.save()




@transaction.atomic
def get_student_course_enrollment(course):
    try:
        edx_course_obj=edxcourses.objects.get(courseid=course)
    except Exception as e:
         print "Error  %s,(%s) - EdxCourse object for course %s doesnot exists"%(e.message,str(type(e)),course)
         return   [-1]
    try:
        if edx_course_obj.org == 'IITBombayX':
           default_user=default_iitbx
           default_org=0
        else:
           default_user=default_iimbx
           default_org=10

        person_info_obj=Personinformation.objects.get(email=default_user)
    except Exception as e:
         print "Error  %s,(%s) -Personinformation object for default user doesnot exist while finding enrollments for %s"%(e.message,str(type(e)),course)
         return  [-1] 
    try:   
           course_level_obj=Courselevelusers.objects.get( courseid=edx_course_obj, personid = person_info_obj )
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
    runtime = timezone.now()
    
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
       coursemod = course_modlist(display_name=disnm,module_type=motype,module_id=moid, related_id=rel_id,order=sort1, visible_to_staff_only=visible_to_staff_only, graded=graded, long_name=long_name, maxmarks=weight1, questions=count, startdate=release_date, duedate=due_date,hasproblems=0,course=cid,gradetype=gradetype)
       coursemod.save()
       return coursemod.id

@transaction.atomic      
def open_module(collection,obj,children,blocklist,sortorder,csr_id,module_list):
  runtime = timezone.now()
  weight=0
  has_problem=0
  count=0
  totalques=0
  totalmarks=0
  dict={}
  count=0 
  weight=0
  graded=0 
  childgraded=0
  finallist=module_list
  for block in blocklist:
       blist=block['blocks']
       if children!= None:
         for child  in children:
            sortorder=sortorder+1
            block = next((blck for blck in  blist if (blck["block_type"] == child[0] and blck["block_id"] == child[1])), None)
            mod="block-v1:"+obj.org+"+"+obj.course+"+"+ obj.name + "+type@"+child[0]+ "+block@" + child[1]

            try:
               dname=block['fields']["display_name"].encode('utf-8')
            except:
               dname=""
            try:
               gradetype=block['fields']["format"]
            except:
               gradetype=""
            try:
               
               due_date=block['fields']["due"]
            except:
               due_date=obj.courseend
            try:
               release_date= block['fields']["start"]

            except Exception as e :
               release_date=obj.coursestart

            visible_to_staff_only=0 
            try:
               children=block["fields"]["children"]
            except:
               children=None
            try:
               if block['fields']['graded'] ==True:
                  graded=1
                  #print block["block_id"],dname,due_date,release_date,"open_module"
            except:
               graded=0 
            if child[0] == 'openassessment':
              total=0
              details=collection[0].find({"_id":block['definition']})
              for each in details:
                try:  
                  t=each["fields"]["rubric_criteria"] 
                  for criteria in  t :
                     pt=0.0
                     for option in criteria["options"]:
                         try: 
                            if(pt < option["points"]):
                                 pt=option["points"]
                         except:
                            pass
                     total =total+pt
                except:
                  pass 
              has_problem=1
              count=1
              weight=total
            if child[0] == 'problem':
             has_problem=1
             try:
               definition_data=block['fields']['markdown']
               try:
                   weight=block['fields']["weight"]
                   count=1
               except Exception as e:
                   count=0;weight=0
                   for type in question_types:
                      weight+=definition_data.count(type)
                      count+=definition_data.count(type)
               totalques=totalques+1
               totalmarks=totalmarks+weight
              
             except Exception as ex:
                    weight=0
                    count =0
            
            insert_id=insert_modlist(dname,child[0],child[1],csr_id,sortorder,visible_to_staff_only,graded,mod,weight, count,release_date,due_date,obj.id,gradetype) 
            finallist.append(child[1])
            result=open_module(collection,obj,children, blocklist, sortorder, insert_id,finallist)
            
            
            sortorder=result['sortorder']
            finallist=result['module_list'] 
  dict['graded']=graded
  dict['questions']=totalques
  dict['maxmarks']=totalmarks
  dict['sortorder']=sortorder
  dict['has_problem']=has_problem
  dict['module_list']=finallist
  return dict        


@transaction.atomic
def print_courseware(course_obj):
    evallist=[];qlist=[]
    grades_dict={}
    updated_problem_count=0
    inserted_problem_count=0
    error_updated_count=0
    dict={}
    evaluation_dict=collections.OrderedDict()
    csr=course_obj.courseid
    org= course_obj.org
    cid=course_obj.id

    gradedprob=0
    curtime = timezone.now()
    ques_dict={} 
    modlist=course_modlist.objects.get(module_id= csr,course=cid,visible_to_staff_only=0)
    chlist=course_modlist.objects.filter(related_id= modlist.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id')
         
    for chap in chlist:
       ecount=0  # keep track on evaluation order
       seqlist=course_modlist.objects.filter(related_id= chap.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id') 
       for seq in seqlist:
           #print seq.module_id,"module_id"
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
            #print vert.module_id,"verical module_id"
            if (seq.graded==1) or (vert.graded==1) :
               problist=course_modlist.objects.filter(related_id=vert.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime,module_type__in=('problem',"openassessment")).exclude(maxmarks=0).order_by('order','related_id')
               for prob in problist:
                    #print prob.module_id,"problem module id",prob.module_type
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
               grade_total=grade_total+total    # To get the total grade for a particular evaluation
               #print q_dict,"q_dict"
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
                   #print evaluations_obj,"evaluations_obj update"
               except Exception as e:
                   evaluations_obj=evaluations(course=course_obj, sectionid=seq.module_id,sec_name=seq.display_name.encode('utf-8') ,type=seq.gradetype ,release_date=seq.startdate, due_date=seq.duedate, total_weight=0,grade_weight=0,total_marks=total)
                   evaluations_obj.save()
                   #print evaluations_obj,"evaluations_obj insert"
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
               #print evl_dict,"evl_dict"
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
      headers=["RollNumber","Username","Email Id","Progress <br>in %"] ;tooltip=[]; grades_policy_dict=collections.OrderedDict(); header='"RollNumber","Username","Email Id","Progress <br>in %"'
      tt="" ;tooltip_header=""
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
    drop_count=0;min_count=0;weight=0
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




@transaction.atomic
def course_modules(collection,course):
     
    course_id=course[0]
    children=course[1]
    blocklist=course[2]
    obj=course[3]
    result={}
    sortby=0  
    module_list=[]
    csr_id=insert_modlist(  obj.name,"course",obj.courseid,"0",sortby,0,0,obj.courseid,0,0,obj.coursestart,obj.courseend,obj.id,"")
    module_list.append(obj.courseid)
    if len(children) !=0:
          
          result=open_module(collection,obj,children,blocklist,sortby,csr_id, module_list)
    #print result['module_list']
    t=course_modlist.objects.filter(course=obj.id).exclude(module_id__in=result['module_list'])
    deletedques=[];deletedassign=[]
    for moddata in t:
       print moddata.module_id, moddata.module_type
       if moddata.module_type=='sequential' :
          deletedassign.append(moddata.module_id)
       if moddata.module_type=='problem' or  moddata.module_type=='openassessment' : 
          deletedques.append(moddata.long_name)
    q= questions.objects.filter(course=obj,qid__in=deletedques).delete()
    e= evaluations.objects.filter(course=obj,sectionid__in=deletedassign).delete()
    t.delete()
    '''for a in q:
       print a
    
    for b in e:
       print b'''
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
          
def ObtainDate():
    isValid=False
    while not isValid:
        userIn = raw_input("Type Refresh Date in format(YYYY-MM-DD_HHhMIm). Example:2015-11-18_10h30m :")
        try:
            ref = datetime.strptime(userIn, "%Y-%m-%d_%Hh%Mm").strftime("%b %d, '%y %H:%M %p")
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

########################################## Start Email Change ################################################
@transaction.atomic
def email_change():
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error  %s,(%s) -Establishing mysql connection"%(e.message,str(type(e)))
      return [-1]
    enrollment_count=0
    mysql_csr.execute(''' select a.id,a.email as "new_email",a.username,i.email as "old_email" from iitbxblended.SIP_iitbx_auth_user i ,edxapp.auth_user a where a.username=i.username and i.email != a.email''')
    auth_users=mysql_csr.fetchall()
    for auth_user in auth_users:
       try:
           iitbx_auth_user_obj=iitbx_auth_user.objects.get(edxuserid=auth_user[0],username=auth_user[2],email=auth_user[3])
           iitbx_auth_user_obj.email=auth_user[1]
           enrollment_count=enrollment_count+1
           iitbx_auth_user_obj.save()
       except Exception as e:
           print "No changes detected",str(e.message),e.__class__.__name__
    return enrollment_count

########################################## End Email Change ################################################
def main(argv):
    refreshDate=ObtainDate() 
    init()
    collection=mongo_openconnection()
    curtime = timezone.now()
    changed_emails_count=0
    collection_active_versions=collection[2]
    print "i am here"
    for courses_data in collection_active_versions.find({},{"_id":0, "course":1, "org":1,"run":1,"versions":1 }):
        print courses_data["course"],"courses"
        try:
          published_version=courses_data["versions"]["published-branch"]
        except :
          published_version=None
        print courses_data,published_version
        if published_version != None :
           print "no issue",courses_data["course"],courses_data["org"],courses_data["run"], published_version
           coursedata=get_course_detail(collection,courses_data["course"],courses_data["org"],courses_data["run"], published_version)
           print coursedata[0],coursedata[4],"ye haiiii"
           if coursedata[4]==0:
              print "open course"
              if coursedata[3].blended_mode==1:
                  get_student_course_enrollment(coursedata[0])
                  print coursedata[3].courseid,"course_idddddd"
              course_modules(collection,coursedata)
              print_courseware(coursedata[3])
    try:
        refresh=Lookup.objects.get(category='RefreshDate',code=1)
        refresh.description=refreshDate
        refresh.save()
    except:
        None  
    iitbxactivity()
    changed_emails_count=email_change()   
    print "The number of email ids changed ",changed_emails_count
    generate_emails(refreshDate,curtime)

if __name__ == "__main__":
    main(sys.argv[1:])


#end main

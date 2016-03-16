'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from managerapp.models import *
from iitbx.models import *
from SIP.validations import *
from SIP.globalss import *
import MySQLdb
import random
from datetime import date,timedelta
from SIP.models import *
from SIP.views import *
import collections
import csv
######################### Begin of  iitbxsessiondata module      ################################################################
def iitbxsessiondata(request):
       args = {}
       args.update(csrf(request))
       try:
          person=Personinformation.objects.get(email=request.session['email_id'])
          args['person']=person
       except Exception as e:
          args['error_message'] = getErrorContent("unique_person")
          args['error_message'] = "\n Error " + str(e.message) + str(type(e))
          return render(request,error_,args)
       args['email_id']= request.session['email_id']
       args['institute']=institute=T10KT_Institute.objects.get(instituteid=person.instituteid_id)
       request.session['institute_id']=institute.instituteid
       args['institutename']=institute.institutename
       args['firstname']=person.firstname
       args['lastname']=person.lastname
       request.session['lastname']=person.lastname
       request.session['institutename']=institute.institutename
       request.session['firstname']=person.firstname
       request.session['role_id'] =0
       request.session['rolename']="Super User"
       args['role_id'] =0
       args['rolename']="Super User"
       args['email']=request.session['email_id']
       request.session['rcid']=T10KT_Approvedinstitute.objects.get(instituteid__instituteid=0).remotecenterid.remotecenterid
       args['rcid']= request.session['rcid']  
       args['rooturl']=ROOT_URL
       args['refreshdate']=refreshdate=Lookup.updatedate()
   
       return args 
######################### End of iitbxsessiondata module         #################################################################




def home(request,bflag):
    
    currentcourselist=[]
    archivecourselist=[]
    args=iitbxsessiondata(request)    
    person=Personinformation.objects.get(email=args['email']) 
    request.session['pid']=person.id
    args['pid']=person.id
    faculty=1
    sevenenddate=timezone.now()-timezone.timedelta(days=7)
    request.session['faculty']=faculty
    if  (int(bflag) == 0) or (int(bflag) == 1):   
        currentedxcourse=edxcourses.objects.filter(blended_mode=int(bflag),courseend__gte=sevenenddate).order_by("-courseend")
        archiveedxcourse=edxcourses.objects.filter(blended_mode=int(bflag),courseend__lt=sevenenddate).order_by("-courseend")
        #courselist=edxcourses.objects.filter(blended_mode=int(bflag)).order_by("-courseend")
    else:
           args['error_message'] = "You  have access wrong page."
           return render(request,error_,args)

    for c in currentedxcourse:
         currentcourselist.append([str(c.courseid),str(c.coursename),str(c.coursestart.date().strftime("%d-%m-%Y")),str(c.courseend.date().strftime("%d-%m-%Y"))])
    for c in archiveedxcourse:
         archivecourselist.append([str(c.courseid),str(c.coursename),str(c.coursestart.date().strftime("%d-%m-%Y")),str(c.courseend.date().strftime("%d-%m-%Y"))])
    args['currentcourselist']=currentcourselist
    args['archivedcourselist']=archivecourselist
    args['bflag']=bflag  
    #print course
    request.session['courselist_flag']=0
    return render_to_response('iitbx/home.html',args)


def coursedesc(request,courseid,pid):
     args={}
     args['institutename']=request.session['org']
     args['courseid']=courseid
     course=edxcourses.objects.get(courseid=courseid).course
     args['course']=course
     args['email']=request.user
     args['pid']=pid
     return render_to_response('iitbx/teacherhome.html',args)

def studentdetails(request,courseid,pid):
      email=request.user
      args={}
      student_list=AuthUser.objects.raw('''select "1" id ,au.email email,au.username username from student_courseenrollment sce , auth_user au where sce.course_id=%s and sce.user_id not in (select user_id from student_courseaccessrole scr where course_id =%s) and sce.user_id =au.id''',[courseid,courseid])
      #student_list=mysql_csr.fetchall()
      student_detail=[]
      args['email']=request.user
      args['institutename']=request.session['org']
      course=edxcourses.objects.get(courseid=courseid).course
      args['course']=course
      for i in student_list:
           student_detail.append([i.email,i.username])
      args['studentdetail']=student_detail
      return render_to_response('iitbx/participantdetails.html',args)

def coursedetails(request,courseid,pid):
    args=iitbxsessiondata(request)
    course=edxcourses.objects.get(courseid=courseid)
    args['coursenm']=course.coursename
    args['course']=course.course
    args['coursestart']=course.coursestart.date()
    args['courseend']=course.courseend.date()
    args['enrollstart']=course.enrollstart.date()
    args['enrollend']=course.enrollend.date()
    policy=[["Assignment","Total","Mandatory","Weight(%)","Comments"]]
    criteria=[["Grade","Min %","Max %"]]
    evaluate=[["Assignment","Assignment Type","Due Date"]]
    try:
        grpolicy=gradepolicy.objects.filter(courseid__courseid=courseid)
        for gp in grpolicy:
            if gp.drop_count==0:
                policy.append([gp.type+' ('+ gp.short_label +')',gp.min_count,gp.min_count-gp.drop_count,(gp.weight *100),""])
            else:
                 if gp.weight == 0.0:
                     continue
                 else:
                     policy.append([gp.type+' ('+ gp.short_label +')',gp.min_count,gp.min_count-gp.drop_count,(gp.weight * 100),"Best of "+str((gp.min_count-gp.drop_count))])
        grcriteria=gradescriteria.objects.filter(courseid__courseid=courseid).values('cutoffs','grade').order_by('cutoffs').reverse().distinct()
        l=len(grcriteria)
        for  gc in range(0,len(grcriteria)):
             # print grcriteria,gc
              if gc==0:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs']*100,100])
              else:
                 criteria.append([grcriteria[gc]['grade'],grcriteria[gc]['cutoffs']*100,grcriteria[gc-1]['cutoffs']*100])
        evaluat=gen_evaluations.objects.filter(course__courseid=courseid).values('sectionid','sec_name','type','due_date').order_by('sectionid').distinct()
        for eva in evaluat:
            evaluate.append([eva['sec_name'],eva['type'],eva['due_date']])

    except Exception as e:
           args['error_message'] ="my name is khan"
           return render(request,error_,args)

    args['evaluate']=evaluate
    args['criteria']=criteria
    args['policy']=policy
    args['id'] = pid
    return render_to_response('iitbx/coursedetails.html',args)

##################### Begin of evaluation module   ####################################################################################
def genevaluation(request,courseid,pid,evalflag):
    args =iitbxsessiondata(request)    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid       
       args['selectedinstitute']="IITBombay"       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

    person=Personinformation.objects.get(id=pid)    
    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    evaluation_obj=gen_evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,"iitbx/genevaluation.html",args)

def genquizdata(request,courseid,pid):    
    args =iitbxsessiondata(request)    
    header=[]
    try:
       secid=request.POST['quiz']
       evalu=gen_evaluations.objects.filter(sectionid=secid).values('sec_name').distinct()
       args['secname']=evalu[0]['sec_name']
    except Exception as e:
           return genevaluation(request,courseid,pid,1)
     
    args['selectedinstitute']="IITBombay"         
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
       person=Personinformation.objects.get(id=pid)
       args['teacher']= str(person.firstname)+' '+str(person.lastname)
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    
    try:
      head_str=gen_headings.objects.get(section=secid).heading
      heading=map(str,head_str.split(","))      
    except Exception as e:
      print str(e.message),str(type(e))
    
    ques_dict={}
    stud_rec=[]
    try:
      marks=AuthUser.objects.raw('''SELECT  "1" id,e.edxuserid "edxuserid" ,a.username "username",a.email "email",e.section "section",e.eval "eval",e.total "total" FROM   iitbxblended.iitbx_gen_markstable  e, edxapp.auth_user a where e.edxuserid=a.id and e.section=%s''',[secid]) 
      NAList=[]
      for i in marks: 
                marks=(i.eval).split(",")
                stud_rec.append([i.edxuserid,i.username,i.email,i.total,marks])        

      stud_obj=  StudentCourseenrollment.objects.filter(course_id=courseid)

    except Exception as e:
           print "Error Ocurred",str(e.message),str(type(e))

    request.session['genevaluation_heading']= heading       
    request.session['genheading']= heading           	 	
    args['headings']=heading              
    request.session['gen_stud_rec']= stud_rec          
    args['stud_rec']=stud_rec
    return render(request,"iitbx/genquizdata.html",args)
  
def downloadgenquizcsv(request,courseid,pid):
    args =iitbxsessiondata(request)    
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    person=Personinformation.objects.get(id=pid)
    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    result=request.session['gen_stud_rec']    
    name=  "genquizreport"+"_"+str(courseobj.id)+"_"+str(pid)+"_"+currenttime+'.csv'
    response = HttpResponse(content_type='text/csv')    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    heading=request.session['genevaluation_heading']
    heading = [h.replace('<br>', '\n') for h in heading]     
    
    writer.writerow(heading)
    for data in result:
                count=0
                createrow=[]
                for row in data:
                    count=count+1
                    if count==5:
                       for r in row:                            
                           createrow.append(r)                       
                    else:
                         createrow.append(row)
                writer.writerow(createrow)
    return response



##################### End of evaluation module     ####################################################################################



##################### Begin of general evaluation Status  module ########################################################################
def genevalstatus(request,courseid,pid,evalflag):
    args =iitbxsessiondata(request)
    
    try:
       print courseid
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['selectedinstitute']="IITBombay"
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    args['personid']=request.session['person_id']
    person=Personinformation.objects.get(id=pid)
    args['teacher']= str(person.firstname)+' '+str(person.lastname)  
  
    evaluation_obj=gen_evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')

    if evalflag==1:
        args['error_message'] = "Please select any quiz"
    
    args['evaluation']=evaluation_obj
    print evaluation_obj
    return render(request,'iitbx/genevalstatus.html',args)

def genstudentstatus(request,courseid,pid,report):
    if request.POST:
           if request.POST['status']=="Select":
              return genevalstatus(request,courseid,pid,1)
           request.session['secid']=request.POST['status']
    args =iitbxsessiondata(request)
    args.update(csrf(request))
    header=[]

    try:
        
        args['selectedinstitute']="IITBombayX"
        heading=['UserId','Username','Email']
        
        person=Personinformation.objects.get(id=pid)
        args['teacher']= str(person.firstname)+' '+str(person.lastname)
    except Exception as e:
           args['error_message'] ="You are not valid Teacher for the course ",courseid
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    try:
            secid=request.session['secid']
            marks_obj=[]            
            NA_stud_rec=[]; PA_stud_rec=[]; AA_stud_rec=[]
            NA_count=0; PA_count=0; AA_count=0
            marks=AuthUser.objects.raw('''SELECT  "1" id,e.edxuserid "edxuserid" ,a.username "username",a.email "email",e.section "section",e.eval "eval",e.total "total" FROM   iitbxblended.iitbx_gen_markstable  e, edxapp.auth_user a where e.edxuserid=a.id and e.section=%s''',[secid]) # objects.filter(section=secid,edxuserid)
            NAList=[]
            for i in marks: 
                evallist=(i.eval).split(",") 
                PAbool=any(data != "NA" for data in evallist)                
                if "NA" in i.eval and PAbool:                         
                   PA_count=PA_count+1
                   PA_stud_rec.append([i.edxuserid,i.username,i.email])         
                
                else:                  
                   AA_count=AA_count+1
                   AA_stud_rec.append([i.edxuserid,i.username,i.email])
                NAList.append(i.edxuserid)
            stud_obj= list( StudentCourseenrollment.objects.filter(course_id=courseid).exclude(user__id__in=NAList).values_list('user__id','user__username','user__email'))
                  
    except Exception as e:
           print e
           return genevalstatus(request,courseid,pid,1)
    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)    
    args['secname']=gen_evaluations.objects.filter(sectionid=secid)[0].sec_name
    ques_dict={}
       
    args['NA_count']= len(stud_obj); args['PA_count']= PA_count ; args['AA_count']= AA_count

    if int(report) == 0:
         return render(request,'iitbx/genstudentstatus.html',args) 
    elif int(report) == 5:
          args['stud_rec']= stud_obj          
    elif int(report) == 6:          
          args['stud_rec']= PA_stud_rec           
    else:
          args['stud_rec']= AA_stud_rec 

    args['filename']='tmp/'+downloadstatucsv(request,courseid,pid,report,args['stud_rec'])    
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    request.session['stud_rec']=args['stud_rec']           
    args['heading']= heading
    command = "python "+full_path+"/manage.py collectstatic  --noinput"
    subprocess.call(command, shell=True)
    return render(request,'iitbx/genstudentstatus.html',args)
  

def downloadstatucsv(request,courseid,pid,report,stud_rec):
    args =iitbxsessiondata(request)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    
    if int(report) == 5:
       realname= "student_notattempted_"+str(courseobj.id)+"_"+str(pid)+'.csv'
       
    elif int(report) == 6:
       realname= "student_attemptsomeques_"+str(courseobj.id)+"_"+str(pid)+'.csv'
    else:
       realname= "student_attemptall_"+str(courseobj.id)+"_"+str(pid)+'.csv'
    name=os.path.join(full_path,'static/tmp/',realname)
    print name
    with open(name,"wb") as downloadfile:
         writer=csv.writer(downloadfile,delimiter=',')
         heading=['UserId','Username','Email']
         writer.writerow(heading)
         for row in  stud_rec:
             writer.writerow(row)
    
    return realname

##################### End of evaluation Status module    ####################################################################


#################################### Start of grades Report ############################################################################
def gengrades_report(request,courseid,pid):
    faculty=request.session['faculty']
    args =iitbxsessiondata(request)
    
    try:
        course = edxcourses.objects.get(courseid = courseid).course
    except Exception as e:
        print "ERROR occured",str(e.message),str(type(e))  
        return [-1,-1]

    header=[] 
    try:        
       header=gen_headings.objects.get(section=course).heading      
    except Exception as e:
       print "Header does not exists",str(e.message),str(type(e))

    header_data=map(str,header.split(","))
    try:      
         if int(pid) == -1:
           args['teacher']="All Teachers"
         else:
           person=Personinformation.objects.get(id=pid)
           args['teacher']= str(person.firstname)+' '+str(person.lastname)          
    except Exception as e:
        print "Error occured",str(e.message),str(type(e))

    student_record=[]   
    gradestable_obj=AuthUser.objects.raw('''SELECT  "1" id,e.edxuserid "edxuserid" ,a.username "username",a.email "email",e.eval "eval" ,e.grade FROM   iitbxblended.iitbx_gen_gradestable  e, edxapp.auth_user a where e.edxuserid=a.id and e.course=%s order by e.edxuserid ''',[course])
    for i in gradestable_obj:               
                marks=(i.eval).split(",")
                grade=i.grade
                student_record.append([str(i.edxuserid),str(i.username),str(i.email),grade,marks])
   
    request.session['grade_heading']= header_data  
    args['headings']=header_data             
    request.session['student_record']= student_record         
    args['student_record']=student_record
    args['course']=course
    args['pid']=pid
    return render(request,"iitbx/gencourse_grades.html",args) 

# end grades_report
#################################### End of grades Report ############################################################################

##################################### Beginning of download grade Report #############################################################

def downloadgengradecsv(request,courseid,pid):
    args =iitbxsessiondata(request)
    
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
       courseobj = edxcourses.objects.get(course = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseobj.courseid
       args['pid']=pid
      
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)
    args['teacher']= str(args['firstname'])+' '+str(args['lastname'])
    header_data = request.session['grade_heading'] 
    header = [h.replace('<br>', '\n') for h in header_data]
    result=request.session['student_record']
   
    name=  "grade"+"_"+str(courseobj.id)+"_"+str(pid)+"_"+currenttime+'.csv'
    response = HttpResponse(content_type='text/csv')
    
    response['Content-Disposition'] = 'attachment; filename=" %s"'%(name)
    context=RequestContext(request)
    writer = csv.writer(response)
    
    
    if int(pid)==-1:
       count=0
       teacherheader=[]
       for i in header:
           count = count +1
           if count == 2:
              teacherheader.append("Teacher")
              teacherheader.append(i)
           else:
               teacherheader.append(i)
       writer.writerow(teacherheader)
       for j in result:
        count=0
        list1 =[]
        for data in j:            
            count = count +1
            if count==6:                
                for row in data:
                    list1.append(row)                
            else:                
                list1.append(data)
                
        writer.writerow(list1)  
    else:
      writer.writerow(header)
      for j in result:
        count=0
        list1 =[]
        for data in j:            
            count = count +1
            if count==5:                
                for row in data:
                    list1.append(row)                
            else:                
                list1.append(data)
                
        writer.writerow(list1)   
    return response
##################### End of download grade report ####################################################################################
############################################### Begin of  student Profile #############################################################
def studentprofile(request,courseid):
    args =iitbxsessiondata(request)
    args['courseid']=courseid
    
    email=request.user
    profilelist=[]
    edxcourse=edxcourses.objects.get(courseid=courseid)
    args['coursenumber']=edxcourse.course
    args['coursename']=edxcourse.coursename
    args['coursestartdate']=edxcourse.coursestart
    args['courseenddate']=edxcourse.courseend
    sqla='''SELECT "" id, PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM max(modified) ),
EXTRACT(YEAR_MONTH FROM date_format('2015-01-26', "%%Y%%m%%d"))) AS months, date(max(modified)) "maxdate"
from courseware_studentmodule;'''
    mi=AuthUser.objects.raw(sqla)
    for i in mi:
        as_on_date=i.maxdate
   
    profiledata=AuthUser.objects.raw('''select distinct "1" id,a.id "userid",a.username "username",c.name "name",a.email "email",c.year_of_birth "yob",
case c.gender when'm'then"Male"  when 'f' then "Female"  when 'o' then "Other"else "" END
"Gender" ,case c.level_of_education  when 'p' then "Doctorate"  when 'm' then "Masters"
when 'b' then "Bachelors"  when  'hs' then "School" else "" END "Level_of_Education"
,c.mailing_address,c.goals, d.name "state",e.name "city",f.pincode,f.aadhar_id
,if(role is null,"Student","Staff") Role
from auth_user a,  student_courseenrollment b ,  auth_userprofile c,
student_mooc_state d,  student_mooc_city e, student_mooc_person f  left outer join student_courseaccessrole g on g.user_id=f.user_id
and g.course_id =%s
where b.user_id = a.id  and b.course_id= %s  and a.is_staff = 0   and b.is_active=1
and c.user_id=a.id   and f.user_id=a.id   and f.state_id=d.id   and f.city_id=e.id 
order by a.id''',[courseid,courseid])
    for i in profiledata:
        profilelist.append([i.userid,i.username,i.name,i.email,i.yob,i.Gender,i.Level_of_Education,i.state,i.city,i.pincode,i.aadhar_id,i.mailing_address,i.goals,i.Role])
    args['profilelist']=profilelist
    #args['iterator']=iterator
    args['as_on_date']=as_on_date
    return render(request,"iitbx/genstudentprofile.html",args)


############################################### End of  student Profile #############################################################
############################################### Begin of  PostalInfo #############################################################

def postalinfo(request):
    args =iitbxsessiondata(request)
  
    sqla='''SELECT "1" id , pincode, Rural,Section, Head,Type FROM postalinfo '''
    postallist=Personinformation.objects.raw(sqla)
    
    args['postallist']=postallist
    args['postallistlen']=len(list(postallist))
    return render(request,"iitbx/postalinfo.html",args)


############################################### End of  PostalInfo  #############################################################
  



def systemreports(request,courseid):
     args=sessiondata(request)
     args['courseid']=courseid
     course=edxcourses.objects.get(courseid=courseid).course
     args['course']=course
     
     return render_to_response('iitbx/systemreports.html',args)

##################################################################################################                   
###########################################Assignment summary module ###########################################
def assignmentevaluation(request,courseid,pid,evalflag):
    args =iitbxsessiondata(request)    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid       
       args['selectedinstitute']="IITBombay"       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

    person=Personinformation.objects.get(id=pid) 

    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('id','sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    args['evalflag']=evalflag
    args['evaluation']=evaluation_obj
    return render(request,"iitbx/assignmentevaluation.html",args)


def assignmentsummary(request,courseid,pid):
    #args =iitbxsessiondata(request) 
    #print "hello , I am here" 
    coursename =edxcourses.objects.get(courseid=courseid).coursename
    atotoal=0   
    args =sessiondata(request)
    args.update(csrf(request))
    args['coursename']= coursename
    report=[]
    report1=[]
    notsubmitted=""
    ctotal=""
    viewed=""
    notviewed=""    
    #total=0
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       totalstudent=CoursewareStudentmodule.objects.filter(course_id=courseid).values('student__id').distinct().count()
       print totalstudent          
       questionid=request.POST['quiz']
       print "que", questionid  
       sectionname=evaluations.objects.get(id=questionid).sec_name
       currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
       report_name="Assignment Summary report of"+"_"+str(courseid)+" _ "+str(sectionname)+"_"+currenttime 
       #print sectionname
       #print questionid  
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid 
       args['sectionname']=sectionname      
       args['selectedinstitute']="IITBombay"       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

    person=Personinformation.objects.get(id=pid) 
    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    assignmentsummaryreport=Courselevelusers.objects.raw('''SELECT a.id id,count(*) total,qid,q_name,q_weight,sum(if(grade=0 and b.grade is not null,1,0)) incorrect,
sum(if(grade/max_grade=1 and b.grade is not null,1,0)) correct
,sum(if(grade/max_grade<1 and grade>0 and b.grade is not null,1,0)) partially_correct,sum(if(grade is null and state not like '%%"student_answers"%%',1,0)) "seenbutnotanswered",
sum(if(grade is null and state like '%%"student_answers": {}%%',1,0)) as "savedbutnotanswered",
sum(if(grade is null and state not like '%%"student_answers": {}%%' and state like '%%"student_answers": {%%',1,0)) "savedbutanswered"
FROM iitbxblended.SIP_questions a, edxapp.courseware_studentmodule b 
where eval_id=%s 
and b.module_id=a.qid
group by qid,q_name,q_weight
order by a.id''',[questionid])
    
    for assignment in assignmentsummaryreport:
       #print assignment.qid
       ctotal=assignment.correct+assignment.incorrect+assignment.partially_correct 
       #ltotal=assignment.savedbutanswered+assignment.savedbutnotanswered  
       notsubmitted=assignment.total-ctotal
       viewed=assignment.total-ctotal
       notviewed=notsubmitted-viewed
       atotal =assignment.total
       report.append([str(assignment.q_name),str(assignment.q_weight),str(assignment.total),str(ctotal),str(assignment.correct),str (assignment.incorrect),str(assignment.partially_correct),str(notsubmitted),str(viewed), str(notviewed),str(assignment.savedbutanswered),str(assignment.savedbutnotanswered),str(assignment.seenbutnotanswered),str(assignment.id)])
       persubmitted=round(float((ctotal/assignment.total)*100),2)
       #print "persubmitted", persubmitted
       pernotsubmitted=round(float((notsubmitted/assignment.total)*100),2) 
       percorrect=round(float((assignment.correct/assignment.total)*100),2)
       perincorrect=round(float((assignment.incorrect/assignment.total)*100),2)
       perparcorrect=round(float((assignment.partially_correct/assignment.total)*100),2)
       perviewed=round(float((viewed/assignment.total)*100),2)
       pernotviewed=round(float((notviewed/assignment.total)*100),2)
       persbanswered=round(float((assignment.savedbutanswered/assignment.total)*100),2)
       persbnanswered=round(float((assignment.savedbutnotanswered/assignment.total)*100),2)
       perseenbnanswered=round(float((assignment.seenbutnotanswered/assignment.total)*100),2)
        
       report1.append([str(assignment.q_name),str(assignment.q_weight),str(assignment.total),persubmitted,pernotsubmitted,percorrect,perincorrect,perparcorrect,perviewed,pernotviewed,
persbanswered,persbnanswered,perseenbnanswered,assignment.id])
    args["atotal"]=atotal
    args["report"]=report 
    args["report1"]=report1  
    args["report_name"]=report_name
    args["totalstudent"]=totalstudent
    args["notsubmitted"]=notsubmitted    
    return render(request,"iitbx/assignmentsummary.html",args)
def assignmentanswers(request,courseid,aid,pid,score):
    #print "hello",aid 
    coursename =edxcourses.objects.get(courseid=courseid).coursename
    args =sessiondata(request)
    args.update(csrf(request))
    args['aid']=aid 
    moduleid=questions.objects.get(id=int(aid)).qid
    print 'module', moduleid
    args['courseid']=courseid
    args['pid']=pid
    problemname=questions.objects.filter(id=int(aid)).distinct()
    args['problem']= problemname[0].q_name
    args['sectionname']=problemname[0].eval.sec_name
    args['coursename']= coursename
    courseobj = edxcourses.objects.get(courseid = courseid)
    args['course']=courseobj.course
    args['selectedinstitute']="IITBombay"
    person=Personinformation.objects.get(id=pid) 
    args['teacher']= str(person.firstname)+' '+str(person.lastname)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    report_name="Assignment Answers of"+"_"+str(problemname[0].q_name)+" _ "+str(problemname[0].eval.sec_name)+"_"+currenttime   
    report=[]
    report1=[]
    report2=[]  
    submitted=int(float(score))
    #print submitted
    test=""
    check=""
    assignmentchoicereport=AuthUser.objects.raw('''SELECT "1" id, if(instr(t1,'[')=1,"MO",if(instr(t1,'"choice_')=1,"MCQ","Others")) t1type,  substring(concat(if(t1 like '%%_0%%',",0","") ,if(t1 like '%%_1%%',",1",""),if(t1 like '%%_2%%',",2",""),if(t1 like '%%_3%%',",3",""),if(t1 like '%%_4%%',",4",""),if(t1 like '%%_5%%',",5","")),2) t1correct,if(instr(t2,'[')=1,"MO",if(instr(t2,'"choice_')=1,"MCQ","Others")) t2type,  substring(concat(if(t2 like '%%_0%%',",0","") ,if(t2 like '%%_1%%',",1",""),if(t2 like '%%_2%%',",2",""),if(t2 like '%%_3%%',",3",""),if(t2 like '%%_4%%',",4",""),if(t2 like '%%_5%%',",5","")),2) t2correct,if(instr(t3,'[')=1,"MO",if(instr(t3,'"choice_')=1,"MCQ","Others")) t3type,  substring(concat(if(t3 like '%%_0%%',",0","") ,if(t3 like '%%_1%%',",1",""),if(t3 like '%%_2%%',",2",""),if(t3 like '%%_3%%',",3",""),if(t3 like '%%_4%%',",4",""),if(t3 like '%%_5%%',",5","")),2) t3correct,if(instr(t4,'[')=1,"MO",if(instr(t4,'"choice_')=1,"MCQ","Others")) t4type,  substring(concat(if(t4 like '%%_0%%',",0","") ,if(t4 like '%%_1%%',",1",""),if(t4 like '%%_2%%',",2",""),if(t4 like '%%_3%%',",3",""),if(t4 like '%%_4%%',",4",""),if(t4 like '%%_5%%',",5","")),2) t4correct,if(instr(t5,'[')=1,"MO",if(instr(t5,'"choice_')=1,"MCQ","Others")) t5type,  substring(concat(if(t5 like '%%_0%%',",0","") ,if(t5 like '%%_1%%',",1",""),if(t5 like '%%_2%%',",2",""),if(t5 like '%%_3%%',",3",""),if(t5 like '%%_4%%',",4",""),if(t5 like '%%_5%%',",5","")),2) t5correct,if(instr(t6,'[')=1,"MO",if(instr(t6,'"choice_')=1,"MCQ","Others")) t6type,  substring(concat(if(t6 like '%%_0%%',",0","") ,if(t6 like '%%_1%%',",1",""),if(t6 like '%%_2%%',",2",""),if(t6 like '%%_3%%',",3",""),if(t6 like '%%_4%%',",4",""),if(t6 like '%%_5%%',",5","")),2) t6correct,if(instr(t7,'[')=1,"MO",if(instr(t7,'"choice_')=1,"MCQ","Others")) t7type,  substring(concat(if(t7 like '%%_0%%',",0","") ,if(t7 like '%%_1%%',",1",""),if(t7 like '%%_2%%',",2",""),if(t7 like '%%_3%%',",3",""),if(t7 like '%%_4%%',",4",""),if(t7 like '%%_5%%',",5","")),2) t7correct,if(instr(t8,'[')=1,"MO",if(instr(t8,'"choice_')=1,"MCQ","Others")) t8type,  substring(concat(if(t8 like '%%_0%%',",0","") ,if(t8 like '%%_1%%',",1",""),if(t8 like '%%_2%%',",2",""),if(t8 like '%%_3%%',",3",""),if(t8 like '%%_4%%',",4",""),if(t8 like '%%_5%%',",5","")),2) t8correct,if(instr(t9,'[')=1,"MO",if(instr(t9,'"choice_')=1,"MCQ","Others")) t9type,  substring(concat(if(t9 like '%%_0%%',",0","") ,if(t9 like '%%_1%%',",1",""),if(t9 like '%%_2%%',",2",""),if(t9 like '%%_3%%',",3",""),if(t9 like '%%_4%%',",4",""),if(t9 like '%%_5%%',",5","")),2) t9correct,if(instr(t10,'[')=1,"MO",if(instr(t10,'"choice_')=1,"MCQ","Others")) t10type,  substring(concat(if(t10 like '%%_0%%',",0","") ,if(t10 like '%%_1%%',",1",""),if(t10 like '%%_2%%',",2",""),if(t10 like '%%_3%%',",3",""),if(t10 like '%%_4%%',",4",""),if(t10 like '%%_5%%',",5","")),2) t10correct
from (SELECT "1" id,if(ans1 LIKE '["choi%%%%',concat(substring_index(ans1,']',1),']'),if( ans1 like '"choi%%%%',concat(substring_index(ans1,'"',2),'"'),'')) t1
,if(ans2 LIKE '["choi%%%%',concat(substring_index(ans2,']',1),']'),if( ans2 like '"choi%%%%',concat(substring_index(ans2,'"',2),'"'),'')) t2
,if(ans3 LIKE '["choi%%%%',concat(substring_index(ans3,']',1),']'),if( ans3 like '"choi%%%%',concat(substring_index(ans3,'"',2),'"'),'')) t3
,if(ans4 LIKE '["choi%%%%',concat(substring_index(ans4,']',1),']'),if( ans4 like '"choi%%%%',concat(substring_index(ans4,'"',2),'"'),'')) t4
,if(ans5 LIKE '["choi%%%%',concat(substring_index(ans5,']',1),']'),if( ans5 like '"choi%%%%',concat(substring_index(ans5,'"',2),'"'),'')) t5
,if(ans6 LIKE '["choi%%%%',concat(substring_index(ans6,']',1),']'),if( ans6 like '"choi%%%%',concat(substring_index(ans6,'"',2),'"'),'')) t6
,if(ans7 LIKE '["choi%%%%',concat(substring_index(ans7,']',1),']'),if( ans7 like '"choi%%%%',concat(substring_index(ans7,'"',2),'"'),'')) t7
,if(ans8 LIKE '["choi%%%%',concat(substring_index(ans8,']',1),']'),if( ans8 like '"choi%%%%',concat(substring_index(ans8,'"',2),'"'),'')) t8
,if(ans9 LIKE '["choi%%%%',concat(substring_index(ans9,']',1),']'),if( ans9 like '"choi%%%%',concat(substring_index(ans9,'"',2),'"'),'')) t9
,if(ans10 LIKE '["choi%%%%',concat(substring_index(ans10,']',1),']'),if( ans10 like '"choi%%%%',concat(substring_index(ans10,'"',2),'"'),'')) t10
FROM (SELECT module_id, student_id,substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_4_1": ') ,-1),'}}',1),'", "i4x',1)  ans3,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_5_1": ') ,-1),'}}',1),'", "i4x',1)  ans4,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_6_1": ') ,-1),'}}',1),'", "i4x',1)  ans5,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_7_1": ') ,-1),'}}',1),'", "i4x',1)  ans6,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_8_1": ') ,-1),'}}',1),'", "i4x',1)  ans7,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_9_1": ') ,-1),'}}',1),'", "i4x',1)  ans8,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_10_1": ') ,-1),'}}',1),'", "i4x',1)  ans9,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_11_1": ') ,-1),'}}',1),'", "i4x',1)  ans10  
 FROM edxapp.courseware_studentmodule where module_type='problem' and module_id= %s and course_id=%s and grade is not null and instr(state,'"done": true')!=0  and grade=max_grade) a  limit 1) X''',[moduleid,courseid]) 
    for assignment in assignmentchoicereport:
        report1=[str(assignment.t1type),str(assignment.t2type),str(assignment.t3type),str(assignment.t4type),str(assignment.t5type),
str(assignment.t6type),str(assignment.t7type),str(assignment.t8type),str(assignment.t9type),str(assignment.t10type),
(assignment.t1correct),(assignment.t2correct),(assignment.t3correct),(assignment.t4correct),(assignment.t5correct),(assignment.t6correct),(assignment.t7correct),(assignment.t8correct),(assignment.t9correct),(assignment.t10correct)]
        if assignment.t1type == 'Others' and assignment.t2type == 'Others' and assignment.t3type == 'Others' and assignment.t4type == 'Others' and assignment.t5type == 'Others' and assignment.t6type == 'Others' and assignment.t7type == 'Others' and assignment.t8type == 'Others' and assignment.t9type == 'Others' and assignment.t10type == 'Others': 
            test=0
        else:
            test=1
    
    assignmentanswerreport=Courselevelusers.objects.raw('''SELECT "1" id, sum(if(instr(t1,"choice_0")=0,0,1))  "A1",sum(if(instr(t1,"choice_1")=0,0,1))  "B1",sum(if(instr(t1,"choice_2")=0,0,1))  "C1", sum(if(instr(t1,"choice_3")=0,0,1))  "D1",sum(if(instr(t1,"choice_4")=0,0,1))  "E1",sum(if(instr(t2,"choice_0")=0,0,1))  "A2",sum(if(instr(t2,"choice_1")=0,0,1))  "B2",sum(if(instr(t2,"choice_2")=0,0,1))  "C2", sum(if(instr(t2,"choice_3")=0,0,1))  "D2",sum(if(instr(t2,"choice_4")=0,0,1))  "E2",sum(if(instr(t3,"choice_0")=0,0,1))  "A3",sum(if(instr(t3,"choice_1")=0,0,1))  "B3",sum(if(instr(t3,"choice_2")=0,0,1))  "C3", sum(if(instr(t3,"choice_3")=0,0,1))  "D3",sum(if(instr(t3,"choice_4")=0,0,1))  "E3",sum(if(instr(t4,"choice_0")=0,0,1))  "A4",sum(if(instr(t4,"choice_1")=0,0,1))  "B4",sum(if(instr(t4,"choice_2")=0,0,1))  "C4", sum(if(instr(t4,"choice_3")=0,0,1))  "D4",sum(if(instr(t4,"choice_4")=0,0,1))  "E4",sum(if(instr(t5,"choice_0")=0,0,1))  "A5",sum(if(instr(t5,"choice_1")=0,0,1))  "B5",sum(if(instr(t5,"choice_2")=0,0,1))  "C5", sum(if(instr(t5,"choice_3")=0,0,1))  "D5",sum(if(instr(t5,"choice_4")=0,0,1))  "E5",sum(if(instr(t6,"choice_0")=0,0,1))  "A6",sum(if(instr(t6,"choice_1")=0,0,1))  "B6",sum(if(instr(t6,"choice_2")=0,0,1))  "C6", sum(if(instr(t6,"choice_3")=0,0,1))  "D6", if(instr(t6,"choice_4")=0,0,1)  "E6",sum(if(instr(t7,"choice_0")=0,0,1))  "A7",sum(if(instr(t7,"choice_1")=0,0,1))  "B7",sum(if(instr(t7,"choice_2")=0,0,1))  "C7", sum(if(instr(t7,"choice_3")=0,0,1))  "D7", if(instr(t7,"choice_4")=0,0,1)  "E7",sum(if(instr(t8,"choice_0")=0,0,1))  "A8",sum(if(instr(t8,"choice_1")=0,0,1))  "B8",sum(if(instr(t8,"choice_2")=0,0,1))  "C8", sum(if(instr(t8,"choice_3")=0,0,1))  "D8", if(instr(t8,"choice_4")=0,0,1)  "E8",sum(if(instr(t9,"choice_0")=0,0,1))  "A9",sum(if(instr(t9,"choice_1")=0,0,1))  "B9",sum(if(instr(t9,"choice_2")=0,0,1))  "C9", sum(if(instr(t9,"choice_3")=0,0,1))  "D9", if(instr(t9,"choice_4")=0,0,1)  "E9",sum(if(instr(t10,"choice_0")=0,0,1))  "A10",sum(if(instr(t10,"choice_1")=0,0,1))  "B10",sum(if(instr(t10,"choice_2")=0,0,1))  "C10", sum(if(instr(t10,"choice_3")=0,0,1))  "D10", if(instr(t10,"choice_4")=0,0,1)  "E10"
FROM
(SELECT module_id,student_id,if(ans1 LIKE '["choi%%%%',concat(substring_index(ans1,']',1),']'),if( ans1 like '"choi%%%%',concat(substring_index(ans1,'"',2),'"'),'')) t1
,if(ans2 LIKE '["choi%%%%',concat(substring_index(ans2,']',1),']'),if( ans2 like '"choi%%%%',concat(substring_index(ans2,'"',2),'"'),'')) t2
,if(ans3 LIKE '["choi%%%%',concat(substring_index(ans3,']',1),']'),if( ans3 like '"choi%%%%',concat(substring_index(ans3,'"',2),'"'),'')) t3
,if(ans4 LIKE '["choi%%%%',concat(substring_index(ans4,']',1),']'),if( ans4 like '"choi%%%%',concat(substring_index(ans4,'"',2),'"'),'')) t4
,if(ans5 LIKE '["choi%%%%',concat(substring_index(ans5,']',1),']'),if( ans5 like '"choi%%%%',concat(substring_index(ans5,'"',2),'"'),'')) t5
,if(ans6 LIKE '["choi%%%%',concat(substring_index(ans6,']',1),']'),if( ans6 like '"choi%%%%',concat(substring_index(ans6,'"',2),'"'),'')) t6
,if(ans7 LIKE '["choi%%%%',concat(substring_index(ans7,']',1),']'),if( ans7 like '"choi%%%%',concat(substring_index(ans7,'"',2),'"'),'')) t7
,if(ans8 LIKE '["choi%%%%',concat(substring_index(ans8,']',1),']'),if( ans8 like '"choi%%%%',concat(substring_index(ans8,'"',2),'"'),'')) t8
,if(ans9 LIKE '["choi%%%%',concat(substring_index(ans9,']',1),']'),if( ans9 like '"choi%%%%',concat(substring_index(ans9,'"',2),'"'),'')) t9
,if(ans10 LIKE '["choi%%%%',concat(substring_index(ans10,']',1),']'),if( ans10 like '"choi%%%%',concat(substring_index(ans10,'"',2),'"'),'')) t10

FROM (SELECT module_id, student_id,substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_4_1": ') ,-1),'}}',1),'", "i4x',1)  ans3,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_5_1": ') ,-1),'}}',1),'", "i4x',1)  ans4,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_6_1": ') ,-1),'}}',1),'", "i4x',1)  ans5,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_7_1": ') ,-1),'}}',1),'", "i4x',1)  ans6,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_8_1": ') ,-1),'}}',1),'", "i4x',1)  ans7,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_9_1": ') ,-1),'}}',1),'", "i4x',1)  ans8,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_10_1": ') ,-1),'}}',1),'", "i4x',1)  ans9,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_11_1": ') ,-1),'}}',1),'", "i4x',1)  ans10  
 FROM edxapp.courseware_studentmodule where module_type='problem' and module_id =%s and course_id=%s and grade is not null and instr(state,'"done": true')!=0 ) a) X''',[moduleid,courseid])
    for assignment in assignmentanswerreport:
        report=[[str(assignment.A1),str(assignment.B1),str(assignment.C1),str(assignment.D1),str(assignment.E1)],
        [str(assignment.A2),str(assignment.B2),str(assignment.C2),str(assignment.D2),str(assignment.E2)],
        [str(assignment.A3),str(assignment.B3),str(assignment.C3),str(assignment.D3),str(assignment.E3)],
        [str(assignment.A4),str(assignment.B4),str(assignment.C4),str(assignment.D4),str(assignment.E4)],
        [str(assignment.A5),str(assignment.B5),str(assignment.C5),str(assignment.D5),str(assignment.E5)],
        [str(assignment.A6),str(assignment.B6),str(assignment.C6),str(assignment.D6),str(assignment.E6)],
        [str(assignment.A7),str(assignment.B7),str(assignment.C7),str(assignment.D7),str(assignment.E7)],
        [str(assignment.A8),str(assignment.B8),str(assignment.C8),str(assignment.D8),str(assignment.E8)],
        [str(assignment.A9),str(assignment.B9),str(assignment.C9),str(assignment.D9),str(assignment.E9)],
        [str(assignment.A10),str(assignment.B10),str(assignment.C10),str(assignment.D10),str(assignment.E10)]]     
        if submitted!=0:    
           report2=[[round(float((assignment.A1/submitted)*100),2),round(float((assignment.B1/submitted)*100),2),round(float((assignment.C1/submitted)*100),2),round(float((assignment.D1/submitted)*100),2),round(float((assignment.E1/submitted)*100),2)],
        [round(float((assignment.A2/submitted)*100),2),round(float((assignment.B2/submitted)*100),2),round(float((assignment.C2/submitted)*100),2),round(float((assignment.D2/submitted)*100),2),round(float((assignment.E2/submitted)*100),2)],
        [round(float((assignment.A3/submitted)*100),2),round(float((assignment.B3/submitted)*100),2),round(float((assignment.C3/submitted)*100),2),round(float((assignment.D3/submitted)*100),2),round(float((assignment.E3/submitted)*100),2)],
        [round(float((assignment.A4/submitted)*100),2),round(float((assignment.B4/submitted)*100),2),round(float((assignment.C4/submitted)*100),2),round(float((assignment.D4/submitted)*100),2),round(float((assignment.E4/submitted)*100),2)],
        [round(float((assignment.A5/submitted)*100),2),round(float((assignment.B5/submitted)*100),2),round(float((assignment.C5/submitted)*100),2),round(float((assignment.D5/submitted)*100),2),round(float((assignment.E5/submitted)*100),2)],
        [round(float((assignment.A6/submitted)*100),2),round(float((assignment.B6/submitted)*100),2),round(float((assignment.C6/submitted)*100),2),round(float((assignment.D6/submitted)*100),2),round(float((assignment.E6/submitted)*100),2)],
        [round(float((assignment.A7/submitted)*100),2),round(float((assignment.B7/submitted)*100),2),round(float((assignment.C7/submitted)*100),2),round(float((assignment.D7/submitted)*100),2),round(float((assignment.E7/submitted)*100),2)],
        [round(float((assignment.A8/submitted)*100),2),round(float((assignment.B8/submitted)*100),2),round(float((assignment.C8/
submitted)*100),2),round(float((assignment.D8/submitted)*100),2),round(float((assignment.E8/submitted)*100),2)],
        [round(float((assignment.A9/submitted)*100),2),round(float((assignment.B9/submitted)*100),2),round(float((assignment.C9/submitted)*100),2),round(float((assignment.D9/submitted)*100),2),round(float((assignment.E9/submitted)*100),2)],
        [round(float((assignment.A10/submitted)*100),2),round(float((assignment.B10/submitted)*100),2),round(float((assignment.C10/submitted)*100),2),round(float((assignment.D10/submitted)*100),2),round(float((assignment.E10/submitted)*100),2)]]
             
        
    rc=0
    rc1=0
     
    answers=[]
    answersper=[] 
    args["check"] = check; 
    ch=''
    ch1=''  
    r=0
    h=0
    r1=0
    h1=0
    moflag=0
    if submitted!=0:
       for i in report:
           option=[]
           #for j in report1[rc]:
           if int(i[4])!=0:
              h=1
           try:
              t=report1[rc+10]#fetch option for row count in report1
              ch=report1[r]
              a=t.split(',')
              for x in a:
                 if not x:
                    option.append(-1)
                 else:
                    if i[int(x)] in i:
                   #print i,"value",i[int(x)]
                        option.append(i[int(x)])
           except:
              option=[]
          
           if ch != 'Others':
              answers.append([i,option,ch])#creating list of options and correct option
           else:
              answers.append([i,option])
           rc=rc+1
           r= r+1
    else:
        answers=[]
     
    h1=0
    r1=0
    for i in report2:
        option1=[]
        if float(i[4])!=0.0:
            h1=1
          
        try:
          t1=report1[rc1+10]#fetch option for row count in report1
          ch1=report1[r1]
          a1=t1.split(',')
          for x in a1:
             if not x:
                option1.append(-1)
             else:
                if i[int(x)] in i:
                   #print i,"value",i[int(x)]
                   option1.append(i[int(x)])
        except:
            option1=[]
        #print report1,"heyd",a,"rc",rc
        #print i,i[int(t)-1]
        if ch1 != 'Others':
            answersper.append([i,option1,ch1])#creating list of options and correct option
        else:
            answersper.append([i,option1])
        rc1=rc1+1
        r1= r1+1
    #print "answers " ,answersper

    args["flag"]=h
    args["flag1"]=h1
    #print "h1", h 
    #print "h",h
    args["test"] = test;
    args["report"]=answers
    args["report1"]=report1  
    args["report2"]=answersper
    args["report_name"]=report_name
     
    return render(request,"iitbx/assignmentanswers.html",args)


def problemwisedata(request):

    quizid=request.GET['id']
    #print "qz", quizid
    problems=[]
    
    args ={}
    problemdata=questions.objects.filter(eval= int(quizid))
    
    for i in problemdata:
         problems.append([i.id,i.q_name]) 
    output=problems 
    
    #data = serializers.serialize('json',problemsdata)
   
    return HttpResponse(json.dumps(output), content_type="application/json")
def problemwiseevaluation(request,courseid,pid,evalflag):
    args =iitbxsessiondata(request)    
    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid       
       args['selectedinstitute']="IITBombay"       
       args['pid']=pid
    except Exception as e:
           args['error_message'] = getErrorContent("no_IITBombayX_course")
           args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           return render(request,error_,args)

    person=Personinformation.objects.get(id=pid) 

    args['teacher']= str(person.firstname)+' '+str(person.lastname)    
    args['personid']=request.session['person_id']
    evaluation_obj=evaluations.objects.filter(course=courseobj,release_date__lte=current).values('id','sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    args['evalflag']=evalflag
    args['evaluation']=evaluation_obj
    return render(request,"iitbx/problemwiseevaluation.html",args)

def problemwisedetails(request,courseid,pid):
    args =iitbxsessiondata(request) 
    problemid=request.POST['Problem']
    coursename =edxcourses.objects.get(courseid=courseid).coursename 
    moduleid=questions.objects.get(id=int(problemid)).qid
    report=[]
    report1=[]
    print "mid" ,moduleid
    args['courseid']=courseid
    args['pid']=pid
    problemname=questions.objects.filter(id=int(problemid)).distinct()
    args['problem']= problemname[0].q_name
    args['sectionname']=problemname[0].eval.sec_name
    args['coursename']= coursename
    courseobj = edxcourses.objects.get(courseid = courseid)
    args['course']=courseobj.course
    args['selectedinstitute']="IITBombay"
    print "problem name", problemname[0].q_name, " " ,problemname[0].eval.sec_name
    person=Personinformation.objects.get(id=pid) 
    args['teacher']= str(person.firstname)+' '+str(person.lastname)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    report_name="Assignment Answers of"+"_"+str(problemname[0].q_name)+" _ "+str(problemname[0].eval.sec_name)+"_"+currenttime  
 
    assignmentchoicereport=AuthUser.objects.raw('''SELECT "1" id, if(instr(t1,'[')=1,"MO",if(instr(t1,'"choice_')=1,"MCQ","Others")) t1type,  substring(concat(if(t1 like '%%_0%%',",0","") ,if(t1 like '%%_1%%',",1",""),if(t1 like '%%_2%%',",2",""),if(t1 like '%%_3%%',",3",""),if(t1 like '%%_4%%',",4",""),if(t1 like '%%_5%%',",5","")),2) t1correct,if(instr(t2,'[')=1,"MO",if(instr(t2,'"choice_')=1,"MCQ","Others")) t2type,  substring(concat(if(t2 like '%%_0%%',",0","") ,if(t2 like '%%_1%%',",1",""),if(t2 like '%%_2%%',",2",""),if(t2 like '%%_3%%',",3",""),if(t2 like '%%_4%%',",4",""),if(t2 like '%%_5%%',",5","")),2) t2correct,if(instr(t3,'[')=1,"MO",if(instr(t3,'"choice_')=1,"MCQ","Others")) t3type,  substring(concat(if(t3 like '%%_0%%',",0","") ,if(t3 like '%%_1%%',",1",""),if(t3 like '%%_2%%',",2",""),if(t3 like '%%_3%%',",3",""),if(t3 like '%%_4%%',",4",""),if(t3 like '%%_5%%',",5","")),2) t3correct,if(instr(t4,'[')=1,"MO",if(instr(t4,'"choice_')=1,"MCQ","Others")) t4type,  substring(concat(if(t4 like '%%_0%%',",0","") ,if(t4 like '%%_1%%',",1",""),if(t4 like '%%_2%%',",2",""),if(t4 like '%%_3%%',",3",""),if(t4 like '%%_4%%',",4",""),if(t4 like '%%_5%%',",5","")),2) t4correct,if(instr(t5,'[')=1,"MO",if(instr(t5,'"choice_')=1,"MCQ","Others")) t5type,  substring(concat(if(t5 like '%%_0%%',",0","") ,if(t5 like '%%_1%%',",1",""),if(t5 like '%%_2%%',",2",""),if(t5 like '%%_3%%',",3",""),if(t5 like '%%_4%%',",4",""),if(t5 like '%%_5%%',",5","")),2) t5correct,if(instr(t6,'[')=1,"MO",if(instr(t6,'"choice_')=1,"MCQ","Others")) t6type,  substring(concat(if(t6 like '%%_0%%',",0","") ,if(t6 like '%%_1%%',",1",""),if(t6 like '%%_2%%',",2",""),if(t6 like '%%_3%%',",3",""),if(t6 like '%%_4%%',",4",""),if(t6 like '%%_5%%',",5","")),2) t6correct,if(instr(t7,'[')=1,"MO",if(instr(t7,'"choice_')=1,"MCQ","Others")) t7type,  substring(concat(if(t7 like '%%_0%%',",0","") ,if(t7 like '%%_1%%',",1",""),if(t7 like '%%_2%%',",2",""),if(t7 like '%%_3%%',",3",""),if(t7 like '%%_4%%',",4",""),if(t7 like '%%_5%%',",5","")),2) t7correct,if(instr(t8,'[')=1,"MO",if(instr(t8,'"choice_')=1,"MCQ","Others")) t8type,  substring(concat(if(t8 like '%%_0%%',",0","") ,if(t8 like '%%_1%%',",1",""),if(t8 like '%%_2%%',",2",""),if(t8 like '%%_3%%',",3",""),if(t8 like '%%_4%%',",4",""),if(t8 like '%%_5%%',",5","")),2) t8correct,if(instr(t9,'[')=1,"MO",if(instr(t9,'"choice_')=1,"MCQ","Others")) t9type,  substring(concat(if(t9 like '%%_0%%',",0","") ,if(t9 like '%%_1%%',",1",""),if(t9 like '%%_2%%',",2",""),if(t9 like '%%_3%%',",3",""),if(t9 like '%%_4%%',",4",""),if(t9 like '%%_5%%',",5","")),2) t9correct,if(instr(t10,'[')=1,"MO",if(instr(t10,'"choice_')=1,"MCQ","Others")) t10type,  substring(concat(if(t10 like '%%_0%%',",0","") ,if(t10 like '%%_1%%',",1",""),if(t10 like '%%_2%%',",2",""),if(t10 like '%%_3%%',",3",""),if(t10 like '%%_4%%',",4",""),if(t10 like '%%_5%%',",5","")),2) t10correct
from (SELECT "1" id,if(ans1 LIKE '["choi%%%%',concat(substring_index(ans1,']',1),']'),if( ans1 like '"choi%%%%',concat(substring_index(ans1,'"',2),'"'),'')) t1
,if(ans2 LIKE '["choi%%%%',concat(substring_index(ans2,']',1),']'),if( ans2 like '"choi%%%%',concat(substring_index(ans2,'"',2),'"'),'')) t2
,if(ans3 LIKE '["choi%%%%',concat(substring_index(ans3,']',1),']'),if( ans3 like '"choi%%%%',concat(substring_index(ans3,'"',2),'"'),'')) t3
,if(ans4 LIKE '["choi%%%%',concat(substring_index(ans4,']',1),']'),if( ans4 like '"choi%%%%',concat(substring_index(ans4,'"',2),'"'),'')) t4
,if(ans5 LIKE '["choi%%%%',concat(substring_index(ans5,']',1),']'),if( ans5 like '"choi%%%%',concat(substring_index(ans5,'"',2),'"'),'')) t5
,if(ans6 LIKE '["choi%%%%',concat(substring_index(ans6,']',1),']'),if( ans6 like '"choi%%%%',concat(substring_index(ans6,'"',2),'"'),'')) t6
,if(ans7 LIKE '["choi%%%%',concat(substring_index(ans7,']',1),']'),if( ans7 like '"choi%%%%',concat(substring_index(ans7,'"',2),'"'),'')) t7
,if(ans8 LIKE '["choi%%%%',concat(substring_index(ans8,']',1),']'),if( ans8 like '"choi%%%%',concat(substring_index(ans8,'"',2),'"'),'')) t8
,if(ans9 LIKE '["choi%%%%',concat(substring_index(ans9,']',1),']'),if( ans9 like '"choi%%%%',concat(substring_index(ans9,'"',2),'"'),'')) t9
,if(ans10 LIKE '["choi%%%%',concat(substring_index(ans10,']',1),']'),if( ans10 like '"choi%%%%',concat(substring_index(ans10,'"',2),'"'),'')) t10
FROM (SELECT module_id, student_id,substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_4_1": ') ,-1),'}}',1),'", "i4x',1)  ans3,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_5_1": ') ,-1),'}}',1),'", "i4x',1)  ans4,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_6_1": ') ,-1),'}}',1),'", "i4x',1)  ans5,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_7_1": ') ,-1),'}}',1),'", "i4x',1)  ans6,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_8_1": ') ,-1),'}}',1),'", "i4x',1)  ans7,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_9_1": ') ,-1),'}}',1),'", "i4x',1)  ans8,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_10_1": ') ,-1),'}}',1),'", "i4x',1)  ans9,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_11_1": ') ,-1),'}}',1),'", "i4x',1)  ans10  
 FROM edxapp.courseware_studentmodule where module_type='problem' and module_id= %s and course_id=%s and grade is not null and instr(state,'"done": true')!=0  and grade=max_grade) a  limit 1) X''',[moduleid,courseid]) 

    for assignment in assignmentchoicereport:
        #print str(assignment.t1type),str(assignment.t2type),str(assignment.t3type),str(assignment.t4type),str(assignment.t5type),str(assignment.t6type),str(assignment.t7type),str(assignment.t8type),str(assignment.t9type),str(assignment.t10type),str(assignment.t1correct),str(assignment.t2correct),str(assignment.t3correct),str(assignment.t4correct),str(assignment.t5correct),(assignment.t6correct),str(assignment.t7correct),str(assignment.t8correct),str(assignment.t9correct),str(assignment.t10correct)
        
        report1=[str(assignment.t1type),str(assignment.t2type),str(assignment.t3type),str(assignment.t4type),str(assignment.t5type),
str(assignment.t6type),str(assignment.t7type),str(assignment.t8type),str(assignment.t9type),str(assignment.t10type),
(assignment.t1correct),(assignment.t2correct),(assignment.t3correct),(assignment.t4correct),(assignment.t5correct),(assignment.t6correct),(assignment.t7correct),(assignment.t8correct),(assignment.t9correct),(assignment.t10correct)]

        if assignment.t1type == 'Others' and assignment.t2type == 'Others' and assignment.t3type == 'Others' and assignment.t4type == 'Others' and assignment.t5type == 'Others' and assignment.t6type == 'Others' and assignment.t7type == 'Others' and assignment.t8type == 'Others' and assignment.t9type == 'Others' and assignment.t10type == 'Others': 
            test=0
        else:
            test=1
    assignmentanswerreport=Courselevelusers.objects.raw('''SELECT "1" id, sum(if(instr(t1,"choice_0")=0,0,1))  "A1",sum(if(instr(t1,"choice_1")=0,0,1))  "B1",sum(if(instr(t1,"choice_2")=0,0,1))  "C1", sum(if(instr(t1,"choice_3")=0,0,1))  "D1", sum(if(instr(t1,"choice_4")=0,0,1))  "E1",sum(if(instr(t2,"choice_0")=0,0,1))  "A2",sum(if(instr(t2,"choice_1")=0,0,1))  "B2",sum(if(instr(t2,"choice_2")=0,0,1))  "C2",sum(if(instr(t2,"choice_3")=0,0,1))  "D2",sum(if(instr(t2,"choice_4")=0,0,1))  "E2",sum(if(instr(t3,"choice_0")=0,0,1))  "A3",sum(if(instr(t3,"choice_1")=0,0,1))  "B3",sum(if(instr(t3,"choice_2")=0,0,1))  "C3", sum(if(instr(t3,"choice_3")=0,0,1))  "D3",sum(if(instr(t3,"choice_4")=0,0,1))  "E3",sum(if(instr(t4,"choice_0")=0,0,1))  "A4",sum(if(instr(t4,"choice_1")=0,0,1))  "B4",sum(if(instr(t4,"choice_2")=0,0,1))  "C4", sum(if(instr(t4,"choice_3")=0,0,1))  "D4",sum(if(instr(t4,"choice_4")=0,0,1))  "E4",sum(if(instr(t5,"choice_0")=0,0,1))  "A5",sum(if(instr(t5,"choice_1")=0,0,1))  "B5",sum(if(instr(t5,"choice_2")=0,0,1))  "C5",sum(if(instr(t5,"choice_3")=0,0,1))  "D5",sum(if(instr(t5,"choice_4")=0,0,1))  "E5",sum(if(instr(t6,"choice_0")=0,0,1))  "A6",sum(if(instr(t6,"choice_1")=0,0,1))  "B6",sum(if(instr(t6,"choice_2")=0,0,1))  "C6", sum(if(instr(t6,"choice_3")=0,0,1))  "D6",sum(if(instr(t6,"choice_4")=0,0,1))  "E6",sum(if(instr(t7,"choice_0")=0,0,1))  "A7",sum(if(instr(t7,"choice_1")=0,0,1))  "B7",sum(if(instr(t7,"choice_2")=0,0,1))  "C7", sum(if(instr(t7,"choice_3")=0,0,1))  "D7",sum(if(instr(t7,"choice_4")=0,0,1))  "E7",sum(if(instr(t8,"choice_0")=0,0,1))  "A8",sum(if(instr(t8,"choice_1")=0,0,1))  "B8",sum(if(instr(t8,"choice_2")=0,0,1))  "C8",sum(if(instr(t8,"choice_3")=0,0,1))  "D8",sum(if(instr(t8,"choice_4")=0,0,1))  "E8",sum(if(instr(t9,"choice_0")=0,0,1))  "A9",sum(if(instr(t9,"choice_1")=0,0,1))  "B9",sum(if(instr(t9,"choice_2")=0,0,1))  "C9", sum(if(instr(t9,"choice_3")=0,0,1))  "D9", sum(if(instr(t9,"choice_4")=0,0,1))  "E9",sum(if(instr(t10,"choice_0")=0,0,1))  "A10",sum(if(instr(t10,"choice_1")=0,0,1))  "B10",sum(if(instr(t10,"choice_2")=0,0,1))  "C10", sum(if(instr(t10,"choice_3")=0,0,1))  "D10", sum(if(instr(t10,"choice_4")=0,0,1))  "E10"
FROM
(SELECT module_id,student_id,if(ans1 LIKE '["choi%%%%',concat(substring_index(ans1,']',1),']'),if( ans1 like '"choi%%%%',concat(substring_index(ans1,'"',2),'"'),'')) t1
,if(ans2 LIKE '["choi%%%%',concat(substring_index(ans2,']',1),']'),if( ans2 like '"choi%%%%',concat(substring_index(ans2,'"',2),'"'),'')) t2
,if(ans3 LIKE '["choi%%%%',concat(substring_index(ans3,']',1),']'),if( ans3 like '"choi%%%%',concat(substring_index(ans3,'"',2),'"'),'')) t3
,if(ans4 LIKE '["choi%%%%',concat(substring_index(ans4,']',1),']'),if( ans4 like '"choi%%%%',concat(substring_index(ans4,'"',2),'"'),'')) t4
,if(ans5 LIKE '["choi%%%%',concat(substring_index(ans5,']',1),']'),if( ans5 like '"choi%%%%',concat(substring_index(ans5,'"',2),'"'),'')) t5
,if(ans6 LIKE '["choi%%%%',concat(substring_index(ans6,']',1),']'),if( ans6 like '"choi%%%%',concat(substring_index(ans6,'"',2),'"'),'')) t6
,if(ans7 LIKE '["choi%%%%',concat(substring_index(ans7,']',1),']'),if( ans7 like '"choi%%%%',concat(substring_index(ans7,'"',2),'"'),'')) t7
,if(ans8 LIKE '["choi%%%%',concat(substring_index(ans8,']',1),']'),if( ans8 like '"choi%%%%',concat(substring_index(ans8,'"',2),'"'),'')) t8
,if(ans9 LIKE '["choi%%%%',concat(substring_index(ans9,']',1),']'),if( ans9 like '"choi%%%%',concat(substring_index(ans9,'"',2),'"'),'')) t9
,if(ans10 LIKE '["choi%%%%',concat(substring_index(ans10,']',1),']'),if( ans10 like '"choi%%%%',concat(substring_index(ans10,'"',2),'"'),'')) t10

FROM (SELECT module_id, student_id,substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_4_1": ') ,-1),'}}',1),'", "i4x',1)  ans3,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_5_1": ') ,-1),'}}',1),'", "i4x',1)  ans4,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_6_1": ') ,-1),'}}',1),'", "i4x',1)  ans5,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_7_1": ') ,-1),'}}',1),'", "i4x',1)  ans6,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_8_1": ') ,-1),'}}',1),'", "i4x',1)  ans7,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_9_1": ') ,-1),'}}',1),'", "i4x',1)  ans8,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_10_1": ') ,-1),'}}',1),'", "i4x',1)  ans9,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_11_1": ') ,-1),'}}',1),'", "i4x',1)  ans10  
 FROM edxapp.courseware_studentmodule where module_type='problem' and module_id =%s and course_id=%s and grade is not null and instr(state,'"done": true')!=0 ) a) X''',[moduleid,courseid])

    for assignment in assignmentanswerreport:
        report=[[str(assignment.A1),str(assignment.B1),str(assignment.C1),str(assignment.D1),str(assignment.E1)],
        [str(assignment.A2),str(assignment.B2),str(assignment.C2),str(assignment.D2),str(assignment.E2)],
        [str(assignment.A3),str(assignment.B3),str(assignment.C3),str(assignment.D3),str(assignment.E3)],
        [str(assignment.A4),str(assignment.B4),str(assignment.C4),str(assignment.D4),str(assignment.E4)],
        [str(assignment.A5),str(assignment.B5),str(assignment.C5),str(assignment.D5),str(assignment.E5)],
        [str(assignment.A6),str(assignment.B6),str(assignment.C6),str(assignment.D6),str(assignment.E6)],
        [str(assignment.A7),str(assignment.B7),str(assignment.C7),str(assignment.D7),str(assignment.E7)],
        [str(assignment.A8),str(assignment.B8),str(assignment.C8),str(assignment.D8),str(assignment.E8)],
        [str(assignment.A9),str(assignment.B9),str(assignment.C9),str(assignment.D9),str(assignment.E9)],
        [str(assignment.A10),str(assignment.B10),str(assignment.C10),str(assignment.D10),str(assignment.E10)]]     
        
      
    rc=0
    answers=[]
     
    r=0
    h=0
    for i in report:
        option=[]
        if int(i[4])!= 0:
            h=1
        try:
          t=report1[rc+10]
          ch=report1[r]
          a=t.split(',')
          for x in a:
             if not x:
                option.append(-1)
             else:
                if i[int(x)] in i:
                   #print i,"value",i[int(x)]
                   option.append(i[int(x)])
        except:
            option=[]
        #print report1,"heyd",a,"rc",rc
        #print i,i[int(t)-1]
        if ch != 'Others':
            answers.append([i,option,ch])#creating list of options and correct option
        else:
            answers.append([i,option])
        rc=rc+1
        r= r+1
    #print "answers " ,answers
    args["report"]=answers
    args["flag"]=h
    args["report_name"]=report_name
    args["test"] = test;
    args["problemid"]=problemid
    return render(request,"iitbx/problemwisedetails.html",args)
def assignmentmultipleoptions(request,courseid,pid,aid,part):
    args=iitbxsessiondata(request) 
    coursename =edxcourses.objects.get(courseid=courseid).coursename
    args.update(csrf(request))
    moduleid=questions.objects.get(id=int(aid)).qid
    
    partid ='t'+part
    #print "part is" ,type(part)
    part=int(part)
    args['courseid']=courseid
    args['pid']=pid
    problemname=questions.objects.filter(id=int(aid)).distinct()
    args['problem']= problemname[0].q_name
    args['sectionname']=problemname[0].eval.sec_name
    args['coursename']= coursename
    courseobj = edxcourses.objects.get(courseid = courseid)
    args['course']=courseobj.course
    args['selectedinstitute']="IITBombay"
    person=Personinformation.objects.get(id=pid) 
    args['teacher']= str(person.firstname)+' '+str(person.lastname)
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    report_name="Assignment multiple options of"+"_"+str(problemname[0].q_name)+" _ "+str(problemname[0].eval.sec_name)+"_"+"Part _"+str(part)+" _"+currenttime   
    report=[]
    fla=0
    assignmentchoicereport=AuthUser.objects.raw('''SELECT "1" id, if(instr(t1,'[')=1,"MO",if(instr(t1,'"choice_')=1,"MCQ","Others")) t1type,  substring(concat(if(t1 like '%%_0%%',",A","") ,if(t1 like '%%_1%%',",B",""),if(t1 like '%%_2%%',",C",""),if(t1 like '%%_3%%',",D",""),if(t1 like '%%_4%%',",E",""),if(t1 like '%%_5%%',",F","")),2) t1correct,if(instr(t2,'[')=1,"MO",if(instr(t2,'"choice_')=1,"MCQ","Others")) t2type,  substring(concat(if(t2 like '%%_0%%',",A","") ,if(t2 like '%%_1%%',",B",""),if(t2 like '%%_2%%',",C",""),if(t2 like '%%_3%%',",D",""),if(t2 like '%%_4%%',",E",""),if(t2 like '%%_5%%',",F","")),2) t2correct,if(instr(t3,'[')=1,"MO",if(instr(t3,'"choice_')=1,"MCQ","Others")) t3type,  substring(concat(if(t3 like '%%_0%%',",A","") ,if(t3 like '%%_1%%',",B",""),if(t3 like '%%_2%%',",C",""),if(t3 like '%%_3%%',",D",""),if(t3 like '%%_4%%',",E",""),if(t3 like '%%_5%%',",F","")),2) t3correct,if(instr(t4,'[')=1,"MO",if(instr(t4,'"choice_')=1,"MCQ","Others")) t4type,  substring(concat(if(t4 like '%%_0%%',",A","") ,if(t4 like '%%_1%%',",B",""),if(t4 like '%%_2%%',",C",""),if(t4 like '%%_3%%',",D",""),if(t4 like '%%_4%%',",E",""),if(t4 like '%%_5%%',",","")),2) t4correct,if(instr(t5,'[')=1,"MO",if(instr(t5,'"choice_')=1,"MCQ","Others")) t5type,  substring(concat(if(t5 like '%%_0%%',",A","") ,if(t5 like '%%_1%%',",B",""),if(t5 like '%%_2%%',",C",""),if(t5 like '%%_3%%',",D",""),if(t5 like '%%_4%%',",E",""),if(t5 like '%%_5%%',",F","")),2) t5correct,if(instr(t6,'[')=1,"MO",if(instr(t6,'"choice_')=1,"MCQ","Others")) t6type,  substring(concat(if(t6 like '%%_0%%',",A","") ,if(t6 like '%%_1%%',",B",""),if(t6 like '%%_2%%',",C",""),if(t6 like '%%_3%%',",D",""),if(t6 like '%%_4%%',",E",""),if(t6 like '%%_5%%',",F","")),2) t6correct,if(instr(t7,'[')=1,"MO",if(instr(t7,'"choice_')=1,"MCQ","Others")) t7type,  substring(concat(if(t7 like '%%_0%%',",A","") ,if(t7 like '%%_1%%',",B",""),if(t7 like '%%_2%%',",C",""),if(t7 like '%%_3%%',",D",""),if(t7 like '%%_4%%',",E",""),if(t7 like '%%_5%%',",F","")),2) t7correct,if(instr(t8,'[')=1,"MO",if(instr(t8,'"choice_')=1,"MCQ","Others")) t8type,  substring(concat(if(t8 like '%%_0%%',",A","") ,if(t8 like '%%_1%%',",B",""),if(t8 like '%%_2%%',",C",""),if(t8 like '%%_3%%',",D",""),if(t8 like '%%_4%%',",E",""),if(t8 like '%%_5%%',",F","")),2) t8correct,if(instr(t9,'[')=1,"MO",if(instr(t9,'"choice_')=1,"MCQ","Others")) t9type,  substring(concat(if(t9 like '%%_0%%',",A","") ,if(t9 like '%%_1%%',",B",""),if(t9 like '%%_2%%',",C",""),if(t9 like '%%_3%%',",D",""),if(t9 like '%%_4%%',",E",""),if(t9 like '%%_5%%',",F","")),2) t9correct,if(instr(t10,'[')=1,"MO",if(instr(t10,'"choice_')=1,"MCQ","Others")) t10type,  substring(concat(if(t10 like '%%_0%%',",A","") ,if(t10 like '%%_1%%',",B",""),if(t10 like '%%_2%%',",C",""),if(t10 like '%%_3%%',",D",""),if(t10 like '%%_4%%',",E",""),if(t10 like '%%_5%%',",F","")),2) t10correct
from (SELECT "1" id,if(ans1 LIKE '["choi%%%%',concat(substring_index(ans1,']',1),']'),if( ans1 like '"choi%%%%',concat(substring_index(ans1,'"',2),'"'),'')) t1
,if(ans2 LIKE '["choi%%%%',concat(substring_index(ans2,']',1),']'),if( ans2 like '"choi%%%%',concat(substring_index(ans2,'"',2),'"'),'')) t2
,if(ans3 LIKE '["choi%%%%',concat(substring_index(ans3,']',1),']'),if( ans3 like '"choi%%%%',concat(substring_index(ans3,'"',2),'"'),'')) t3
,if(ans4 LIKE '["choi%%%%',concat(substring_index(ans4,']',1),']'),if( ans4 like '"choi%%%%',concat(substring_index(ans4,'"',2),'"'),'')) t4
,if(ans5 LIKE '["choi%%%%',concat(substring_index(ans5,']',1),']'),if( ans5 like '"choi%%%%',concat(substring_index(ans5,'"',2),'"'),'')) t5
,if(ans6 LIKE '["choi%%%%',concat(substring_index(ans6,']',1),']'),if( ans6 like '"choi%%%%',concat(substring_index(ans6,'"',2),'"'),'')) t6
,if(ans7 LIKE '["choi%%%%',concat(substring_index(ans7,']',1),']'),if( ans7 like '"choi%%%%',concat(substring_index(ans7,'"',2),'"'),'')) t7
,if(ans8 LIKE '["choi%%%%',concat(substring_index(ans8,']',1),']'),if( ans8 like '"choi%%%%',concat(substring_index(ans8,'"',2),'"'),'')) t8
,if(ans9 LIKE '["choi%%%%',concat(substring_index(ans9,']',1),']'),if( ans9 like '"choi%%%%',concat(substring_index(ans9,'"',2),'"'),'')) t9
,if(ans10 LIKE '["choi%%%%',concat(substring_index(ans10,']',1),']'),if( ans10 like '"choi%%%%',concat(substring_index(ans10,'"',2),'"'),'')) t10
FROM (SELECT module_id, student_id,substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_4_1": ') ,-1),'}}',1),'", "i4x',1)  ans3,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_5_1": ') ,-1),'}}',1),'", "i4x',1)  ans4,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_6_1": ') ,-1),'}}',1),'", "i4x',1)  ans5,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_7_1": ') ,-1),'}}',1),'", "i4x',1)  ans6,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_8_1": ') ,-1),'}}',1),'", "i4x',1)  ans7,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_9_1": ') ,-1),'}}',1),'", "i4x',1)  ans8,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_10_1": ') ,-1),'}}',1),'", "i4x',1)  ans9,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_11_1": ') ,-1),'}}',1),'", "i4x',1)  ans10  
 FROM edxapp.courseware_studentmodule where module_type='problem' and module_id= %s and course_id=%s and grade is not null and instr(state,'"done": true')!=0  and grade=max_grade) a  limit 1) X''',[moduleid,courseid]) 
    for assignment in assignmentchoicereport:
                
        report1=    [assignment.t1correct,assignment.t2correct,assignment.t3correct,assignment.t4correct,assignment.t5correct,assignment.t6correct,assignment.t7correct,assignment.t8correct,assignment.t9correct,assignment.t10correct]
        
          
    ans=str(report1[part-1])
    #print ans
    sqlq='''Select "1" id, count(student_id) as count ,%s as Choice from (SELECT student_id, if(ans1 LIKE '["choi%%%%',concat(substring_index(ans1,']',1),']'),if( ans1 like '"choi%%%%',concat(substring_index(ans1,'"',2),'"'),'')) t1
,if(ans2 LIKE '["choi%%%%',concat(substring_index(ans2,']',1),']'),if( ans2 like '"choi%%%%',concat(substring_index(ans2,'"',2),'"'),'')) t2
,if(ans3 LIKE '["choi%%%%',concat(substring_index(ans3,']',1),']'),if( ans3 like '"choi%%%%',concat(substring_index(ans3,'"',2),'"'),'')) t3
,if(ans4 LIKE '["choi%%%%',concat(substring_index(ans4,']',1),']'),if( ans4 like '"choi%%%%',concat(substring_index(ans4,'"',2),'"'),'')) t4
,if(ans5 LIKE '["choi%%%%',concat(substring_index(ans5,']',1),']'),if( ans5 like '"choi%%%%',concat(substring_index(ans5,'"',2),'"'),'')) t5
,if(ans6 LIKE '["choi%%%%',concat(substring_index(ans6,']',1),']'),if( ans6 like '"choi%%%%',concat(substring_index(ans6,'"',2),'"'),'')) t6
,if(ans7 LIKE '["choi%%%%',concat(substring_index(ans7,']',1),']'),if( ans7 like '"choi%%%%',concat(substring_index(ans7,'"',2),'"'),'')) t7
,if(ans8 LIKE '["choi%%%%',concat(substring_index(ans8,']',1),']'),if( ans8 like '"choi%%%%',concat(substring_index(ans8,'"',2),'"'),'')) t8
,if(ans9 LIKE '["choi%%%%',concat(substring_index(ans9,']',1),']'),if( ans9 like '"choi%%%%',concat(substring_index(ans9,'"',2),'"'),'')) t9
,if(ans10 LIKE '["choi%%%%',concat(substring_index(ans10,']',1),']'),if( ans10 like '"choi%%%%',concat(substring_index(ans10,'"',2),'"'),'')) t10
FROM (SELECT module_id, student_id,substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_2_1": ') ,-1),'}}',1),'", "i4x',1)  ans1,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_3_1": ') ,-1),'}}',1),'", "i4x',1)  ans2,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_4_1": ') ,-1),'}}',1),'", "i4x',1)  ans3,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_5_1": ') ,-1),'}}',1),'", "i4x',1)  ans4,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_6_1": ') ,-1),'}}',1),'", "i4x',1)  ans5,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_7_1": ') ,-1),'}}',1),'", "i4x',1)  ans6,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1), concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_8_1": ') ,-1),'}}',1),'", "i4x',1)  ans7,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_9_1": ') ,-1),'}}',1),'", "i4x',1)  ans8,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_10_1": ') ,-1),'}}',1),'", "i4x',1)  ans9,
 substring_index(substring_index(substring_index(substring_index(state,'"student_answers": {"',-1),
 concat(REPLACE(REPLACE(REPLACE(module_id,"/","-"),":--","-"),".","_"),'_11_1": ') ,-1),'}}',1),'", "i4x',1)  ans10  
 FROM edxapp.courseware_studentmodule where module_type='problem' and module_id='%s' and course_id='%s' and grade is not null and instr(state,'"done": true')!=0) a ) b group by %s order by length(%s), %s '''%(partid,moduleid,courseid,partid,partid,partid)
    
    assignmentanswerreport=Courselevelusers.objects.raw(sqlq)
    for assignment in assignmentanswerreport:
        choice = assignment.Choice
        #print choice  
        choice1=""
        if choice !="":
           choice1 = str(choice.replace('"choice_0"','A'))
           choice1 = str(choice1.replace('"choice_1"','B'))
           choice1 = str(choice1.replace('"choice_2"','C')) 
           choice1 = str(choice1.replace('"choice_3"','D'))
           choice1 = str(choice1.replace('"choice_4"','E'))
           
           choice1 = choice1[1:-1]
          
        tempa=choice1.translate(None,' ')
        if ans == tempa:
            fla=1
            report.append([assignment.count,choice1,fla])
        else:
            fla=0   
            report.append([assignment.count,choice1,fla]) 
         
               
        #print report
    #print fla  
    args["part"]=part
    args["fla"]=fla
    args["report"]=report
    args["report_name"]=report_name
    return render(request,"iitbx/assignmentmultipleoptions.html",args)
#######################################################Start of weekly course report ################################################

#######################################################Start of weekly course report ################################################

def weeklyreport(request,courseid):
    args=iitbxsessiondata(request)
    report=[]
    total=[]
    args['courseid']=courseid
    courseobj = edxcourses.objects.get(courseid = courseid)
    #print courseobj.coursestart.date().isocalendar()[0:1],"helllooooo"

    totalstud=AuthUser.objects.raw('''select "1" id,count(distinct `student_id`) stud from edxapp.courseware_studentmodule a where a.course_id=%s and created between date_format(%s,"%%y-%%m-%%d") and  date_format(%s,"%%y-%%m-%%d")''',[courseid,courseobj.coursestart.date(),courseobj.courseend.date()])
    
    weeklyreport=AuthUser.objects.raw('''SELECT "1" id,wedate, sum(video) Video,sum(problem) AnyProblem ,sum(gproblem) GradedProblem ,count(distinct student_id) "Users" FROM (SELECT distinct student_id, DATE_FORMAT(DATE_ADD(IFNULL(b.created,a.modified),INTERVAL(7-DAYOFWEEK(IFNULL(b.created,a.modified))) DAY),'%%Y-%%m-%%d') wedate,if(module_type='video',1,0) video, if(module_type='problem' and a.grade is null,1,0) problem, if(module_type='problem' and a.grade is not null ,1,0) gproblem from  `courseware_studentmodule`a  LEFT OUTER JOIN courseware_studentmodulehistory b  ON  b.student_module_id=a.id  where module_type in ('video','course','problem') and a.course_id= %s and IFNULL(b.created,a.modified) between %s and %s) A group by wedate''',[courseid,courseobj.coursestart.date(),courseobj.courseend.date()])

    for j in totalstud:
        args["stud"]=j.stud
   
    for i in weeklyreport:
          report.append([i.wedate,i.Video,i.AnyProblem,i.GradedProblem,i.Users])
    args["totalstud"]=totalstud
    args["report"]=report
    args['coursedisplayname']=courseobj.coursename
    args['coursestart']=courseobj.coursestart.date()
    args['courseend']=courseobj.courseend.date()
################## Below code is for graphics############################
    studlist=[]
    diststud=[]
    videodict = collections.OrderedDict()
    weekdict = collections.OrderedDict()
    pdict = collections.OrderedDict()
    gpdict = collections.OrderedDict()
    args['refreshdate']=refreshdate=Lookup.updatedate()

    totalstud=AuthUser.objects.raw('''select distinct `student_id` id from edxapp.courseware_studentmodule a where a.course_id=%s and created between date_format(%s,"%%y-%%m-%%d") and  date_format(%s,"%%y-%%m-%%d") order by id''',[courseid,courseobj.coursestart.date(),courseobj.courseend.date()])

    weeklyreport=AuthUser.objects.raw('''SELECT "1" id, student_id, week(DATE_FORMAT(DATE_ADD(IFNULL(b.created,a.modified),INTERVAL(7-DAYOFWEEK(IFNULL(b.created,a.modified))) DAY),'%%Y-%%m-%%d')) wedate,if(module_type='video',1,0) video, if(module_type='problem' and a.grade is null,1,0) problem, if(module_type='problem' and a.grade is not null ,1,0) gproblem from  `courseware_studentmodule`a  LEFT OUTER JOIN courseware_studentmodulehistory b  ON  b.student_module_id=a.id  where module_type in ('course','video','problem') and a.course_id= %s and IFNULL(b.created,a.modified) between %s and %s''',[courseid,courseobj.coursestart.date(),courseobj.courseend.date()])
    wstart=courseobj.coursestart.date().isocalendar()[1]
    ystart=courseobj.coursestart.date().isocalendar()[0]
    wend=courseobj.courseend.date().isocalendar()[1]
    yend=courseobj.courseend.date().isocalendar()[0]
    welist=[]
    i=wstart
    y=ystart
    while (i != wend or y != yend):
       welist.append(str(i)+"-"+str(y))
       i=(i+1)%52
       if i==1:
             y=y+1
       elif i==0:
             i=52
       #print i,y      
    welist.append(str(i)+"-"+str(y))
            
    #print wstart,wend, welist
    for i in totalstud:
        a=videodict.setdefault(int(i.id ),{})
        b=pdict.setdefault(int(i.id),{})
        c=gpdict.setdefault(int(i.id),{})
        for j in range(wstart,wend+1):
           a.setdefault(int(j),0)
           b.setdefault(int(j),0)
           c.setdefault(int(j),0)
    for l in weeklyreport:
         dt=int(l.wedate)
         st=int(l.student_id)
         if (l.video!=0) and dt >=wstart and dt <= wend :
             videodict[st][dt]=1
         if (l.problem!=0):
             pdict[st][dt]=1
         if (l.gproblem!=0):
             gpdict[st][dt]=1
    realnamev="activitycomparision"+"_"+"video"+"_"+str(courseobj.course)+"_"+str(refreshdate)+'.csv'
    full_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    name=os.path.join(full_path,'static/',realnamev)     
    with open(name,"wb") as downloadfile:   
         writer=csv.writer(downloadfile,delimiter=',')
         writer.writerow(["student_id"]+welist)
         for k,v in videodict.iteritems():
              s=[k]+v.values()
              writer.writerow(s)
    realnamep="activitycomparision"+"_"+"problem"+"_"+str(courseobj.course)+"_"+refreshdate+'.csv' 
    name=os.path.join(full_path,'static/',realnamep)         
    with open(name,"wb") as downloadfile:   
         writer=csv.writer(downloadfile,delimiter=',')
         writer.writerow(["student_id"]+welist)
         for k,v in pdict.iteritems():
              s=[int(k)]+v.values()
              writer.writerow(s) 
    realnameg="activitycomparision"+"_"+"gproblem"+"_"+str(courseobj.course)+"_"+refreshdate+'.csv' 
    name=os.path.join(full_path,'static/',realnameg)         
    with open(name,"wb") as downloadfile:   
         writer=csv.writer(downloadfile,delimiter=',')
         writer.writerow(["student_id"]+welist)
         for k,v in gpdict.iteritems():
              s=[int(k)]+v.values()
              writer.writerow(s) 
    args['realnamev']=realnamev
    args['realnamep']=realnamep
    args['realnameg']=realnameg

    return render_to_response('iitbx/weeklyreport.html',args)
########################################################################################################################################################################################################################################################################################

def courseenrollment(request):
    args={}
    args=iitbxsessiondata(request)
    enroll_detail=[]
    

    enrollment=AuthUser.objects.raw('''SELECT ""id, A.course_id course, B.coursename displaynm, Date(B.coursestart) startdt, Date(B.courseend) enddt, count(*) enrollment FROM edxapp.student_courseenrollment A,iitbxblended.SIP_edxcourses B WHERE A.course_id = B.courseid GROUP BY A.course_id order by B.courseend desc''')

    for i in enrollment:
        enroll_detail.append([i.course,i.displaynm,i.startdt,i.enddt,i.enrollment])

    args["enroll_detail"]=enroll_detail

    return render_to_response('iitbx/courseenrollment.html',args) 

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
       return args 
######################### End of iitbxsessiondata module         #################################################################




def home(request):
    
    course=[]
    args=iitbxsessiondata(request)    
    person=Personinformation.objects.get(email=args['email']) 
    request.session['pid']=person.id
    args['pid']=person.id
    faculty=1
    request.session['faculty']=faculty
           
    courselist=edxcourses.objects.filter(blended_mode=0)
    for c in courselist:
         course.append([str(c.courseid),str(c.coursename),str(c.coursestart.date().strftime("%d-%m-%Y")),str(c.courseend.date().strftime("%d-%m-%Y"))])
    args['courselist']=course  
    print course
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





def systemreports(request,courseid):
     args=sessiondata(request)
     args['courseid']=courseid
     course=edxcourses.objects.get(courseid=courseid).course
     args['course']=course
     
     return render_to_response('iitbx/systemreports.html',args)

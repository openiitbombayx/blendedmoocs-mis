from django.shortcuts import render
from SIP.views import *
from iitbx.models import *
from SIP.models import *
from .models import *
from datetime import datetime
from iitbx.views import *
def usersummary(request):
    args =iitbxsessiondata(request)
    email=request.user
    summary=AuthUser.objects.raw('''SELECT "1" id,count(*) Total,sum(Active) Active, sum(NotActive)  NotActive ,sum(Cur_Year) Cur_Year, sum(Cur_Month) Cur_Month ,sum(Cur_Quarter) Cur_Quarter ,sum(Cur_Week) Cur_Week ,sum(Yesterday) Yesterday,sum(Never) "NeverLogged", sum(LoggedIn) "LoggedIn",sum(ActiveCurYear) ActiveCurYear, sum(ActiveCurMonth) "ActiveCurMonth",sum(ActiveCurWeek) "ActiveCurWeek", sum(ActiveYesterday) "ActiveYesterday",sum(NoEnrollment) "NoEnrollment",
sum(SingleCourse) "SingleCourse",sum(MultipleCourse) "MultipleCourse"
FROM
(SELECT if(is_active=1,1,0) "Active"
      ,if(is_active=0,1,0) "NotActive"
      ,if(is_active=1 and YEAR(date_joined)=YEAR(current_date()),1,0) "Cur_Year"
      ,if(is_active=1 and YEAR(date_joined)=YEAR(current_date()) and QUARTER(date_joined)=QUARTER(current_date()),1,0) "Cur_Quarter"
      ,if(is_active=1 and YEAR(date_joined)=YEAR(current_date()) and MONTH(date_joined)=MONTH(current_date()),1,0) "Cur_Month"
,if(is_active=1 and YEAR(date_joined)=YEAR(current_date()) and WEEK(date_joined)=WEEK(current_date()),1,0) "Cur_Week"
,if(date_joined > current_date()-1,1,0) "Yesterday"
,if (is_active=1 and TotalEnrolled =0,1,0) "NoEnrollment"
,if (is_active=1 and TotalEnrolled =1,1,0) "SingleCourse"
,if (is_active=1 and TotalEnrolled >1,1,0) "MultipleCourse"
,if(last_login= date_joined and is_active=1,1,0) "Never",
if(last_login!= date_joined and is_active=1,1,0) "LoggedIn",
if(is_active=1 and last_login!= date_joined and year(last_login) = year( current_date()),1,0) "ActiveCurYear",
if(is_active=1 and last_login!= date_joined and date_format(last_login,'%%m-%%y') = date_format( current_date(),'%%m-%%y'),1,0) "ActiveCurMonth"
,if(is_active=1 and last_login!= date_joined and date_format(last_login,'%%m-%%y') = date_format( current_date(),'%%m-%%y') and week(last_login)=week(date_joined),1,0) "ActiveCurWeek" ,
 if(is_active=1 and last_login!= date_joined and date_format(last_login,'%%d-%%m-%%y') = date_format( current_date()-1,'%%d-%%m-%%y'),1,0) "ActiveYesterday"
FROM (SELECT username,email,date_joined,b.is_active,last_login,sum(if(course_id IS NULL,0,1)) "TotalEnrolled" FROM `student_courseenrollment` a RIGHT OUTER JOIN auth_user b ON b.id=a.user_id group by username,email,date_joined,b.is_active,last_login
) b)
a
''')

    damoyr=AuthUser.objects.raw('''SELECT "" id ,months,maxdate ,lastday,YEAR(lastday) year,date_format(lastday,'%%b-%%y') mname,YEAR(lastday) year,CONCAT(DATE_FORMAT( MAKEDATE(YEAR(lastday), 1) + INTERVAL QUARTER(lastday) QUARTER  - INTERVAL    1 QUARTER,"%%b")  ," to ",
  DATE_FORMAT(MAKEDATE(YEAR(lastday), 1) + INTERVAL QUARTER(lastday) QUARTER - INTERVAL 1 DAY ,"%%b-%%y")) "quartername",DATE_ADD(DATE_FORMAT(lastday,"%%Y-%%m-%%d"),interval -7 day ) week, week(lastday) weekno, month(lastday) monthno, quarter(lastday)  quarterno from
(SELECT  PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM max(modified) ),
EXTRACT(YEAR_MONTH FROM date_format( current_date(), "%%Y%%m%%d"))) AS months, date(max(modified)) "maxdate" ,date(max(modified)-1) "lastday"
from courseware_studentmodule ) d
''')

    for i in summary:
        args["total"]=i.Total
        args["active"]=i.Active
        args["notactive"]=i.NotActive
        args["Cur_Year"]=i.Cur_Year
        args["Cur_Month"]=i.Cur_Month
        args["Cur_Quarter"]=i.Cur_Quarter
        args["Cur_Week"]=i.Cur_Week
        args["Yesterday"]=i.Yesterday
        args["NeverLogged"]=i.NeverLogged
        args["LoggedIn"]=i.LoggedIn
        args["ActiveCurYear"]=i.ActiveCurYear
        args["ActiveCurMonth"]=i.ActiveCurMonth
        args["ActiveCurWeek"]=i.ActiveCurWeek
        args["SingleCourse"]=i.SingleCourse
        args["MultipleCourse"]=i.MultipleCourse
        args["ActiveYesterday"]=i.ActiveYesterday
        args["NoEnrollment"]=i.NoEnrollment
        args['email']=request.user
        #args['institutename']=request.session['org']
        args['institutename']=request.session['institutename']
        args['rcid']= request.session['rcid']

    for j in damoyr:
        args['months']=j.months
        args['maxdate']=j.maxdate
        args['lastday']=j.lastday
        args['mname']=j.mname
        args['quartername']=j.quartername
        args['weekno']=j.weekno
        args['year']=j.year
        args['monthno']=j.monthno
        args['quarterno']=j.quarterno
        

    return render_to_response('managerapp/home1.html',args)

def registrationsummary(request):
    args =iitbxsessiondata(request)
    regdata=[]
    email=request.user
    datejoin=AuthUser.objects.raw('''SELECT  "1" id,date_format(date_joined,'%%b-%%y')  doj,YEAR(date_joined) year  , count( * ) "Total"  FROM auth_user where is_active=1  GROUP BY DATE_FORMAT( date_joined, '%%m-%%Y' ) ORDER BY date_format(date_joined,'%%m-%%y')  DESC''')
    for j in datejoin:
         regdata.append([j.doj,j.year ,j.Total])
    args["regdata"]=regdata
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['email']=request.user
    return render_to_response('managerapp/registrationsummery.html',args) 

def userjoinedsummary(request):
    args={}
    userdata=[]
    email=request.user
    userjoin=AuthUser.objects.raw('''SELECT "1" id, DATE_FORMAT(date_joined, '%%d-%%m-%%Y') doj ,count(*) "Total" from auth_user where date_joined < current_date() -7 and is_active=1 group by DATE_FORMAT(date_joined, '%%d-%%m-%%Y') ''')
    for j in userjoin:
         userdata.append([j.doj ,j.Total])
    args["userdata"]=userdata
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['email']=request.user

def courseenrrollment(request,courseid):
    args =iitbxsessiondata(request)

    
    edxcourse_inst=edxcourses.objects.get(courseid=courseid)
    startdate=edxcourse_inst.coursestart
   
    enrolldata=AuthUser.objects.raw('''SELECT "1" id, sum(enroll) "enroll",sum(unenroll) "unenroll",sum(students) "totalstudent",sum(staff) "totalstaff",sum(afterstartenroll) "afterstartenroll",sum(beforestartenroll) "beforestartenroll",sum(afterstartunenroll) "afterstartunenroll",sum(beforestartunenroll) "beforestartunenroll" FROM (
SELECT if(A.is_active=1,1,0) "enroll",if(A.is_active=0,1,0) "unenroll", if(B.role is NULL and A.is_active=1,1,0) "students",if(B.role is not NULL and A.is_active=1,1,0) "staff",
if(A.created >DATE_FORMAT(%s,"%%Y-%%m-%%d")  and A.is_active=1,1,0)"afterstartenroll",
if(A.created <=DATE_FORMAT(%s,"%%Y-%%m-%%d")  and A.is_active=1,1,0)"beforestartenroll",
if(A.created >DATE_FORMAT(%s,"%%Y-%%m-%%d")  and A.is_active=0,1,0)"afterstartunenroll",
if(A.created <=DATE_FORMAT(%s,"%%Y-%%m-%%d")  and A.is_active=0,1,0)"beforestartunenroll"
FROM student_courseaccessrole B RIGHT OUTER JOIN student_courseenrollment A on A.user_id=B.user_id  and A.course_id=B.course_id where A.course_id= %s ORDER BY `A`.`user_id` ASC
) B''',[startdate,startdate,startdate,startdate,courseid])

    for i in enrolldata:
        args['enroll']=i.enroll
        args['unenroll']=i.unenroll
        args['totalstudent']=i.totalstudent
        args['totalstaff']=i.totalstaff
        args['afterstartenroll']=i.afterstartenroll
        args['afterstartunenroll']=i.afterstartunenroll
        args['beforestartunenroll']=i.beforestartunenroll
        args['beforestartenroll']=i.beforestartenroll

    coursedata=AuthUser.objects.raw('''SELECT "1" id, count(distinct course) "Course" ,count(distinct video) "Video",count(distinct problem) "problem" ,count(distinct gproblem) "gradedproblem" from
(
SELECT if(module_type="course",student_id,-1) "course",if(module_type="video",student_id,-1) "video", if(module_type="problem",student_id,-1) "problem",if(module_type="problem" and grade is not null,student_id,-1) "gproblem" FROM `courseware_studentmodule` where course_id =%s) A''',[courseid])

    for i in coursedata:
        args['course']=i.Course
        args['video']=i.Video
        args['problem']=i.problem
        args['gradedproblem']=i.gradedproblem
        

    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['email']=request.user
    args['coursedisplayname']=edxcourse_inst.coursename
    args['courseid']=courseid
    return render_to_response('managerapp/coursenrolldetails.html',args) 


def coursedailyreport(request,courseid):
    args=iitbxsessiondata(request)
    report=[]
    #print courseid
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    coursename =edxcourses.objects.get(courseid=courseid).coursename
    args['coursename']= coursename
    report_name="Daily Report of "+"_"+str(courseid)+" _ "+currenttime 
    #print 'report_name  is ' , report_name 
    sumtotal= 0
    sumstudents= 0 
    sumenrolled= 0
    sumunenrolled= 0
    sumactive= 0
    sumstudents= 0
    sumstaff= 0
    #courseid="IITBombayX/CS101.1xA15/2015_T1"
    args['courseid']=courseid
    sqlq='''SELECT "1" id,  @sum:=@sum+query.Total as Id,tdate ,Enrolled,Unenrolled,Total,students,staff
FROM
(select  count(distinct idd) "Total", created "tdate", sum(enrolled) "Enrolled", sum(unenrolled) "Unenrolled",sum(students) "students",sum(staff) "staff"
FROM (
select  
        distinct s.user_id idd,
        if(s.is_active=0,1,0) unenrolled,
        if(s.is_active=1,1,0) enrolled,
        date(s.created) created ,
        
        if(c.role is null  and is_active=1,1,0) students,
        if(c.role is not null,1,0)staff,s.id
        
from student_courseenrollment s   LEFT OUTER JOIN student_courseaccessrole c ON c.user_id=s.user_id and s.course_id=c.course_id
where s.course_id = %s
   ) x  group by  tdate order by  created asc) as query
CROSS JOIN (SELECT @sum :=0) as dummy
''' %('"'+courseid+'"')
    
    
    course_report=AuthUser.objects.raw(sqlq)
    
    for k in course_report:
           sumtotal+=k.Total
           #print sumtotal
           sumenrolled+=k.Enrolled
           sumunenrolled+=k.Unenrolled
           sumstudents+=k.students
           sumstaff+=k.staff
           date = datetime.strptime(str(k.tdate), "%Y-%m-%d").strftime("%d-%m-%Y") 
           report.append([str(date),str(k.Enrolled),str(k.Unenrolled),str(k.Total),int(k.Id),str(k.students),str(k.staff)])
    args["report"]=report.reverse()
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['email']=request.user
    args["report"]=report
    args["sumtotal"]=sumtotal
    args["sumenrolled"]=sumenrolled
    args["sumunenrolled"]=sumunenrolled
    args["report_name"]=report_name 
    args["sumstudents"]=sumstudents
    args["sumstaff"]=sumstaff
    return render_to_response('managerapp/coursedailyreport.html',args) 

def courseweeklyreport(request,courseid):
    args=iitbxsessiondata(request)
    report=[]
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    coursename =edxcourses.objects.get(courseid=courseid).coursename
    args['coursename']= coursename
    report_name="Weekly Report of "+"_"+str(courseid)+" _ "+currenttime
    sumtotal= 0
    sumstudents= 0 
    sumenrolled= 0
    sumunenrolled= 0
    sumactive= 0
    sumstudents= 0
    sumstaff= 0
    args['courseid']=courseid
    sqlq='''SELECT "1" id,  @sum:=@sum+query.Total as Id,week,Enrolled,Unenrolled,Total,students,staff
FROM
(select  count(distinct idd) "Total",DATE_ADD(created, INTERVAL(7-DAYOFWEEK(created)) DAY)  "week", sum(enrolled) "Enrolled", sum(unenrolled) "Unenrolled",sum(students) "students",sum(staff) "staff"
FROM (
select  distinct s.user_id idd,
        if(s.is_active=0,1,0) unenrolled,
        if(s.is_active=1,1,0) enrolled,
        date(s.created) created ,
        
        if(c.role is null  and is_active=1,1,0) students,
        if(c.role is not null,1,0)staff,s.id 
        
from student_courseenrollment s   LEFT OUTER JOIN student_courseaccessrole c ON c.user_id=s.user_id and s.course_id=c.course_id
where s.course_id = %s
   ) X group by  week(created) asc ) as query
CROSS JOIN (SELECT @sum :=0) as dummy
''' %('"'+courseid+'"')
    
    
    course_report=AuthUser.objects.raw(sqlq)
    
    for k in course_report:
           sumtotal+=k.Total
           sumenrolled+=k.Enrolled
           sumunenrolled+=k.Unenrolled
           sumstudents+=k.students
           sumstaff+=k.staff
           date = datetime.strptime(str(k.week), "%Y-%m-%d").strftime("%d-%m-%Y")
           report.append([str(date),str(k.Enrolled),str(k.Unenrolled),str(k.Total),int(k.Id),k.students,k.staff])
    args["report"]=report.reverse()
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['email']=request.user
    args["report"]=report
    args["sumtotal"]=sumtotal
    args["sumenrolled"]=sumenrolled
    args["sumunenrolled"]=sumunenrolled
    args["sumstudents"]=sumstudents
    args["sumstaff"]=sumstaff
    args["report_name"]=report_name
    return render_to_response('managerapp/courseweeklyreport.html',args) 

def coursemonthlyreport(request,courseid):
    args=iitbxsessiondata(request)
    report=[]
    args['courseid']=courseid
    coursename =edxcourses.objects.get(courseid=courseid).coursename
    args['coursename']= coursename 
    currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    sumtotal= 0
    sumstudents= 0
    sumenrolled= 0
    sumunenrolled= 0
    sumactive= 0
    sumstudents= 0
    sumstaff= 0
    report_name="Monthly Report of "+"_"+str(courseid)+" _ "+currenttime
    
    sqlq='''SELECT "1" id,  @sum:=@sum+query.Total as Id, concat(month,"-",year) as month,Enrolled,Unenrolled,Total,students,staff
FROM
(select  count(*) "Total",MONTHNAME(created) "month",YEAR(created) "year", sum(enrolled) "Enrolled", sum(unenrolled) "Unenrolled",sum(students) "students",sum(staff) "staff"
FROM (select  distinct s.user_id idd,
        if(s.is_active=0,1,0) unenrolled,
        if(s.is_active=1,1,0) enrolled,
        date(s.created) created ,
        
        if(c.role is null  and is_active=1,1,0) students,
        if(c.role is not null,1,0)staff,s.id 


from student_courseenrollment s   LEFT OUTER JOIN student_courseaccessrole c ON c.user_id=s.user_id and s.course_id=c.course_id
where s.course_id = %s
   ) X  group by  MONTH(created)
 ) as query
CROSS JOIN (SELECT @sum :=0) as dummy

''' %('"'+courseid+'"')

    
    course_report=AuthUser.objects.raw(sqlq)
    #print "before for loop"
    for k in course_report:
           #print "after for loop"
           sumtotal+=k.Total
           sumenrolled+=k.Enrolled
           sumunenrolled+=k.Unenrolled
           sumstudents+=k.students
           sumstaff+=k.staff

           report.append([str(k.month),str(k.Enrolled),str(k.Unenrolled),str(k.Total),int(k.Id),str(k.students),str(k.staff)])
    args["report"]=report.reverse()
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['email']=request.user
    args["report"]=report
    args["sumtotal"]=sumtotal
    args["sumenrolled"]=sumenrolled
    args["sumunenrolled"]=sumunenrolled
    args["sumstudents"]=sumstudents
    args["sumstaff"]=sumstaff
    args["report_name"]=report_name
    return render_to_response('managerapp/coursemonthlyreport.html',args) 


############################################## Start of iitbombayx at a glance############################################################

def ataglance(request):
    args={}
    iitbxdata=[]
    email=request.user
    TotalStats=[]
    ruralurbandata=[]
    monthinci=[]
    edusumm=[]
    agesumm=[]
    monthsince=[]
    TotalStats.append(AuthUser.objects.count())

    sqla='''SELECT "" id, PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM max(modified) ),
EXTRACT(YEAR_MONTH FROM date_format('2015-01-26', "%%Y%%m%%d"))) AS months, date(max(modified)) "maxdate"
from courseware_studentmodule;
'''
    mi=AuthUser.objects.raw(sqla)
    for i in mi:
        monthinci.append([i.months,i.maxdate]) 
        
    sqlb='''SELECT 0 id, count(distinct state_id) "states" ,count(distinct(city_id)) "cities" FROM student_mooc_person'''
    Geographical_Diversity=AuthUser.objects.raw(sqlb)
    ldate =Geographical_Diversity[0]
    TotalStats.append(ldate.states)
    TotalStats.append(ldate.cities)
    totalstates=StudentMoocState.objects.count()
    if (totalstates ==  ldate.states):
       TotalStats.append(getErrorContent("all ststes and u.t"))
    else:
       TotalStats.append("")
    
    TotalStats.append(StudentCourseenrollment.objects.count())
      
    TotalStats.append(CoursewareOrganization.objects.count()-1)
    insti=list(CoursewareOrganization.objects.exclude(org_id="IITBombayX").values('org_id'))
    partners=[]
    for i in insti:
       partners.append(i['org_id'])
    TotalStats.append(", ".join(map(str,partners)))
    certificate=CertificatesGeneratedcertificate.objects.exclude(status="notpassing").count()
    TotalStats.append(certificate) 
######################################################blended##########################################################################
    sqla='''SELECT " " id,course, count(*) "TotalLearners", sum(blended) "BlendedStudents",sum(others) "OtherLearners",count(Distinct personid_id) "numberofClasses" ,count(Distinct instituteid_id) "numberofInstitutes"
FROM(
select e.course,c.id,
if(c.personid_id!=1,1,0) blended,
if(c.personid_id=1,1,0) others
,
c.personid_id,c.instituteid_id
from iitbxblended.SIP_edxcourses e ,iitbxblended.SIP_studentdetails s ,iitbxblended.SIP_courselevelusers c
where e.blended_mode=1
and e.courseid=s.courseid
and s.teacherid_id=c.id
) A group by course
union all
SELECT " " id,"Grand Total", count(*) "Total Learners", sum(blended) "Blended Students",sum(others) "Other Learners",count(Distinct personid_id) "# ofTeachers" ,count(Distinct instituteid_id) "# of Institutes"
FROM(
select e.course,c.id,
if(c.personid_id!=1,1,0) blended,
if(c.personid_id=1,1,0) others
,
c.personid_id,c.instituteid_id
from iitbxblended.SIP_edxcourses e ,iitbxblended.SIP_studentdetails s ,iitbxblended.SIP_courselevelusers c
where e.blended_mode=1
and e.courseid=s.courseid
and s.teacherid_id=c.id
) A
'''

    iitbxsummary=AuthUser.objects.raw(sqla)
    total=iitbxsummary[-1]
    for i in iitbxsummary:
           iitbxdata.append([i.course,i.TotalLearners,i.BlendedStudents,i.OtherLearners,i.numberofClasses,i.numberofInstitutes])
    iitbxdata.pop()
############################################################rural urban###################################################################
    sqld='''select "" id, a,b, round(a/c*100,2) "x" from   (SELECT count(*) a ,type b FROM iitbxblended.postalinfo a RIGHT OUTER JOIN edxapp.student_mooc_person b ON a.pincode=b.pincode and b.pincode is not null group by type) X cross join (SELECT count(*) c FROM iitbxblended.postalinfo a RIGHT OUTER JOIN edxapp.student_mooc_person b ON a.pincode=b.pincode ) Y  ;
'''  
    ruralurban=AuthUser.objects.raw(sqld)
    
    rural=[0]*2
    urban=[0]*2
    semiurban=[0]*2
    urb=[0]*6
    for j in ruralurban: 
          if (j.b=='Rural'):
              rural[0]=j.a
              rural[1]= str(j.x)+"%"
    rururb=[rural[0],semiurban[0],urban[0],rural[1],semiurban[1],urban[1]]
     
    for j in ruralurban: 
          if (j.b=='SemiUrban'):
              semiurban[0]=j.a
              semiurban[1]= str(j.x)+"%"
    semiurb=[rural[0],semiurban[0],urban[0],rural[1],semiurban[1],urban[1]]

    for j in ruralurban: 
          if (j.b=='Urban'):
              urban[0]=j.a
              urban[1]= str(j.x)+"%"
    urb=[rural[0],semiurban[0],urban[0],rural[1],semiurban[1],urban[1]]
################################################male female distibution###########################################

    sqle='''select "" id,gtotal, gender,round(gtotal/total*100,2) "per" from (SELECT count(*) gtotal,gender FROM auth_userprofile where gender is not null and gender in ('m','f') group by gender ) A cross join (select count(*)  total from auth_userprofile where gender is not null and gender in ('m','f') ) B'''

    mafe = AuthUser.objects.raw(sqle)

    female = [0]*2
    male = [0]*2
    fecount = [0]*6
    mcount = [0]*6
  
    for k in mafe:
        if (k.gender=='f'):
              female[0]=k.gtotal
              female[1]=str(k.per)+"%"
    fecount=[female[0],male[0],female[1],male[1]]

    for k in mafe:
        if (k.gender=='m'):
              male[0]=k.gtotal
              male[1]=str(k.per)+"%"
    mcount=[female[0],male[0],female[1],male[1]]
###############################################################Education###############################################################
    sqlf='''SELECT "" id,UnderGrad,
Graduates,
PostGrads,
Doctorates,
round(UnderGrad/Total*100,2) "UnderGradPer",
round(Graduates/Total*100,2) "GraduatesPer",
round(PostGrads/Total*100,2) "PostGradPer",
round(Doctorates/Total*100,2) "DoctoratesPer" FROM (
SELECT sum(if(level_of_education in ('el','hs','jhs','a'),1,0)) "UnderGrad",sum(if(level_of_education='b',1,0)) "Graduates" ,
sum(if(level_of_education='m',1,0)) "PostGrads",
sum(if(level_of_education='p',1,0)) "Doctorates" , sum(if(level_of_education in ('el','hs','jhs','a','b','m','p'),1,0)) Total FROM `auth_userprofile`) A
'''

    edu=[0]*8
    educationsummary=AuthUser.objects.raw(sqlf)
    for l in educationsummary:
          edu[0]=l.UnderGrad
          edu[1]=l.Graduates
          edu[2]=l.PostGrads
          edu[3]=l.Doctorates
          edu[4]=str(l.UnderGradPer)+"%"
          edu[5]=str(l.GraduatesPer)+"%"
          edu[6]=str(l.PostGradPer)+"%"
          edu[7]=str(l.DoctoratesPer)+"%"

    
   
###############################################################Age#####################################################################
    sqlr='''SELECT "" id,sum(if(age_group ="under 18",1,0)) "Under18",
sum(if(age_group ="18-25",1,0)) "Students",
sum(if(age_group ="25-60",1,0)) "Working",
sum(if(age_group ="above 60",1,0)) "Seniors"
from
(SELECT if( year_of_birth <1955, "above 60", if( year_of_birth <1990, "25-60", if( year_of_birth <1997, "18-25", if( year_of_birth <2015, "under 18", "ND" ) ) ) ) "age_group"
FROM edxapp.auth_userprofile )X
'''
    agegrp=AuthUser.objects.raw(sqlr)
    for m in agegrp:
        agesumm=[m.Under18,m.Students,m.Working,m.Seniors]
        tot=m.Under18+m.Students+m.Working+ m.Seniors
        agesumm=agesumm+[str(round(m.Under18/tot*100,2))+"%",str(round(m.Students/tot*100,2))+"%",str(round(m.Working/tot*100,2))+"%",str(round(m.Seniors/tot*100,2))+"%"]
    args['firstname']=request.session['firstname']
    args['lastname']=request.session['lastname']        
    args['TotalStats']=TotalStats
    args['iitbxdata']=iitbxdata
    args['mcount']=mcount
    args['edu']=edu
    args['agesumm']=agesumm
    args['urb']=urb
    args['total']=total
    args['email']=request.user
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['rolename']="Super User"
    args['monthinci']=monthinci

    return render_to_response('managerapp/ataglance.html',args)
######################################## End of iitbombayx at a glance###########################################################
def activityrep(request):
    args={}
    total=[]
    count=0
    actsumm=gen_repout.objects.filter(reportid=1).order_by('id')
    for i in actsumm:
        if(count!=0):
           total.append([i.A,i.B,i.C,i.D,i.E])
        else:
           total.append(["",i.B,i.C,i.D,i.E])
           header=i.A 
           header_data=map(str,header.split(","))
        count=count+1

    args['header_data']=header_data
    args['total']=total
    args['firstname']=request.session['firstname']
    args['lastname']=request.session['lastname']  
    args['email']=request.user
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['rolename']="Super User"
    return render_to_response('managerapp/iitbxactivity.html',args)


#######################################################student Demography#################################################################

def studntdemography(request,courseid):
    args={}
    args['courseid']=courseid
    email=request.user
    TotalStats=[]
    ruralurbandata=[]
    monthinci=[]
    edusumm=[]
    agesumm=[]
    monthsince=[]


    edxcourse_name=edxcourses.objects.get(courseid=courseid)

    sqla='''SELECT "" id, PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM max(modified) ),
EXTRACT(YEAR_MONTH FROM date_format('2015-01-26', "%%Y%%m%%d"))) AS months, date(max(modified)) "maxdate"
from courseware_studentmodule;
'''
    mi=AuthUser.objects.raw(sqla)
    for i in mi:
        monthinci.append([i.months,i.maxdate]) 
        
    Geographical_Diversity=AuthUser.objects.raw('''SELECT 0 id, count(distinct state_id) "states" ,count(distinct(city_id)) "cities" FROM student_mooc_person A,student_courseenrollment B where B.course_id =%s and A.user_id=B.user_id''',[courseid])
    ldate =Geographical_Diversity[0]
    TotalStats.append(ldate.states)
    TotalStats.append(ldate.cities)
    print TotalStats, "hello"
    
############################################################rural urban###################################################################
    ruralurban=AuthUser.objects.raw('''select "" id, a,b, round(a/c*100,2) "x" from   (SELECT count(*) a ,type b FROM iitbxblended.postalinfo a RIGHT OUTER JOIN edxapp.student_mooc_person b ON a.pincode=b.pincode and b.pincode is not null,student_courseenrollment A where A.course_id=%s and b.user_id=A.user_id group by type) X cross join (SELECT count(*) c FROM iitbxblended.postalinfo a RIGHT OUTER JOIN edxapp.student_mooc_person b ON a.pincode=b.pincode,student_courseenrollment A where A.course_id=%s and b.user_id=A.user_id ) Y''',[courseid,courseid])
    
    rural=[0]*2
    urban=[0]*2
    semiurban=[0]*2
    urb=[0]*6
    for j in ruralurban: 
          if (j.b=='Rural'):
              rural[0]=j.a
              rural[1]= str(j.x)+"%"
    rururb=[rural[0],semiurban[0],urban[0],rural[1],semiurban[1],urban[1]]
     
    for j in ruralurban: 
          if (j.b=='SemiUrban'):
              semiurban[0]=j.a
              semiurban[1]= str(j.x)+"%"
    semiurb=[rural[0],semiurban[0],urban[0],rural[1],semiurban[1],urban[1]]

    for j in ruralurban: 
          if (j.b=='Urban'):
              urban[0]=j.a
              urban[1]= str(j.x)+"%"
    urb=[rural[0],semiurban[0],urban[0],rural[1],semiurban[1],urban[1]]
################################################male female distibution###########################################
    mafe = AuthUser.objects.raw('''select "" id,gtotal, gender,round(gtotal/total*100,2) "per" from (SELECT count(*) gtotal,gender FROM auth_userprofile p,  student_courseenrollment  q where q.course_id=%s and p.user_id=q.user_id 
and gender is not null and gender in ('m','f') group by gender ) A cross join (select count(*)  total from auth_userprofile p,  student_courseenrollment q where q.course_id=%s and p.user_id=q.user_id 
and gender is not null and gender in ('m','f') ) B''',[courseid,courseid])

    female = [0]*2
    male = [0]*2
    fecount = [0]*6
    mcount = [0]*6
  
    for k in mafe:
        if (k.gender=='f'):
              female[0]=k.gtotal
              female[1]=str(k.per)+"%"
    fecount=[female[0],male[0],female[1],male[1]]

    for k in mafe:
        if (k.gender=='m'):
              male[0]=k.gtotal
              male[1]=str(k.per)+"%"
    mcount=[female[0],male[0],female[1],male[1]]
###############################################################Education###############################################################
    edu=[0]*8
    educationsummary=AuthUser.objects.raw('''SELECT "" id,UnderGrad,
Graduates,
PostGrads,
Doctorates,
round(UnderGrad/Total*100,2) "UnderGradPer",
round(Graduates/Total*100,2) "GraduatesPer",
round(PostGrads/Total*100,2) "PostGradPer",
round(Doctorates/Total*100,2) "DoctoratesPer" FROM (
SELECT sum(if(level_of_education in ('el','hs','jhs','a'),1,0)) "UnderGrad",sum(if(level_of_education='b',1,0)) "Graduates" ,
sum(if(level_of_education='m',1,0)) "PostGrads",
sum(if(level_of_education='p',1,0)) "Doctorates" , sum(if(level_of_education in ('el','hs','jhs','a','b','m','p'),1,0)) Total FROM `auth_userprofile`   A,student_courseenrollment B where B.course_id =%s and A.user_id=B.user_id) P
''',[courseid])

    for l in educationsummary:
          edu[0]=l.UnderGrad
          edu[1]=l.Graduates
          edu[2]=l.PostGrads
          edu[3]=l.Doctorates
          edu[4]=str(l.UnderGradPer)+"%"
          edu[5]=str(l.GraduatesPer)+"%"
          edu[6]=str(l.PostGradPer)+"%"
          edu[7]=str(l.DoctoratesPer)+"%"

    
   
###############################################################Age#####################################################################
    agegrp=AuthUser.objects.raw('''SELECT "" id,sum(if(age_group ="under 18",1,0)) "Under18",
sum(if(age_group ="18-25",1,0)) "Students",
sum(if(age_group ="25-60",1,0)) "Working",
sum(if(age_group ="above 60",1,0)) "Seniors"
from
(SELECT if( year_of_birth <1955, "above 60", if( year_of_birth <1990, "25-60", if( year_of_birth <1997, "18-25", if( year_of_birth <2015, "under 18", "ND" ) ) ) ) "age_group"
FROM edxapp.auth_userprofile X,student_courseenrollment B where B.course_id =%s and X.user_id=B.user_id) P''',[courseid])
    for m in agegrp:
        agesumm=[m.Under18,m.Students,m.Working,m.Seniors]
        tot=m.Under18+m.Students+m.Working+ m.Seniors
        agesumm=agesumm+[str(round(m.Under18/tot*100,2))+"%",str(round(m.Students/tot*100,2))+"%",str(round(m.Working/tot*100,2))+"%",str(round(m.Seniors/tot*100,2))+"%"]

    args['coursedisplayname']=edxcourse_name.coursename
    args['firstname']=request.session['firstname']
    args['lastname']=request.session['lastname']        
    args['TotalStats']=TotalStats
    args['mcount']=mcount
    args['edu']=edu
    args['agesumm']=agesumm
    args['urb']=urb
    args['email']=request.user
    args['institutename']=request.session['institutename']
    args['rcid']= request.session['rcid']
    args['rolename']="Super User"
    args['monthinci']=monthinci

    return render_to_response('managerapp/studntdemography.html',args)


def genquizanswers(request,courseid,pid):

    args =iitbxsessiondata(request)
    report=[]
    header=[]
    try:
       secid=request.POST['quiz']

       evalu=gen_evaluations.objects.filter(sectionid=secid).values('sec_name').distinct()
       args['secname']=evalu[0]['sec_name']
    except Exception as e:
           return genevaluationoption(request,courseid,pid,1)

    args['selectedinstitute']="IITBombay"

    try:
       courseobj = edxcourses.objects.get(courseid = courseid)
       args['coursename']=courseobj.coursename
       args['course']=courseobj.course
       args['courseid']=courseid
       args['pid']=pid
       currenttime = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
       report_name="Evaluation Report of "+"_"+str(courseid)+" _ "+currenttime
       person=Personinformation.objects.get(id=pid)
       args['teacher']= str(person.firstname)+' '+str(person.lastname)
    except Exception as e:
           args['error_message'] ="IITBombayX course is not present."
           args['error_message'] = "\n Error " + e.message + type(e)
           return render(request,error_,args)

    try:
      head_str=gen_headings.objects.get(section=secid).heading
      heading=map(str,head_str.split(","))
      del heading[3]

    except Exception as e:
      print str(e.message),str(type(e))
    sqlmod=""
    ques_dict={}
    qidslist=[]
    count=0
    totalweight=0
    evaluation_obj=gen_questions.objects.filter(course=courseobj,eval__sectionid=secid ).exclude(q_weight=0 ).order_by('eval_id','id')
    for evaluate in evaluation_obj:
           if evaluate.q_weight != 0:
              sqlmod= sqlmod +'"'+evaluate.qid+'",'
              qidslist.append(evaluate.qid)
           count=count+1
           totalweight=totalweight+evaluate.q_weight
    sqlmod=sqlmod[:-1]
    if len(sqlmod) == 0:
         stud_rec=[]
    else:
         sqlstmt= '''SELECT "1" id,student_id,username,email,module_id, case prob_count when 0 then '' when 1 then t1 when 2 then concat(t1,'~',t2) when 3 then concat(t1,'~',t2,'~',t3) when 4 then concat(t1,'~',t2,'~',t3, '~',t4) when 5 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5) when  6 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6) when  7 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7) when  8 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7,'~',t8) when  9 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7,'~',t8,'~',t9) when  10 then concat(t1,'~',t2,'~',t3, '~',t4,'~',t5,'~',t6, '~',t7,'~',t8,'~',t9,'~',t10) end as answer  FROM
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
,prob_count
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
 FROM edxapp.courseware_studentmodule where module_type=%s and module_id in (%s) and course_id=%s and grade is not null and instr(state,'"done": true')!=0 ) a,iitbxblended.iitbx_gen_questions b where a.module_id=b.qid) X,
  auth_user b where   student_id=b.id order by student_id''' %('"'+"problem"+'"',sqlmod,'"'+str(courseobj.courseid)+'"')
         answersheets=AuthUser.objects.raw(sqlstmt)
         oldstudent=-1; anslist={};replist=[];stud_rec=[]
         for answer in answersheets:
           #print "hello"
           if oldstudent == -1:
               replist=[answer.student_id,answer.username,answer.email]
               oldstudent=answer.student_id
           #print oldstudent, answer.student_id
           if answer.student_id == oldstudent:
               anslist[answer.module_id]=answer.answer
           else:
               for qid in qidslist:
                     if (anslist.has_key(qid)):
                        replist.append(anslist[qid])
                     else:
                        replist.append('')
               stud_rec.append(replist)
               replist=[];anslist={}
               oldstudent=answer.student_id
               anslist[answer.module_id]=answer.answer
               replist=[answer.student_id,answer.username,answer.email]

         for qid in qidslist:
            if (anslist.has_key(qid)):
                  replist.append(anslist[qid])
            else:
                 replist.append('')
         stud_rec.append(replist)
    args['stud_rec']=stud_rec
    #print stud_rec
    args['headings']=heading
    args["report_name"]=report_name
    return render(request,"managerapp/genanswer.html",args)


def genevaluationoption(request,courseid,pid,evalflag):
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
    #try:
       # courselevelid=Courselevelusers.objects.get(personid__id=pid,courseid__courseid=courseid,startdate__lte=current,enddate__gte=current)
    #except Exception as e:
          # args['error_message'] = getErrorContent("teacher_not_valid"),courseid
          # args['error_message'] = "\n Error " + str(e.message) + str(type(e))
           #return render(request,error_,args)
    evaluation_obj=gen_evaluations.objects.filter(course=courseobj,release_date__lte=current).values('sectionid','sec_name').distinct().order_by('due_date')
    if evalflag==1:
        args['error_message'] = getErrorContent("select_quiz")+"<br>"
    
    args['evaluation']=evaluation_obj
    return render(request,"managerapp/genevaluationoption.html",args)



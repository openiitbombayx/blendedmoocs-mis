'''The Information System for Blended MOOCs combines the benefits of MOOCs on IITBombayX with the conventional teaching-learning process at the various partnering institutes. This system envisages the factoring of MOOCs marks in the grade computed for a student of that subject, in a regular degree program. 
Copyright (C) 2015  BMWinfo 
This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses>.'''


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AssessmentAiclassifier(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    classifier_set = models.ForeignKey('AssessmentAiclassifierset')
    criterion = models.ForeignKey('AssessmentCriterion')
    classifier_data = models.CharField(max_length=100)
    def __unicode__(self):
        return self.id
    class Meta:
        managed = False
        db_table = 'assessment_aiclassifier'


class AssessmentAiclassifierset(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    rubric = models.ForeignKey('AssessmentRubric')
    created_at = models.DateTimeField()
    algorithm_id = models.CharField(max_length=128)
    course_id = models.CharField(max_length=40)
    item_id = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'assessment_aiclassifierset'



class AssessmentAigradingworkflow(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    uuid = models.CharField(unique=True, max_length=36)
    scheduled_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    submission_uuid = models.CharField(max_length=128)
    classifier_set = models.ForeignKey(AssessmentAiclassifierset, blank=True, null=True)
    algorithm_id = models.CharField(max_length=128)
    rubric = models.ForeignKey('AssessmentRubric')
    assessment = models.ForeignKey('AssessmentAssessment', blank=True, null=True)
    student_id = models.CharField(max_length=40)
    item_id = models.CharField(max_length=128)
    course_id = models.CharField(max_length=40)
    essay_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'assessment_aigradingworkflow'


class AssessmentAitrainingworkflow(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    uuid = models.CharField(unique=True, max_length=36)
    algorithm_id = models.CharField(max_length=128)
    classifier_set = models.ForeignKey(AssessmentAiclassifierset, blank=True, null=True)
    scheduled_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    item_id = models.CharField(max_length=128)
    course_id = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'assessment_aitrainingworkflow'


class AAitrainingworkflowTraining(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    aitrainingworkflow = models.ForeignKey(AssessmentAitrainingworkflow)
    trainingexample = models.ForeignKey('AssessmentTrainingexample' )

    class Meta:
        managed = False
        db_table = 'assessment_aitrainingworkflow_training_examples'
        #verbose_name_plural = "assessment_aitrainingworkflow_training_examples"
        

class AssessmentAssessment(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    submission_uuid = models.CharField(max_length=128)
    rubric = models.ForeignKey('AssessmentRubric')
    scored_at = models.DateTimeField()
    scorer_id = models.CharField(max_length=40)
    score_type = models.CharField(max_length=2)
    feedback = models.TextField()

    class Meta:
        managed = False
        db_table = 'assessment_assessment'


class AssessmentAssessmentfeedback(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    submission_uuid = models.CharField(unique=True, max_length=128)
    feedback_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedback'


class AAssessmentfeedbackAssessments(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    assessmentfeedback = models.ForeignKey(AssessmentAssessmentfeedback)
    assessment = models.ForeignKey(AssessmentAssessment)
    
    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedback_assessments'


class AssessmentAssessmentfeedbackOptions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    assessmentfeedback = models.ForeignKey(AssessmentAssessmentfeedback)
    assessmentfeedbackoption = models.ForeignKey('AssessmentAssessmentfeedbackoption')

    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedback_options'
        
    def __unicode__(self):
        return u'%s %s' % (self.assessmentfeedback.submission_uuid,self.assessmentfeedbackoption.text)
    
class AssessmentAssessmentfeedbackoption(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    text = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'assessment_assessmentfeedbackoption'


class AssessmentAssessmentpart(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    assessment = models.ForeignKey(AssessmentAssessment,related_name='assesassess')
    option = models.ForeignKey('AssessmentCriterionoption', blank=True, null=True)
    feedback = models.TextField()
    criterion = models.ForeignKey('AssessmentCriterionoption',related_name='assescritera')

    class Meta:
        managed = False
        db_table = 'assessment_assessmentpart'


class AssessmentCriterion(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    rubric = models.ForeignKey('AssessmentRubric')
    name = models.CharField(max_length=100)
    order_num = models.IntegerField()
    prompt = models.TextField()
    label = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'assessment_criterion'


class AssessmentCriterionoption(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    criterion = models.ForeignKey(AssessmentCriterion)
    order_num = models.IntegerField()
    points = models.IntegerField()
    name = models.CharField(max_length=100)
    explanation = models.TextField()
    label = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'assessment_criterionoption'


class AssessmentPeerworkflow(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    student_id = models.CharField(max_length=40)
    item_id = models.CharField(max_length=128)
    course_id = models.CharField(max_length=40)
    submission_uuid = models.CharField(unique=True, max_length=128)
    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    grading_completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assessment_peerworkflow'


class AssessmentPeerworkflowitem(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    scorer = models.ForeignKey(AssessmentPeerworkflow ,related_name='assesscorer')
    author = models.ForeignKey(AssessmentPeerworkflow,related_name='assesauthor')
    submission_uuid = models.CharField(max_length=128)
    started_at = models.DateTimeField()
    assessment = models.ForeignKey(AssessmentAssessment, blank=True, null=True)
    scored = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assessment_peerworkflowitem'


class AssessmentRubric(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_hash = models.CharField(unique=True, max_length=40)
    structure_hash = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'assessment_rubric'


class AssessmentStudenttrainingworkflow(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    submission_uuid = models.CharField(unique=True, max_length=128)
    student_id = models.CharField(max_length=40)
    item_id = models.CharField(max_length=128)
    course_id = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'assessment_studenttrainingworkflow'


class AssessmentStudenttrainingworkflowitem(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    workflow = models.ForeignKey(AssessmentStudenttrainingworkflow )
    order_num = models.IntegerField()
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    training_example = models.ForeignKey('AssessmentTrainingexample')

    class Meta:
        managed = False
        db_table = 'assessment_studenttrainingworkflowitem'


class AssessmentTrainingexample(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    raw_answer = models.TextField()
    rubric = models.ForeignKey(AssessmentRubric)
    content_hash = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'assessment_trainingexample'


class ATrainingexampleOptionsSelected(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    trainingexample = models.ForeignKey(AssessmentTrainingexample)
    criterionoption = models.ForeignKey(AssessmentCriterionoption)

    class Meta:
        managed = False
        db_table = 'assessment_trainingexample_options_selected'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthRegistration(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey('AuthUser', unique=True)
    activation_key = models.CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'auth_registration'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(unique=True, max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
    def __unicode__(self):
        return "%s" %(self.email)


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class AuthUserprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, unique=True)
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    meta = models.TextField()
    courseware = models.CharField(max_length=255)
    gender = models.CharField(max_length=6, blank=True)
    mailing_address = models.TextField(blank=True)
    year_of_birth = models.IntegerField(blank=True, null=True)
    level_of_education = models.CharField(max_length=6, blank=True)
    goals = models.TextField(blank=True)
    allow_certificate = models.IntegerField()
    country = models.CharField(max_length=2, blank=True)
    city = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'auth_userprofile'


class BulkEmailCourseauthorization(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(unique=True, max_length=255)
    email_enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bulk_email_courseauthorization'


class BulkEmailCourseemail(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    sender = models.ForeignKey(AuthUser, blank=True, null=True)
    slug = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    html_message = models.TextField(blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    course_id = models.CharField(max_length=255)
    to_option = models.CharField(max_length=64)
    text_message = models.TextField(blank=True)
    template_name = models.CharField(max_length=255, blank=True)
    from_addr = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'bulk_email_courseemail'


class BulkEmailCourseemailtemplate(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    html_template = models.TextField(blank=True)
    plain_template = models.TextField(blank=True)
    name = models.CharField(unique=True, max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'bulk_email_courseemailtemplate'


class BulkEmailOptout(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bulk_email_optout'


class CeleryTaskmeta(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    result = models.TextField(blank=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True)
    hidden = models.IntegerField()
    meta = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'celery_taskmeta'


class CeleryTasksetmeta(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    taskset_id = models.CharField(unique=True, max_length=255)
    result = models.TextField()
    date_done = models.DateTimeField()
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'celery_tasksetmeta'


class CertificatesCertificatewhitelist(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    course_id = models.CharField(max_length=255)
    whitelist = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'certificates_certificatewhitelist'


class CertificatesGeneratedcertificate(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    download_url = models.CharField(max_length=128)
    grade = models.CharField(max_length=5)
    course_id = models.CharField(max_length=255)
    key = models.CharField(max_length=32)
    distinction = models.IntegerField()
    status = models.CharField(max_length=32)
    verify_uuid = models.CharField(max_length=32)
    download_uuid = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    error_reason = models.CharField(max_length=512)
    mode = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'certificates_generatedcertificate'


class CircuitServercircuit(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=32)
    schematic = models.TextField()

    class Meta:
        managed = False
        db_table = 'circuit_servercircuit'


class CourseActionStateCoursererunstate(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    created_user = models.ForeignKey(AuthUser, blank=True, null=True,related_name='coursecreated')
    updated_user = models.ForeignKey(AuthUser, blank=True, null=True,related_name='courseupdated')
    course_key = models.CharField(max_length=255)
    action = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    should_display = models.IntegerField()
    message = models.CharField(max_length=1000)
    source_course_key = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'course_action_state_coursererunstate'


class CourseCreatorsCoursecreator(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, unique=True)
    state_changed = models.DateTimeField()
    state = models.CharField(max_length=24)
    note = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'course_creators_coursecreator'


class CourseGroupsCourseusergroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    group_type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'course_groups_courseusergroup'


class CourseGroupsCourseusergroupUsers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    courseusergroup = models.ForeignKey(CourseGroupsCourseusergroup)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'course_groups_courseusergroup_users'


class CGroupsCourseusergrouppartitiongroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_user_group = models.ForeignKey(CourseGroupsCourseusergroup, unique=True)
    partition_id = models.IntegerField()
    group_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'course_groups_courseusergrouppartitiongroup'


class CourseModesCoursemode(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(max_length=255)
    mode_slug = models.CharField(max_length=100)
    mode_display_name = models.CharField(max_length=255)
    min_price = models.IntegerField()
    suggested_prices = models.CharField(max_length=255)
    currency = models.CharField(max_length=8)
    expiration_date = models.DateField(blank=True, null=True)
    expiration_datetime = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'course_modes_coursemode'


class CourseModesCoursemodesarchive(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(max_length=255)
    mode_slug = models.CharField(max_length=100)
    mode_display_name = models.CharField(max_length=255)
    min_price = models.IntegerField()
    suggested_prices = models.CharField(max_length=255)
    currency = models.CharField(max_length=8)
    expiration_date = models.DateField(blank=True, null=True)
    expiration_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_modes_coursemodesarchive'


class CoursewareCourseSubject(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    subject_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'courseware_course_subject'


class CoursewareOfflinecomputedgrade(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField()
    gradeset = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'courseware_offlinecomputedgrade'


class CoursewareOfflinecomputedgradelog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    seconds = models.IntegerField()
    nstudents = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'courseware_offlinecomputedgradelog'


class CoursewareOrganization(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    org_id = models.CharField(max_length=255)
    org_name = models.TextField()
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    url = models.TextField()
    information = models.TextField()
    image_name = models.CharField(max_length=255)
    header_graphic = models.CharField(max_length=255)
    contact_marketing = models.CharField(max_length=255)
    contact_course_content = models.CharField(max_length=255)
    contact_review_process = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'courseware_organization'


class CoursewareStudentmodule(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    module_type = models.CharField(max_length=32)
    module_id = models.CharField(max_length=255)
    student = models.ForeignKey(AuthUser)
    state = models.TextField(blank=True)
    grade = models.FloatField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    max_grade = models.FloatField(blank=True, null=True)
    done = models.CharField(max_length=8)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'courseware_studentmodule'
    def __unicode__(self):
          return u"%s %s" %(self.module_id ,self.state)


class CoursewareStudentmodulehistory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    student_module = models.ForeignKey(CoursewareStudentmodule)
    version = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField()
    state = models.TextField(blank=True)
    grade = models.FloatField(blank=True, null=True)
    max_grade = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courseware_studentmodulehistory'


class CoursewareSubject(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    subject_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'courseware_subject'


class CoursewareXmodulestudentinfofield(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    field_name = models.CharField(max_length=64)
    value = models.TextField()
    student = models.ForeignKey(AuthUser)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'courseware_xmodulestudentinfofield'


class CoursewareXmodulestudentprefsfield(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    field_name = models.CharField(max_length=64)
    module_type = models.CharField(max_length=64)
    value = models.TextField()
    student = models.ForeignKey(AuthUser)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'courseware_xmodulestudentprefsfield'


class CoursewareXmoduleuserstatesummaryfield(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    field_name = models.CharField(max_length=64)
    usage_id = models.CharField(max_length=255)
    value = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'courseware_xmoduleuserstatesummaryfield'


class DarkLangDarklangconfig(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    change_date = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, blank=True, null=True)
    enabled = models.IntegerField()
    released_languages = models.TextField()

    class Meta:
        managed = False
        db_table = 'dark_lang_darklangconfig'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCommentClientPermission(models.Model):
    name = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'django_comment_client_permission'


class DjangoCommentClientPermissionRoles(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    permission = models.ForeignKey(DjangoCommentClientPermission)
    role = models.ForeignKey('DjangoCommentClientRole')

    class Meta:
        managed = False
        db_table = 'django_comment_client_permission_roles'


class DjangoCommentClientRole(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=30)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'django_comment_client_role'


class DjangoCommentClientRoleUsers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    role = models.ForeignKey(DjangoCommentClientRole)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_comment_client_role_users'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoOpenidAuthAssociation(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    server_url = models.TextField()
    handle = models.CharField(max_length=255)
    secret = models.TextField()
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_openid_auth_association'


class DjangoOpenidAuthNonce(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    server_url = models.CharField(max_length=2047)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'django_openid_auth_nonce'


class DjangoOpenidAuthUseropenid(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    claimed_id = models.TextField()
    display_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_openid_auth_useropenid'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class DjceleryCrontabschedule(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    minute = models.CharField(max_length=64)
    hour = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=64)
    month_of_year = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'djcelery_crontabschedule'


class DjceleryIntervalschedule(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'djcelery_intervalschedule'


class DjceleryPeriodictask(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    interval = models.ForeignKey(DjceleryIntervalschedule, blank=True, null=True)
    crontab = models.ForeignKey(DjceleryCrontabschedule, blank=True, null=True)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True)
    exchange = models.CharField(max_length=200, blank=True)
    routing_key = models.CharField(max_length=200, blank=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'djcelery_periodictask'


class DjceleryPeriodictasks(models.Model):
    ident = models.IntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'djcelery_periodictasks'


class DjceleryTaskstate(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    state = models.CharField(max_length=64)
    task_id = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=200, blank=True)
    tstamp = models.DateTimeField()
    args = models.TextField(blank=True)
    kwargs = models.TextField(blank=True)
    eta = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True)
    traceback = models.TextField(blank=True)
    runtime = models.FloatField(blank=True, null=True)
    retries = models.IntegerField()
    worker = models.ForeignKey('DjceleryWorkerstate', blank=True, null=True)
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'djcelery_taskstate'


class DjceleryWorkerstate(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    hostname = models.CharField(unique=True, max_length=255)
    last_heartbeat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_workerstate'


class EdxvalCoursevideo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(max_length=255)
    video = models.ForeignKey('EdxvalVideo')

    class Meta:
        managed = False
        db_table = 'edxval_coursevideo'


class EdxvalEncodedvideo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    url = models.CharField(max_length=200)
    file_size = models.IntegerField()
    bitrate = models.IntegerField()
    profile = models.ForeignKey('EdxvalProfile')
    video = models.ForeignKey('EdxvalVideo')

    class Meta:
        managed = False
        db_table = 'edxval_encodedvideo'


class EdxvalProfile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    profile_name = models.CharField(unique=True, max_length=50)
    extension = models.CharField(max_length=10)
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'edxval_profile'


class EdxvalSubtitle(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    video = models.ForeignKey('EdxvalVideo')
    fmt = models.CharField(max_length=20)
    language = models.CharField(max_length=8)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'edxval_subtitle'


class EdxvalVideo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    edx_video_id = models.CharField(unique=True, max_length=100)
    client_video_id = models.CharField(max_length=255)
    duration = models.FloatField()
    created = models.DateTimeField()
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'edxval_video'


class EmbargoEmbargoedcourse(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(unique=True, max_length=255)
    embargoed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'embargo_embargoedcourse'


class EmbargoEmbargoedstate(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    change_date = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, blank=True, null=True)
    enabled = models.IntegerField()
    embargoed_countries = models.TextField()

    class Meta:
        managed = False
        db_table = 'embargo_embargoedstate'


class EmbargoIpfilter(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    change_date = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, blank=True, null=True)
    enabled = models.IntegerField()
    whitelist = models.TextField()
    blacklist = models.TextField()

    class Meta:
        managed = False
        db_table = 'embargo_ipfilter'


class ExternalAuthExternalauthmap(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    external_id = models.CharField(max_length=255)
    external_domain = models.CharField(max_length=255)
    external_credentials = models.TextField()
    external_email = models.CharField(max_length=255)
    external_name = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser, unique=True, blank=True, null=True)
    internal_password = models.CharField(max_length=31)
    dtcreated = models.DateTimeField()
    dtsignup = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'external_auth_externalauthmap'


class FolditPuzzlecomplete(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    unique_user_id = models.CharField(max_length=50)
    puzzle_id = models.IntegerField()
    puzzle_set = models.IntegerField()
    puzzle_subset = models.IntegerField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'foldit_puzzlecomplete'


class FolditScore(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    unique_user_id = models.CharField(max_length=50)
    puzzle_id = models.IntegerField()
    best_score = models.FloatField()
    current_score = models.FloatField()
    score_version = models.IntegerField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'foldit_score'


class InstructorTaskInstructortask(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    task_type = models.CharField(max_length=50)
    course_id = models.CharField(max_length=255)
    task_key = models.CharField(max_length=255)
    task_input = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255)
    task_state = models.CharField(max_length=50, blank=True)
    task_output = models.CharField(max_length=1024, blank=True)
    requester = models.ForeignKey(AuthUser)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField()
    subtasks = models.TextField()

    class Meta:
        managed = False
        db_table = 'instructor_task_instructortask'


class LicensesCoursesoftware(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'licenses_coursesoftware'


class LicensesUserlicense(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    software = models.ForeignKey(LicensesCoursesoftware)
    user = models.ForeignKey(AuthUser, blank=True, null=True)
    serial = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'licenses_userlicense'


class LinkedinLinkedin(models.Model):
    user = models.ForeignKey(AuthUser, primary_key=True)
    has_linkedin_account = models.IntegerField(blank=True, null=True)
    emailed_courses = models.TextField()

    class Meta:
        managed = False
        db_table = 'linkedin_linkedin'


class LmsXblockXblockasidesconfig(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    change_date = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, blank=True, null=True)
    enabled = models.IntegerField()
    disabled_blocks = models.TextField()

    class Meta:
        managed = False
        db_table = 'lms_xblock_xblockasidesconfig'


class NotesNote(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    course_id = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)
    text = models.TextField()
    quote = models.TextField()
    range_start = models.CharField(max_length=2048)
    range_start_offset = models.IntegerField()
    range_end = models.CharField(max_length=2048)
    range_end_offset = models.IntegerField()
    tags = models.TextField()
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notes_note'


class NotificationsArticlesubscription(models.Model):
    subscription_ptr = models.ForeignKey('NotifySubscription', unique=True)
    articleplugin_ptr = models.ForeignKey('WikiArticleplugin', primary_key=True)

    class Meta:
        managed = False
        db_table = 'notifications_articlesubscription'


class NotifyNotification(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    subscription = models.ForeignKey('NotifySubscription', blank=True, null=True)
    message = models.TextField()
    url = models.CharField(max_length=200, blank=True)
    is_viewed = models.IntegerField()
    is_emailed = models.IntegerField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'notify_notification'


class NotifyNotificationtype(models.Model):
    key = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, blank=True)
    content_type = models.ForeignKey(DjangoContentType, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notify_notificationtype'


class NotifySettings(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    interval = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'notify_settings'


class NotifySubscription(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    settings = models.ForeignKey(NotifySettings)
    notification_type = models.ForeignKey(NotifyNotificationtype)
    object_id = models.CharField(max_length=64, blank=True)
    send_emails = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'notify_subscription'


class Oauth2Accesstoken(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    token = models.CharField(max_length=255)
    client = models.ForeignKey('Oauth2Client')
    expires = models.DateTimeField()
    scope = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oauth2_accesstoken'


class Oauth2Client(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, blank=True, null=True)
    url = models.CharField(max_length=200)
    redirect_uri = models.CharField(max_length=200)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    client_type = models.IntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'oauth2_client'


class Oauth2Grant(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    client = models.ForeignKey(Oauth2Client)
    code = models.CharField(max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.CharField(max_length=255)
    scope = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oauth2_grant'


class Oauth2ProviderTrustedclient(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    client = models.ForeignKey(Oauth2Client)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_trustedclient'


class Oauth2Refreshtoken(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    token = models.CharField(max_length=255)
    access_token = models.ForeignKey(Oauth2Accesstoken, unique=True)
    client = models.ForeignKey(Oauth2Client)
    expired = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'oauth2_refreshtoken'


class PsychometricsPsychometricdata(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    studentmodule_id = models.IntegerField(unique=True)
    done = models.IntegerField()
    attempts = models.IntegerField()
    checktimes = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'psychometrics_psychometricdata'


class RMidcoursereverificationwindow(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(max_length=255)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reverification_midcoursereverificationwindow'


class ShoppingcartCertificateitem(models.Model):
    orderitem_ptr = models.ForeignKey('ShoppingcartOrderitem', primary_key=True)
    course_id = models.CharField(max_length=128)
    course_enrollment = models.ForeignKey('StudentCourseenrollment')
    mode = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'shoppingcart_certificateitem'


class ShoppingcartCoupon(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    code = models.CharField(max_length=32)
    description = models.CharField(max_length=255, blank=True)
    course_id = models.CharField(max_length=255)
    percentage_discount = models.IntegerField()
    created_by = models.ForeignKey(AuthUser)
    created_at = models.DateTimeField()
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shoppingcart_coupon'


class ShoppingcartCouponredemption(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    order = models.ForeignKey('ShoppingcartOrder')
    user = models.ForeignKey(AuthUser)
    coupon = models.ForeignKey(ShoppingcartCoupon)

    class Meta:
        managed = False
        db_table = 'shoppingcart_couponredemption'


class ShoppingcartCourseregcodeitem(models.Model):
    orderitem_ptr = models.ForeignKey('ShoppingcartOrderitem', primary_key=True)
    course_id = models.CharField(max_length=128)
    mode = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'shoppingcart_courseregcodeitem'


class SCourseregcodeitemannotation(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(unique=True, max_length=128)
    annotation = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_courseregcodeitemannotation'


class ShoppingcartCourseregistrationcode(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    code = models.CharField(unique=True, max_length=32)
    course_id = models.CharField(max_length=255)
    created_by = models.ForeignKey(AuthUser)
    created_at = models.DateTimeField()
    invoice = models.ForeignKey('ShoppingcartInvoice', blank=True, null=True)
    order = models.ForeignKey('ShoppingcartOrder', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_courseregistrationcode'


class ShoppingcartDonation(models.Model):
    orderitem_ptr = models.ForeignKey('ShoppingcartOrderitem', primary_key=True)
    donation_type = models.CharField(max_length=32)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'shoppingcart_donation'


class ShoppingcartDonationconfiguration(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    change_date = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, blank=True, null=True)
    enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'shoppingcart_donationconfiguration'


class ShoppingcartInvoice(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    total_amount = models.FloatField()
    company_name = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    internal_reference = models.CharField(max_length=255, blank=True)
    is_valid = models.IntegerField()
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    address_line_3 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=64, blank=True)
    recipient_name = models.CharField(max_length=255)
    recipient_email = models.CharField(max_length=255)
    customer_reference_number = models.CharField(max_length=63, blank=True)
    company_contact_name = models.CharField(max_length=255)
    company_contact_email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'shoppingcart_invoice'


class ShoppingcartOrder(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    currency = models.CharField(max_length=8)
    status = models.CharField(max_length=32)
    purchase_time = models.DateTimeField(blank=True, null=True)
    bill_to_first = models.CharField(max_length=64)
    bill_to_last = models.CharField(max_length=64)
    bill_to_street1 = models.CharField(max_length=128)
    bill_to_street2 = models.CharField(max_length=128)
    bill_to_city = models.CharField(max_length=64)
    bill_to_state = models.CharField(max_length=8)
    bill_to_postalcode = models.CharField(max_length=16)
    bill_to_country = models.CharField(max_length=64)
    bill_to_ccnum = models.CharField(max_length=8)
    bill_to_cardtype = models.CharField(max_length=32)
    processor_reply_dump = models.TextField()
    refunded_time = models.DateTimeField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True)
    company_contact_name = models.CharField(max_length=255, blank=True)
    company_contact_email = models.CharField(max_length=255, blank=True)
    recipient_name = models.CharField(max_length=255, blank=True)
    recipient_email = models.CharField(max_length=255, blank=True)
    customer_reference_number = models.CharField(max_length=63, blank=True)
    order_type = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'shoppingcart_order'


class ShoppingcartOrderitem(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    order = models.ForeignKey(ShoppingcartOrder)
    user = models.ForeignKey(AuthUser)
    status = models.CharField(max_length=32)
    qty = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=30, decimal_places=2)
    line_desc = models.CharField(max_length=1024)
    currency = models.CharField(max_length=8)
    fulfilled_time = models.DateTimeField(blank=True, null=True)
    report_comments = models.TextField()
    refund_requested_time = models.DateTimeField(blank=True, null=True)
    service_fee = models.DecimalField(max_digits=30, decimal_places=2)
    list_price = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shoppingcart_orderitem'


class ShoppingcartPaidcourseregistration(models.Model):
    orderitem_ptr = models.ForeignKey(ShoppingcartOrderitem, primary_key=True)
    course_id = models.CharField(max_length=128)
    mode = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'shoppingcart_paidcourseregistration'


class SPaidcourseregistrationannotation(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    course_id = models.CharField(unique=True, max_length=128)
    annotation = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_paidcourseregistrationannotation'


class ShoppingcartRegistrationcoderedemption(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    order = models.ForeignKey(ShoppingcartOrder, blank=True, null=True)
    registration_code = models.ForeignKey(ShoppingcartCourseregistrationcode)
    redeemed_by = models.ForeignKey(AuthUser)
    redeemed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shoppingcart_registrationcoderedemption'


class SouthMigrationhistory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_name = models.CharField(max_length=255)
    migration = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'south_migrationhistory'


class SplashSplashconfig(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    change_date = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, blank=True, null=True)
    enabled = models.IntegerField()
    cookie_name = models.TextField()
    cookie_allowed_values = models.TextField()
    unaffected_usernames = models.TextField()
    redirect_url = models.CharField(max_length=200)
    unaffected_url_paths = models.TextField()

    class Meta:
        managed = False
        db_table = 'splash_splashconfig'


class StudentAnonymoususerid(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    anonymous_user_id = models.CharField(unique=True, max_length=32)
    course_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'student_anonymoususerid'


class StudentCourseaccessrole(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    org = models.CharField(max_length=64)
    course_id = models.CharField(max_length=255)
    role = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'student_courseaccessrole'


class StudentCourseenrollment(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField()
    mode = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'student_courseenrollment'


class StudentCourseenrollmentallowed(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    email = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    created = models.DateTimeField(blank=True, null=True)
    auto_enroll = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student_courseenrollmentallowed'


class StudentDashboardconfiguration(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    change_date = models.DateTimeField()
    changed_by = models.ForeignKey(AuthUser, blank=True, null=True)
    enabled = models.IntegerField()
    recent_enrollment_time_delta = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student_dashboardconfiguration'


class StudentLoginfailures(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    failure_count = models.IntegerField()
    lockout_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_loginfailures'


class StudentMoocCity(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255)
    state = models.ForeignKey('StudentMoocState')

    class Meta:
        managed = False
        db_table = 'student_mooc_city'


class StudentMoocPerson(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, unique=True)
    state = models.ForeignKey('StudentMoocState')
    city = models.ForeignKey(StudentMoocCity)
    pincode = models.IntegerField()
    aadhar_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_mooc_person'


class StudentMoocState(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'student_mooc_state'


class StudentPasswordhistory(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    password = models.CharField(max_length=128)
    time_set = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'student_passwordhistory'


class StudentPendingemailchange(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, unique=True)
    new_email = models.CharField(max_length=255)
    activation_key = models.CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'student_pendingemailchange'


class StudentPendingnamechange(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, unique=True)
    new_name = models.CharField(max_length=255)
    rationale = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'student_pendingnamechange'


class StudentUsersignupsource(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    site = models.CharField(max_length=255)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'student_usersignupsource'


class StudentUserstanding(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, unique=True,related_name='studentuser')
    account_status = models.CharField(max_length=31)
    changed_by = models.ForeignKey(AuthUser,related_name='studentchangedby')
    standing_last_changed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'student_userstanding'


class StudentUsertestgroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=32)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'student_usertestgroup'


class StudentUsertestgroupUsers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    usertestgroup = models.ForeignKey(StudentUsertestgroup)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'student_usertestgroup_users'


class SubmissionsScore(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    student_item = models.ForeignKey('SubmissionsStudentitem')
    submission = models.ForeignKey('SubmissionsSubmission', blank=True, null=True)
    points_earned = models.IntegerField()
    points_possible = models.IntegerField()
    created_at = models.DateTimeField()
    reset = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'submissions_score'


class SubmissionsScoresummary(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    student_item = models.ForeignKey('SubmissionsStudentitem', unique=True)
    highest = models.ForeignKey(SubmissionsScore,related_name='submissionhighest')
    latest = models.ForeignKey(SubmissionsScore,related_name='submissionlatest')

    class Meta:
        managed = False
        db_table = 'submissions_scoresummary'


class SubmissionsStudentitem(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    student_id = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    item_type = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'submissions_studentitem'


class SubmissionsSubmission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    uuid = models.CharField(max_length=36)
    student_item = models.ForeignKey(SubmissionsStudentitem)
    attempt_number = models.IntegerField()
    submitted_at = models.DateTimeField()
    created_at = models.DateTimeField()
    raw_answer = models.TextField()

    class Meta:
        managed = False
        db_table = 'submissions_submission'


class SurveySurveyanswer(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    form = models.ForeignKey('SurveySurveyform')
    field_name = models.CharField(max_length=255)
    field_value = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'survey_surveyanswer'


class SurveySurveyform(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    form = models.TextField()

    class Meta:
        managed = False
        db_table = 'survey_surveyform'


class TrackTrackinglog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    dtcreated = models.DateTimeField()
    username = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    event_source = models.CharField(max_length=32)
    event_type = models.CharField(max_length=512)
    event = models.TextField()
    agent = models.CharField(max_length=256)
    page = models.CharField(max_length=512, blank=True)
    time = models.DateTimeField()
    host = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'track_trackinglog'


class UserApiUsercoursetag(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    key = models.CharField(max_length=255)
    course_id = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_api_usercoursetag'


class UserApiUserorgtag(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    key = models.CharField(max_length=255)
    org = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_api_userorgtag'


class UserApiUserpreference(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_api_userpreference'


class VSSoftwaresecurephotoverification(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    status = models.CharField(max_length=100)
    status_changed = models.DateTimeField()
    user = models.ForeignKey(AuthUser,related_name='verifyuser')
    name = models.CharField(max_length=255)
    face_image_url = models.CharField(max_length=255)
    photo_id_image_url = models.CharField(max_length=255)
    receipt_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    submitted_at = models.DateTimeField(blank=True, null=True)
    reviewing_user = models.ForeignKey(AuthUser, blank=True, null=True,related_name='verifyreviewing')
    reviewing_service = models.CharField(max_length=255)
    error_msg = models.TextField()
    error_code = models.CharField(max_length=50)
    photo_id_key = models.TextField()
    window = models.ForeignKey(RMidcoursereverificationwindow, blank=True, null=True)
    display = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'verify_student_softwaresecurephotoverification'


class WikiArticle(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    current_revision = models.ForeignKey('WikiArticlerevision', unique=True, blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    owner = models.ForeignKey(AuthUser, blank=True, null=True)
    group = models.ForeignKey(AuthGroup, blank=True, null=True)
    group_read = models.IntegerField()
    group_write = models.IntegerField()
    other_read = models.IntegerField()
    other_write = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wiki_article'


class WikiArticleforobject(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    article = models.ForeignKey(WikiArticle)
    content_type = models.ForeignKey(DjangoContentType)
    object_id = models.IntegerField()
    is_mptt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wiki_articleforobject'


class WikiArticleplugin(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    article = models.ForeignKey(WikiArticle)
    deleted = models.IntegerField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wiki_articleplugin'


class WikiArticlerevision(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    revision_number = models.IntegerField()
    user_message = models.TextField()
    automatic_log = models.TextField()
    ip_address = models.CharField(max_length=15, blank=True)
    user = models.ForeignKey(AuthUser, blank=True, null=True)
    modified = models.DateTimeField()
    created = models.DateTimeField()
    previous_revision = models.ForeignKey('self', blank=True, null=True)
    deleted = models.IntegerField()
    locked = models.IntegerField()
    article = models.ForeignKey(WikiArticle)
    content = models.TextField()
    title = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'wiki_articlerevision'


class WikiArticlesubscription(models.Model):
    subscription_ptr = models.ForeignKey(NotifySubscription, unique=True)
    articleplugin_ptr = models.ForeignKey(WikiArticleplugin, primary_key=True)

    class Meta:
        managed = False
        db_table = 'wiki_articlesubscription'


class WikiAttachment(models.Model):
    reusableplugin_ptr = models.ForeignKey('WikiReusableplugin', primary_key=True)
    current_revision = models.ForeignKey('WikiAttachmentrevision', unique=True, blank=True, null=True)
    original_filename = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'wiki_attachment'


class WikiAttachmentrevision(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    revision_number = models.IntegerField()
    user_message = models.TextField()
    automatic_log = models.TextField()
    ip_address = models.CharField(max_length=15, blank=True)
    user = models.ForeignKey(AuthUser, blank=True, null=True)
    modified = models.DateTimeField()
    created = models.DateTimeField()
    previous_revision = models.ForeignKey('self', blank=True, null=True)
    deleted = models.IntegerField()
    locked = models.IntegerField()
    attachment = models.ForeignKey(WikiAttachment)
    file = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'wiki_attachmentrevision'


class WikiImage(models.Model):
    revisionplugin_ptr = models.ForeignKey('WikiRevisionplugin', primary_key=True)

    class Meta:
        managed = False
        db_table = 'wiki_image'


class WikiImagerevision(models.Model):
    revisionpluginrevision_ptr = models.ForeignKey('WikiRevisionpluginrevision', primary_key=True)
    image = models.CharField(max_length=2000, blank=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_imagerevision'


class WikiReusableplugin(models.Model):
    articleplugin_ptr = models.ForeignKey(WikiArticleplugin, primary_key=True)

    class Meta:
        managed = False
        db_table = 'wiki_reusableplugin'


class WikiReusablepluginArticles(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    reusableplugin = models.ForeignKey(WikiReusableplugin)
    article = models.ForeignKey(WikiArticle)

    class Meta:
        managed = False
        db_table = 'wiki_reusableplugin_articles'


class WikiRevisionplugin(models.Model):
    articleplugin_ptr = models.ForeignKey(WikiArticleplugin, primary_key=True)
    current_revision = models.ForeignKey('WikiRevisionpluginrevision', unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wiki_revisionplugin'


class WikiRevisionpluginrevision(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    revision_number = models.IntegerField()
    user_message = models.TextField()
    automatic_log = models.TextField()
    ip_address = models.CharField(max_length=15, blank=True)
    user = models.ForeignKey(AuthUser, blank=True, null=True)
    modified = models.DateTimeField()
    created = models.DateTimeField()
    previous_revision = models.ForeignKey('self', blank=True, null=True)
    deleted = models.IntegerField()
    locked = models.IntegerField()
    plugin = models.ForeignKey(WikiRevisionplugin)

    class Meta:
        managed = False
        db_table = 'wiki_revisionpluginrevision'


class WikiSimpleplugin(models.Model):
    articleplugin_ptr = models.ForeignKey(WikiArticleplugin, primary_key=True)
    article_revision = models.ForeignKey(WikiArticlerevision)

    class Meta:
        managed = False
        db_table = 'wiki_simpleplugin'


class WikiUrlpath(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    slug = models.CharField(max_length=50, blank=True)
    site = models.ForeignKey(DjangoSite)
    parent = models.ForeignKey('self', blank=True, null=True)
    lft = models.IntegerField()
    rght = models.IntegerField()
    tree_id = models.IntegerField()
    level = models.IntegerField()
    article = models.ForeignKey(WikiArticle)

    class Meta:
        managed = False
        db_table = 'wiki_urlpath'


class WorkflowAssessmentworkflow(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    status = models.CharField(max_length=100)
    status_changed = models.DateTimeField()
    submission_uuid = models.CharField(unique=True, max_length=36)
    uuid = models.CharField(unique=True, max_length=36)
    course_id = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'workflow_assessmentworkflow'


class WorkflowAssessmentworkflowstep(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    workflow = models.ForeignKey(WorkflowAssessmentworkflow)
    name = models.CharField(max_length=20)
    submitter_completed_at = models.DateTimeField(blank=True, null=True)
    assessment_completed_at = models.DateTimeField(blank=True, null=True)
    order_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'workflow_assessmentworkflowstep'

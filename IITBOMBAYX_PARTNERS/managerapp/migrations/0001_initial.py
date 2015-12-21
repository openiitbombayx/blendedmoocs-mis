# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AAitrainingworkflowTraining',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'assessment_aitrainingworkflow_training_examples',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AAssessmentfeedbackAssessments',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'assessment_assessmentfeedback_assessments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAiclassifier',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('classifier_data', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'assessment_aiclassifier',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAiclassifierset',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField()),
                ('algorithm_id', models.CharField(max_length=128)),
                ('course_id', models.CharField(max_length=40)),
                ('item_id', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'assessment_aiclassifierset',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAigradingworkflow',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36)),
                ('scheduled_at', models.DateTimeField()),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
                ('submission_uuid', models.CharField(max_length=128)),
                ('algorithm_id', models.CharField(max_length=128)),
                ('student_id', models.CharField(max_length=40)),
                ('item_id', models.CharField(max_length=128)),
                ('course_id', models.CharField(max_length=40)),
                ('essay_text', models.TextField()),
            ],
            options={
                'db_table': 'assessment_aigradingworkflow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAitrainingworkflow',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36)),
                ('algorithm_id', models.CharField(max_length=128)),
                ('scheduled_at', models.DateTimeField()),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
                ('item_id', models.CharField(max_length=128)),
                ('course_id', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'assessment_aitrainingworkflow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAssessment',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('submission_uuid', models.CharField(max_length=128)),
                ('scored_at', models.DateTimeField()),
                ('scorer_id', models.CharField(max_length=40)),
                ('score_type', models.CharField(max_length=2)),
                ('feedback', models.TextField()),
            ],
            options={
                'db_table': 'assessment_assessment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAssessmentfeedback',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('submission_uuid', models.CharField(unique=True, max_length=128)),
                ('feedback_text', models.TextField()),
            ],
            options={
                'db_table': 'assessment_assessmentfeedback',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAssessmentfeedbackoption',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('text', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'assessment_assessmentfeedbackoption',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAssessmentfeedbackOptions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'assessment_assessmentfeedback_options',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentAssessmentpart',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('feedback', models.TextField()),
            ],
            options={
                'db_table': 'assessment_assessmentpart',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentCriterion',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('order_num', models.IntegerField()),
                ('prompt', models.TextField()),
                ('label', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'assessment_criterion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentCriterionoption',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('order_num', models.IntegerField()),
                ('points', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('explanation', models.TextField()),
                ('label', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'assessment_criterionoption',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentPeerworkflow',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('student_id', models.CharField(max_length=40)),
                ('item_id', models.CharField(max_length=128)),
                ('course_id', models.CharField(max_length=40)),
                ('submission_uuid', models.CharField(unique=True, max_length=128)),
                ('created_at', models.DateTimeField()),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
                ('grading_completed_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'assessment_peerworkflow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentPeerworkflowitem',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('submission_uuid', models.CharField(max_length=128)),
                ('started_at', models.DateTimeField()),
                ('scored', models.IntegerField()),
            ],
            options={
                'db_table': 'assessment_peerworkflowitem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentRubric',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('content_hash', models.CharField(unique=True, max_length=40)),
                ('structure_hash', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'assessment_rubric',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentStudenttrainingworkflow',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('submission_uuid', models.CharField(unique=True, max_length=128)),
                ('student_id', models.CharField(max_length=40)),
                ('item_id', models.CharField(max_length=128)),
                ('course_id', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'assessment_studenttrainingworkflow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentStudenttrainingworkflowitem',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('order_num', models.IntegerField()),
                ('started_at', models.DateTimeField()),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'assessment_studenttrainingworkflowitem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentTrainingexample',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('raw_answer', models.TextField()),
                ('content_hash', models.CharField(unique=True, max_length=40)),
            ],
            options={
                'db_table': 'assessment_trainingexample',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ATrainingexampleOptionsSelected',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'assessment_trainingexample_options_selected',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthRegistration',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('activation_key', models.CharField(unique=True, max_length=32)),
            ],
            options={
                'db_table': 'auth_registration',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(unique=True, max_length=75)),
                ('password', models.CharField(max_length=128)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('is_superuser', models.IntegerField()),
                ('last_login', models.DateTimeField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserprofile',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('meta', models.TextField()),
                ('courseware', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=6, blank=True)),
                ('mailing_address', models.TextField(blank=True)),
                ('year_of_birth', models.IntegerField(null=True, blank=True)),
                ('level_of_education', models.CharField(max_length=6, blank=True)),
                ('goals', models.TextField(blank=True)),
                ('allow_certificate', models.IntegerField()),
                ('country', models.CharField(max_length=2, blank=True)),
                ('city', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'auth_userprofile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BulkEmailCourseauthorization',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(unique=True, max_length=255)),
                ('email_enabled', models.IntegerField()),
            ],
            options={
                'db_table': 'bulk_email_courseauthorization',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BulkEmailCourseemail',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('slug', models.CharField(max_length=128)),
                ('subject', models.CharField(max_length=128)),
                ('html_message', models.TextField(blank=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('course_id', models.CharField(max_length=255)),
                ('to_option', models.CharField(max_length=64)),
                ('text_message', models.TextField(blank=True)),
                ('template_name', models.CharField(max_length=255, blank=True)),
                ('from_addr', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'db_table': 'bulk_email_courseemail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BulkEmailCourseemailtemplate',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('html_template', models.TextField(blank=True)),
                ('plain_template', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'db_table': 'bulk_email_courseemailtemplate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BulkEmailOptout',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'bulk_email_optout',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CeleryTaskmeta',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('task_id', models.CharField(unique=True, max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('result', models.TextField(blank=True)),
                ('date_done', models.DateTimeField()),
                ('traceback', models.TextField(blank=True)),
                ('hidden', models.IntegerField()),
                ('meta', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'celery_taskmeta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CeleryTasksetmeta',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('taskset_id', models.CharField(unique=True, max_length=255)),
                ('result', models.TextField()),
                ('date_done', models.DateTimeField()),
                ('hidden', models.IntegerField()),
            ],
            options={
                'db_table': 'celery_tasksetmeta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CertificatesCertificatewhitelist',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('whitelist', models.IntegerField()),
            ],
            options={
                'db_table': 'certificates_certificatewhitelist',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CertificatesGeneratedcertificate',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('download_url', models.CharField(max_length=128)),
                ('grade', models.CharField(max_length=5)),
                ('course_id', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=32)),
                ('distinction', models.IntegerField()),
                ('status', models.CharField(max_length=32)),
                ('verify_uuid', models.CharField(max_length=32)),
                ('download_uuid', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
                ('error_reason', models.CharField(max_length=512)),
                ('mode', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'certificates_generatedcertificate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CGroupsCourseusergrouppartitiongroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('partition_id', models.IntegerField()),
                ('group_id', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'course_groups_courseusergrouppartitiongroup',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CircuitServercircuit',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('schematic', models.TextField()),
            ],
            options={
                'db_table': 'circuit_servercircuit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CourseActionStateCoursererunstate',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('course_key', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=50)),
                ('should_display', models.IntegerField()),
                ('message', models.CharField(max_length=1000)),
                ('source_course_key', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'course_action_state_coursererunstate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CourseCreatorsCoursecreator',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('state_changed', models.DateTimeField()),
                ('state', models.CharField(max_length=24)),
                ('note', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'course_creators_coursecreator',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CourseGroupsCourseusergroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('course_id', models.CharField(max_length=255)),
                ('group_type', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'course_groups_courseusergroup',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CourseGroupsCourseusergroupUsers',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'course_groups_courseusergroup_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CourseModesCoursemode',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('mode_slug', models.CharField(max_length=100)),
                ('mode_display_name', models.CharField(max_length=255)),
                ('min_price', models.IntegerField()),
                ('suggested_prices', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=8)),
                ('expiration_date', models.DateField(null=True, blank=True)),
                ('expiration_datetime', models.DateTimeField(null=True, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'course_modes_coursemode',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CourseModesCoursemodesarchive',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('mode_slug', models.CharField(max_length=100)),
                ('mode_display_name', models.CharField(max_length=255)),
                ('min_price', models.IntegerField()),
                ('suggested_prices', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=8)),
                ('expiration_date', models.DateField(null=True, blank=True)),
                ('expiration_datetime', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'course_modes_coursemodesarchive',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareCourseSubject',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('course_name', models.CharField(max_length=255)),
                ('subject_id', models.IntegerField()),
            ],
            options={
                'db_table': 'courseware_course_subject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareOfflinecomputedgrade',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField()),
                ('gradeset', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'courseware_offlinecomputedgrade',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareOfflinecomputedgradelog',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('seconds', models.IntegerField()),
                ('nstudents', models.IntegerField()),
            ],
            options={
                'db_table': 'courseware_offlinecomputedgradelog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareOrganization',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('org_id', models.CharField(max_length=255)),
                ('org_name', models.TextField()),
                ('state', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('url', models.TextField()),
                ('information', models.TextField()),
                ('image_name', models.CharField(max_length=255)),
                ('header_graphic', models.CharField(max_length=255)),
                ('contact_marketing', models.CharField(max_length=255)),
                ('contact_course_content', models.CharField(max_length=255)),
                ('contact_review_process', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'courseware_organization',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareStudentmodule',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('module_type', models.CharField(max_length=32)),
                ('module_id', models.CharField(max_length=255)),
                ('state', models.TextField(blank=True)),
                ('grade', models.FloatField(null=True, blank=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('max_grade', models.FloatField(null=True, blank=True)),
                ('done', models.CharField(max_length=8)),
                ('course_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'courseware_studentmodule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareStudentmodulehistory',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('version', models.CharField(max_length=255, blank=True)),
                ('created', models.DateTimeField()),
                ('state', models.TextField(blank=True)),
                ('grade', models.FloatField(null=True, blank=True)),
                ('max_grade', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'courseware_studentmodulehistory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareSubject',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('subject_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'courseware_subject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareXmodulestudentinfofield',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('field_name', models.CharField(max_length=64)),
                ('value', models.TextField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'courseware_xmodulestudentinfofield',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareXmodulestudentprefsfield',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('field_name', models.CharField(max_length=64)),
                ('module_type', models.CharField(max_length=64)),
                ('value', models.TextField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'courseware_xmodulestudentprefsfield',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CoursewareXmoduleuserstatesummaryfield',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('field_name', models.CharField(max_length=64)),
                ('usage_id', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'courseware_xmoduleuserstatesummaryfield',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DarkLangDarklangconfig',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('change_date', models.DateTimeField()),
                ('enabled', models.IntegerField()),
                ('released_languages', models.TextField()),
            ],
            options={
                'db_table': 'dark_lang_darklangconfig',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.IntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoCommentClientPermission',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'django_comment_client_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoCommentClientPermissionRoles',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'django_comment_client_permission_roles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoCommentClientRole',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('course_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'django_comment_client_role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoCommentClientRoleUsers',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'django_comment_client_role_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoOpenidAuthAssociation',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('server_url', models.TextField()),
                ('handle', models.CharField(max_length=255)),
                ('secret', models.TextField()),
                ('issued', models.IntegerField()),
                ('lifetime', models.IntegerField()),
                ('assoc_type', models.TextField()),
            ],
            options={
                'db_table': 'django_openid_auth_association',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoOpenidAuthNonce',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('server_url', models.CharField(max_length=2047)),
                ('timestamp', models.IntegerField()),
                ('salt', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'django_openid_auth_nonce',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoOpenidAuthUseropenid',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('claimed_id', models.TextField()),
                ('display_id', models.TextField()),
            ],
            options={
                'db_table': 'django_openid_auth_useropenid',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSite',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('domain', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'django_site',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryCrontabschedule',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('minute', models.CharField(max_length=64)),
                ('hour', models.CharField(max_length=64)),
                ('day_of_week', models.CharField(max_length=64)),
                ('day_of_month', models.CharField(max_length=64)),
                ('month_of_year', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'djcelery_crontabschedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryIntervalschedule',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('every', models.IntegerField()),
                ('period', models.CharField(max_length=24)),
            ],
            options={
                'db_table': 'djcelery_intervalschedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryPeriodictask',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('task', models.CharField(max_length=200)),
                ('args', models.TextField()),
                ('kwargs', models.TextField()),
                ('queue', models.CharField(max_length=200, blank=True)),
                ('exchange', models.CharField(max_length=200, blank=True)),
                ('routing_key', models.CharField(max_length=200, blank=True)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('enabled', models.IntegerField()),
                ('last_run_at', models.DateTimeField(null=True, blank=True)),
                ('total_run_count', models.IntegerField()),
                ('date_changed', models.DateTimeField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'djcelery_periodictask',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryPeriodictasks',
            fields=[
                ('ident', models.IntegerField(serialize=False, primary_key=True)),
                ('last_update', models.DateTimeField()),
            ],
            options={
                'db_table': 'djcelery_periodictasks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryTaskstate',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('state', models.CharField(max_length=64)),
                ('task_id', models.CharField(unique=True, max_length=36)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('tstamp', models.DateTimeField()),
                ('args', models.TextField(blank=True)),
                ('kwargs', models.TextField(blank=True)),
                ('eta', models.DateTimeField(null=True, blank=True)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('result', models.TextField(blank=True)),
                ('traceback', models.TextField(blank=True)),
                ('runtime', models.FloatField(null=True, blank=True)),
                ('retries', models.IntegerField()),
                ('hidden', models.IntegerField()),
            ],
            options={
                'db_table': 'djcelery_taskstate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjceleryWorkerstate',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=255)),
                ('last_heartbeat', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'djcelery_workerstate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EdxvalCoursevideo',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'edxval_coursevideo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EdxvalEncodedvideo',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('url', models.CharField(max_length=200)),
                ('file_size', models.IntegerField()),
                ('bitrate', models.IntegerField()),
            ],
            options={
                'db_table': 'edxval_encodedvideo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EdxvalProfile',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('profile_name', models.CharField(unique=True, max_length=50)),
                ('extension', models.CharField(max_length=10)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
            options={
                'db_table': 'edxval_profile',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EdxvalSubtitle',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('fmt', models.CharField(max_length=20)),
                ('language', models.CharField(max_length=8)),
                ('content', models.TextField()),
            ],
            options={
                'db_table': 'edxval_subtitle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EdxvalVideo',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('edx_video_id', models.CharField(unique=True, max_length=100)),
                ('client_video_id', models.CharField(max_length=255)),
                ('duration', models.FloatField()),
                ('created', models.DateTimeField()),
                ('status', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'edxval_video',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmbargoEmbargoedcourse',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(unique=True, max_length=255)),
                ('embargoed', models.IntegerField()),
            ],
            options={
                'db_table': 'embargo_embargoedcourse',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmbargoEmbargoedstate',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('change_date', models.DateTimeField()),
                ('enabled', models.IntegerField()),
                ('embargoed_countries', models.TextField()),
            ],
            options={
                'db_table': 'embargo_embargoedstate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmbargoIpfilter',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('change_date', models.DateTimeField()),
                ('enabled', models.IntegerField()),
                ('whitelist', models.TextField()),
                ('blacklist', models.TextField()),
            ],
            options={
                'db_table': 'embargo_ipfilter',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExternalAuthExternalauthmap',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('external_id', models.CharField(max_length=255)),
                ('external_domain', models.CharField(max_length=255)),
                ('external_credentials', models.TextField()),
                ('external_email', models.CharField(max_length=255)),
                ('external_name', models.CharField(max_length=255)),
                ('internal_password', models.CharField(max_length=31)),
                ('dtcreated', models.DateTimeField()),
                ('dtsignup', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'external_auth_externalauthmap',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FolditPuzzlecomplete',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('unique_user_id', models.CharField(max_length=50)),
                ('puzzle_id', models.IntegerField()),
                ('puzzle_set', models.IntegerField()),
                ('puzzle_subset', models.IntegerField()),
                ('created', models.DateTimeField()),
            ],
            options={
                'db_table': 'foldit_puzzlecomplete',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FolditScore',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('unique_user_id', models.CharField(max_length=50)),
                ('puzzle_id', models.IntegerField()),
                ('best_score', models.FloatField()),
                ('current_score', models.FloatField()),
                ('score_version', models.IntegerField()),
                ('created', models.DateTimeField()),
            ],
            options={
                'db_table': 'foldit_score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InstructorTaskInstructortask',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('task_type', models.CharField(max_length=50)),
                ('course_id', models.CharField(max_length=255)),
                ('task_key', models.CharField(max_length=255)),
                ('task_input', models.CharField(max_length=255)),
                ('task_id', models.CharField(max_length=255)),
                ('task_state', models.CharField(max_length=50, blank=True)),
                ('task_output', models.CharField(max_length=1024, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField()),
                ('subtasks', models.TextField()),
            ],
            options={
                'db_table': 'instructor_task_instructortask',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LicensesCoursesoftware',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('course_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'licenses_coursesoftware',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LicensesUserlicense',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('serial', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'licenses_userlicense',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LmsXblockXblockasidesconfig',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('change_date', models.DateTimeField()),
                ('enabled', models.IntegerField()),
                ('disabled_blocks', models.TextField()),
            ],
            options={
                'db_table': 'lms_xblock_xblockasidesconfig',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotesNote',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('uri', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('quote', models.TextField()),
                ('range_start', models.CharField(max_length=2048)),
                ('range_start_offset', models.IntegerField()),
                ('range_end', models.CharField(max_length=2048)),
                ('range_end_offset', models.IntegerField()),
                ('tags', models.TextField()),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'notes_note',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotifyNotification',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('message', models.TextField()),
                ('url', models.CharField(max_length=200, blank=True)),
                ('is_viewed', models.IntegerField()),
                ('is_emailed', models.IntegerField()),
                ('created', models.DateTimeField()),
            ],
            options={
                'db_table': 'notify_notification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotifyNotificationtype',
            fields=[
                ('key', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'db_table': 'notify_notificationtype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotifySettings',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('interval', models.IntegerField()),
            ],
            options={
                'db_table': 'notify_settings',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotifySubscription',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('object_id', models.CharField(max_length=64, blank=True)),
                ('send_emails', models.IntegerField()),
            ],
            options={
                'db_table': 'notify_subscription',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Oauth2Accesstoken',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('expires', models.DateTimeField()),
                ('scope', models.IntegerField()),
            ],
            options={
                'db_table': 'oauth2_accesstoken',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Oauth2Client',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('url', models.CharField(max_length=200)),
                ('redirect_uri', models.CharField(max_length=200)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('client_type', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'oauth2_client',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Oauth2Grant',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=255)),
                ('expires', models.DateTimeField()),
                ('redirect_uri', models.CharField(max_length=255)),
                ('scope', models.IntegerField()),
            ],
            options={
                'db_table': 'oauth2_grant',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Oauth2ProviderTrustedclient',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'oauth2_provider_trustedclient',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Oauth2Refreshtoken',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('expired', models.IntegerField()),
            ],
            options={
                'db_table': 'oauth2_refreshtoken',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PsychometricsPsychometricdata',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('studentmodule_id', models.IntegerField(unique=True)),
                ('done', models.IntegerField()),
                ('attempts', models.IntegerField()),
                ('checktimes', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'psychometrics_psychometricdata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RMidcoursereverificationwindow',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'reverification_midcoursereverificationwindow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SCourseregcodeitemannotation',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(unique=True, max_length=128)),
                ('annotation', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'shoppingcart_courseregcodeitemannotation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartCoupon',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('course_id', models.CharField(max_length=255)),
                ('percentage_discount', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('is_active', models.IntegerField()),
            ],
            options={
                'db_table': 'shoppingcart_coupon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartCouponredemption',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'shoppingcart_couponredemption',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartCourseregistrationcode',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=32)),
                ('course_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'shoppingcart_courseregistrationcode',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartDonationconfiguration',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('change_date', models.DateTimeField()),
                ('enabled', models.IntegerField()),
            ],
            options={
                'db_table': 'shoppingcart_donationconfiguration',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartInvoice',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('total_amount', models.FloatField()),
                ('company_name', models.CharField(max_length=255)),
                ('course_id', models.CharField(max_length=255)),
                ('internal_reference', models.CharField(max_length=255, blank=True)),
                ('is_valid', models.IntegerField()),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(max_length=255, blank=True)),
                ('address_line_3', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255, blank=True)),
                ('state', models.CharField(max_length=255, blank=True)),
                ('zip', models.CharField(max_length=15, blank=True)),
                ('country', models.CharField(max_length=64, blank=True)),
                ('recipient_name', models.CharField(max_length=255)),
                ('recipient_email', models.CharField(max_length=255)),
                ('customer_reference_number', models.CharField(max_length=63, blank=True)),
                ('company_contact_name', models.CharField(max_length=255)),
                ('company_contact_email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'shoppingcart_invoice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartOrder',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('currency', models.CharField(max_length=8)),
                ('status', models.CharField(max_length=32)),
                ('purchase_time', models.DateTimeField(null=True, blank=True)),
                ('bill_to_first', models.CharField(max_length=64)),
                ('bill_to_last', models.CharField(max_length=64)),
                ('bill_to_street1', models.CharField(max_length=128)),
                ('bill_to_street2', models.CharField(max_length=128)),
                ('bill_to_city', models.CharField(max_length=64)),
                ('bill_to_state', models.CharField(max_length=8)),
                ('bill_to_postalcode', models.CharField(max_length=16)),
                ('bill_to_country', models.CharField(max_length=64)),
                ('bill_to_ccnum', models.CharField(max_length=8)),
                ('bill_to_cardtype', models.CharField(max_length=32)),
                ('processor_reply_dump', models.TextField()),
                ('refunded_time', models.DateTimeField(null=True, blank=True)),
                ('company_name', models.CharField(max_length=255, blank=True)),
                ('company_contact_name', models.CharField(max_length=255, blank=True)),
                ('company_contact_email', models.CharField(max_length=255, blank=True)),
                ('recipient_name', models.CharField(max_length=255, blank=True)),
                ('recipient_email', models.CharField(max_length=255, blank=True)),
                ('customer_reference_number', models.CharField(max_length=63, blank=True)),
                ('order_type', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'shoppingcart_order',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartOrderitem',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=32)),
                ('qty', models.IntegerField()),
                ('unit_cost', models.DecimalField(max_digits=30, decimal_places=2)),
                ('line_desc', models.CharField(max_length=1024)),
                ('currency', models.CharField(max_length=8)),
                ('fulfilled_time', models.DateTimeField(null=True, blank=True)),
                ('report_comments', models.TextField()),
                ('refund_requested_time', models.DateTimeField(null=True, blank=True)),
                ('service_fee', models.DecimalField(max_digits=30, decimal_places=2)),
                ('list_price', models.DecimalField(null=True, max_digits=30, decimal_places=2, blank=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'shoppingcart_orderitem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartRegistrationcoderedemption',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('redeemed_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'shoppingcart_registrationcoderedemption',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SouthMigrationhistory',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('app_name', models.CharField(max_length=255)),
                ('migration', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'south_migrationhistory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SPaidcourseregistrationannotation',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(unique=True, max_length=128)),
                ('annotation', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'shoppingcart_paidcourseregistrationannotation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SplashSplashconfig',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('change_date', models.DateTimeField()),
                ('enabled', models.IntegerField()),
                ('cookie_name', models.TextField()),
                ('cookie_allowed_values', models.TextField()),
                ('unaffected_usernames', models.TextField()),
                ('redirect_url', models.CharField(max_length=200)),
                ('unaffected_url_paths', models.TextField()),
            ],
            options={
                'db_table': 'splash_splashconfig',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentAnonymoususerid',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('anonymous_user_id', models.CharField(unique=True, max_length=32)),
                ('course_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'student_anonymoususerid',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentCourseaccessrole',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('org', models.CharField(max_length=64)),
                ('course_id', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'student_courseaccessrole',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentCourseenrollment',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('course_id', models.CharField(max_length=255)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('is_active', models.IntegerField()),
                ('mode', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'student_courseenrollment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentCourseenrollmentallowed',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('email', models.CharField(max_length=255)),
                ('course_id', models.CharField(max_length=255)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('auto_enroll', models.IntegerField()),
            ],
            options={
                'db_table': 'student_courseenrollmentallowed',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentDashboardconfiguration',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('change_date', models.DateTimeField()),
                ('enabled', models.IntegerField()),
                ('recent_enrollment_time_delta', models.IntegerField()),
            ],
            options={
                'db_table': 'student_dashboardconfiguration',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentLoginfailures',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('failure_count', models.IntegerField()),
                ('lockout_until', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'student_loginfailures',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentMoocCity',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'student_mooc_city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentMoocPerson',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('pincode', models.IntegerField()),
                ('aadhar_id', models.BigIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'student_mooc_person',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentMoocState',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'student_mooc_state',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentPasswordhistory',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('time_set', models.DateTimeField()),
            ],
            options={
                'db_table': 'student_passwordhistory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentPendingemailchange',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('new_email', models.CharField(max_length=255)),
                ('activation_key', models.CharField(unique=True, max_length=32)),
            ],
            options={
                'db_table': 'student_pendingemailchange',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentPendingnamechange',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('new_name', models.CharField(max_length=255)),
                ('rationale', models.CharField(max_length=1024)),
            ],
            options={
                'db_table': 'student_pendingnamechange',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentUsersignupsource',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('site', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'student_usersignupsource',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentUserstanding',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('account_status', models.CharField(max_length=31)),
                ('standing_last_changed_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'student_userstanding',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentUsertestgroup',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'student_usertestgroup',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StudentUsertestgroupUsers',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'student_usertestgroup_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubmissionsScore',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('points_earned', models.IntegerField()),
                ('points_possible', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('reset', models.IntegerField()),
            ],
            options={
                'db_table': 'submissions_score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubmissionsScoresummary',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'submissions_scoresummary',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubmissionsStudentitem',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('student_id', models.CharField(max_length=255)),
                ('course_id', models.CharField(max_length=255)),
                ('item_id', models.CharField(max_length=255)),
                ('item_type', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'submissions_studentitem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubmissionsSubmission',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('uuid', models.CharField(max_length=36)),
                ('attempt_number', models.IntegerField()),
                ('submitted_at', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('raw_answer', models.TextField()),
            ],
            options={
                'db_table': 'submissions_submission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SurveySurveyanswer',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('field_name', models.CharField(max_length=255)),
                ('field_value', models.CharField(max_length=1024)),
            ],
            options={
                'db_table': 'survey_surveyanswer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SurveySurveyform',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(unique=True, max_length=255)),
                ('form', models.TextField()),
            ],
            options={
                'db_table': 'survey_surveyform',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TrackTrackinglog',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('dtcreated', models.DateTimeField()),
                ('username', models.CharField(max_length=32)),
                ('ip', models.CharField(max_length=32)),
                ('event_source', models.CharField(max_length=32)),
                ('event_type', models.CharField(max_length=512)),
                ('event', models.TextField()),
                ('agent', models.CharField(max_length=256)),
                ('page', models.CharField(max_length=512, blank=True)),
                ('time', models.DateTimeField()),
                ('host', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'track_trackinglog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserApiUsercoursetag',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('course_id', models.CharField(max_length=255)),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'user_api_usercoursetag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserApiUserorgtag',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('key', models.CharField(max_length=255)),
                ('org', models.CharField(max_length=255)),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'user_api_userorgtag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserApiUserpreference',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'user_api_userpreference',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VSSoftwaresecurephotoverification',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('status', models.CharField(max_length=100)),
                ('status_changed', models.DateTimeField()),
                ('name', models.CharField(max_length=255)),
                ('face_image_url', models.CharField(max_length=255)),
                ('photo_id_image_url', models.CharField(max_length=255)),
                ('receipt_id', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('submitted_at', models.DateTimeField(null=True, blank=True)),
                ('reviewing_service', models.CharField(max_length=255)),
                ('error_msg', models.TextField()),
                ('error_code', models.CharField(max_length=50)),
                ('photo_id_key', models.TextField()),
                ('display', models.IntegerField()),
            ],
            options={
                'db_table': 'verify_student_softwaresecurephotoverification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiArticle',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('group_read', models.IntegerField()),
                ('group_write', models.IntegerField()),
                ('other_read', models.IntegerField()),
                ('other_write', models.IntegerField()),
            ],
            options={
                'db_table': 'wiki_article',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiArticleforobject',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('object_id', models.IntegerField()),
                ('is_mptt', models.IntegerField()),
            ],
            options={
                'db_table': 'wiki_articleforobject',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiArticleplugin',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('deleted', models.IntegerField()),
                ('created', models.DateTimeField()),
            ],
            options={
                'db_table': 'wiki_articleplugin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiArticlerevision',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('revision_number', models.IntegerField()),
                ('user_message', models.TextField()),
                ('automatic_log', models.TextField()),
                ('ip_address', models.CharField(max_length=15, blank=True)),
                ('modified', models.DateTimeField()),
                ('created', models.DateTimeField()),
                ('deleted', models.IntegerField()),
                ('locked', models.IntegerField()),
                ('content', models.TextField()),
                ('title', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'wiki_articlerevision',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiAttachmentrevision',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('revision_number', models.IntegerField()),
                ('user_message', models.TextField()),
                ('automatic_log', models.TextField()),
                ('ip_address', models.CharField(max_length=15, blank=True)),
                ('modified', models.DateTimeField()),
                ('created', models.DateTimeField()),
                ('deleted', models.IntegerField()),
                ('locked', models.IntegerField()),
                ('file', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'wiki_attachmentrevision',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiReusablepluginArticles',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'wiki_reusableplugin_articles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiRevisionpluginrevision',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('revision_number', models.IntegerField()),
                ('user_message', models.TextField()),
                ('automatic_log', models.TextField()),
                ('ip_address', models.CharField(max_length=15, blank=True)),
                ('modified', models.DateTimeField()),
                ('created', models.DateTimeField()),
                ('deleted', models.IntegerField()),
                ('locked', models.IntegerField()),
            ],
            options={
                'db_table': 'wiki_revisionpluginrevision',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiUrlpath',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('slug', models.CharField(max_length=50, blank=True)),
                ('lft', models.IntegerField()),
                ('rght', models.IntegerField()),
                ('tree_id', models.IntegerField()),
                ('level', models.IntegerField()),
            ],
            options={
                'db_table': 'wiki_urlpath',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WorkflowAssessmentworkflow',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('status', models.CharField(max_length=100)),
                ('status_changed', models.DateTimeField()),
                ('submission_uuid', models.CharField(unique=True, max_length=36)),
                ('uuid', models.CharField(unique=True, max_length=36)),
                ('course_id', models.CharField(max_length=255)),
                ('item_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'workflow_assessmentworkflow',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WorkflowAssessmentworkflowstep',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('submitter_completed_at', models.DateTimeField(null=True, blank=True)),
                ('assessment_completed_at', models.DateTimeField(null=True, blank=True)),
                ('order_num', models.IntegerField()),
            ],
            options={
                'db_table': 'workflow_assessmentworkflowstep',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LinkedinLinkedin',
            fields=[
                ('user', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.AuthUser')),
                ('has_linkedin_account', models.IntegerField(null=True, blank=True)),
                ('emailed_courses', models.TextField()),
            ],
            options={
                'db_table': 'linkedin_linkedin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NotificationsArticlesubscription',
            fields=[
                ('articleplugin_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiArticleplugin')),
            ],
            options={
                'db_table': 'notifications_articlesubscription',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartCertificateitem',
            fields=[
                ('orderitem_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.ShoppingcartOrderitem')),
                ('course_id', models.CharField(max_length=128)),
                ('mode', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'shoppingcart_certificateitem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartCourseregcodeitem',
            fields=[
                ('orderitem_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.ShoppingcartOrderitem')),
                ('course_id', models.CharField(max_length=128)),
                ('mode', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'shoppingcart_courseregcodeitem',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartDonation',
            fields=[
                ('orderitem_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.ShoppingcartOrderitem')),
                ('donation_type', models.CharField(max_length=32)),
                ('course_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'shoppingcart_donation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ShoppingcartPaidcourseregistration',
            fields=[
                ('orderitem_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.ShoppingcartOrderitem')),
                ('course_id', models.CharField(max_length=128)),
                ('mode', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'shoppingcart_paidcourseregistration',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiArticlesubscription',
            fields=[
                ('articleplugin_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiArticleplugin')),
            ],
            options={
                'db_table': 'wiki_articlesubscription',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiImagerevision',
            fields=[
                ('revisionpluginrevision_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiRevisionpluginrevision')),
                ('image', models.CharField(max_length=2000, blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('height', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'wiki_imagerevision',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiReusableplugin',
            fields=[
                ('articleplugin_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiArticleplugin')),
            ],
            options={
                'db_table': 'wiki_reusableplugin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiRevisionplugin',
            fields=[
                ('articleplugin_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiArticleplugin')),
            ],
            options={
                'db_table': 'wiki_revisionplugin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiSimpleplugin',
            fields=[
                ('articleplugin_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiArticleplugin')),
            ],
            options={
                'db_table': 'wiki_simpleplugin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiAttachment',
            fields=[
                ('reusableplugin_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiReusableplugin')),
                ('original_filename', models.CharField(max_length=256, blank=True)),
            ],
            options={
                'db_table': 'wiki_attachment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WikiImage',
            fields=[
                ('revisionplugin_ptr', models.ForeignKey(primary_key=True, serialize=False, to='managerapp.WikiRevisionplugin')),
            ],
            options={
                'db_table': 'wiki_image',
                'managed': False,
            },
        ),
    ]

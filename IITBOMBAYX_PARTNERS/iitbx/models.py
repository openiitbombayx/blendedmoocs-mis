from django.db import models
from SIP.models import *

class gen_evaluations(models.Model):
     course =models.ForeignKey(edxcourses)
     sectionid =models.CharField(max_length=250) 
     sec_name  =models.CharField(max_length=250)
     subsec_id =models.CharField(max_length=250)
     subsec_name =models.CharField(max_length=250)
     type =models.CharField(max_length=150)
     release_date =models.DateTimeField()
     due_date =models.DateTimeField()
     total_weight =models.FloatField()
     grade_weight =models.FloatField()    
     total_marks=models.IntegerField(null = True)  
     
class gen_questions(models.Model):
      course =models.ForeignKey(edxcourses)
      eval =models.ForeignKey(gen_evaluations)
      qid =models.CharField(max_length=250) 
      q_name = models.CharField(max_length=250)    
      q_weight= models.FloatField() 
      prob_count=models.IntegerField()

class gen_markstable(models.Model):
	  edxuserid =models.IntegerField()
	  section= models.CharField(max_length=250)
	  total=models.CharField(max_length=25)
	  eval = models.TextField(null=True)


class gen_gradestable(models.Model):
	  edxuserid =models.IntegerField()
	  course = models.CharField(max_length=250)
	  grade =models.CharField(max_length=25)
	  eval = models.TextField(null=True)  

class gen_headings(models.Model):
      section=models.CharField(max_length=200)
      heading=models.TextField()

class gen_temp(models.Model):
      edxuserid=models.IntegerField(max_length=200)
      section=models.CharField(max_length=200)
      total=models.CharField(max_length=200)
      eval=models.TextField(max_length=200)

class gen_repout(models.Model):
      reportid=models.IntegerField()
      num_cols=models.IntegerField()
      A=models.TextField()
      B=models.TextField()
      C=models.TextField()
      D=models.TextField()
      E=models.TextField()
      F=models.TextField()
      G=models.TextField()
      H=models.TextField()
      I=models.TextField()
      J=models.TextField()





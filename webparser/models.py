from django.db import models


# Create your models here.
class Course(models.Model):
    CourseID = models.CharField(max_length=15, primary_key=True)
    CourseName = models.CharField(max_length=50)
    # GroupID = models.IntegerField()
    Description = models.TextField()


# class Prerequisite(models.Model):
#     GroupID1 = models.IntegerField()
#     GroupID2 = models.IntegerField()


class Slots(models.Model):
    CRN = models.IntegerField(primary_key=True)
    Type = models.CharField(max_length=50)
    Time = models.CharField(max_length=30)
    Section = models.CharField(max_length=30)
    Days = models.CharField(max_length=30)
    Location = models.CharField(max_length=150)
    Professor = models.CharField(max_length=50)
    CourseID = models.ForeignKey(Course)



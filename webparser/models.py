from django.db import models


# Create your models here.
class Course(models.Model):
    CourseID = models.CharField(max_length=15, primary_key=True)
    CourseName = models.CharField(max_length=50)
    Description = models.TextField()
    SameAS = models.TextField()
    PreReq = models.TextField()

    def __unicode__(self):
        return self.CourseID

    # def __str__(self):
    #     return self.CourseID

# class Prerequisite(models.Model):
#     GroupID1 = models.IntegerField()
#     GroupID2 = models.IntegerField()


class Course2Group(models.Model):
    CourseID = models.CharField(max_length=15, primary_key=True)
    GroupID = models.IntegerField()

    def __unicode__(self):
        return self.CourseID

    # def __str__(self):
    #     return self.CourseID


class Slots(models.Model):
    CRN = models.IntegerField(primary_key=True)
    Type = models.CharField(max_length=50)
    Time = models.CharField(max_length=70)
    Section = models.CharField(max_length=30)
    Days = models.CharField(max_length=30)
    Location = models.CharField(max_length=150)
    Professor = models.CharField(max_length=50)
    CourseID = models.CharField(max_length=15)

    def __unicode__(self):
        return self.CRN

    # def __str__(self):
    #     return self.CourseID



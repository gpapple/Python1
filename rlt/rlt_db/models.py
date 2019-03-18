from django.db import models

# Create your models here.
class School(models.Model):
    school_name = models.CharField(max_length=20)
    school_id = models.IntegerField()

    def __str__(self):
        return self.school_name

class Manager(models.Model):
    manager_name = models.CharField(max_length=20)
    manager_id = models.IntegerField()
    my_school = models.OneToOneField(School)

    def __str__(self):
        return self.manager_namess

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=5)
    my_school = models.ForeignKey("School")

    def __str__(self):
        return self.teacher_name
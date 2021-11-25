from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudentUser(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	mobile = models.CharField(max_length=15,null=True)
	image = models.FileField(null=True)
	gender = models.CharField(max_length=10,null=True)
	usertype = models.CharField(max_length=15,null=True)

	def __str__(self):
		return self.user.username


class Recruiter(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	mobile = models.CharField(max_length=15,null=True)
	image = models.FileField(null=True)
	gender = models.CharField(max_length=10,null=True)
	company = models.CharField(max_length=255,null=True)
	usertype = models.CharField(max_length=15,null=True)
	status = models.CharField(max_length=20,null=True)

	def __str__(self):
		return self.user.username


class Jobs(models.Model):
	recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=300)
	salary = models.FloatField(max_length=20)
	experience = models.CharField(max_length=50)
	location = models.CharField(max_length=255)
	skills = models.CharField(max_length=100)
	image = models.FileField()
	start_date = models.DateField()
	end_date = models.DateField()
	creation_date = models.DateField()

	def __str__(self):
		return self.title


class UserApply(models.Model):
	user = models.ForeignKey(StudentUser,on_delete=models.CASCADE)
	job = models.ForeignKey(Jobs,on_delete=models.CASCADE)
	resume = models.FileField(null=True)


class Contact(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	message = models.TextField()

	def __str__(self):
		return self.name
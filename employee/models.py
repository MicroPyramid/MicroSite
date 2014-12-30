from django.db import models
from django.conf import settings
from projects.models import Project


class Skills(models.Model):
	name = models.CharField(max_length=100)


class Designations(models.Model):
	name = models.CharField(max_length=100)


class Employee(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	designation = models.ForeignKey(Designations)
	skills = models.ManyToManyField(Skills)

	@property
	def author(self):
		return self.user.first_name + ' ' + self.user.last_name


class Leaves(models.Model):
	date = models.DateField()
	reason = models.CharField(max_length=2000)


class DailyReport(models.Model):
	employee = models.ForeignKey(settings.AUTH_USER_MODEL)
	project = models.ForeignKey(Project, blank=True, null=True)
	created_on = models.DateTimeField(auto_now_add=True)
	report = models.TextField(max_length=10000)


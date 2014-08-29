from django.db import models
from django.conf import settings


class Technology(models.Model):
	name = models.CharField(max_length=100)


class Project(models.Model):
	name =  models.CharField(max_length=100)
	client = models.CharField(max_length=100)
	slug = models.SlugField()
	notes = models.TextField()
	technologies = models.ManyToManyField(Technology)
	team_members = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='team_member')
	start_date = models.DateField()
	end_date = models.DateField()
	project_lead = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='project_lead')
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='created_by')
	daily_reports = models.BooleanField(default=False) # show daily reports to clients


class MileStone(models.Model):
	name = models.CharField(max_length=50)
	project = models.ForeignKey(Project, null=True, blank=True)
	deadline = models.DateField()
	desctrion = models.CharField(max_length=2000)


class Ticket(models.Model):
	project = models.ForeignKey(Project)
	milestone = models.ForeignKey(MileStone, blank=True, null=True)
	title = models.CharField(max_length=500)
	severity = models.CharField(max_length=20) # High, Low, Blocker, Medium
	ticket_type = models.CharField(max_length=20) # Design, Performance, Security, Feature, Bug,
	target_date = models.DateField(blank=True, null=True)
	assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL)
	finished_on = models.DateTimeField(blank=True, null=True)
	status = models.CharField(max_length=10) # Closed, Finished, Active


class Comment(models.Model):
	ticket = models.ForeignKey(Ticket)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_on = models.DateTimeField(auto_now_add=True)
	comments = models.CharField(max_length=2000)
	attachment = models.CharField(max_length=150)



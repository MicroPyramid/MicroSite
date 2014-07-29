from django.db import models
from django.conf import settings


class Skills(models.Model):
	name = models.CharField(max_length=100)


class Designations(models.Model):
	name = models.CharField(max_length=100)


class Employee(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	designation = models.ForeignKey(Designations)
	skills = models.ManyToManyField(Skills)


class Leaves(models.Model):
	date = models.DateField()
	reason = models.CharField(max_length=2000)

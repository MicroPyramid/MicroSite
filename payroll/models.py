from django.db import models
from django.conf import settings


class Skills(models.Model):
	name = models.charField(max_length=100)


class Designations(models.Model):
	name = models.charField(max_length=100)


class Employee(models.Model):
	user = models.foreignKey(settings.AUTH_USER_MODEL)
	designation = models.foreignKey(Designations)
	skills = models.manyToManyField(Skills)


class Leaves(models.Model):
	date = models.dateField()
	reason = models.charField(max_length=2000)

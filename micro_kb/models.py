from django.db import models
from django.conf import settings


class Category(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', blank=True, null=True)
	content = models.TextField()

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Doc(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField()
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tag)
	content = models.TextField()
	edited_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	edited_on = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('slug', 'category')

	def __unicode__(self):
		return self.title



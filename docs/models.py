from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', blank=True, null=True)
	content = models.TextField()


class Doc(models.Model):
	title
	slug
	category
	tags
	content
	edited_by
	edited_on

    class Meta:
        unique_together = ('slug', 'category')

    
class Resources(models.Model):
	name
	res_type


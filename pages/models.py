from django.db import models
from django.template import RequestContext

# Create your models here.
class page(models.Model):
	title = models.CharField(max_length=100, null=True, blank=True)
	content = models.TextField(max_length=20000)
	category = models.CharField(max_length=50)
	slug = models.SlugField()

class contact(models.Model):
	CONTACT_TYPES = (
					('Hire','Hire Us'),
					('Contact','Contact Us'),
					('Report','Report Issue'),
					)

	CONTACT_REQUIREMENTS = (
							('new site', 'New website from scratch'),
							('revamp', 'Revamp existing website / application'),
							('new features', 'Addition of new features'),
							('minor changes' , 'Minor design changes / tweaks'),
							('integration' ,'Integrate selected platform into my website'),
							('security', 'Enhance security to my application'),
							('performance', 'Tune performance of my application'),
							('maintenance', 'Maintenance of web application / server'),
							('payment gateway', 'Integrate / enhance payment gateway'),
							)

	ENQUERY_TYPES = (
					('general' , 'Request For Services'),
					('partnership' ,'Partnership Queries'),
					('media', 'Media Queries'),
					('general', 'General Queries'),
					('feedback', 'Website Feedback'),
					('others', 'Others'),
					)

	category = models.CharField(max_length=100, choices=CONTACT_TYPES)
	name = models.CharField(max_length=100)
	company = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	mobile = models.CharField(max_length=20)
	skype = models.CharField(max_length=50)
	country = models.CharField(max_length=100)
	budget = models.IntegerField()
	technology = models.CharField(max_length=100)
	requirements = models.CharField(max_length=200, choices=CONTACT_REQUIREMENTS)
	website = models.URLField(max_length=200)
	content = models.CharField(max_length=2000)
	ip = models.CharField(max_length=15)
	contacted_on = models.DateTimeField(auto_now_add=True)
	enquery_type = models.CharField(max_length=100, choices=ENQUERY_TYPES)
	callback_time = models.DateTimeField()
	timezone = models.CharField(max_length=10)
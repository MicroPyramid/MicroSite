from django.db import models
from django.template.defaultfilters import slugify

def create_slug(tempslug):
	slugcount = 0
	while True:
		try:
			page.objects.get(slug = tempslug)
			slugcount = slugcount + 1
			tempslug = tempslug + '-' + str(slugcount)
		except:
			return tempslug
			break

# Create your models here.
class page(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField(max_length=20000)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		tempslug = slugify(self.title)
		if self.id:
			existed_page = page.objects.get(pk=self.id)
			if existed_page.title != self.title:
				self.slug = create_slug(tempslug)
		else:
			self.slug = create_slug(tempslug)

		super(page, self).save(*args, **kwargs)


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


class Menu(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=5, default="off", blank=True)
    lvl = models.IntegerField()
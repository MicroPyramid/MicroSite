from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings

class Category(models.Model):
	name = models.CharField(max_length=20, unique = True)

class Tags(models.Model):
	name = models.CharField(max_length=20, unique = True)

class Post(models.Model):
	STATUS_CHOICE = (
					('D','Draft'),
					('P','Published'),
					('T','Trash'),
					)

	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateField(auto_now = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content = models.TextField(max_length=10000)
	category = models.ForeignKey(Category)
	tags = models.ManyToManyField(Tags)
	status = models.CharField(max_length=2, choices=STATUS_CHOICE)

	@property
	def google_author(self):
	    return self.user.google_plus_url

	def set_slug(self, slugtext):
	    self.slug = slugtext
	    self.save()

	def save(self, *args, **kwargs):
		tempslug = slugify(self.title)
		slugcount = 0
		while True:
			try:
				Post.objects.get(slug = tempslug)
				slugcount = slugcount + 1
				tempslug = slugify(self.title) + '-' + str(slugcount)
			except:
				self.slug = tempslug
				break

		super(Post, self).save(*args, **kwargs)


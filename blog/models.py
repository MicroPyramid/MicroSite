from django.db import models
from django.conf import settings

class Category(models.Model):
	name = models.CharField(max_length=20)

class Tags(models.Model):
	name = models.CharField(max_length=20)

class Post(models.Model):
	STATUS_CHOICE = (
					('D','Draft'),
					('P','Published'),
					('T','Trash'),
					)
	
	title = models.CharField(max_length=100)
	slug = models.SlugField()
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateField(auto_now = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	content = models.TextField(max_length=10000)
	category = models.ForeignKey(Cateory)
	tags = models.ManyToManyField(Tags)
	status = models.CharField(max_length=2, choices=STATUS_CHOICE)

	@property
	def google_author(self):
	    return self.user.google_plus_url

	@property
	def set_slug(self, slugtext):
	    return self.user.google_plus_url

	@property
	def save(self, *args, **kwargs):
        '''
        Overriden save method, to handle slugifying the name
        '''
        self.slug = slugify(self.title)
        cmp = []
        cmp = Post.objects.filter(slug=self.slug)
        if self.id <> cmp[0].id:
            l = 0
            slug = self.slug
            while cmp:
                l += 1
                self.slug = slug + '-' + str(l)
                cmp = Post.objects.filter(slug=self.slug)  

        super(Listing, self).save(args, kwargs)
	
from django.test import TestCase
from django.test import Client
from micro_blog.forms import BlogpostForm, CommentForm, BlogCategoryForm
from micro_blog.models import Category, Post, BlogComments
from micro_admin.models import User
from micro_blog.views import store_image, upload_photos, recent_photos
import unittest
from microsite.settings import BASE_DIR
from django.core.files import File


class micro_blog_forms_test(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')
		self.c=Category.objects.create(name='django', description='django desc')
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, featured_post = 'on', status = 'D')


	def test_blogpostform(self):
		form = BlogpostForm(data={'title':'python introduction','content':'This is content','category':self.c.id, 'featured_post':'on','status':'D'})
		self.assertTrue(form.is_valid())

	def test_commentform(self):
		form = CommentForm(data = {'post':self.p.id,'name':'Micro','email':'micro@micr.com', 'message':'Hai', 'weburl':'micro.com', 'phonenumber':'994477'})
		self.assertTrue(form.is_valid())

	def test_BlogCategoryForm(self):
		form = BlogCategoryForm(data = {'name':'django form','description':'django'})
		self.assertTrue(form.is_valid())


class micro_blogviews_get(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')
		self.c=Category.objects.create(name='django', description='django desc')
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, featured_post = 'on', status = 'D')
		comment = BlogComments.objects.create(name='john', post=self.p, email='ravi@mp.com',message='good post')

	def test_blog_get(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/index.html')

		response = self.client.get('/blog/admin/list/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-posts.html')

		response = self.client.get('/blog/admin/new/')
		self.assertTemplateUsed(response,'admin/blog/blog-new.html')
		self.assertEqual(response.status_code, 200)


		response = self.client.get('/blog/edit/python-introduction/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-edit.html')

		response = self.client.get('/blog/category-list/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-category-list.html')

		response = self.client.get('/blog/new-category/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-category.html')


		response = self.client.get('/blog/category/django/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/index.html')

		response = self.client.get('/blog/category/django/?page=1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/index.html')

		response = self.client.get('/blog/python-introduction/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/article.html')

		response = self.client.get('/blog/2014/12/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/index.html')

		response = self.client.get('/blog/2014/12/?page=1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/index.html')

		response = self.client.get('/blog/change/featured-state/python-introduction/')
		self.assertEqual(response.status_code, 302)

		response = self.client.get('/blog/delete/blog-post/python-introduction/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/blog/edit-category/django/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-category-edit.html')

		response = self.client.get('/blog/delete-category/django/')
		self.assertEqual(response.status_code, 302)

		
		##To activate comment
		response = self.client.get('/blog/edit-comment-status/1')
		self.assertEqual(response.status_code, 301)


		##to deactivate comment
		response = self.client.get('/blog/edit-comment-status/1')
		self.assertEqual(response.status_code, 301)

		response = self.client.get('/blog/delete/blog-comment/1')
		self.assertEqual(response.status_code,301)

		#sending correct data
		response = self.client.post('/blog/python-introduction/add-comment/',{'name':'john','email':'ravi@mp.com','message':'good post','weburl':'micropyramid.com'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('comment posted successfully' in response.content)

		#sending wrong data
		response = self.client.post('/blog/python-introduction/add-comment/',{})
		self.assertEqual(response.status_code,200)


class micro_blog_post_data(TestCase):

	'''
		Saving(POST data) data to the database in django
	'''

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')
		self.c=Category.objects.create(name='django', description='django desc')
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, featured_post = 'on', status = 'D')

	def test_blog_post(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/blog/?page=1')
		self.assertEqual(response.status_code, 200)

		# with correct input
		response = self.client.post('/blog/admin/new/',{'title':'python introduction','content':'This is content','category':self.c.id, 'featured_post':'on','status':'D', 'tags':'django'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('Blog Post created' in response.content)


		# with wrong input
		response = self.client.post('/blog/admin/new/',{'content':'This is content','category':self.c.id, 'featured_post':'on','status':'D'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('Blog Post created' in response.content)


		response = self.client.post('/blog/edit/python-introduction/', {'title':'python introduction','content':'This is content','category':self.c.id, 'featured_post':'on','status':'D'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('Blog Post edited' in response.content)

		response = self.client.post('/blog/edit/python-introduction/', {'content':'This is content','category':self.c.id, 'featured_post':'on','status':'D', 'tags':'python'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('Blog Post edited' in response.content)

		response = self.client.post('/blog/new-category/',{'name':'django form','description':'django'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('Blog category created' in response.content)

		response = self.client.post('/blog/new-category/',{'description':'django'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('Blog category created' in response.content)

		response = self.client.get('/blog/edit-category/django/')
		self.assertEqual(response.status_code, 200)

		response = self.client.post('/blog/edit-category/django-form/',{'name':'django new','description':'django'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('Blog category updated' in response.content)

		response = self.client.post('/blog/edit-category/django-new/',{'description':'django'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('Blog category updated' in response.content)

		response = self.client.get('/blog/tag/django/')
		self.assertEqual(response.status_code,200)

		response = self.client.get('/blog/tag/django/?page=1')
		self.assertEqual(response.status_code,200)


# class image_upload(unittest.TestCase):
# 	def setUp(self):
# 		img = open(BASE_DIR + '/static/site/images/1-c-n.png')
# 		img = File(img)

# 	def test_img(self):
# 		resp=store_image(img,'')
# 		self.assertTrue(resp)

	# def test_upload(self):
	# 	img = open()

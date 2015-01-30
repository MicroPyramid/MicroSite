from django.test import TestCase
from django.test import Client
from micro_blog.forms import BlogpostForm, BlogCategoryForm
from micro_blog.models import Category, Post
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
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, status = 'D')


	def test_blogpostform(self):
		form = BlogpostForm(data={'title':'python introduction','content':'This is content','category':self.c.id,'status':'D'})
		self.assertTrue(form.is_valid())

	def test_BlogCategoryForm(self):
		form = BlogCategoryForm(data = {'name':'django form','description':'django'})
		self.assertTrue(form.is_valid())


class micro_blogviews_get(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')
		self.c=Category.objects.create(name='django', description='django desc')
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c,status = 'D')

	def test_blog_get(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/index.html')

		response = self.client.get('/blog/list/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-posts.html')

		response = self.client.get('/blog/new-post/')
		self.assertTemplateUsed(response,'admin/blog/blog-new.html')
		self.assertEqual(response.status_code, 200)


		response = self.client.get('/blog/edit-post/python-introduction/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-edit.html')

		response = self.client.post('/blog/view-post/python-introduction/')
		self.assertEqual(response.status_code,200)


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

		response = self.client.get('/blog/edit-category/django/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-category-edit.html')

		response = self.client.get('/blog/delete-post/python-introduction/')
		self.assertEqual(response.status_code, 200)

		# response = self.client.post('/blog/view-post/python-introduction/')
		# self.assertEqual(response.status_code,200)

		response = self.client.get('/blog/delete-category/django/')
		self.assertEqual(response.status_code, 302)




class micro_blog_post_data(TestCase):

	'''
		Saving(POST data) data to the database in django
	'''

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')
		self.c=Category.objects.create(name='django', description='django desc')
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, status = 'D')

	def test_blog_post(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/blog/?page=1')
		self.assertEqual(response.status_code, 200)

		# with correct input
		response = self.client.post('/blog/new-post/',{'title':'python introduction','content':'This is content','category':self.c.id,'status':'D', 'tags':'django'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('Blog Post created' in response.content)


		# with wrong input
		response = self.client.post('/blog/new-post/',{'content':'This is content','category':self.c.id,'status':'D'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('Blog Post created' in response.content)


		response = self.client.post('/blog/edit-post/python-introduction/', {'title':'python introduction','content':'This is content','category':self.c.id,'status':'D'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('Blog Post edited' in response.content)

		response = self.client.post('/blog/edit-post/python-introduction/', {'content':'This is content','category':self.c.id, 'status':'D', 'tags':'python'})
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

		# img = open(BASE_DIR + '/static/site/images/1-c-n.png')
		# img = File(img)

		# response = self.client.get('/blog/ajax/photos/upload/')
		# self.assertEqual(response.status_code,200)

		# response = self.client.post('/blog/ajax/photos/upload/',{'upload':img})
		# self.assertEqual(response.status_code,200)

		# response = self.client.get('/blog/ajax/photos/recent/')
		# self.assertEqual(response.status_code,200)




# class image_upload(unittest.TestCase):
# 	def setUp(self):
# 		img = open(BASE_DIR + '/static/site/images/1-c-n.png')
# 		img = File(img)

# 	def test_img(self):
# 		img = open(BASE_DIR + '/static/site/images/1-c-n.png')
# 		img = File(img)
		# resp=store_image(img,'')
		# self.assertTrue(resp)

	# def test_upload(self):
	# 	img = upload_photos('')
	# 	print img


class micro_user_test(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('test@micropyramid.com', 'test')
		self.c=Category.objects.create(name='django', description='django desc')
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, status = 'D')

	def test_blog_without_user(self):

		user_login=self.client.login(email='test@micropyramid.com', password='test')
		self.assertTrue(user_login)
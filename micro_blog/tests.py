from django.test import TestCase
from django.test import Client
from micro_blog.forms import BlogpostForm, CommentForm, BlogCategoryForm
from micro_blog.models import Category, Post
from micro_admin.models import User


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

		response = self.client.get('/blog/python-introduction/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/article.html')

		response = self.client.get('/blog/2014/12/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'site/blog/index.html')

		response = self.client.get('/blog/change/featured-state/python-introduction/')
		self.assertEqual(response.status_code, 302)

		response = self.client.get('/blog/delete/blog-post/python-introduction/')
		self.assertEqual(response.status_code, 302)

		response = self.client.get('/blog/edit-category/django/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/blog/blog-category-edit.html')

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
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, featured_post = 'on', status = 'D')
		

	def test_blog_post(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)

		response = self.client.post('/blog/admin/new/',{'title':'python introduction','content':'This is content','category':self.c.id, 'featured_post':'on','status':'D'})
		self.assertEqual(response.status_code, 200)

		response = self.client.post('/blog/edit/python-introduction/', {'title':'python introduction','content':'This is content','category':self.c.id, 'featured_post':'on','status':'D'})
		self.assertEqual(response.status_code, 200)

		response = self.client.post('/blog/new-category/',{'name':'django form','description':'django'})
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/blog/edit-category/django/',{'name':'django form','description':'django'})
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/blog/edit-category/django/',{'name':'django form','description':'django'})
		self.assertEqual(response.status_code, 200)




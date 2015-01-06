from django.test import TestCase
from django.test import Client
from pages.forms import PageForm, MenuForm, ContactForm
from micro_admin.models import User
from pages.models import Page, Menu




class pages_forms_test(TestCase):

	def test_pageforms(self):
		self.client = Client()
		form = PageForm(data={'title':'Page', 'content': 'page_content'})
		self.assertTrue(form.is_valid())

	def test_Menuform(self):
		self.client = Client()
		form = MenuForm(data={'title':'main', 'url':'micro.in', 'status':'on'})
		self.assertTrue(form.is_valid())


	def test_ContactForm(self):
		self.client= Client()
		form = ContactForm(data={'full_name':'jagadeesh','message': 'sample', 'email':'john@gmail.com', 'phone':'94'})
		self.assertTrue(form.is_valid())


class pages_views_test(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('pyramid@mp.com', 'mp')
		self.p=Page.objects.create(title='Page', content= 'page_content')
		self.m= Menu.objects.create(title='main', url='micro.in', status='on', lvl=1)


	def test_views(self):
		user_login=self.client.login(email='pyramid@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/blog/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/portal/content/page/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/portal/content/page/new/')
		self.assertEqual(response.status_code, 200)

		response = self.client.post('/portal/content/page/new/',{'title':'Page2', 'content': 'page_content'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('Page created successfully' in response.content)

		response = self.client.post('/portal/content/page/new/',{'content': 'page_content'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('Page created successfully' in response.content)


		response = self.client.get('/portal/content/menu')
		self.assertEqual(response.status_code, 301)

		response = self.client.get('/portal/content/menu/add_menu_item/')
		self.assertEqual(response.status_code, 200)

		## With right input
		response = self.client.post('/portal/content/menu/add_menu_item/', {'title':'main', 'url':'micro.in', 'status':'on'})
		self.assertEqual(response.status_code, 200)

		##with wrong input
		response = self.client.post('/portal/content/menu/add_menu_item/', {'url':'micro.in', 'status':'on'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('successfully' in response.content)


		response = self.client.post('/portal/content/page/1/edit/',{'title':'Page', 'content': 'page_content'})
		self.assertEqual(response.status_code, 200)
		self.assertTrue('successfully' in response.content)


		response = self.client.post('/portal/content/page/1/edit/',{'content': 'page_content'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('successfully' in response.content)


		response = self.client.get('/portal/content/page/1/delete/')
		self.assertEqual(response.status_code, 302)

		##chnage menu status to off
		response = self.client.get('/portal/content/menu/1/status/')
		self.assertEqual(response.status_code, 302)

		##change menu status to on
		response = self.client.get('/portal/content/menu/1/status/')
		self.assertEqual(response.status_code, 302)

		response = self.client.get('/portal/content/menu/1/edit')
		self.assertTrue(response.status_code,200)

		response = self.client.post('/portal/content/menu/1/edit', {'title':'main2', 'url':'micro.in', 'status':'on'})
		self.assertTrue(response.status_code,200)


		response = self.client.post('/portal/content/menu/1/edit', {'url':'micro.in', 'status':'on'})
		self.assertTrue(response.status_code,200)
		self.assertFalse('successfully' in response.content)


		response = self.client.get('/portal/content/menu/1/delete')
		self.assertTrue(response.status_code,200)

		response = self.client.get('/Page2')
		self.assertEqual(response.status_code, 301)
from django.test import TestCase
from micro_admin.forms import *
from django.test import Client
from django.contrib.auth import login, authenticate, logout
from micro_admin.models import User



class Modelforms_test(TestCase):
	def test_userform(self):
		form = UserForm(data={'first_name':'Micro', 'last_name':'Pyramid','google_plus_url':'http://gmail.com/mp', 'email':'micro@micropyramid.com', 'password':'micro123','user_roles':'Admin','state':'Ap','address':'andhrapradesh','country':'india','phones':'9876543210','pincode':'505301','fb_profile':'http://facebook.com/maheshbabu','tw_profile':'http:twitter.com/maheshbabu','ln_profile':'http:linkedin.com/maheshbabu','about':'alot','mobile':'9876543210'})
		self.assertFalse(form.is_valid())

	def test_CareerForm(self):
		form = CareerForm(data={'title':'Python developer', 'experience':1, 'skills': 'Python, django', 'description':'sample description', 'num_of_opening':5,'url':'http://peeljobs.com/java/'})
		self.assertTrue(form.is_valid())


class Views_test(TestCase):
	'''
	user without login it directly redirects login page 302(redirect)
	'''

	def test_views(self):
		c = Client()

		#Login code test
		user = c.post('/portal/', {'email': 'micro@micropyramid.com', 'password': 'JNZUNA61EC'})
		self.assertEqual(user.status_code,200)

		resp = c.get('/portal/')
		self.assertEqual(resp.status_code,200)

		resp = c.get('/portal/contacts/')
		self.assertEqual(resp.status_code,302)

		resp = c.get('/portal/jobs/')
		self.assertEqual(resp.status_code, 302)

		resp = c.post('/portal/new-jobs/', {'title':'Python developer', 'experience':1, 'skills': 'Python, django', 'description':'sample description', 'num_of_opening':5,'url':'http://peeljobs.com/java/'})
		self.assertEqual(resp.status_code, 302)

		resp = c.get('/portal/edit-jobs/python-developer/')
		self.assertEqual(resp.status_code, 302)


class test_portal_admin(TestCase):
	'''
	setup user and "login" with user
	'''
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')

	def test_user_index(self):
		user = self.client.post('/portal/', {'email': 'mp@mp.com', 'password': 'mp'})
		self.assertEqual(user.status_code,200)

	def test_views_user(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/portal/contacts/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response,'admin/content/contacts/simplecontact.html')

		resp = self.client.get('/portal/jobs/')
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp,'admin/content/jobs/job_list.html')

		resp = self.client.post('/portal/new-jobs/', {'title':'Python developer', 'experience':1, 'skills': 'Python, django', 'description':'sample description', 'num_of_opening':5,'url':'http://peeljobs.com/java/'})
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('created' in resp.content)

		resp = self.client.post('/portal/new-jobs/', {'experience':1, 'skills': 'Python, django', 'description':'sample description', 'num_of_opening':5,'url':'http://peeljobs.com/java/'})
		self.assertEqual(resp.status_code, 200)
		self.assertFalse('created' in resp.content)

		resp = self.client.get('/portal/new-jobs/')
		self.assertEqual(resp.status_code, 200)

		resp = self.client.get('/portal/edit-jobs/1/')
		self.assertEqual(resp.status_code, 200)

		resp = self.client.post('/portal/edit-jobs/1/',{'title':'Python developer', 'experience':1, 'skills': 'Python, django', 'description':'sample description', 'num_of_opening':5,'url':'http://peeljobs.com/java/'})
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('updated successfully' in resp.content)

		resp = self.client.post('/portal/edit-jobs/1/',{'title':'Python developer', 'experience':1, 'skills': '', 'description':''})
		self.assertEqual(resp.status_code, 200)
		self.assertFalse('updated successfully' in resp.content)

		resp = self.client.get('/portal/delete-jobs/1/')
		self.assertEqual(resp.status_code, 302)

		resp = self.client.post('/portal/',{'email':'mp@mp.com','password':'mp'})
		self.assertEqual(resp.status_code,200)

		resp = self.client.get('/portal/out/')
		self.assertEqual(resp.status_code,302)



class user_test(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('micro@mp.com', 'micro')

	def test_views_user(self):
		user_login=self.client.login(email='micro@mp.com', password='micro')
		self.assertTrue(user_login)

		response = self.client.get('/portal/users/new/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'admin/user/new.html')

		response = self.client.get('/portal/users/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'admin/user/index.html')

		response = self.client.get('/portal/user/change-password/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'admin/user/change_password.html')

		response = self.client.get('/portal/user/change-password/')
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'admin/user/change_password.html')


		response = self.client.post('/portal/users/new/',{'first_name':'Micro', 'last_name':'Pyramid', 'email':'micro@micropyramid.com', 'password':'micro123','user_roles':'Admin', 'is_active': False,'state':'Ap','address':'ap','country':'india','phones':'9876543210','pincode':'505301','fb_profile':'http://facebook.com/maheshbabu','tw_profile':'http:twitter.com/maheshbabu','ln_profile':'http:linkedin.com/maheshbabu','about':' alot','mobile':'9876543210','google_plus_url':'http://gmail.com/mp'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('created successfully' in response.content)

		response = self.client.post('/portal/users/new/',{'first_name':'Micro','password':'micro123','user_roles':'Admin'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('created successfully' in response.content)

		response = self.client.get('/portal/users/edit/1/')
		self.assertEqual(response.status_code,200)


		response = self.client.post('/portal/users/edit/1/',{'first_name':'Micro-edit', 'last_name':'Pyramid', 'email':'micro-edit@micropyramid.com', 'password':'micro123','user_roles':'Admin', 'is_active': False,'state':'Ap','address':'ap','country':'india','phones':'9876543210','pincode':'505301','fb_profile':'http://facebook.com/maheshbabu','tw_profile':'http:twitter.com/maheshbabu','ln_profile':'http:linkedin.com/maheshbabu','about':' alot','mobile':'9876543210','google_plus_url':'http://gmail.com/mp'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('updated successfully' in response.content)

		response = self.client.post('/portal/users/edit/1/',{'last_name':'Pyramid', 'email':'micro-edit@micropyramid.com', 'password':'micro123','user_roles':'Admin'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('updated successfully' in response.content)

		response = self.client.post('/portal/user/change-password/',{'oldpassword':'micro12', 'newpassword':'pwd', 'retypepassword':'pwd'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('Password changed' in response.content)

		response = self.client.post('/portal/user/change-password/',{'oldpassword':'micro123', 'newpassword':'pwd', 'retypepassword':'pw'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('Password changed' in response.content)

		response = self.client.post('/portal/user/change-password/',{'oldpassword':'micro123', 'newpassword':'pwd', 'retypepassword':'pwd'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('Password changed' in response.content)

		response = self.client.post('/portal/user/change-password/',{'newpassword':'pwd', 'retypepassword':'pwd'})
		self.assertEqual(response.status_code,200)
		self.assertFalse('Password changed' in response.content)

		response = self.client.post('/portal/users/change-state/1/')
		self.assertEqual(response.status_code,302)

		response = self.client.post('/portal/users/change-state/1/')
		self.assertEqual(response.status_code,302)

from django.test import TestCase
from django import forms
from django.forms.models import ModelForm
import unittest
from employee.forms import *
from django.test import Client
from micro_admin.models import User




class TestBasic(unittest.TestCase):
    "Basic tests"

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)

class Modelforms_test(TestCase):

    def test_report(self):
        form = DailyReportForm(data = {'employee': 'test@micropyramid.com', 'report':'Sample report','date': '19-09-1990'})
        self.assertFalse(form.is_valid())

class Views_test(TestCase):

	'''
	Employee without login
	'''

	def test_employee_report(self):
		c = Client()
		resp = c.get('/portal/employee/')
		self.assertEqual(resp.status_code, 302)

		resp = c.get('/portal/employee/reports/new/')
		self.assertEqual(resp.status_code, 302)

		resp = c.get('/portal/employee/reports/edit/1/')
		self.assertEqual(resp.status_code, 302)

		resp = c.get('/portal/employee/reports/delete/1/')
		self.assertEqual(resp.status_code, 302)

class test_employee_as_admin(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')


	def test_views_user(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/portal/employee/')
		self.assertEqual(response.status_code, 200)

		##with right input
		resp = self.client.post('/portal/employee/reports/new/',{'employee': 'mp@mp.com', 'report':'Sample report','date':'09/09/1990'})
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('Report created successfully' in resp.content)

		## with wrong input
		resp = self.client.get('/portal/employee/reports/new/',{'report':'Sample report'})
		self.assertEqual(resp.status_code, 200)
		self.assertFalse('Report created successfully' in resp.content)


		resp = self.client.get('/portal/employee/reports/new/')
		self.assertEqual(resp.status_code, 200)

		resp = self.client.post('/portal/employee/reports/edit/1/')
		self.assertEqual(resp.status_code, 200)


		resp = self.client.post('/portal/employee/reports/delete/1/')
		self.assertEqual(resp.status_code, 200)


class test_employee(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('micro@mp.com', 'mp')
		self.u = str(self.user.id)

	def test_user(self):
		self.client = Client()
		user_login=self.client.login(email='micro@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/portal/employee/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/portal/employee/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/portal/employee/reports/' + self.u + '/')
		self.assertEqual(response.status_code, 200)


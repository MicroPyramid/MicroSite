from django.test import TestCase
from django import forms
from django.forms.models import ModelForm
import unittest
from projects.models import Project
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
        form = DailyReportForm(data = {'employee': 'ravi@mp.com', 'project': 'ravi', 'report':'Sample report'})
        self.assertTrue(form.is_valid())

class Views_test(TestCase):

	'''
	Employee without login
	'''

	def test_employee_report(self):
		c = Client()
		resp = c.get('/portal/staff/')
		self.assertEqual(resp.status_code, 302)

		resp = c.get('/portal/staff/reports/new/')
		self.assertEqual(resp.status_code, 302)

		resp = c.get('/portal/staff/reports/edit/1/')
		self.assertEqual(resp.status_code, 302)

		resp = c.get('/portal/staff/reports/delete/1/')
		self.assertEqual(resp.status_code, 302)

class test_employee_as_admin(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')
		self.project = Project.objects.create(name='Microsite',client='Ravi',slug='micro', notes='simple_site', start_date='2014-10-12',end_date='2014-10-10', created_by=self.user)



	def test_views_user(self):
		user_login=self.client.login(email='mp@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/portal/staff/')
		self.assertEqual(response.status_code, 200)

		##with right input
		resp = self.client.post('/portal/staff/reports/new/',{'employee': 'mp@mp.com', 'project':self.project.id, 'report':'Sample report'})
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('Report created successfully' in resp.content)

		## with wrong input
		resp = self.client.get('/portal/staff/reports/new/',{'project': 'MicoPyramid', 'report':'Sample report'})
		self.assertEqual(resp.status_code, 200)
		self.assertFalse('Report created successfully' in resp.content)


		resp = self.client.get('/portal/staff/reports/new/')
		self.assertEqual(resp.status_code, 200)

		resp = self.client.post('/portal/staff/reports/edit/1/')
		self.assertEqual(resp.status_code, 200)

		##wirth right input
		resp = self.client.post('/portal/staff/reports/edit/1/',{'project': 'MicoPyramid','project': 'MicoPyramid', 'report':'Sample report'})
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('successfully' in resp.content)


		##with wrong input
		resp = self.client.get('/portal/staff/reports/edit/1/',{'project': 'MicoPyramid','project': 'MicoPyramid', 'report':'Sample report'})
		self.assertEqual(resp.status_code, 200)
		self.assertFalse('successfully' in resp.content)


		resp = self.client.post('/portal/staff/reports/delete/1/')
		self.assertEqual(resp.status_code, 302)


class test_employee(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('micro@mp.com', 'mp')
		self.project = Project.objects.create(name='Microsite',client='Ravi',slug='micro', notes='simple_site', start_date='2014-10-12',end_date='2014-10-10', created_by=self.user)

	def test_user(self):
		self.client = Client()
		user_login=self.client.login(email='micro@mp.com', password='mp')
		self.assertTrue(user_login)

		response = self.client.get('/portal/staff/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/portal/staff/')
		self.assertEqual(response.status_code, 200)

		response = self.client.get('/portal/staff/reports/1/')
		self.assertEqual(response.status_code, 200)


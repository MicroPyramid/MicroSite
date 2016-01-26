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
        form = DailyReportForm(data={'employee': 'test@micropyramid.com', 'report': 'Sample report', 'date': '19-09-1990'})
        self.assertFalse(form.is_valid())


class Views_test(TestCase):
    '''
    Employee without login
    '''
    def test_employee_report(self):
        client = Client()
        response = client.get('/portal/employee/')
        self.assertEqual(response.status_code, 302)

        response = client.get('/portal/employee/reports/new/')
        self.assertEqual(response.status_code, 302)

        response = client.get('/portal/employee/reports/edit/1/')
        self.assertEqual(response.status_code, 302)

        response = client.get('/portal/employee/reports/delete/1/')
        self.assertEqual(response.status_code, 302)


class test_employee_as_admin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'microtest', 'mp')
        self.employee = User.objects.create_user("ravi@micropyramid.com", 'testemployee', 'pwd')

    def test_views_user(self):
        user_login=self.client.login(username='microtest', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/portal/employee/')
        self.assertEqual(response.status_code, 200)

        # Test case for new report view (new_report) with right input
        response = self.client.post('/portal/employee/reports/new/', {'employee': 'mp@mp.com', 'report': 'Sample report','date': '09/09/1990'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Report created successfully' in response.content)

        # Test cases for Report detail view (view_report)
        response = self.client.get('/portal/employee/reports/view/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/employee/reports/view/1/')
        self.assertEqual(response.status_code, 200)

        # Test cases for new report view (new_report) with wrong input
        response = self.client.post('/portal/employee/reports/new/', {'report': 'Sample report'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("'error': true" in response.content)

        response = self.client.get('/portal/employee/reports/new/')
        self.assertEqual(response.status_code, 200)

        # Test cases for edit report view (edit_report)
        response = self.client.get('/portal/employee/reports/edit/1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/portal/employee/reports/edit/1/', {'employee': 'mp@mp.com', 'report': 'Sample report edited','date': '09/09/1990'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Report updated successfully' in response.content)

        response = self.client.post('/portal/employee/reports/edit/1/')
        self.assertEqual(response.status_code, 200)

        # Test case for delete report view (delete_report)
        response = self.client.post('/portal/employee/reports/delete/1/')
        self.assertEqual(response.status_code, 200)


class test_employee(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('micro@mp.com', 'testuser', 'mp')
        self.employee = User.objects.create_user("ravi@micropyramid.com", 'testemployee', 'pwd')
        self.user_id = str(self.user.id)

    def test_user(self):
        self.client = Client()
        user_login = self.client.login(username='testuser', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/portal/employee/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/employee/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/employee/reports/' + self.user_id + '/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/employee/reports/' + str(self.employee.id) + '/')
        self.assertEqual(response.status_code, 200)


from django.test import TestCase
from django import forms
from django.forms.models import ModelForm
import unittest
from employee.forms import *
from django.test import Client




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
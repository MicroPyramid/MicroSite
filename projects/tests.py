from django.test import TestCase
from django.test import Client

# Create your tests here.
class test_projects(TestCase):
	def test_project_views(self):
		client=Client()
		response = self.client.get('/portal/projects/')
		self.assertEqual(response.status_code,200)
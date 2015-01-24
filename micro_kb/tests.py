from django.test import TestCase
from django.test import Client

# Create your tests here.

class test_micro_kb_views(TestCase):


	def test_views(self):
		client = Client()
		response = self.client.get('/portal/kb/')
		self.assertEqual(response.status_code,200)
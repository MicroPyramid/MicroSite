from django.test import TestCase
from django.test import Client


class frontend_test(TestCase):
	def test_home_page(self):
		c=Client()
		response = c.get('/')
		self.assertEqual(response.status_code, 200)

		responce = c.get('/careers/')
		self.assertEqual(responce.status_code, 200)

		response = c.post('/',{'full_name':'ravikumar','message':'how r u','email':'ravi@mp.com','phone':'94407'})
		self.assertEqual(response.status_code, 200)

	def test_xml(self):
		client=Client()
		response = self.client.get('/rss.xml')
		self.assertEqual(response.status_code,200)
		self.assertTrue('xml' in response.content)

		response = self.client.get('/sitemap.xml')
		self.assertEqual(response.status_code,200)
		self.assertTrue('xml' in response.content)

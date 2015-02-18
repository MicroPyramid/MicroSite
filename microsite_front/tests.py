from django.test import TestCase
from django.test import Client
from micro_admin.models import User
from micro_blog.models import Category, Post



class frontend_test(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_superuser('mp@mp.com', 'mp')
		self.c=Category.objects.create(name='django', description='django desc')
		self.p=Post.objects.create(title = 'python introduction',user = self.user,content = 'This is content',category = self.c, status = 'P')



	def test_home_page(self):
		c=Client()
		response = c.get('/')
		self.assertEqual(response.status_code, 200)

		responce = c.get('/careers/')
		self.assertEqual(responce.status_code, 200)

		response = c.post('/',{'full_name':'ravikumar','message':'how r u','email':'ravi@mp.com','phone':'94407'})
		self.assertEqual(response.status_code, 200)
		self.assertFalse('Thank you,  For Ur Message.!' in response.content)

		# response = c.post('/',{'phone':'9444'})
		# self.assertEqual(response.status_code, 200)


	def test_xml(self):
		client=Client()
		response = self.client.get('/rss.xml')
		self.assertEqual(response.status_code,200)
		self.assertTrue('xml' in response.content)

		response = self.client.get('/sitemap.xml')
		self.assertEqual(response.status_code,200)
		self.assertTrue('xml' in response.content)

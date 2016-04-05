from django.test import TestCase
from django.test import Client
from micro_admin.models import User
from micro_blog.models import Category, Post
from pages.models import Page


class frontend_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro', 'mp')
        self.c = Category.objects.create(
            name='Django', description='django desc')
        self.contactpage = Page.objects.create(title="Contact", is_active=True)
        self.category = Category.objects.create(
            name='python', description='django desc', is_display=True)

    def test_home_page(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

        # responce = c.get('/careers/')
        # self.assertEqual(responce.status_code, 200)

        response = c.post(
            '/', {'full_name': 'ravikumar', 'message': 'how r u', 'email': 'ravi@mp.com', 'phone': '94407'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('Thank you, For Ur Message') in response.content.decode('utf8'))

        # response = c.post('/',{'phone':'9444'})
        # self.assertEqual(response.status_code, 200)

    def test_xml(self):
        client = Client()
        response = self.client.get('/rss.xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/rss.xml?category=python')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/blog.rss')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/blog.rss?category=python')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

    def test_microsite_front_views(self):
        client = Client()

        # response = client.get('/books/git/index.html')
        # self.assertEqual(response.status_code, 200)

        response = client.get('/books/')
        self.assertEqual(response.status_code, 200)

        response = client.get('/sitemap/')
        self.assertEqual(response.status_code, 200)


class micro_front_views_test_with_employee(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro', 'mp')

    def test_microsite_front_employee_views(self):
        user_login = self.client.login(username='micro', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/tools/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/tools/url-checker/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/tools/url-checker/', {'urls': 'https://www.google.com/\nhttps://www.facebook.com/pages\
                        \nhttp://dsgfdg\ndsgfdg\nhttp:dsgfdg'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/tools/set-meta-data-for-S3-objects/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/tools/set-meta-data-for-S3-objects/', {'max_age': 'dfdf', 'expiry_time': 'dfdf', 'bucket_name': 'dffd', 'access_key': 'dfdsf', 'secret_key': 'dfd'})
        self.assertEqual(response.status_code, 200)

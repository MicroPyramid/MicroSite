from django.test import TestCase
from django.test import Client
from micro_admin.models import User
from micro_blog.models import Category, Post, Country
from pages.models import Page
from django.core.urlresolvers import reverse


class frontend_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro', 'mp')
        self.c = Category.objects.create(
            name='Django', description='django desc', max_published_blogs=5, min_published_blogs=2)
        self.contactpage = Page.objects.create(title="Contact", is_active=True)
        self.category = Category.objects.create(
            name='python', description='django desc', is_display=True, max_published_blogs=5, min_published_blogs=2)
        self.country = Country.objects.create(name='us', code='us', slug='us')
        self.blogppost = Post.objects.create(
            title='python introduction', user=self.user,
            content='This is content', category=self.category,
            meta_description='meta', status='P')

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
        # client = Client()
        response = self.client.get('/rss.xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/rss.xml?category=python')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/blog.rss?category=python')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/blog.rss')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/facebook.rss')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        response = self.client.get('/blog.rss?category=python')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

        kwargs = {'country_name': 'india', 'page_number': 1, 'page': 1}
        response = self.client.get('/sitemap.xml', kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('xml') in response.content.decode('utf8'))

    def test_microsite_front_views(self):
        client = Client()

        # response = client.get('/books/git/index.html')
        # self.assertEqual(response.status_code, 200)
        response = client.get('/books/')
        self.assertEqual(response.status_code, 200)

        url = reverse('sitemap')

        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        response = client.get(url, {'country_name': 'US'})
        self.assertEqual(response.status_code, 200)

        response = client.get(url, {'country_name': 'US', 'page_num': 1})
        self.assertEqual(response.status_code, 200)

        response = client.get(url, {'country_name': 'US', 'page_num': 'a'})
        self.assertEqual(response.status_code, 200)

        response = client.get(url, {'page_num': 1})
        self.assertEqual(response.status_code, 200)

        response = client.get(url, {'page_num': ''})
        self.assertEqual(response.status_code, 200)

        url = reverse('tools')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        url = reverse('s3_objects_set_metadata')
        user_login = self.client.login(username='micro', password='mp')
        self.assertTrue(user_login)

        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed('site/tools/s3_objects_set_metadata.html')

        response = self.client.post(url, {
            'expiry_time': 200, 'max_age': 48, 'bucket_name': 'new'})
        self.assertEqual(response.status_code, 301)


class micro_front_views_test_with_employee(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro', 'mp')

    def test_microsite_front_employee_views(self):
        user_login = self.client.login(username='micro', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/tools/url-checker/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/tools/url-checker/', {'urls': 'https://www.google.com/\nhttps://www.facebook.com/pages\
                        \nhttp://dsgfdg\ndsgfdg\nhttp:dsgfdg'})
        self.assertEqual(response.status_code, 200)

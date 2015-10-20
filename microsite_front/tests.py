from django.test import TestCase
from django.test import Client
from micro_admin.models import User
from micro_blog.models import Category, Post
from books.models import *
from pages.models import Page



class frontend_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro', 'mp')
        self.c = Category.objects.create(name='Django', description='django desc')
        self.blog = Post.objects.create(title='python introduction', user=self.user,
                                        content='This is content', category=self.c, status='P')
        self.python_book = Book.objects.create(admin=self.user, title="Python",
                                        status="Approved", privacy="Public")
        self.python_book.authors.add(self.user)
        self.topic1 = Topic.objects.create(book=self.python_book, title="Topic1", status="Approved")
        self.contactpage = Page.objects.create(title="Contact", is_active=True)



    def test_home_page(self):
        c=Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

        responce = c.get('/careers/')
        self.assertEqual(responce.status_code, 200)

        response = c.post('/',{'full_name':'ravikumar','message':'how r u','email':'ravi@mp.com','phone':'94407'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Thank you, For Ur Message' in response.content)

        # response = c.post('/',{'phone':'9444'})
        # self.assertEqual(response.status_code, 200)


    def test_xml(self):
        client=Client()
        response = self.client.get('/rss.xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('xml' in response.content)

        response = self.client.get('/rss.xml?category=Django')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('xml' in response.content)

        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('xml' in response.content)


    def test_microsite_front_views(self):
        client = Client()
        response = client.get('/tools/')
        self.assertEqual(response.status_code, 200)

        response = client.get('/tools/url-checker/')
        self.assertEqual(response.status_code, 200)

        response = client.post('/tools/url-checker/',
                        {'urls': 'https://www.google.com/\nhttps://www.facebook.com/pages\
                        \nhttp://dsgfdg\ndsgfdg\nhttp:dsgfdg'})
        self.assertEqual(response.status_code, 200)

        response = client.get('/tools/set-meta-data-for-S3-objects/')
        self.assertEqual(response.status_code, 200)

        response = client.post('/tools/set-meta-data-for-S3-objects/',
                        {'max_age': 'dfdf', 'expiry_time': 'dfdf', 'bucket_name': 'dffd',
                        'access_key': 'dfdsf','secret_key': 'dfd'})
        self.assertEqual(response.status_code, 200)



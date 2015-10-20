from django.test import TestCase
from django.test import Client
from pages.forms import PageForm, MenuForm, ContactForm, SimpleContactForm
from micro_admin.models import User
from pages.models import Page, Menu


class pages_forms_test(TestCase):

    def test_pageforms(self):
        self.client = Client()
        form = PageForm(data={'title': 'Page', 'content': 'page_content'})
        self.assertTrue(form.is_valid())

    def test_Menuform(self):
        self.client = Client()
        form = MenuForm(data={'title': 'main', 'url': 'micro.in', 'status': 'on'})
        self.assertTrue(form.is_valid())

    def test_SimpleContactForm(self):
        self.client = Client()
        form = SimpleContactForm(data={'full_name': 'jagadeesh', 'message': 'sample', 'email': 'john@gmail.com', 'phone': '9876543210'})
        self.assertTrue(form.is_valid())

    def test_ContactForm(self):
        self.client = Client()
        form = SimpleContactForm(data={'full_name':'jagadeesh','message': 'sample', 'email': 'john@gmail.com', 'phone': '94'})
        self.assertTrue(form.is_valid())


class pages_views_test_with_employee(TestCase):

    def setUp(self):
        self.client = Client()
        self.employee = User.objects.create_user('testemployee', "testemployee@micropyramid.com", 'pwd')

    def test_views_with_employee_login(self):
        user_login = self.client.login(username='testemployee@micropyramid.com', password='pwd')
        self.assertTrue(user_login)
        
        response = self.client.get('/portal/content/page/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/accessdenied.html')

        response = self.client.get('/portal/content/page/edit/1/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

        response = self.client.get('/portal/content/page/delete/1/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

        response = self.client.get('/portal/content/menu/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/accessdenied.html')

        response = self.client.get('/portal/content/menu/edit/1/')
        self.assertTrue(response.status_code, 404)
        self.assertTemplateUsed(response, 'admin/accessdenied.html')

        response = self.client.get('/portal/content/menu/delete_menu/1/')
        self.assertTrue(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

        response = self.client.get('/page-test/')
        self.assertTrue(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class pages_views_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('pyramid@mp.com', 'microtest', 'mp')
        self.page = Page.objects.create(title='Page', content= 'page_content')
        # self.menu = Menu.objects.create(title='main', url='micro.in', status='on', lvl=1)

    def test_views(self):
        user_login = self.client.login(username='microtest', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/content/page/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/content/page/new/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/portal/content/page/new/', {'title': 'Page2', 'content': 'page_content'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Page created successfully' in response.content)

        response = self.client.post('/portal/content/page/new/', {'content': 'page_content'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('Page created successfully' in response.content)

        response = self.client.get('/portal/content/menu')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/portal/content/menu/new/')
        self.assertEqual(response.status_code, 200)

        ## With right input
        response = self.client.post('/portal/content/menu/new/', {'title': 'main', 'url': 'micro.in/m', 'status': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Menu created successfully' in response.content)

        # Test cases for changing menu order
        response = self.client.post('/portal/content/menu/1/order/', {'mode': 'down'})
        self.assertTrue(response.status_code, 200)
        self.assertTrue('You cant move down' in response.content)

        response = self.client.post('/portal/content/menu/1/order/', {'mode': 'up'})
        self.assertTrue(response.status_code,200)
        self.assertTrue('You cant move up' in response.content)

        ##with wrong input
        response = self.client.post('/portal/content/menu/new/', {'url': 'micro.in/m', 'status': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('successfully' in response.content)

        response = self.client.get('/portal/content/page/edit/'+str(self.page.id)+'/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/content/menu/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/portal/content/page/edit/'+str(self.page.id)+'/', {'title': 'Page', 'content': 'page_content'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('successfully' in response.content)

        response = self.client.post('/portal/content/page/edit/'+str(self.page.id)+'/', {'content': 'page_content'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse('successfully' in response.content)

        ##chnage menu status to off
        response = self.client.get('/portal/content/menu/status/1/')
        self.assertEqual(response.status_code, 302)

        ##change menu status to on
        response = self.client.get('/portal/content/menu/status/1/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/portal/content/menu/edit/1/')
        self.assertTrue(response.status_code, 200)

        response = self.client.post('/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on'})
        self.assertTrue(response.status_code, 200)
        self.assertTrue('updated successfully' in response.content)

        response = self.client.post('/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on', 'parent': 1})
        self.assertTrue(response.status_code, 200)
        self.assertTrue('can not choose the same as parent' in response.content)

        response = self.client.post('/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on', 'parent': 2})
        self.assertTrue(response.status_code, 200)
        #self.assertTrue('can not choose the same as parent' in response.content)

        response = self.client.post('/portal/content/menu/edit/1/', {'url': 'micro.in', 'status': 'on'})
        self.assertTrue(response.status_code, 200)
        self.assertFalse('successfully' in response.content)

        response = self.client.post('/portal/content/menu/new/', {'title': 'menu2', 'url': 'http://micro.com/menu2', 'status': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Menu created successfully' in response.content)

        # Test cases for changing menu order
        response = self.client.post('/portal/content/menu/1/order/', {'mode': 'down'})
        self.assertTrue(response.status_code, 200)

        response = self.client.post('/portal/content/menu/1/order/', {'mode': 'up'})
        self.assertTrue(response.status_code, 200)

        response = self.client.post('/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on', 'parent': 2})
        self.assertTrue(response.status_code, 200)
        self.assertTrue('updated successfully' in response.content)

        response = self.client.get('/portal/content/menu/delete_menu/1/')
        self.assertTrue(response.status_code, 200)

        response = self.client.get('/page2/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/content/page/delete/'+str(self.page.id)+'/')
        self.assertEqual(response.status_code, 302)

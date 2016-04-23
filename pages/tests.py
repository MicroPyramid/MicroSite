from django.test import TestCase
from django.test import Client
from pages.forms import PageForm, MenuForm, SimpleContactForm
from micro_admin.models import User
from pages.models import Page, simplecontact, Contact


class pages_forms_test(TestCase):

    def test_pageforms(self):
        self.client = Client()
        form = PageForm(
            data={
                'title': 'Page',
                'content': 'page_content',
                'slug' : 'slug',
                'meta_title' : 'meta_title',
                'meta_description': 'description',
                'keywords': 'keywords'
            })
        self.assertTrue(form.is_valid())

    def test_Menuform(self):
        self.client = Client()
        form = MenuForm(
            data={'title': 'main', 'url': 'micro.in', 'status': 'on'})
        self.assertTrue(form.is_valid())

    def test_SimpleContactForm(self):
        self.client = Client()
        form = SimpleContactForm(
            data={'full_name': 'ashwin', 'message': 'sample', 'email': 'john@gmail.com', 'phone': '9876543210'})
        self.assertTrue(form.is_valid())

    def test_ContactForm(self):
        self.client = Client()
        form = SimpleContactForm(
            data={'full_name': 'ashwin', 'message': 'sample', 'email': 'john@gmail.com', 'phone': '94'})
        self.assertTrue(form.is_valid())


# models test
class pages_models_test(TestCase):

    def create_page(
            self,
            title="simple page",
            content="simple page content",
            slug="page",
            meta_title="meta_title",
            meta_description="description",
            keywords="keywords"):
        return Page.objects.create(title=title, content=content, slug=slug, meta_title=meta_title, meta_description=meta_description, keywords=keywords)

    def test_whatever_creation(self):
        w = self.create_page()
        self.assertTrue(isinstance(w, Page))
        self.assertEqual(w.__unicode__(), w.title)


class simplecontact_models_test(TestCase):

    def create_simplecontact(self, full_name="simple page", message="simple page content", email='contact@mp.com'):
        return simplecontact.objects.create(full_name=full_name, message=message, email=email)

    def test_simplecontact_creation(self):
        w = self.create_simplecontact()
        self.assertTrue(isinstance(w, simplecontact))
        self.assertEqual(w.__unicode__(), w.full_name)


class contact_models_test(TestCase):

    def create_contact(
            self, domain="simple page",
            domain_url="simple page content",
            country="",
            enquery_type="feedback",
            full_name="simple page",
            message="simple page content",
            email='contact@mp.com'):
        simple_contact = simplecontact.objects.create(
            full_name=full_name,
            message=message, email=email)
        return Contact.objects.create(
            domain="https://micropyramid.com",
            domain_url="https://micropyramid.com",
            country="india",
            enquery_type="feedback",
            contact_info=simple_contact)

    def test_whatever_creation(self):
        w = self.create_contact()
        self.assertTrue(isinstance(w, Contact))
        self.assertEqual(w.__unicode__(), w.contact_info.full_name)


class pages_views_test_with_employee(TestCase):

    def setUp(self):
        self.client = Client()
        self.employee = User.objects.create_user(
            'testemployee', "testemployee@micropyramid.com", 'pwd')

    def test_views_with_employee_login(self):
        user_login = self.client.login(
            username='testemployee@micropyramid.com', password='pwd')
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
        self.user = User.objects.create_superuser(
            'pyramid@mp.com', 'microtest', 'mp')
        self.page = Page.objects.create(title='Page', content='page_content', slug='page')
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

        response = self.client.post(
            '/portal/content/page/new/',
            {
                'title': 'Page2',
                'content': 'page_content',
                'slug' : 'slug',
                'meta_title' : 'meta_title',
                'meta_description': 'meta_description',
                'keywords': 'keywords'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('Page created successfully') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/content/page/new/',
            {
                'content': 'page_content',
                'meta_description': 'meta_description',
                'keywords': 'keywords'
            })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('Page created successfully') in response.content.decode('utf8'))

        response = self.client.get('/portal/content/menu')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/portal/content/menu/new/')
        self.assertEqual(response.status_code, 200)

        # With right input
        response = self.client.post(
            '/portal/content/menu/new/', {'title': 'main', 'url': 'micro.in/m', 'status': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('Menu created successfully') in response.content.decode('utf8'))

        # Test cases for changing menu order
        response = self.client.post(
            '/portal/content/menu/1/order/', {'mode': 'down'})
        self.assertTrue(response.status_code, 200)
        self.assertTrue(str('You cant move down') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/content/menu/1/order/', {'mode': 'up'})
        self.assertTrue(response.status_code, 200)
        self.assertTrue(str('You cant move up') in response.content.decode('utf8'))

        # with wrong input
        response = self.client.post(
            '/portal/content/menu/new/', {'url': 'micro.in/m', 'status': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('successfully') in response.content.decode('utf8'))

        response = self.client.get(
            '/portal/content/page/edit/'+str(self.page.id)+'/')
        self.assertEqual(response.status_code, 200)

        # chnage menu status to off
        response = self.client.get('/portal/content/page/status/'+str(self.page.id)+'/')
        self.assertEqual(response.status_code, 302)

        # change menu status to on
        response = self.client.get('/portal/content/page/status/'+str(self.page.id)+'/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/portal/content/menu/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/portal/content/page/edit/'+str(self.page.id)+'/',
            {
                'title': 'Page',
                'content': 'page_content',
                'slug' : 'page',
                'meta_title' : 'meta_title',
                'meta_description': 'meta_description',
                'keywords': 'keywords'
            })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('successfully') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/content/page/edit/'+str(self.page.id)+'/',
            {
                'content': 'page_content',
                'meta_description': 'meta_description',
                'keywords': 'keywords'
            })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('successfully') in response.content.decode('utf8'))

        # chnage menu status to off
        response = self.client.get('/portal/content/menu/status/1/')
        self.assertEqual(response.status_code, 302)

        # change menu status to on
        response = self.client.get('/portal/content/menu/status/1/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/portal/content/menu/edit/1/')
        self.assertTrue(response.status_code, 200)

        response = self.client.post(
            '/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on'})
        self.assertTrue(response.status_code, 200)
        self.assertTrue(str('updated successfully') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on', 'parent': 1})
        self.assertTrue(response.status_code, 200)
        self.assertTrue(
            str('can not choose the same as parent') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on', 'parent': 2})
        self.assertTrue(response.status_code, 200)
        # self.assertTrue('can not choose the same as parent' in response.content)

        response = self.client.post(
            '/portal/content/menu/edit/1/', {'url': 'micro.in', 'status': 'on'})
        self.assertTrue(response.status_code, 200)
        self.assertFalse(str('successfully') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/content/menu/new/', {'title': 'menu2', 'url': 'http://micro.com/menu2', 'status': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('Menu created successfully') in response.content.decode('utf8'))

        # Test cases for changing menu order
        response = self.client.post(
            '/portal/content/menu/1/order/', {'mode': 'down'})
        self.assertTrue(response.status_code, 200)

        response = self.client.post(
            '/portal/content/menu/1/order/', {'mode': 'up'})
        self.assertTrue(response.status_code, 200)

        response = self.client.post(
            '/portal/content/menu/edit/1/', {'title': 'main2', 'url': 'micro.in/menu', 'status': 'on', 'parent': 2})
        self.assertTrue(response.status_code, 200)
        self.assertTrue(str('updated successfully') in response.content.decode('utf8'))

        response = self.client.get('/portal/content/menu/delete_menu/1/')
        self.assertTrue(response.status_code, 200)

        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/'+str(self.page.slug)+'/')
        self.assertEqual(response.status_code, 200)
        

        response = self.client.get(
            '/portal/content/page/delete/'+str(self.page.id)+'/')
        self.assertEqual(response.status_code, 302)

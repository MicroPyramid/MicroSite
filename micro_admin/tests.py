from django.test import TestCase
from micro_admin.forms import *
from django.test import Client
from micro_admin.models import User
from pages.models import simplecontact


class Modelforms_test(TestCase):

    def test_userform(self):
        form = UserForm(
            data={
                'first_name': 'Micro', 'last_name': 'Pyramid', 'email': 'micro@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'state': 'MP', 'city': 'HYD',
                'area': 'KPHB', 'fb_profile': 'www.fb.com', 'last_login': '1970-01-01', 'date_of_birth': '1970-01-01',
                'address': 'ravi', 'tw_profile': 'www.twitter.com', 'ln_profile': 'www.linkedln.com',
                'google_plus_url': 'www.django.com', 'mobile': 123456, 'phones': 123456, 'pincode': 502286
            })

        self.assertTrue(form.is_valid())

    def test_CareerForm(self):
        form = CareerForm(
            data={
                'title': 'Python developer', 'experience': 1, 'skills': 'Python, django',
                'description': 'sample description', 'num_of_opening': 5, 'url': 'http://peeljobs.com/java/'
            })

        self.assertTrue(form.is_valid())


class Views_test(TestCase):

    '''
    User without login it directly redirects login page 302(redirect)
    '''

    def test_views(self):
        self.client = Client()

        # Login code test
        response = self.client.post(
            '/portal/', {'email': 'micro@micropyramid.com', 'password': 'JNZUNA61EC'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/contacts/')
        self.assertEqual(response.status_code, 302)

        # Testcase for user logout without login
        response = self.client.get('/portal/out/')
        self.assertEqual(response.status_code, 200)

        # resp = self.client.get('/portal/jobs/')
        # self.assertEqual(resp.status_code, 302)

        # resp = self.client.post('/portal/new-jobs/', {'title':'Python developer', 'experience':1, 'skills': 'Python, django', 'description':'sample description', 'num_of_opening':5,'url':'http://peeljobs.com/java/'})
        # self.assertEqual(resp.status_code, 302)

        # resp = self.client.get('/portal/edit-jobs/python-developer/')
        # self.assertEqual(resp.status_code, 302)


class test_portal_admin(TestCase):

    '''
    setup user and "login" with user
    '''

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'microtest', 'mp@mp.com', 'mp')
        self.inactive_user = User.objects.create(
            username='inactive', email='inactive@mp.com', user_roles='Admin', is_active=False)
        self.inactive_user.set_password('test')
        self.inactive_user.save()
        self.employee = User.objects.create_user(
            'testemployee', "test@gmail.com", 'pwd')
        self.simplecontact = simplecontact.objects.create(
                full_name='mp', message='test message',
                email='testuser@mp.com',
                phone='1234567890'
            )

    def test_user_index(self):
        # Testcase for forgot password with wrong input
        response = self.client.post(
            '/portal/forgot-password/', {'email': 'dfdfd'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            '"message": "Entered Email id is incorrect."' in response.content)

        # Testcase for forgot password with correct input
        response = self.client.post(
            '/portal/forgot-password/', {'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            '"message": "Password has been sent to your email sucessfully."' in response.content)

        # Testcase for user login with wrong input
        response = self.client.post(
            '/portal/', {'email': 'dfdfd', 'password': 'mpdfdf'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            '"message": "The username and password are incorrect."' in response.content)

        response = self.client.get('/portal/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'admin/login.html')

        # Testcase for user login with inactive user
        response = self.client.post(
            '/portal/', {'email': 'inactive@mp.com', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            '"message": "The password is valid, but the account has been disabled!"' in response.content)

        # Testcase for user login with correct input
        response = self.client.post(
            '/portal/', {'email': 'mp@mp.com', 'password': 'mp'})
        self.assertEqual(response.status_code, 200)

    def test_views_user(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/portal/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'admin/content/contacts/simplecontact.html')

        resp = self.client.get('/portal/contacts/' + str(self.simplecontact.id) + '/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/portal/clear_cache/')
        self.assertEqual(resp.status_code, 302)

        response = self.client.post(
            '/portal/', {'email': 'mp@mp.com', 'password': 'mp'})
        self.assertEqual(response.status_code, 200)

        # Testcase for user logout with login
        response = self.client.get('/portal/out/')
        self.assertEqual(response.status_code, 302)


class user_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'micro@mp.com', 'micro', 'mp')
        self.u = str(self.user.id)

    def test_views_user(self):
        user_login = self.client.login(username='micro', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/portal/users/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/user/new.html')

        response = self.client.get('/portal/users/blogposts/' + self.u + '/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/users/reports/' + self.u + '/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/users/' + self.u + '/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/portal/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/user/index.html')

        response = self.client.get('/portal/user/change-password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/user/change_password.html')

        response = self.client.get('/portal/user/change-password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/user/change_password.html')

        response = self.client.post(
            '/portal/users/new/',
            {
                'first_name': 'Micro', 'last_name': 'Pyramid', 'user_roles': 'Admin',
                'state': 'MP', 'city': 'HYD', 'area': 'KPHB'
            })

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/portal/users/new/',
            {
                'first_name': 'Micro', 'last_name': 'Pyramid', 'email': 'micro@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'state': 'MP', 'city': 'HYD', 'area': 'KPHB',
                'fb_profile': 'www.fb.com', 'last_login': '01/01/1970', 'date_of_birth': '01/01/1970',
                'address': 'ravi', 'tw_profile': 'www.twitter.com', 'ln_profile': 'www.linkedln.com',
                'google_plus_url': 'www.django.com', 'mobile': 123456, 'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('created successfully' in response.content)

        response = self.client.post(
            '/portal/users/new/',
            {
                'first_name': 'Microfb', 'last_name': 'Pyramid', 'email': 'microfb@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'state': 'MP', 'city': 'HYD', 'area': 'KPHB',
                'fb_profile': '', 'last_login': '01/01/1970', 'date_of_birth': '01/01/1970', 'address': 'ravi',
                'tw_profile': 'www.twitter.com', 'ln_profile': 'www.linkedln.com', 'google_plus_url': 'www.django.com',
                'mobile': 123456, 'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('created successfully' in response.content)

        response = self.client.post(
            '/portal/users/new/',
            {
                'first_name': 'Microtw', 'last_name': 'Pyramid', 'email': 'microtw@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'state': 'MP', 'city': 'HYD', 'area': 'KPHB',
                'fb_profile': 'www.fb.com', 'last_login': '01/01/1970', 'date_of_birth': '01/01/1970',
                'address': 'ravi', 'tw_profile': '', 'ln_profile': 'www.linkedln.com',
                'google_plus_url': 'www.django.com', 'mobile': 123456, 'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('created successfully' in response.content)

        response = self.client.post(
            '/portal/users/new/',
            {
                'first_name': 'Microln', 'last_name': 'Pyramid', 'email': 'microln@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'state': 'MP', 'city': 'HYD', 'area': 'KPHB',
                'fb_profile': 'www.fb.com', 'last_login': '01/01/1970', 'date_of_birth': '01/01/1970',
                'address': 'ravi', 'tw_profile': 'www.twitter.com', 'ln_profile': '',
                'google_plus_url': 'www.django.com', 'mobile': 123456, 'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('created successfully' in response.content)

        response = self.client.get('/portal/users/edit/' + self.u + '/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/portal/users/edit/' + self.u + '/',
            {
                'first_name': 'Micro-edit', 'last_name': 'Pyramid', 'email': 'micro-edit@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'is_active': False, 'state': 'MP',
                'city': 'HYD', 'area': 'KPHB', 'fb_profile': 'www.fb.com', 'last_login': '01/01/1970',
                'date_of_birth': '01/01/1970', 'address': 'ravi', 'tw_profile': 'www.twitter.com',
                'ln_profile': 'www.linkedln.com', 'google_plus_url': 'www.django.com', 'mobile': 123456,
                'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('updated successfully' in response.content)

        response = self.client.post(
            '/portal/users/edit/' + self.u + '/',
            {
                'first_name': 'Micro-edit', 'last_name': 'Pyramid', 'email': 'micro-edit@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'is_active': False, 'state': 'MP',
                'city': 'HYD', 'area': 'KPHB', 'fb_profile': '', 'last_login': '01/01/1970',
                'date_of_birth': '01/01/1970', 'address': 'ravi', 'tw_profile': 'www.twitter.com',
                'ln_profile': 'www.linkedln.com', 'google_plus_url': 'www.django.com', 'mobile': 123456,
                'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('updated successfully' in response.content)

        response = self.client.post(
            '/portal/users/edit/' + self.u + '/',
            {
                'first_name': 'Micro-edit', 'last_name': 'Pyramid', 'email': 'micro-edit@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'is_active': False, 'state': 'MP',
                'city': 'HYD', 'area': 'KPHB', 'fb_profile': 'www.fb.com', 'last_login': '01/01/1970',
                'date_of_birth': '01/01/1970', 'address': 'ravi', 'tw_profile': '',
                'ln_profile': 'www.linkedln.com', 'google_plus_url': 'www.django.com', 'mobile': 123456,
                'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('updated successfully' in response.content)

        response = self.client.post(
            '/portal/users/edit/' + self.u + '/',
            {
                'first_name': 'Micro-edit', 'last_name': 'Pyramid', 'email': 'micro-edit@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'is_active': False, 'state': 'MP',
                'city': 'HYD', 'area': 'KPHB', 'fb_profile': 'www.fb.com', 'last_login': '01/01/1970',
                'date_of_birth': '01/01/1970', 'address': 'ravi', 'tw_profile': 'www.twitter.com',
                'ln_profile': '', 'google_plus_url': 'www.django.com', 'mobile': 123456,
                'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('updated successfully' in response.content)

        response = self.client.post(
            '/portal/users/edit/' + self.u + '/',
            {
                'first_name': 'Micro-edit', 'last_name': 'Pyramid', 'email': 'micro-edit@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin', 'is_active': False, 'state': 'MP',
                'city': 'HYD', 'area': 'KPHB', 'fb_profile': 'www.fb.com', 'last_login': '01/01/1970',
                'date_of_birth': '01/01/1970', 'address': 'ravi', 'tw_profile': 'www.twitter.com',
                'ln_profile': 'www.linkedln.com', 'google_plus_url': '', 'mobile': 123456,
                'phones': 123456, 'pincode': 502286
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('updated successfully' in response.content)

        response = self.client.post(
            '/portal/users/edit/' + self.u + '/',
            {
                'last_name': 'Pyramid', 'email': 'micro-edit@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse('updated successfully' in response.content)

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'oldpassword': 'micro12', 'newpassword': 'pwd', 'retypepassword': 'pwd'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse('Password changed' in response.content)

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'oldpassword': 'micro123', 'newpassword': 'pwd', 'retypepassword': 'pw'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse('Password changed' in response.content)

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'oldpassword': 'micro123', 'newpassword': 'pwd', 'retypepassword': 'pwd'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Password changed' in response.content)

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'newpassword': 'pwd', 'retypepassword': 'pwd'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse('Password changed' in response.content)

        response = self.client.post('/portal/users/change-state/' + self.u + '/')
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/portal/users/change-state/' + self.u + '/')
        self.assertEqual(response.status_code, 302)

import json
from django.test import (TestCase,
                         Client)
from micro_admin.forms import *
from django.test import Client
from micro_admin.models import (User, career)
from django.core.urlresolvers import reverse


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
    setup user then "login" with the same user
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

    def test_user_index(self):
        # Testcase for forgot password with wrong input
        response = self.client.post(
            '/portal/forgot-password/', {'email': 'dfdfd'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            str('"message": "Entered Email id is incorrect."') in response.content.decode('utf8'))

        # Testcase for forgot password with correct input
        response = self.client.post(
            '/portal/forgot-password/', {'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            str('"message": "Password has been sent to your email sucessfully."') in response.content.decode('utf8'))

        # Testcase for user login with wrong input
        response = self.client.post(
            '/portal/', {'email': 'dfdfd', 'password': 'mpdfdf'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            str('"message": "The username and password are incorrect."') in response.content.decode('utf8'))

        response = self.client.get('/portal/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'admin/login.html')

        # Testcase for user login with inactive user
        response = self.client.post(
            '/portal/', {'email': 'inactive@mp.com', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            str('"message": "Your account has been disabled!"') in response.content.decode('utf8'))

        # Testcase for user login with correct input
        response = self.client.post(
            '/portal/', {'email': 'mp@mp.com', 'password': 'mp'})
        self.assertEqual(response.status_code, 200)

    def test_views_user(self):
        user_login = self.client.login(username='mp@mp.com', password='mp')
        self.assertTrue(user_login)

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
        self.assertTrue(str('created successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('created successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('created successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('created successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('updated successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('updated successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('updated successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('updated successfully') in response.content.decode('utf8'))

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
        self.assertTrue(str('updated successfully') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/users/edit/' + self.u + '/',
            {
                'last_name': 'Pyramid', 'email': 'micro-edit@micropyramid.com',
                'password': 'micro123', 'user_roles': 'Admin'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('updated successfully') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'oldpassword': 'micro12', 'newpassword': 'pwd', 'retypepassword': 'pwd'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('Password changed') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'oldpassword': 'micro123', 'newpassword': 'pwd', 'retypepassword': 'pw'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('Password changed') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'oldpassword': 'micro123', 'newpassword': 'pwd', 'retypepassword': 'pwd'
            })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str('Password changed') in response.content.decode('utf8'))

        response = self.client.post(
            '/portal/user/change-password/',
            {
                'newpassword': 'pwd', 'retypepassword': 'pwd'
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(str('Password changed') in response.content.decode('utf8'))

        response = self.client.post('/portal/users/change-state/' + self.u + '/')
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/portal/users/change-state/' + self.u + '/')
        self.assertEqual(response.status_code, 302)


# TEST CASES FOR models.py
class TestForUserModel(TestCase):

    def test_user_create(self):
        user = User(email='daniel@micropyramid.com',
                    user_roles='Developer',
                    date_of_birth='1980-01-01',
                    first_name='Daniel',
                    last_name='Janak',
                    gender='M')
        self.assertEqual(user.get_full_name(), 'Daniel Janak')
        self.assertEqual(user.get_short_name(), user.first_name)
        self.assertEqual(user.total_posts(), 0)
        self.assertEqual(user.drafted_posts(), 0)

class TestForcareerModel(TestCase):

    def test_career_obj_create(self):
        c = career(title="career",
                   slug="career",
                   experience=2,
                   skills="python, django",
                   description="for quick development")

        c.save()
        self.assertEqual(c.slug, 'career')
        c.delete()


# TEST CASES FOR users.py
class UserDetails(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.user = User(email='daniel@micropyramid.com',
                         user_roles='Developer',
                         date_of_birth='1980-01-01',
                         first_name='Daniel',
                         last_name='Janak',
                         is_admin=True,
                         gender='M')

        self.user.set_password('password')
        self.user.save()
        self.password = 'password'


class TestForUsers(UserDetails):

    def setUp(self):
        super(TestForUsers, self).setUp()

    def test_users_view(self):
        url = reverse('micro_admin:users')
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/user/index.html')

    def tearDown(self):
        super(TestForUsers, self).tearDown()


class TestForUserPasswordChange(UserDetails):

    def setUp(self):
        super(TestForUserPasswordChange, self).setUp()

    def test_user_password_change(self):
        # get
        url = reverse('micro_admin:change_password')
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # post
        context = {'oldpassword': '',
                   'newpassword': '',
                   'retypepassword': ''
                   }
        response = self.client.post(url, context)
        expected_data = {"response": {"newpassword": ["This field is required."],
                         "oldpassword": ["This field is required."],
                          "retypepassword": ["This field is required."]}, "error": True}
        self.assertEqual(json.loads(response.content.decode('utf-8')), expected_data)

        context = {'oldpassword': self.password,
                   'newpassword': '0000',
                   'retypepassword': '1111'
                   }
        response = self.client.post(url, context)
        expected_data = {"response": 
                        {"newpassword": "New password and ConformPasswords did not match"},\
                         "error": True}
        self.assertEqual(json.loads(response.content.decode('utf-8')), expected_data)
        context = {'oldpassword': self.password,
                   'newpassword': '0000',
                   'retypepassword': '0000'
                   }
        response = self.client.post(url, context)
        expected_data = {"response": "Password changed successfully", "error": False}
        self.assertEqual(json.loads(response.content.decode('utf-8')), expected_data)

    def tearDown(self):
        super(TestForUserPasswordChange, self).tearDown()

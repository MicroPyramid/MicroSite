from django.test import TestCase
from django.test import Client
from micro_blog.forms import (BlogpostForm, BlogCategoryForm,
                              CustomBlogSlugInlineFormSet)
from micro_blog.models import Category, Post, Tags, Post_Slugs
from micro_admin.models import User
from django.forms.models import inlineformset_factory
import json

BlogSlugFormSet = inlineformset_factory(
    Post, Post_Slugs,
    can_delete=True, extra=3, fields=('slug', 'is_active'),
    formset=CustomBlogSlugInlineFormSet
)


class micro_blog_forms_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            'mp@mp.com', 'micro-test', 'mp')
        self.category = Category.objects.create(
            name='django', description='django desc')
        self.blogppost = Post.objects.create(
            title='python introduction', user=self.user,
            content='This is content', category=self.category,
            status='D', meta_description='meta')

    def test_blogpostform(self):
        form = BlogpostForm(
            data={
                'title': 'python introduction', 'content': 'This is content',
                'category': self.category.id, 'status': 'D',
                'meta_description': 'meta', 'is_superuser': 'True',
                'excerpt': "Description"
                })
        self.assertTrue(form.is_valid())

    def test_BlogCategoryForm(self):
        form = BlogCategoryForm(
            data={'name': 'django form', 'description': 'django'})
        self.assertTrue(form.is_valid())

    def test_invalid_BlogSlugFormSetForm(self):
        form = BlogSlugFormSet(instance=Post())
        self.assertEqual(form.is_valid(), False)

    def test_valid_BlogSlugFormSetForm(self):
        form = BlogSlugFormSet({
            'slugs-MAX_NUM_FORMS': '1000',
            'slugs-TOTAL_FORMS': '3', 'slugs-MIN_NUM_FORMS': '0',
            'slugs-0-slug': 'python-introduction', 'slugs-1-slug': '',
            'slugs-2-slug': '', 'slugs-INITIAL_FORMS': '0',
            'slugs-0-id': '', 'slugs-1-id': '', 'slugs-2-id': '',
            'slugs-0-is_active': '', 'slugs-1-is_active': '',
            'slugs-2-is_active': '', 'slugs-0-blog': '',
            'slugs-1-blog': '', 'slugs-2-blog': ''
            }, instance=Post())
        self.assertTrue(form.is_valid())


# models test
class category_models_test(TestCase):

    def create_category(
        self, name="simple page", description="simple page content"
    ):
        return Category.objects.create(name=name, description=description)

    def test_category_creation(self):
        w = self.create_category()
        self.assertTrue(isinstance(w, Category))
        self.assertEqual(w.__unicode__(), w.name)
        # category_url = settings.SITE_BLOG_URL + "category/" + w.slug
        # self.assertEquals(w.get_url(), category_url)


# models test
class tags_models_test(TestCase):

    def create_tags(self, name="simple page"):
        return Tags.objects.create(name=name)

    def test_category_creation(self):
        w = self.create_tags()
        self.assertTrue(isinstance(w, Tags))
        self.assertEqual(w.__unicode__(), w.name)


# models test
class post_models_test(TestCase):

    def create_post(
                self,
                tag="simple page",
                category="simple page",
                description="simple page content",
                meta_description='meta_description',
                title="post",
                content="content",
                status="D"
            ):
        category = Category.objects.create(
            name=category, description=description)
        tag = Tags.objects.create(name=tag)
        user = User.objects.create_superuser('mp@mp.com', 'micro-test', 'mp')

        return Post.objects.create(
                category=category,
                user=user,
                content=content,
                title=title,
                status=status,
                meta_description=meta_description
            )

    def test_category_creation(self):
        w = self.create_post()
        self.assertTrue(isinstance(w, Post))
        self.assertEqual(w.__unicode__(), w.title)


class micro_blog_views_test_with_employee(TestCase):

    def setUp(self):
        self.client = Client()
        self.employee = User.objects.create_user(
            'testemployee', "testemployee@micropyramid.com", 'pwd')
        self.user = User.objects.create_user(
            'testuser', "testuser@micropyramid.com", 'userpws')
        self.category = Category.objects.create(
            name='category', description='category desc')
        self.django_category = Category.objects.create(
            name='django', description='category desc')
        self.blogpost = Post.objects.create(
            title='python blog',
            user=self.user,
            content='This is content',
            category=self.category,
            status='D'
        )
        self.blog_slug = Post_Slugs.objects.create(
            blog=self.blogpost, slug='python-blog', is_active=True)

    def test_views_with_employee_login(self):
        user_login = self.client.login(
            username='testemployee@micropyramid.com', password='pwd')
        self.assertTrue(user_login)
        response = self.client.get('/blog/new-category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/accessdenied.html')

        response = self.client.get('/blog/edit-category/django/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/accessdenied.html')

        response = self.client.get('/blog/delete-category/category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/accessdenied.html')

        response = self.client.get('/blog/edit-post/python-blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/accessdenied.html')

        # Testcase for contact with get
        response = self.client.get('/contact-usa/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/pages/contact-us.html')

        # Testcase for contact with post request simple
        response = self.client.post(
                '/contact-usa/',
                {
                    'full_name': 'client name',
                    'message': 'test message',
                    'email': 'testclient@mp.com',
                    'country': 'india'
                }
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(
                'Contact submitted successfully'
            ) in response.content.decode('utf8'))

        # Testcase for contact with post request advanced
        response = self.client.post(
                '/contact-usa/',
                {
                    'full_name': 'client name',
                    'message': 'test message',
                    'email': 'testclient@mp.com',
                    'phone': '1234567890',
                    'enquery_type': 'general',
                    'country': 'india'
                }
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(
                'Contact submitted successfully'
            ) in response.content.decode('utf8'))

        # Testcase for contact advanced wrong data
        response = self.client.post(
                '/contact-usa/',
                {
                    'full_name': '',
                    'message': 'test message',
                    'email': 'testclient@mp.com',
                    'country': 'india'
                }
            )

        self.assertEqual(response.status_code, 200)

        # Testcase for contact simple wrong data
        response = self.client.post(
                '/contact-usa/',
                {
                    'full_name': '',
                    'message': 'test message',
                    'email': 'testclient@mp.com',
                    'phone': '1234567890',
                    'enquery_type': 'general',
                    'country': 'india'
                }
            )

        self.assertEqual(response.status_code, 200)

        # Testcase for subscribe with get request
        response = self.client.get('/subscribe/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/pages/subscribe.html')

        # Testcase for subscribe
        response = self.client.post(
            '/subscribe/', {'email': '', 'is_blog': '', 'is_category': ''})
        self.assertEqual(response.status_code, 200)

        # Testcase for subscribe on site
        response = self.client.post(
                '/subscribe/',
                {
                    'email': 'testsubscriber@mp.com',
                    'is_blog': 'False',
                    'is_category': ''
                }
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(
                'Your email has been successfully subscribed.'
            ) in response.content.decode('utf8'))

        # Testcase for subscribe on blog
        response = self.client.post(
                '/subscribe/',
                {
                    'email': 'testsubscriber@mp.com',
                    'is_blog': 'True',
                    'is_category': ''
                }
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(
                'Your email has been successfully subscribed.'
            ) in response.content.decode('utf8'))

        # Testcase for subscribe on blog category
        response = self.client.post(
                '/subscribe/',
                {
                    'email': 'testsubscriber@mp.com',
                    'is_blog': 'True',
                    'is_category': str(self.category.id)
                }
            )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(
                'Your email has been successfully subscribed.'
            ) in response.content.decode('utf8'))


class micro_blogviews_get(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro', 'mp')
        self.category = Category.objects.create(
            name='django', description='django desc')
        self.blogppost = Post.objects.create(
            title='other python introduction',
            user=self.user,
            content='This is content',
            category=self.category,
            status='P'
        )
        self.blog_slug = Post_Slugs.objects.create(
            blog=self.blogppost, slug='other-python-introduction',
            is_active=True)
        self.tag = Tags.objects.create(name='testtag')
        self.blogppost.tags.add(self.tag)

    def test_blog_get(self):
        user_login = self.client.login(username='micro', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/blog/index.html')

        response = self.client.get('/blog/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/blog/blog-posts.html')

        response = self.client.get('/blog/new-post/')
        self.assertTemplateUsed(response, 'admin/blog/blog-new.html')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
                        '/blog/edit-post/other-python-introduction/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/blog/blog-edit.html')

        # chnage menu status to off
        response = self.client.get(
                '/blog/category/status/'+str(self.category.slug)+'/')
        self.assertEqual(response.status_code, 302)

        # change menu status to on
        response = self.client.get(
                '/blog/category/status/'+str(self.category.slug)+'/')
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            '/blog/' + str(
                self.blogppost.updated_on.year
            ) + '/' + str(self.blogppost.updated_on.month) + '/'
        )

        self.assertEqual(response.status_code, 302)

        response = self.client.get('/blog/category-list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/blog/blog-category-list.html')

        response = self.client.get('/blog/new-category/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/blog/blog-category.html')

        response = self.client.get('/blog/category/django/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/blog/index.html')

        response = self.client.get('/blog/tag/'+str(self.tag.slug)+'/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/blog/category/django/?page=1')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/blog/' + self.blogppost.slug + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/blog/article.html')

        response = self.client.get(
            '/blog/' + str(
                self.blogppost.updated_on.year
            ) + '/' + str(self.blogppost.updated_on.month) + '/'
        )

        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            '/blog/' +
            str(self.blogppost.updated_on.year) + '/' + str(
                self.blogppost.updated_on.month) + '/' + '?page=1'
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/blog/edit-category/django/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/blog/blog-category-edit.html')

        response = self.client.get('/blog/delete-category/django/')
        self.assertEqual(response.status_code, 302)


class micro_blog_post_data(TestCase):

    '''
        Saving(POST data) data to the database in django
    '''

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('mp@mp.com', 'micro', 'mp')
        self.category = Category.objects.create(
            name='django', description='django desc')
        self.blogppost = Post.objects.create(
            title='django introduction',
            user=self.user,
            content='This is content',
            category=self.category,
            status='D'
        )
        self.blog_slug = Post_Slugs.objects.create(
            blog=self.blogppost, slug='django-introduction', is_active=True)

    def test_blog_post(self):
        user_login = self.client.login(username='micro', password='mp')
        self.assertTrue(user_login)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/blog/?page=1')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/blog/?page=s')
        self.assertEqual(response.status_code, 302)

        # with correct input
        response = self.client.post('/blog/new-post/', {
            'title': 'python introduction 1', 'content': 'This is content',
            'category': self.category.id, 'status': 'D', 'tags': 'django',
            'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
            'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
            'slugs-0-slug': ['python-introduction-1'], 'slugs-1-slug': [''],
            'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            'excerpt': "Description"
        })
        self.assertRedirects(response, '/blog/list/')

        response = self.client.post('/blog/new-post/', {
            'title': 'introduction', 'content': 'This is content',
            'category': self.category.id, 'status': 'D', 'tags': 'django',
            'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
            'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
            'slugs-0-slug': ['introduction-1'], 'slugs-1-slug': [''],
            'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            'excerpt': "Description"})
        self.assertRedirects(response, '/blog/list/')

        response = self.client.post('/blog/new-post/', {
            'title': 'python', 'content': 'This is content',
            'category': self.category.id, 'status': 'P', 'tags': 'python',
            'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
            'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
            'slugs-0-slug': ['test-python'], 'slugs-1-slug': [''],
            'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            'excerpt': "Description"})
        self.assertRedirects(response, '/blog/list/')

        response = self.client.post('/blog/new-post/', {
            'title': 'Django', 'content': 'This is content',
            'category': self.category.id, 'status': 'T', 'tags': 'django',
            'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
            'slugs-TOTAL_FORMS': ['3'], 'slugs-MIN_NUM_FORMS': ['0'],
            'slugs-0-slug': ['django-1'], 'slugs-1-slug': [''],
            'slugs-2-slug': [''], 'slugs-INITIAL_FORMS': ['0'],
            'excerpt': "Description"})
        self.assertRedirects(response, '/blog/list/')

        response = self.client.post(
            '/blog/edit-post/python-introduction-1/',
            {
                'title': 'python introduction', 'content': 'This is content',
                'category': self.category.id, 'status': 'D',
                'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on'],
                'slugs-1-id': [''], 'slugs-2-id': [''], 'slugs-3-id': [''],
                'excerpt': "Description"
            }
        )
        self.assertRedirects(response, '/blog/list/')

        response = self.client.post(
            '/blog/edit-post/python-introduction-1/',
            {
                'title': 'python introduction',
                'excerpt': "Description",
                'content': 'This is edited content',
                'category': self.category.id, 'status': 'P',
                'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': ['python-2'], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on'],
                'slugs-1-is_active': ['on']
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blog_form'].is_valid(), True)
        self.assertEqual(
            response.context['blogslugs_formset'].is_valid(), False)
        self.assertTrue(
            '["Only one slug can be active at a time."]' in json.dumps(
                response.context['blogslugs_formset'].non_form_errors()
            ))

        response = self.client.post(
            '/blog/edit-post/python-introduction-1/',
            {
                'title': 'python introduction', 'content': 'This is content',
                'category': self.category.id, 'status': 'T', 'tags': 'django',
                'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on'],
                'excerpt': "Description"
            }
        )
        self.assertRedirects(response, '/blog/list/')

        response = self.client.post(
            '/blog/edit-post/python-introduction-1/',
            {
                'content': 'This is content', 'category': self.category.id,
                'status': 'D', 'tags': 'python',
                'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'excerpt': "Description",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blog_form'].is_valid(), False)
        self.assertTrue(
            '{"title": ["This field is required."]}' in json.dumps(
                response.context['blog_form'].errors
            ))

        response = self.client.post(
            '/blog/edit-post/python-introduction-1/',
            {
                'title': 'python introduction', 'content': 'This is content',
                'category': self.category.id, 'status': 'T',
                'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'excerpt': "Description",
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on']
            }
        )
        self.assertRedirects(response, '/blog/list/')

        response = self.client.post(
            '/blog/edit-post/python-introduction-1/',
            {
                'title': 'python introduction', 'content': 'This is content',
                'category': self.category.id, 'status': 'D',
                'meta_description': 'meta', 'slugs-MAX_NUM_FORMS': ['1000'],
                'slugs-TOTAL_FORMS': ['4'], 'slugs-MIN_NUM_FORMS': ['0'],
                'slugs-0-slug': ['python-introduction-1'],
                'slugs-1-slug': [''], 'slugs-2-slug': [''],
                'slugs-3-slug': [''], 'slugs-0-id': ['2'],
                'slugs-INITIAL_FORMS': ['1'], 'slugs-0-is_active': ['on'],
                'slugs-1-is_active': ['on'], 'excerpt': "Description",
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['blogslugs_formset'].is_valid(), False)
        self.assertTrue(
            '[{}, {"slug": ["This field is required."]}, {}, {}]' in json.dumps(
                response.context['blogslugs_formset'].errors
            ))

        response = self.client.get('/blog/edit-post/python-introduction-1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/blog/edit-post/test-python/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/blog/test-python/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site/blog/article.html')

        response = self.client.get('/blog/python-introduction-1/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/blog/new-category/',
            {'name': 'django form', 'description': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(
            'Blog category created') in response.content.decode('utf8'))

        response = self.client.post(
            '/blog/new-category/', {'description': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(
            'Blog category created') in response.content.decode('utf8'))

        response = self.client.get('/blog/edit-category/django/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/blog/edit-category/django-form/',
            {'name': 'django new', 'description': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(
            'Blog category updated') in response.content.decode('utf8'))

        response = self.client.post(
            '/blog/edit-category/django-new/', {'description': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(str(
            'Blog category updated') in response.content.decode('utf8'))

        response = self.client.get('/blog/tag/django/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/blog/tag/django/?page=1')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/blog/tag/django/?page=e')
        self.assertEqual(response.status_code, 404)

        # img = open(BASE_DIR + '/static/site/images/1-c-n.png')
        # img = File(img)

        # response = self.client.get('/blog/ajax/photos/upload/')
        # self.assertEqual(response.status_code,200)

        # response = self.client.post('/blog/ajax/photos/upload/',{'upload':img})
        # self.assertEqual(response.status_code,200)

        # response = self.client.get('/blog/ajax/photos/recent/')
        # self.assertEqual(response.status_code,200)


# class image_upload(unittest.TestCase):
#   def setUp(self):
#       img = open(BASE_DIR + '/static/site/images/1-c-n.png')
#       img = File(img)

#   def test_img(self):
#       img = open(BASE_DIR + '/static/site/images/1-c-n.png')
#       img = File(img)
        # resp=store_image(img,'')
        # self.assertTrue(resp)

    # def test_upload(self):
    #   img = upload_photos('')
    #   print img


class micro_user_test(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'test@micropyramid.com', 'testuser', 'test')
        self.category = Category.objects.create(
            name='django', description='django desc')
        self.blogppost = Post.objects.create(
            title='new python introduction', user=self.user,
            content='This is content', category=self.category,
            status='D')

    def test_blog_without_user(self):

        user_login = self.client.login(username='testuser', password='test')
        self.assertTrue(user_login)

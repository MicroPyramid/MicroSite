from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
from micro_blog.models import Category, Tags, Post, Subscribers, create_slug
from pages.models import simplecontact, Contact
import math
# from django.core.files.storage import default_storage
from micro_blog.forms import BlogpostForm, BlogCategoryForm
import datetime
import json
from micro_admin.models import User
from ast import literal_eval
from pages.forms import SimpleContactForm, ContactForm, SubscribeForm
from django.conf import settings
import sendgrid
from django.core.cache import cache
from microurl import google_mini
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from .tasks import *

# @csrf_exempt
# def recent_photos(request):
#     ''' returns all the images from the data base '''

#     imgs = []
#     for obj in Image_File.objects.filter(is_image=True).order_by("-date_created"):
#         uploaded_url = default_storage.url(obj.upload.url)
#         thumburl = default_storage.url(obj.thumbnail.url)
#         imgs.append({'src': uploaded_url, 'thumb': thumburl,
#                 'is_image': True})
#     return render(request, 'admin/browse.html', {'files': imgs})


@login_required
def admin_category_list(request):
    blog_categories = Category.objects.all().order_by('id')
    return render(request, 'admin/blog/blog-category-list.html', {'blog_categories': blog_categories})


@login_required
def new_blog_category(request):
    if request.method == 'POST':
        validate_blogcategory = BlogCategoryForm(request.POST)
        if validate_blogcategory.is_valid():
            validate_blogcategory.save()

            cache._cache.flush_all()
            data = {'error': False, 'response': 'Blog category created'}
        else:
            data = {'error': True, 'response': validate_blogcategory.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    if request.user.is_superuser:
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/blog/blog-category.html', {'csrf_token': c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def edit_category(request, category_slug):
    blog_category = get_object_or_404(Category, slug=category_slug)
    if request.method == 'POST':
        validate_blogcategory = BlogCategoryForm(request.POST, instance=blog_category)
        if validate_blogcategory.is_valid():
            validate_blogcategory.save()

            cache._cache.flush_all()
            data = {'error': False, 'response': 'Blog category updated'}
        else:
            data = {'error': True, 'response': validate_blogcategory.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    if request.user.is_superuser:
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/blog/blog-category-edit.html', {'blog_category': blog_category, 'csrf_token': c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def delete_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if request.user.is_superuser:
        category.delete()

        cache._cache.flush_all()
        return HttpResponseRedirect('/blog/category-list/')
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def change_category_status(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if category.is_display:
        category.is_display = False
    else:
        category.is_display = True
    category.save()
    return HttpResponseRedirect('/blog/category-list/')


def site_blog_home(request):
    items_per_page = 10
    if "page" in request.GET:
        if not request.GET.get('page').isdigit():
            raise Http404
        page = int(request.GET.get('page', 1))
    else:
        page = 1

    posts = Post.objects.filter(status='P')
    no_pages = int(math.ceil(float(posts.count()) / items_per_page))
    blog_posts = posts.order_by('-published_on')[(page - 1) * items_per_page:page * items_per_page]

    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/index.html', {'current_page': page, 'last_page': no_pages,
                            'posts': blog_posts, 'csrf_token': c['csrf_token']})


def blog_article(request, slug):
    blog_post = Post.objects.filter(slug=slug)
    if blog_post:
        blog_post = blog_post[0]
    elif Post.objects.filter(old_slugs__icontains=slug):
        blog_post = Post.objects.filter(old_slugs__icontains=slug)
        blog_post = blog_post[0]
        return redirect(reverse('micro_blog:blog_article', kwargs={'slug': blog_post.slug}), permanent=True)
    else:
        raise Http404
    all_blog_posts = list(Post.objects.filter(status='P').order_by('-published_on'))
    prev_url = ''
    next_url = ''
    for post in all_blog_posts:
        if str(slug) == str(post.slug):
            try:
                current_index = all_blog_posts.index(post)
                next_que = all_blog_posts[current_index+1]
                next_url = '/blog/'+str(next_que.slug)+'/'
            except:
                next_url = ''
            try:
                current_index = all_blog_posts.index(post)
                prev_que = all_blog_posts[current_index-1]
                if current_index == 0:
                    prev_url = ''
                else:
                    prev_url = '/blog/'+str(prev_que.slug)+'/'
            except:
                prev_url = ''
            question = post
            break
    if not blog_post.status == 'P':
        if not request.user.is_authenticated():
            raise Http404
    related_posts = Post.objects.filter(category=blog_post.category, status='P').exclude(id=blog_post.id).order_by('?')[:3]
    minified_url = ''
    if 'HTTP_HOST' in request.META.keys():
        try:
            minified_url = google_mini('https://' + request.META['HTTP_HOST'] + reverse('micro_blog:blog_article', kwargs={'slug': slug}), settings.GGL_URL_API_KEY)
        except:
            minified_url = 'https://' + request.META['HTTP_HOST'] + reverse('micro_blog:blog_article', kwargs={'slug': slug})
    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/article.html', {'csrf_token': c['csrf_token'], 'related_posts': related_posts,
                                                      'post': blog_post, 'minified_url': minified_url, 'prev_url': prev_url, 'next_url': next_url})


def blog_tag(request, slug):
    tag = get_object_or_404(Tags, slug=slug)
    blog_posts = Post.objects.filter(tags__in=[tag], status="P").order_by('-updated_on')
    items_per_page = 6
    if "page" in request.GET:
        if not request.GET.get('page').isdigit():
            raise Http404
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))
    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    if not blog_posts:
        raise Http404
    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/index.html', {'current_page': page, 'tag': tag,
                                'last_page': no_pages, 'posts': blog_posts, 'csrf_token': c['csrf_token']})


def blog_category(request, slug):
    slug = slug.lower()
    category = get_object_or_404(Category, slug=slug)
    blog_posts = Post.objects.filter(category=category, status="P").order_by('-updated_on')
    items_per_page = 6
    if "page" in request.GET:
        if not request.GET.get('page').isdigit():
            raise Http404
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))
    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    if not blog_posts:
        raise Http404
    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/index.html', {'current_page': page, 'category': category, 'last_page': no_pages,
                                    'posts': blog_posts, 'csrf_token': c['csrf_token']})


def archive_posts(request, year, month):
    blog_posts = Post.objects.filter(status="P", updated_on__year=year, updated_on__month=month).order_by('-updated_on')
    items_per_page = 6
    if "page" in request.GET:
        if not request.GET.get('page').isdigit():
            raise Http404
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))
    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    if not blog_posts:
        raise Http404
    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/index.html', {'current_page': page, 'year':year, 'month': month, 'last_page': no_pages,
                                                        'posts': blog_posts, 'csrf_token': c['csrf_token']})


@login_required
def admin_post_list(request):
    blog_posts = Post.objects.all().order_by('-created_on')
    return render(request, 'admin/blog/blog-posts.html', {'blog_posts': blog_posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        validate_blog = BlogpostForm(request.POST)
        if validate_blog.is_valid():
            blog_post = validate_blog.save(commit=False)
            blog_post.user = request.user
            blog_post.meta_description = request.POST['meta_description']
            blog_post.status = 'D'
            if request.POST.get('status') == "P":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                    blog_post.status = 'P'
                    blog_post.published_on = datetime.datetime.now().date()

            elif request.POST.get('status') == "T":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                    blog_post.status = 'T'

            elif request.POST.get('status') == "R":
                blog_post.status = 'R'

            blog_post.save()
            if request.user.is_superuser and request.POST.get('slug'):
                blog_post.slug = request.POST.get('slug')
            else:
                tempslug = slugify(blog_post.title)
                blog_post.slug = tempslug
            blog_post.save()

            if request.POST.get('tags', ''):
                tags = request.POST.get('tags')
                tags = tags.split(',')
                for tag in tags:
                    blog_tag = Tags.objects.filter(name=tag)
                    if blog_tag:
                        blog_tag = blog_tag[0]
                    else:
                        blog_tag = Tags.objects.create(name=tag)
                    blog_post.tags.add(blog_tag)

            sg = sendgrid.SendGridClient(settings.SG_USER, settings.SG_PWD)
            sending_msg = sendgrid.Mail()
            sending_msg.set_subject("New blog post has been created")

            blog_url = 'https://www.micropyramid.com/blog/' + str(blog_post.slug) + '/'
            message = '<p>New blog post has been created by ' + str(request.user) + ' with the name ' + str(blog_post.title) + ' in the category '
            message += str(blog_post.category.name) + '.</p>' + '<p>Please <a href="' + blog_url + '">click here</a> to view the blog post in the site.</p>'

            sending_msg.set_html(message)
            sending_msg.set_text('New blog post has been created')
            sending_msg.set_from(request.user.email)
            sending_msg.add_to([user.email for user in User.objects.filter(is_admin=True)])
            sg.send(sending_msg)

            cache._cache.flush_all()
            data = {'error': False, 'response': 'Blog Post created'}
        else:
            data = {'error': True, 'response': validate_blog.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    categories = Category.objects.all()
    c = {}
    c.update(csrf(request))
    return render(request, 'admin/blog/blog-new.html', {'categories': categories, 'csrf_token': c['csrf_token']})


@login_required
def edit_blog_post(request, blog_slug):
    if request.method == 'POST':
        current_post = get_object_or_404(Post, slug=blog_slug)
        existing_slug = str(current_post.slug)
        validate_blog = BlogpostForm(request.POST, instance=current_post)
        if validate_blog.is_valid():
            blog_post = validate_blog.save(commit=False)
            blog_post.meta_description = request.POST['meta_description']
            blog_post.status = 'D'
            if request.POST.get('status') == "P":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                    blog_post.status = 'P'
            elif request.POST.get('status') == "T":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                    blog_post.status = 'T'
            elif request.POST.get('status') == "R":
                blog_post.status = 'R'

            if request.user.is_superuser and request.POST.get('slug'):
                if blog_post.old_slugs:
                    blog_post_slugs = blog_post.old_slugs.split(',')
                    if not existing_slug in blog_post_slugs:
                        old_slugs = blog_post.old_slugs
                        old_slugs += ',' + str(existing_slug)
                    else:
                        old_slugs = blog_post.old_slugs
                else:
                    if str(existing_slug) != request.POST.get('slug'):
                        old_slugs = existing_slug
                    else:
                        old_slugs = ''
                blog_post.old_slugs = old_slugs
                blog_post.slug = request.POST.get('slug')
            else:
                tempslug = slugify(blog_post.title)

            blog_post.save()
            blog_post.tags.clear()
            if request.POST.get('tags', ''):
                for tag in blog_post.tags.all():
                    blog_post.tags.remove(tag)
                tags = request.POST.get('tags')
                tags = tags.split(',')
                for tag in tags:
                    blog_tag = Tags.objects.filter(name=tag)
                    if blog_tag:
                        blog_tag = blog_tag[0]
                    else:
                        blog_tag = Tags.objects.create(name=tag)

                    blog_post.tags.add(blog_tag)

            cache._cache.flush_all()
            data = {'error': False, 'response': 'Blog Post edited'}
        else:
            data = {'error': True, 'response': validate_blog.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    blog_post = Post.objects.filter(slug=blog_slug)
    if blog_post:
        blog_post = blog_post[0]
    elif Post.objects.filter(old_slugs__icontains=blog_slug):
        blog_post = Post.objects.filter(old_slugs__icontains=blog_slug)
        blog_post = blog_post[0]
        return redirect(reverse('micro_blog:edit_blog_post', kwargs={'blog_slug': blog_post.slug}), permanent=True)
    else:
        raise Http404
    categories = Category.objects.all()
    if request.user.is_superuser or blog_post.user == request.user:
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/blog/blog-edit.html', {'blog_post': blog_post, 'categories': categories, 'csrf_token': c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def delete_post(request, blog_slug):
    blog_post = get_object_or_404(Post, slug=blog_slug)
    if request.user == blog_post.user or request.user.is_superuser:
        blog_post.delete()

        cache._cache.flush_all()
        data = {"error": False, 'message': 'Blog Post Deleted'}
    else:
        data = {"error": True, 'message': 'Admin or Owner can delete blog post'}
    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


@login_required
def view_post(request, blog_slug):
    blog_post = Post.objects.filter(slug=blog_slug)
    if blog_post:
        blog_post = blog_post[0]
    elif Post.objects.filter(old_slugs__icontains=blog_slug):
        blog_post = Post.objects.filter(old_slugs__icontains=blog_slug)
        blog_post = blog_post[0]
        return redirect(reverse('micro_blog:blog_article', kwargs={'slug': blog_post.slug}), permanent=True)
    else:
        raise Http404
    return render(request, 'admin/blog/view_post.html', {'post': blog_post})

def contact(request):
    if request.method == 'GET':
        return render(request, 'site/pages/contact-us.html')
    validate_simplecontact = SimpleContactForm(request.POST)
    validate_contact = ContactForm(request.POST)
    if 'enquery_type' in request.POST.keys():
        if validate_simplecontact.is_valid() and validate_contact.is_valid():
            contact = simplecontact.objects.create(
                full_name=request.POST.get('full_name'), message=request.POST.get('message'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone') if request.POST.get('phone') else False
            )
            Contact.objects.create(
                contact_info=contact, domain=request.POST.get('domain'),
                domain_url=request.POST.get('domain_url'), country=request.POST.get('country'),
                enquery_type=request.POST.get('enquery_type')
            )
        else:
            errors = {}
            errors = dict((validate_simplecontact.errors).items() + (validate_contact.errors).items())
            data = {'error': True, 'errinfo': errors}
            return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    else:
        if validate_simplecontact.is_valid():
            simplecontact.objects.get_or_create(
                full_name=request.POST.get('full_name'), message=request.POST.get('message'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone') if request.POST.get('phone') else False
            )
        else:
            errors = {}
            errors = dict((validate_simplecontact.errors).items())
            data = {'error': True, 'errinfo': errors}
            return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    message = "<p>From: "+request.POST.get('full_name')+"</p><p>Email Id: "
    message += request.POST.get('email')+"</p><p>Message: "+request.POST.get('message')+"</p>"

    if request.POST.get('phone'):
        message += "<p>Contact Number: "+request.POST.get('phone')+"</p>"

    if 'enquery_type' in request.POST.keys():
        message += "<p><b>Domain Details: </b></p><p>Domain: "+request.POST.get('domain')+\
                    "</p><p>Domain URL: "+request.POST.get('domain_url')+"</p>"

        message += "<p><b>General Information: </b></p>"+"<p>Enquery Type: "+\
                    request.POST.get('enquery_type')+"</p><p>Country: "+request.POST.get('country')

    sg = sendgrid.SendGridClient(settings.SG_USER, settings.SG_PWD)

    contact_msg = sendgrid.Mail()
    contact_msg.set_subject("We received your message | MicroPyramid")
    message_reply = 'Hello ' + request.POST.get('full_name') + ',\n\n'
    message_reply = message_reply + 'Thank you for writing in.\n'
    message_reply = message_reply +  'We appreciate that you have taken the time to share your feedback with us! We will get back to you soon.\n\n'
    message_reply = message_reply + 'Regards\n'
    message_reply = message_reply + 'The MicroPyramid Team.'
    contact_msg.set_text(message_reply)
    contact_msg.set_from("hello@micropyramid.com")
    contact_msg.add_to(request.POST.get('email'))
    sg.send(contact_msg)

    sending_msg = sendgrid.Mail()
    sending_msg.set_subject("Contact Request")
    sending_msg.set_html(message)
    sending_msg.set_text('Contact Request')
    sending_msg.set_from(request.POST.get('email'))
    sending_msg.add_to("hello@micropyramid.com")
    sg.send(sending_msg)

    data = {'error': False, 'response': 'Contact submitted successfully'}
    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def subscribe(request):
    if request.method == 'GET':
        return render(request, 'site/pages/subscribe.html')
    print request.POST
    validate_subscribe = SubscribeForm(request.POST)
    if validate_subscribe.is_valid():
        subscriber = Subscribers.objects.create(email=request.POST.get('email'))
        if str(request.POST.get('is_blog')) == 'True':
            if len(request.POST.get('is_category')) > 0:
                category = Category.objects.get(id=request.POST.get('is_category'))
                subscriber.category = category
                create_contact_in_category.delay(category.slug, request.POST.get('email'))
            else:
                create_contact_in_category.delay('blog', request.POST.get('email'))
            subscriber.blog_post = True
        else:
            create_contact_in_category.delay('site', request.POST.get('email'))
            subscriber.blog_post = False
        subscriber.save()
    else:
        errors = {}
        errors = dict((validate_subscribe.errors).items())
        data = {'error': True, 'errinfo': errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    data = {'error': False, 'response': 'Your email has been successfully subscribed.'}
    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

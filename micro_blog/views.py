from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
# from django.views.decorators.csrf import csrf_exempt
from micro_blog.models import Category, Tags, Post, Subscribers, create_slug, Post_Slugs
from pages.models import Contact
import math
# from django.core.files.storage import default_storage
from micro_blog.forms import BlogpostForm, BlogCategoryForm, CustomBlogSlugInlineFormSet
from django.forms.models import inlineformset_factory
import datetime
import json
from micro_admin.models import User
from ast import literal_eval
from pages.forms import ContactForm, SubscribeForm
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
        validate_blogcategory = BlogCategoryForm(
            request.POST, instance=blog_category)
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

    posts = Post.objects.filter(status='P').order_by(
        '-published_on').select_related("user").prefetch_related(
        Prefetch("slugs", queryset=Post_Slugs.objects.filter(is_active=True),
                 to_attr="active_slugs"
                 )
    )
    no_pages = int(math.ceil(float(posts.count()) / items_per_page))
    try:
        if int(request.GET.get('page')) < 0 or int(request.GET.get('page')) > (no_pages):
            page = 1
            return HttpResponseRedirect(reverse('micro_blog:site_blog_home'))
        else:
            print ("hello")
            page = int(request.GET.get('page'))
    except:
        page = 1
    print (page)
    blog_posts = posts[(page - 1) * items_per_page:page * items_per_page]

    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/index.html', {'current_page': page, 'last_page': no_pages,
                                                    'posts': blog_posts, 'csrf_token': c['csrf_token']})


def blog_article(request, slug):
    blog_post = get_object_or_404(Post, slugs__slug=slug)
    active_slug = blog_post.slug
    if active_slug != slug:
        return redirect(reverse('micro_blog:blog_article',
                                kwargs={'slug': active_slug})
                        )
    if not blog_post.status == 'P':
        if not request.user.is_authenticated():
            raise Http404
    all_blog_posts = list(
        Post.objects.filter(status='P').order_by('-published_on'))
    prev_url = ''
    next_url = ''
    for post in all_blog_posts:
        if str(slug) == str(post.slug):
            try:
                current_index = all_blog_posts.index(post)
                next_que = all_blog_posts[current_index + 1]
                next_url = '/blog/' + str(next_que.slug) + '/'
            except:
                next_url = ''
            try:
                current_index = all_blog_posts.index(post)
                prev_que = all_blog_posts[current_index - 1]
                if current_index == 0:
                    prev_url = ''
                else:
                    prev_url = '/blog/' + str(prev_que.slug) + '/'
            except:
                prev_url = ''
            break
    related_posts = Post.objects.filter(
        category=blog_post.category, status='P').exclude(id=blog_post.id).order_by('?')[:3]
    minified_url = ''
    if 'HTTP_HOST' in request.META.keys():
        try:
            minified_url = google_mini('https://' + request.META['HTTP_HOST'] + reverse(
                'micro_blog:blog_article', kwargs={'slug': slug}), settings.GGL_URL_API_KEY)
        except:
            minified_url = 'https://' + \
                request.META[
                    'HTTP_HOST'] + reverse('micro_blog:blog_article', kwargs={'slug': slug})
    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/article.html', {'csrf_token': c['csrf_token'], 'related_posts': related_posts,
                                                      'post': blog_post, 'minified_url': minified_url, 'prev_url': prev_url, 'next_url': next_url})


def blog_tag(request, slug):
    tag = get_object_or_404(Tags, slug=slug)
    blog_posts = Post.objects.filter(tags__in=[tag], status="P").order_by(
        '-published_on').select_related("user").prefetch_related(
        Prefetch("slugs", queryset=Post_Slugs.objects.filter(is_active=True),
                 to_attr="active_slugs"
                 )
    )
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
    blog_posts = Post.objects.filter(category=category, status="P").order_by(
        '-published_on').select_related("user").prefetch_related(
        Prefetch("slugs", queryset=Post_Slugs.objects.filter(is_active=True),
                 to_attr="active_slugs"
                 )
    )
    items_per_page = 6
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))

    try:
        if int(request.GET.get('page')) < 0 or int(request.GET.get('page')) > (no_pages):
            page = 1
            return HttpResponseRedirect(reverse('micro_blog:blog_category', kwargs={'slug': slug}))
        else:
            print ("hello")
            page = int(request.GET.get('page'))
    except:
        page = 1

    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    if not blog_posts:
        raise Http404
    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/index.html', {'current_page': page, 'category': category, 'last_page': no_pages,
                                                    'posts': blog_posts, 'csrf_token': c['csrf_token']})


def archive_posts(request, year, month):
    blog_posts = Post.objects.filter(status="P", published_on__year=year, published_on__month=month).order_by(
        '-published_on').select_related("user").prefetch_related(
        Prefetch("slugs", queryset=Post_Slugs.objects.filter(is_active=True),
                 to_attr="active_slugs"
                 )
    )
    items_per_page = 6
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))

    try:
        if int(request.GET.get('page')) < 0 or int(request.GET.get('page')) > (no_pages):
            page = 1
            return HttpResponseRedirect(reverse('micro_blog:archive_posts'), kwargs={'year': blog_posts[0].published_on.year, 'month': blog_posts[0].published_on.month})
        else:
            page = int(request.GET.get('page'))
    except:
        page = 1

    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    if not blog_posts:
        raise Http404
    c = {}
    c.update(csrf(request))
    return render(request, 'site/blog/index.html', {'current_page': page, 'year': year, 'month': month, 'last_page': no_pages,
                                                    'posts': blog_posts, 'csrf_token': c['csrf_token']})


@login_required
def admin_post_list(request):
    users = User.objects.all()
    blog_posts = Post.objects.all().order_by(
        '-created_on').select_related("user", "category").prefetch_related(
        Prefetch("slugs", queryset=Post_Slugs.objects.filter(is_active=True),
                 to_attr="active_slugs"
                 )
    )
    if request.method == "POST":
        if request.user.is_site_admin:
            blog_post = get_object_or_404(Post, id=request.POST.get("blog_id"))
            user = get_object_or_404(
                User, id=request.POST.get("change_author"))
            blog_post.user = user
            blog_post.save()
    return render(request, 'admin/blog/blog-posts.html', {'blog_posts': blog_posts, "users": users})


@login_required
def new_post(request):
    BlogSlugFormSet = inlineformset_factory(Post, Post_Slugs,
                                            can_delete=True, extra=3, fields=('slug', 'is_active'),
                                            formset=CustomBlogSlugInlineFormSet
                                            )
    if request.method == 'POST':
        blog_form = BlogpostForm(request.POST)
        blogslugs_formset = BlogSlugFormSet(request.POST)
        if blog_form.is_valid() and blogslugs_formset.is_valid():
            blog_post = blog_form.save(commit=False)
            blogslugs_formset = BlogSlugFormSet(
                request.POST, instance=blog_post)
            if blogslugs_formset.is_valid():
                blog_post.user = request.user
                if request.POST.get('meta_description'):
                    blog_post.meta_description = request.POST[
                        'meta_description']
                blog_post.status = 'D'
                if request.POST.get('status') == "P":
                    if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                        blog_post.status = 'P'
                        if not blog_post.published_on:
                            blog_post.published_on = datetime.datetime.now(
                            ).date()

                elif request.POST.get('status') == "T":
                    if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                        blog_post.status = 'T'

                elif request.POST.get('status') == "R":
                    blog_post.status = 'R'

                blog_post.save()
                blogslugs_formset.save()
                # If no slugs are specified, then create one using title.
                if not blog_post.slugs.all():
                    blog_post.create_blog_slug([slugify(blog_post.title)])
                blog_post.check_and_activate_slug()

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

                blog_url = 'https://www.micropyramid.com/blog/' + \
                    str(blog_post.slug) + '/'
                message = '<p>New blog post has been created by ' + str(request.user) + ' with the name ' + str(
                    blog_post.title) + ' in the category ' + str(blog_post.category.name) + '.</p>'

                sending_msg.set_html(message)
                sending_msg.set_text('New blog post has been created')
                sending_msg.set_from(request.user.email)
                sending_msg.add_to(
                    [user.email for user in User.objects.filter(is_admin=True)])
                sg.send(sending_msg)

                cache._cache.flush_all()
                return redirect(reverse('micro_blog:admin_post_list'))
    else:
        blog_form = BlogpostForm()
        blogslugs_formset = BlogSlugFormSet(instance=Post())

    categories = Category.objects.all()
    c = {}
    c.update(csrf(request))
    return render(request, 'admin/blog/blog-new.html',
                  {'categories': categories, 'csrf_token': c['csrf_token'],
                   'blogslugs_formset': blogslugs_formset, 'blog_form': blog_form}
                  )


@login_required
def edit_blog_post(request, blog_slug):
    blog_post = get_object_or_404(Post, slugs__slug=blog_slug)
    active_slug = blog_post.slug
    old_blog_status = blog_post.status
    if active_slug != blog_slug:
        return redirect(reverse('micro_blog:edit_blog_post',
                                kwargs={'blog_slug': active_slug})
                        )
    if not blog_post.is_editable_by(request.user):
        return render_to_response('admin/accessdenied.html')

    BlogSlugFormSet = inlineformset_factory(Post, Post_Slugs,
                                            can_delete=True, extra=3, fields=('slug', 'is_active'),
                                            formset=CustomBlogSlugInlineFormSet
                                            )
    if request.method == 'POST':
        blog_form = BlogpostForm(request.POST, instance=blog_post)
        blogslugs_formset = BlogSlugFormSet(request.POST, instance=blog_post)
        if blog_form.is_valid() and blogslugs_formset.is_valid():
            blog_post = blog_form.save(commit=False)
            if blogslugs_formset.is_valid():
                blog_post.status = old_blog_status
                blog_post.meta_description = request.POST.get(
                    'meta_description')
                if request.POST.get('status') == "P":
                    if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                        blog_post.status = 'P'
                elif request.POST.get('status') == "T":
                    if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_superuser:
                        blog_post.status = 'T'
                elif (request.POST.get('status') == "R" or
                      request.POST.get('status') == "D"
                      ):
                    blog_post.status = request.POST.get('status')
                else:
                    pass

                blog_post.save()
                blogslugs_formset.save()
                # If no slugs are specified, then create one using title.
                if not blog_post.slugs.all():
                    blog_post.create_blog_slug([slugify(blog_post.title)])
                blog_post.check_and_activate_slug()

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
                return redirect(reverse('micro_blog:admin_post_list'))
    else:
        blog_form = BlogpostForm(instance=blog_post)
        blogslugs_formset = BlogSlugFormSet(instance=blog_post)

    categories = Category.objects.all()
    c = {}
    c.update(csrf(request))
    return render(request, 'admin/blog/blog-edit.html', {'blog_post': blog_post,
                                                         'categories': categories, 'csrf_token': c['csrf_token'],
                                                         'blogslugs_formset': blogslugs_formset, 'blog_form': blog_form}
                  )


@login_required
def delete_post(request, blog_slug):
    blog_post = get_object_or_404(Post, slugs__slug=blog_slug)
    active_slug = blog_post.slug
    if active_slug != blog_slug:
        raise Http404
    if request.user == blog_post.user or request.user.is_superuser:
        blog_post.delete()

        cache._cache.flush_all()
        data = {"error": False, 'message': 'Blog Post Deleted'}
    else:
        data = {
            "error": True, 'message': 'Admin or Owner can delete blog post'}
    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def contact(request):
    if request.method == 'GET':
        return render(request, 'site/pages/contact-us.html')
    validate_contact = ContactForm(request.POST)
    if 'enquery_type' in request.POST.keys():
        if validate_contact.is_valid():
            Contact.objects.create(
                country=request.POST.get('country'),
                enquery_type=request.POST.get('enquery_type')
            )
        else:
            errors = {}
            data = {'error': True, 'errinfo': validate_contact.errors}
            return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    message = "<p>From: "+request.POST.get('full_name')+"</p><p>Email Id: "
    message += request.POST.get('email') + \
        "</p><p>Message: "+request.POST.get('message')+"</p>"

    if request.POST.get('phone'):
        message += "<p>Contact Number: "+request.POST.get('phone')+"</p>"

        message += "<p><b>General Information: </b></p>"+"<p>Enquery Type: " +\
            request.POST.get('enquery_type') + \
            "</p><p>Country: "+request.POST.get('country')

    sg = sendgrid.SendGridClient(settings.SG_USER, settings.SG_PWD)

    contact_msg = sendgrid.Mail()
    contact_msg.set_subject("We received your message | MicroPyramid")
    message_reply = 'Hello ' + request.POST.get('full_name') + ',\n\n'
    message_reply = message_reply + 'Thank you for writing in.\n'
    message_reply = message_reply + \
        'We appreciate that you have taken the time to share your feedback with us! We will get back to you soon.\n\n'
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
    validate_subscribe = SubscribeForm(request.POST)
    if validate_subscribe.is_valid():
        subscriber = Subscribers.objects.create(
            email=request.POST.get('email'))
        if str(request.POST.get('is_blog')) == 'True':
            if len(request.POST.get('is_category')) > 0:
                category = Category.objects.get(
                    id=request.POST.get('is_category'))
                subscriber.category = category
                create_contact_in_category.delay(
                    category.slug, request.POST.get('email'))
            else:
                create_contact_in_category.delay(
                    'blog', request.POST.get('email'))
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

    data = {
        'error': False, 'response': 'Your email has been successfully subscribed.'}
    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

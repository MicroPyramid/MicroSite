import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from micro_blog.models import Image_File, Category, Tags, Post, BlogComments
from pages.models import Menu,Page
from PIL import Image
import os
import math
from django.core.files.storage import default_storage
from django.core.files.base import File as fle
from micro_blog.forms import BlogpostForm, BlogCategoryForm, CommentForm
from microsite.settings import BLOG_IMAGES
import datetime
import requests
import urllib2, json
import urllib 

def store_image(img,location):
    ''' takes the image file and stores that in the local file storage returns file name with
    adding of timestamp to its name'''

    uploaded_file = img
    filename = uploaded_file.name
    now_str = str(datetime.datetime.now())
    now = now_str.replace(' ', '-')
    title_str = filename.split(".")[-0]
    title = title_str.replace(' ', '-')
    ext = filename.split(".")[-1]
    filename = title + now
    x = location + filename + '.' + ext
    y=open(x,'w')
    for i in uploaded_file.chunks():
        y.write(i)
    y.close()
    return filename + '.' + ext


@csrf_exempt
def upload_photos(request):
    '''
    takes all the images coming from the redactor editor and
    stores it in the database and returns all the files'''

    if request.FILES.get("upload"):
        uploaded_file = request.FILES.get("upload")
        stored_image = Image_File.objects.create(upload=uploaded_file, is_image=True)
        size = (128, 128)
        file_name = uploaded_file.name
        thumb_file_name = 'thumb'+uploaded_file.name
        temp_file=open(file_name,'w')
        for i in uploaded_file.chunks():
            temp_file.write(i)
        temp_file.close()
        im = Image.open(file_name)
        im.thumbnail(size)
        im.save(thumb_file_name)
        imdata = open(thumb_file_name)

        stored_image.thumbnail.save(thumb_file_name,fle(imdata) )
        imdata.close()

        os.remove(file_name)
        os.remove(thumb_file_name)
        uploaded_url = default_storage.url(stored_image.upload.url)
    uploaded_url = '/'+uploaded_url
    return HttpResponse("""
    <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction({0}, '{1}');
    </script>""".format(request.GET['CKEditorFuncNum'], uploaded_url)
)


@csrf_exempt
def recent_photos(request):
    ''' returns all the images from the data base '''

    imgs = []
    for obj in Image_File.objects.filter(is_image=True).order_by("-date_created"):
        uploaded_url = default_storage.url(obj.upload.url)
        thumburl = default_storage.url(obj.thumbnail.url)
        imgs.append({'src':uploaded_url,'thumb': thumburl,
                'is_image': True})
    return render_to_response('admin/browse.html',{'files':imgs})

@login_required
def blog_comments(request):
    blog_comments = BlogComments.objects.all()
    return render_to_response('admin/blog/blog-comments.html',{'blog_comments':blog_comments})


@login_required
def comment_status(request, comment_id):
    comment=BlogComments.objects.get(id=comment_id)
    if comment.status=="on":
        comment.status="off"
    else:
        comment.status="on"
    comment.save()
    return HttpResponseRedirect('/blog/blog-comments/')


@login_required
def delete_blog_comments(request,comment_id):
    blog_comment = BlogComments.objects.get(id=comment_id)
    blog_comment.delete()
    return HttpResponseRedirect('/blog/blog-comments/')


@login_required
def admin_category_list(request):
    blog_categories = Category.objects.all()
    return render_to_response('admin/blog/blog-category-list.html',{'blog_categories':blog_categories})


@login_required
def new_blog_category(request):
    if request.method == 'POST':
        validate_blogcategory = BlogCategoryForm(request.POST)
        if validate_blogcategory.is_valid():
            validate_blogcategory.save()
            data = {'error':False,'response':'Blog category created'}
        else:
            data = {'error':True,'response':validate_blogcategory.errors}
        return HttpResponse(json.dumps(data))
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/blog/blog-category.html',{'csrf_token':c['csrf_token']})


@login_required
def edit_category(request,category_slug):
    if request.method == 'POST':
        category = Category.objects.get(slug = category_slug)
        validate_blogcategory = BlogCategoryForm(request.POST,instance = category)
        if validate_blogcategory.is_valid():
            validate_blogcategory.save()
            data = {'error':False,'response':'Blog category updated'}
        else:
            data = {'error':True,'response':validate_blogcategory.errors}
        return HttpResponse(json.dumps(data))
    blog_category = Category.objects.get(slug=category_slug)
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/blog/blog-category-edit.html',{'blog_category':blog_category, 'csrf_token':c['csrf_token']})


@login_required
def delete_category(request,category_slug):
    category = Category.objects.get(slug=category_slug)
    category.delete()
    return HttpResponseRedirect('/blog/category-list/')


def site_blog_home(request):
    current_date = datetime.date.today()
    comments = BlogComments.objects.filter(status="on").order_by('-id')[:5]
    page_list=Page.objects.all()

    archives = []
    for i in reversed(range(-4,1)):
        archives.append(current_date + datetime.timedelta(i*365/12))

    items_per_page = 10
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(Post.objects.filter(status='P').count()) / items_per_page))

    blog_posts = Post.objects.filter(status='P').order_by('-created_on')[(page - 1) * items_per_page:page * items_per_page]

    if page <= 5:
        start_page = 1
    else:
        start_page = page-5

    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page=no_pages

    pages = range(start_page, end_page+1)
    print pages

    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'pagelist':page_list,'current_page':page,'last_page':no_pages, 'pages':pages,'posts':blog_posts,'comments':comments,'archives':archives, 'csrf_token':c['csrf_token']})


def blog_article(request, slug):
    blog_post = Post.objects.get(slug=slug)
    blog_posts = Post.objects.filter(status='P')[:3]
    comments = BlogComments.objects.filter(status="on",post=blog_post).order_by('-id')[:5]
    current_date = datetime.date.today()
    page_list=Page.objects.all()[:4]
    fb=requests.get('http://graph.facebook.com/?id=http://micropyramid.com//blog/'+slug)
    tw=requests.get('http://urls.api.twitter.com/1/urls/count.json?url=http://micropyramid.com//blog/'+slug)
    # r2=requests.get('https://plusone.google.com/_/+1/fastbutton?url= https://keaslteuzq.localtunnel.me/blog/'+slug)
    ln=requests.get('https://www.linkedin.com/countserv/count/share?url=http://micropyramid.com/blog/'+slug+'&format=json')
    linkedin={}
    linkedin.update(ln.json()) 
    facebook={}
    facebook.update(fb.json())
    twitter={}
    twitter.update(tw.json())
    fbshare_count = 0
    twshare_count = 0
    lnshare_count = 0
    try:
        if facebook['shares']:
            fbshare_count = facebook['shares']
    except:
        pass
    try:
        if twitter['count']:
            twshare_count = twitter['count']
    except:
        pass
    try:
        if linkedin['count']:
            lnshare_count = linkedin['count']
    except:
        pass
    archives = []
    for i in reversed(range(-4,1)):
        archives.append(current_date + datetime.timedelta(i*365/12))
    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/article.html',{'csrf_token':c['csrf_token'],'pagelist':page_list,'post':blog_post, 'archives':archives,'comments':comments,'posts':blog_posts,'fbshare_count':fbshare_count,'twshare_count':twshare_count,'lnshare_count':lnshare_count})


def blog_tag(request, slug):
    tag = Tags.objects.get(slug=slug)
    blog_posts = Post.objects.filter(tags__in=[tag],status="P").order_by('-created_on')
    current_date = datetime.date.today()
    comments = BlogComments.objects.filter(status="on").order_by('-id')[:5]
    page_list=Page.objects.all()
    archives = []
    for i in reversed(range(-4,1)):
        archives.append(current_date + datetime.timedelta(i*365/12))

    items_per_page = 6
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))

    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]

    if page <= 5:
        start_page = 1
    else:
        start_page = page-5

    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page=no_pages

    pages = range(start_page, end_page+1)

    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'comments':comments,'pagelist':page_list,'current_page':page,'last_page':no_pages, 'pages':pages,'posts':blog_posts,'archives':archives, 'csrf_token':c['csrf_token']})


def blog_category(request, slug):
    category = Category.objects.get(slug=slug)
    blog_posts = Post.objects.filter(category=category,status="P").order_by('-created_on')
    current_date = datetime.date.today()
    comments = BlogComments.objects.filter(status="on").order_by('-id')[:5]
    page_list=Page.objects.all()

    archives = []
    for i in reversed(range(-4,1)):
        archives.append(current_date + datetime.timedelta(i*365/12))

    items_per_page = 6
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))

    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]

    if page <= 5:
        start_page = 1
    else:
        start_page = page-5

    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page=no_pages

    pages = range(start_page, end_page+1)

    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'pagelist':page_list,'comments':comments, 'current_page':page,'last_page':no_pages, 'pages':pages,'posts':blog_posts,'archives':archives, 'csrf_token':c['csrf_token']})


def add_blog_comment(request, slug):
    if request.method == "POST":
        validate_blog_comment = CommentForm(request.POST)

        if validate_blog_comment.is_valid():
            payload = {'secret': '6Le-1P8SAAAAADOJhIl8UlI7qM0fsPmSIh1edQuA',
                    'response': request.POST.get('g-recaptcha-response'),
                    'remoteip':  request.META.get('REMOTE_ADDR')}
            r = requests.get('https://www.google.com/recaptcha/api/siteverify', params=payload)

            if json.loads(r.text)['success']==True:
                comment = validate_blog_comment.save(commit = False)
                blog_post = Post.objects.get(slug=slug)
                comment.post = blog_post
                comment.status='on'
                comment.save()
                data = {'error':False,'response':'comment posted successfully'}
            else:
                data = {'error':True,'response':'Captcha failed'}
        else:
            data = {'error':True,'response':validate_blog_comment.errors}

        return HttpResponse(json.dumps(data))


def archive_posts(request, year, month):
    blog_posts = Post.objects.filter(status="P",created_on__year=year,created_on__month=month).order_by('-created_on')
    current_date = datetime.date.today()
    comments = BlogComments.objects.filter(status="on").order_by('-id')[:5]
    page_list=Page.objects.all()

    archives = []
    for i in reversed(range(-4,1)):
        archives.append(current_date + datetime.timedelta(i*365/12))

    items_per_page = 6
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1

    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))

    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]

    if page <= 5:
        start_page = 1
    else:
        start_page = page-5

    if no_pages <= 10:
        end_page = no_pages
    else:
        end_page = start_page + 10
        if end_page > no_pages:
            end_page=no_pages

    pages = range(start_page, end_page+1)

    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'pagelist':page_list,'comments':comments,'current_page':page,'last_page':no_pages, 'pages':pages,'posts':blog_posts,'archives':archives, 'csrf_token':c['csrf_token']})


@login_required
def admin_post_list(request):
    blog_posts = Post.objects.all()
    return render_to_response('admin/blog/blog-posts.html',{'blog_posts':blog_posts})


@login_required
def admin_new_post(request):
    if request.method == 'POST':
        validate_blog = BlogpostForm(request.POST)
        if validate_blog.is_valid():
            blog_post = validate_blog.save(commit=False)
            blog_post.user=request.user

            if request.POST.get('status',''):
                blog_post.status='D'
            else:
                blog_post.status='P'

            if request.POST.get('featured_post',''):
                blog_post.featured_post=request.POST.get('featured_post')
                if 'featuredimage' in request.FILES:
                    blog_post.featured_image=store_image(request.FILES.get('featuredimage'),BLOG_IMAGES)
                else:
                    blog_post.featured_image=''

            blog_post.save()
            if request.POST.get('tags',''):
                tags = request.POST.get('tags')
                tags = tags.split(',')
                for tag in tags:
                    blog_tag = Tags.objects.filter(name=tag)
                    if blog_tag:
                        blog_tag = blog_tag[0]
                    else:
                        blog_tag = Tags.objects.create(name=tag)

                    blog_post.tags.add(blog_tag)
            data = {'error':False,'response':'Blog Post created'}
        else:
            data = {'error':True,'response':validate_blog.errors}
        return HttpResponse(json.dumps(data))
    categories = Category.objects.all()
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/blog/blog-new.html',{'categories':categories,'csrf_token':c['csrf_token']})


@login_required
def edit_blog_post(request,blog_slug):
    if request.method == 'POST':
        current_post = Post.objects.get(slug = blog_slug)
        validate_blog = BlogpostForm(request.POST,instance=current_post)
        if validate_blog.is_valid():
            if request.user == current_post.user or request.user.is_admin:
                blog_post = validate_blog.save(commit=False)
                blog_post.user=request.user
                if request.POST.get('status'):
                    blog_post.status='D'
                else:
                    blog_post.status='P'

                if request.POST.get('featured_post',''):
                    blog_post.featured_post==request.POST.get('featured_post')

                if 'featuredimage' in request.FILES:
                    if current_post.featured_image:
                        os.remove(BLOG_IMAGES + current_post.featured_image)
                    blog_post.featured_image=store_image(request.FILES.get('featuredimage'),BLOG_IMAGES)

                blog_post.save()

                if request.POST.get('tags',''):
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
                data = {'error':False,'response':'Blog Post created'}
            else:
                data = {'error':True,'response':'admin or owner can edit blog post'}
        else:
            data = {'error':True,'response':validate_blog.errors}
        return HttpResponse(json.dumps(data))

    blog_post = Post.objects.get(slug=blog_slug)
    categories = Category.objects.all()
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/blog/blog-edit.html',{'blog_post':blog_post,'categories':categories,'csrf_token':c['csrf_token']})


@login_required
def change_featured_state(request,blog_slug):
    blog_post = Post.objects.get(slug=blog_slug)
    if blog_post.featured_post == 'on':
        blog_post.featured_post = 'off'
    else:
        blog_post.featured_post = 'on'
    blog_post.save()
    return HttpResponseRedirect('/blog/admin/list/')


@login_required
def delete_post(request,blog_slug):
    if request.user == current_post.user or request.user.is_admin:
        blog_post = Post.objects.get(slug=blog_slug)
        blog_post.delete()
        data = {'error':False,'response':'Blog Post Deleted'}
        return HttpResponseRedirect('/blog/admin/list/')
    else:
        data = {'error':True,'response':'admin or owner can delete blog post'}
    return HttpResponse(json.dumps(data))
     

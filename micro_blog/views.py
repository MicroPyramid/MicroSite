from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from micro_blog.models import Image_File, Category, Tags, Post
from pages.models import Page, simplecontact, Contact
from PIL import Image
import os
import math
from django.core.files.storage import default_storage
from django.core.files.base import File as fle
from micro_blog.forms import BlogpostForm, BlogCategoryForm
import datetime
import requests
import json
from micro_admin.models import User
from ast import literal_eval
from employee.models import DailyReport, Dailyreport_files
from django.core.mail import send_mail
from pages.forms import SimpleContactForm, ContactForm



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
    if request.user.is_admin:
        c = {}
        c.update(csrf(request))
        return render_to_response('admin/blog/blog-category.html',{'csrf_token':c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


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
    if request.user.is_admin:
        blog_category = Category.objects.get(slug=category_slug)
        c = {}
        c.update(csrf(request))
        return render_to_response('admin/blog/blog-category-edit.html',{'blog_category':blog_category, 'csrf_token':c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def delete_category(request,category_slug):
    category = Category.objects.get(slug=category_slug)
    if request.user.is_admin:
        category.delete()
        return HttpResponseRedirect('/blog/category-list/')
    else:
        return render_to_response('admin/accessdenied.html')


def site_blog_home(request):
    page_list=Page.objects.all()
    items_per_page = 10
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(Post.objects.filter(status='P').count()) / items_per_page))
    blog_posts = Post.objects.filter(status='P').order_by('-created_on')[(page - 1) * items_per_page:page * items_per_page]
    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'pagelist':page_list,'current_page':page,'last_page':no_pages,
                            'posts':blog_posts, 'csrf_token':c['csrf_token']})


def blog_article(request, slug):
    blog_post = Post.objects.get(slug=slug)
    blog_posts = Post.objects.filter(status='P')[:3]
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
    except Exception:
        pass
    try:
        if twitter['count']:
            twshare_count = twitter['count']
    except Exception:
        pass
    try:
        if linkedin['count']:
            lnshare_count = linkedin['count']
    except Exception:
        pass
    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/article.html',{'csrf_token':c['csrf_token'],'pagelist':page_list,
                            'post':blog_post,'posts':blog_posts,'fbshare_count':fbshare_count,
                            'twshare_count':twshare_count,'lnshare_count':lnshare_count})


def blog_tag(request, slug):
    tag = Tags.objects.get(slug=slug)
    blog_posts = Post.objects.filter(tags__in=[tag],status="P").order_by('-created_on')
    page_list=Page.objects.all()
    items_per_page = 6
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))
    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'pagelist':page_list,'current_page':page,
                                'last_page':no_pages,'posts':blog_posts, 'csrf_token':c['csrf_token']})


def blog_category(request, slug):
    category = Category.objects.get(slug=slug)
    blog_posts = Post.objects.filter(category=category,status="P").order_by('-created_on')
    page_list=Page.objects.all()
    items_per_page = 6
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))
    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'pagelist':page_list,
                            'current_page':page,'last_page':no_pages,'posts':blog_posts, 'csrf_token':c['csrf_token']})


def archive_posts(request, year, month):
    blog_posts = Post.objects.filter(status="P",created_on__year=year,created_on__month=month).order_by('-created_on')
    page_list=Page.objects.all()
    items_per_page = 6
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(blog_posts.count()) / items_per_page))
    blog_posts = blog_posts[(page - 1) * items_per_page:page * items_per_page]
    c = {}
    c.update(csrf(request))
    return render_to_response('site/blog/index.html', {'pagelist':page_list,'current_page':page,'last_page':no_pages,
                                                        'posts':blog_posts,'csrf_token':c['csrf_token']})

@login_required
def admin_post_list(request):
    blog_posts = Post.objects.all()
    return render(request,'admin/blog/blog-posts.html',{'blog_posts':blog_posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        validate_blog = BlogpostForm(request.POST)
        if validate_blog.is_valid():
            blog_post = validate_blog.save(commit=False)
            blog_post.user=request.user
            
            blog_post.status = 'D'
            
            if request.POST.get('status') == "P":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_admin:
                    blog_post.status = 'P'
                
            elif request.POST.get('status') == "T":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_admin:
                    blog_post.status = 'T'
            
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
    return render(request,'admin/blog/blog-new.html',{'categories':categories,'csrf_token':c['csrf_token']})


@login_required
def edit_blog_post(request,blog_slug):
    if request.method == 'POST':
        current_post = Post.objects.get(slug = blog_slug)
        validate_blog = BlogpostForm(request.POST,instance=current_post)
        if validate_blog.is_valid():
            blog_post = validate_blog.save(commit=False)

            blog_post.status = 'D'
            
            if request.POST.get('status') == "P":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_admin:
                    blog_post.status = 'P'
                
            elif request.POST.get('status') == "T":
                if request.user.user_roles == "Admin" or request.user.is_special or request.user.is_admin:
                    blog_post.status = 'T'
            
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
            data = {'error':False,'response':'Blog Post edited'}
        else:
            data = {'error':True,'response':validate_blog.errors}
        return HttpResponse(json.dumps(data))
    blog_post = Post.objects.get(slug=blog_slug)
    categories = Category.objects.all()
    if request.user.is_admin or blog_post.user ==request.user :
        c = {}
        c.update(csrf(request))
        return render(request,'admin/blog/blog-edit.html',{'blog_post':blog_post,'categories':categories,'csrf_token':c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def delete_post(request,blog_slug):
    blog_post = Post.objects.get(slug=blog_slug)
    if request.user == blog_post.user or request.user.is_admin:
        blog_post.delete()
        data = {"error":False,'message':'Blog Post Deleted'}
    else:
        data = {"error":True,'message':'admin or owner can delete blog post'}
    return HttpResponse(json.dumps(data))


@login_required
def view_post(request,blog_slug):
    blog_post = Post.objects.get(slug=blog_slug)
    return render_to_response('admin/blog/view_post.html',{'post':blog_post})


def report(request):
    envelope={}
    envelope=request.POST.get('envelope')
    my_dict = literal_eval(envelope)
    user=User.objects.get(email=my_dict['from'])
    rep = DailyReport.objects.create(employee=user,report=request.POST.get('text'))
    if request.POST.get('attachment-info'):
        my_dict1 = literal_eval(request.POST.get('attachment-info'))
        for key in my_dict1.keys():
            Dailyreport_files.objects.create(dailyreport=rep,attachments=my_dict1[key]['filename'],date=datetime.datetime.now().date())
    rep.save()
    print "HTTP/1.1 200 OK"
    return HttpResponseRedirect('/portal/')


def contact(request):
    validate_simplecontact = SimpleContactForm(request.POST)
    validate_contact = ContactForm(request.POST)

    if 'category' in request.POST.keys():
        if validate_simplecontact.is_valid() and validate_contact.is_valid():
            contact = simplecontact.objects.create(full_name=request.POST.get('full_name'),message=request.POST.get('message'),\
                                                        email=request.POST.get('email'),phone=request.POST.get('phone') if request.POST.get('phone') else False)
            Contact.objects.create(contact_info=contact,category=request.POST.get('category'),domain=request.POST.get('category'),domain_url=request.POST.get('doamin_url'),\
                skype=request.POST.get('skype'),country=request.POST.get('country'),budget=request.POST.get('budget'),technology=request.POST.get('technology'),\
                requirements=request.POST.get('requirements'),enquery_type=request.POST.get('enquery_type'))
        else:
            errors = {}
            errors=dict((validate_simplecontact.errors).items() + (validate_contact.errors).items())
            data = {'error':True, 'errinfo':errors}
            return HttpResponse(json.dumps(data))

    if validate_simplecontact.is_valid():
        simplecontact.objects.create(full_name=request.POST.get('full_name'),message=request.POST.get('message'),email=request.POST.get('email'),phone=request.POST.get('phone') if request.POST.get('phone') else False)
    else:
        errors = {}
        errors=dict((validate_simplecontact.errors).items())
        data = {'error':True, 'errinfo':errors}
        return HttpResponse(json.dumps(data))

    send_mail('Thank u for ur message', request.POST.get('message'),request.POST.get('email') ,[request.POST.get('email')], fail_silently=False)
    data = {'error':False, 'response': 'submitted successfully'}

    return HttpResponse(json.dumps(data))
    
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from micro_blog.models import Image_File, Category, Tags, Post
from PIL import Image
import os
from django.core.files.storage import default_storage
from django.core.files.base import File as fle
from micro_blog.forms import BlogpostForm, BlogCategoryForm
from microsite.settings import BLOG_IMAGES
from datetime import datetime

def store_image(img,location):
    ''' takes the image file and stores that in the local file storage returns file name with 
    adding of timestamp to its name'''
    
    uploaded_file = img
    filename = uploaded_file.name
    now_str = str(datetime.now())
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
def blog_category_list(request):
    blog_categories = Category.objects.all()
    return render_to_response('admin/blog/blog-category-list.html',{'blog_categories':blog_categories})


@login_required
def new_category(request):
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
    return HttpResponseRedirect('/portal/blog/category-list/')


def blog_index(request):
	return render_to_response('site/blog/index.html')


def blog_article(request, slug):
	return render_to_response('site/blog/article.html')


def blog_tag(request, tag):
    return render_to_response('site/blog/index.html')


def blog_category(request, tag):
    return render_to_response('site/blog/category.html')


@login_required
def index(request):
	blog_posts = Post.objects.all()
	return render_to_response('admin/blog/blog-posts.html',{'blog_posts':blog_posts})


@login_required
def new(request):
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
                        	print 'hi'
                		blog_post.featured_image=store_image(request.FILES.get('featuredimage'),BLOG_IMAGES)

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
			blog_post = validate_blog.save(commit=False)
			blog_post.user=request.user
			if request.POST.get('status'):
				blog_post.status='D'
			else:
				blog_post.status='P'

			if request.POST.get('featured_post',''):
				blog_post.featured_post==request.POST.get('featured_post')

			if 'featuredimage' in request.FILES:
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
    return HttpResponseRedirect('/portal/blog/')


@login_required
def delete_post(request,blog_slug):
    blog_post = Post.objects.get(slug=blog_slug)
    blog_post.delete()
    return HttpResponseRedirect('/portal/blog/')


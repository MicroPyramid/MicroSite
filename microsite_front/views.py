from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from micro_admin.models import career
import requests
from django.conf import settings
from mimetypes import MimeTypes
from boto.s3.connection import S3Connection
import json
from datetime import datetime, timedelta
from micro_blog.models import Category, Post
from django.views.static import serve
import yaml
import os
from itertools import chain
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'site/index.html', {
        'google_analytics_code': settings.GOOGLE_ANALYTICS_CODE})


def books(request, path):
    if path is None or path == '':
        documents_file = open(os.path.join(
            settings.BASE_DIR + '/books/', 'books.yml'), 'r')
        data = yaml.load(documents_file)
        books = []
        if data.get("documents") and data.get("documents") != None:
            if request.user.is_authenticated():
                books = [
                    book for position, book in sorted(
                        data['documents'].items())]
            else:
                books = [
                    book for position, book in sorted(
                        data['documents'].items()
                    ) if book.get("visibilty").lower() == "public"]
        return render(request, "site/books.html", {"books": books})
        # return render(request, 'html/index.html')
    else:
        # if path.endswith('html'):
        #     return render(request, 'html/' + path)
        # else:
        return serve(
            request, path,
            document_root=settings.BASE_DIR + '/books/templates/html/')

# def career_page(request):
#     jobs = career.objects.filter(is_active=True).order_by('created_on')
#     return render(request, 'site/careers.html', {'jobs': jobs})


@login_required(login_url='/')
def tools(request):
    return render(request, 'site/tools/index.html')


@login_required(login_url='/')
def url_checker_tool(request):
    if request.method == "POST":
        redirects_count = []
        urls = []
        responses = []

        if request.POST.get('urls'):
            urls = request.POST.get('urls').split('\r\n')
        if request.FILES.get('file'):
            for line in request.FILES.get('file'):
                urls.append(line.rstrip('\r\n'))

        for url in urls:
            if url:
                try:
                    response = requests.head(url, allow_redirects=True)
                except Exception:
                    response = {'url': url, 'status_code': 'Invalid Url'}
                responses.append(response)
                try:
                    response_history = len(response.history)
                except Exception:
                    response_history = 0
                redirects_count.append(response_history)

        max_redirects = max(redirects_count) if redirects_count else 1
        return render(request, 'site/tools/url_checker.html', {'responses': responses, 'max_redirects': max_redirects})

    return render(request, 'site/tools/url_checker.html')


@login_required(login_url='/')
def s3_objects_set_metadata(request):
    if request.method == "POST":
        errors = {}
        if not request.POST.get('expiry_time').isnumeric():
            errors['expiry_time'] = "Expiry Time must be in number of days."

        if not request.POST.get('max_age').isnumeric():
            errors['max_age'] = "Invalid max-age value. Max Age must be in seconds."

        # Make an S3 Connection
        conn = S3Connection(request.POST.get('access_key'), request.POST.get('secret_key'))

        # Get a bucket from S3 or None if the bucket does not exist
        bucket = conn.lookup(request.POST.get('bucket_name'))
        if not bucket:
            errors['bucket_name'] = "NoSuchBucket - The specified bucket does not exist."

        if errors:
            return HttpResponse(json.dumps({"error": True, "errors": errors}), content_type='application/json; charset=utf-8')

        for x in bucket.list():
            mime_type = MimeTypes().guess_type(x.key)
            expires = datetime.utcnow() + timedelta(days=request.POST.get('expiry_time'))
            expiration_period = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

            if mime_type[0] is not None:
                x.set_metadata('Cache-Control', 'max-age = ' + request.POST.get('max_age'))
                x.set_metadata('Expires', expiration_period)
                x.set_metadata('Content-Type', mime_type[0])

                x.copy(
                    x.bucket.name,
                    x.name,
                    x.metadata,
                    preserve_acl=True
                )

        return HttpResponse(json.dumps({"error": False}),
                            content_type='application/json; charset=utf-8')

    return render(request, 'site/tools/s3_objects_set_metadata.html')


def html_sitemap(request):
    page = request.GET.get('page')
    categories = Category.objects.all()
    blog_posts = Post.objects.filter(status='P').order_by('-published_on')
    sitemap_links = list(chain(categories, blog_posts))

    object_list = Paginator(sitemap_links, 100)
    try:
        sitemap_links = object_list.page(page)
    except PageNotAnInteger:
        sitemap_links = object_list.page(1)
    except EmptyPage:
        sitemap_links = object_list.page(object_list.num_pages)
    return render(request, 'site/sitemap.html',  {'sitemap_links': sitemap_links})

def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)

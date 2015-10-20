from django.shortcuts import render
from django.http.response import HttpResponse
from micro_admin.models import career
import requests
from django.conf import settings
from mimetypes import MimeTypes
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import time
import json
import boto
from datetime import datetime, timedelta


def index(request):
    latest_featured_posts = {} #Post.objects.filter(status = 'P',featured_post = 'on').order_by('-created_on')[:2]
    return render(request, 'site/index.html', {'latest_featured_posts': latest_featured_posts, 
                            'google_analytics_code': settings.GOOGLE_ANALYTICS_CODE})


def career_page(request):
    jobs = career.objects.filter(is_active=True).order_by('created_on')
    return render(request, 'site/careers.html', {'jobs': jobs})


def tools(request):
    return render(request, 'site/tools/index.html')


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
                except:
                    response = {'url': url, 'status_code': 'Invalid Url'}
                responses.append(response)
                try:
                    response_history = len(response.history)
                except:
                    response_history = 0
                redirects_count.append(response_history)

        max_redirects = max(redirects_count) if redirects_count else 1
        return render(request, 'site/tools/url_checker.html', {'responses': responses,
                        'max_redirects': max_redirects})

    return render(request, 'site/tools/url_checker.html')


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
            return HttpResponse(json.dumps({"error": True, "errors": errors}),
                                    content_type='application/json; charset=utf-8')

        for x in bucket.list():
            mime_type = MimeTypes().guess_type(x.key)
            expires = datetime.utcnow() + timedelta(days=request.POST.get('expiry_time'))
            expiration_period = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

            if mime_type[0] is not None:
                x.set_metadata('Cache-Control', 'max-age = '+ request.POST.get('max_age'))
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


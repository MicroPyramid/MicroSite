from django.shortcuts import render
from micro_admin.models import career
import requests


def index(request):
    latest_featured_posts = {} #Post.objects.filter(status = 'P',featured_post = 'on').order_by('-created_on')[:2]
    return render(request, 'site/index.html', {'latest_featured_posts': latest_featured_posts})


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
                count = 0
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
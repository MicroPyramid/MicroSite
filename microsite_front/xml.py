import time
from email import utils
from django.http.response import HttpResponse 
from pages.models import Page
from micro_blog.models import Category, Post


def sitemap(request):

    # pages, blog categories, blog posts

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''

    pages = Page.objects.filter(is_active = True)
    for page in pages:
        xml = xml + '<url><loc>http://micropyramid.com/page/' + page.slug + '</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    categories = Category.objects.all()
    for category in categories:
        xml = xml + '<url><loc>http://micropyramid.com/blog/category/' + category.slug + '</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    posts = Post.objects.filter(status = "P")
    for post in posts:
        xml = xml + '<url><loc>http://micropyramid.com/blog/' + post.slug + '</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    xml = xml + '</urlset>'

    return HttpResponse(xml,content_type="text/xml")


def rss(request):

    xml = '''<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
                <channel>
                <atom:link href="http://micropyramid.com/rss.xml" rel="self" type="application/rss+xml" />
                <title>MicroPyramid | Web Development | Mobile App Development</title>
                <description>MicroPyramid python development company.
                 Our ambit of service encompasses and is as vivid as e-commerce,
                  web applications, news portals, community and job portals design &amp;
                   development. We work on Python, Django, Mongodb, Responsive web design, CSS3,
                    JavaScript, Jquery, Angularjs, Amazon web services, iphone, ruby on rails</description>
                <link>http://micropyramid.com</link>
                <category domain="micropyramid.com">
                MicroPyramid | Web Development | Mobile App Development
                </category>
                <copyright>Copyright 2014 MicroPyramid Informatics Private Limited</copyright>
                <language>en-us</language>
                <image>
                <url>http://micropyramid.com/static/site/images/logo.png</url>
                <title>MicroPyramid | Web Development | Mobile App Development</title>
                <link>http://micropyramid.com</link>
                <description>MicroPyramid python development company.
                 Our ambit of service encompasses and is as vivid as e-commerce,
                 web applications, news portals, community and job portals design &amp;
                  development. We work on Python, Django, Mongodb, Responsive web design, CSS3,
                   JavaScript, Jquery, Angularjs, Amazon web services, iphone, ruby on rails</description>
                </image>
                    '''
    if 'category' in request.GET.keys():
        posts = Post.objects.filter(status = 'P', category__name=request.GET.get('category')).order_by('-updated_on')[:10]
    else:
        posts = Post.objects.filter(status = 'P').order_by('-updated_on')[:10]
        
    for post in posts:

        nowtuple = post.updated_on.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        published_date = utils.formatdate(nowtimestamp)

        xml = xml + '<item><title><![CDATA[' + post.title + ']]></title>'
        xml = xml + '<description><![CDATA[' + post.content + ']]></description>'
        xml = xml + '<link>http://micropyramid.com/blog/' + post.slug + '</link>'
        xml = xml + '<category domain="micropyramid.com"><![CDATA[' + post.category.name + ']]></category>'
        xml = xml + '<comments>http://micropyramid.com/blog/' + post.slug + '</comments>'
        xml = xml + '<pubDate>' + published_date + '</pubDate>'
        xml = xml + '<guid>http://micropyramid.com/tutorial/article/' + post.slug + '</guid></item>'

    xml = xml + '</channel></rss>'

    return HttpResponse(xml,content_type="text/xml")
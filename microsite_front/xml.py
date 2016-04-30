import time
from email import utils
from django.http.response import HttpResponse
from pages.models import Page, Menu
from micro_blog.models import Category, Post
import math


def sitemap(request):

    # pages, blog categories, blog posts

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
             <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
             http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'''

    menus = Menu.objects.filter()
    for menu in menus:
        xml = xml + '<url><loc>' + menu.url + '/</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    categories = Category.objects.filter(is_display=True)
    for category in categories:
        if category.post_set.filter(status='P').exists():
            xml = xml + '<url><loc>https://micropyramid.com/blog/category/' + category.slug
            xml = xml + '/</loc><changefreq>daily</changefreq><priority>0.85</priority>/</url>'

    posts = Post.objects.filter(status="P").order_by('-published_on')
    for post in posts:
        xml = xml + '<url><loc>https://micropyramid.com/blog/' + post.slug + '/</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    no_pages = int(math.ceil(float(posts.count()) / 10))
    for page_num in range(1, no_pages+1):
        xml = xml + '<url><loc>https://micropyramid.com/blog/?page=' + str(page_num) + '/</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    xml = xml + '<url><loc>https://micropyramid.com/sitemap/</loc><changefreq>daily</changefreq><priority>0.5</priority></url>'
    xml = xml + '</urlset>'

    return HttpResponse(xml, content_type="text/xml")


def rss(request):

    xml = '''<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
                <channel>
                <atom:link href="https://micropyramid.com/rss.xml" rel="self" type="application/rss+xml" />
                <title>MicroPyramid | Web Development | Mobile App Development</title>
                <description>MicroPyramid python development company.
                 Our ambit of service encompasses and is as vivid as e-commerce,
                  web applications, news portals, community and job portals design &amp;
                   development. We work on Python, Django, Mongodb, Responsive web design, CSS3,
                    JavaScript, Jquery, Angularjs, Amazon web services, iphone, ruby on rails</description>
                <link>https://micropyramid.com</link>
                <category domain="micropyramid.com">
                MicroPyramid | Web Development | Mobile App Development
                </category>
                <copyright>Copyright 2014 MicroPyramid Informatics Private Limited</copyright>
                <language>en-us</language>
                <image>
                <url>https://micropyramid.com/static/site/images/logo.png</url>
                <title>MicroPyramid | Web Development | Mobile App Development</title>
                <link>https://micropyramid.com</link>
                <description>MicroPyramid python development company.
                 Our ambit of service encompasses and is as vivid as e-commerce,
                 web applications, news portals, community and job portals design &amp;
                  development. We work on Python, Django, Mongodb, Responsive web design, CSS3,
                   JavaScript, Jquery, Angularjs, Amazon web services, iphone, ruby on rails</description>
                </image>
                    '''
    if 'category' in request.GET.keys():
        posts = Post.objects.filter(status='P', category__name__icontains=request.GET.get('category')).order_by('-updated_on')[:10]
    else:
        posts = Post.objects.filter(status='P').order_by('-updated_on')[:10]
    for post in posts:

        nowtuple = post.updated_on.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        published_date = utils.formatdate(nowtimestamp)

        xml = xml + '<item><title><![CDATA[' + post.title + ']]></title>'
        xml = xml + '<description><![CDATA[' + post.content + ']]></description>'
        xml = xml + '<link>https://micropyramid.com/blog/' + post.slug + '/</link>'
        xml = xml + '<category domain="micropyramid.com"><![CDATA[' + post.category.name + ']]></category>'
        xml = xml + '<comments>https://micropyramid.com/blog/' + post.slug + '/</comments>'
        xml = xml + '<pubDate>' + published_date + '</pubDate>'
        xml = xml + '<guid>https://micropyramid.com/blog/' + post.slug + '/</guid></item>'

    xml = xml + '</channel></rss>'

    return HttpResponse(xml, content_type="text/xml")


def blog_rss(request):

    xml = '''<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
                <channel>
                <atom:link href="https://micropyramid.com/blog.rss" rel="self" type="application/rss+xml" />
                <title>MicroPyramid | Web Development | Mobile App Development</title>
                <description>MicroPyramid python development company.
                 Our ambit of service encompasses and is as vivid as e-commerce,
                  web applications, news portals, community and job portals design &amp;
                   development. We work on Python, Django, Mongodb, Responsive web design, CSS3,
                    JavaScript, Jquery, Angularjs, Amazon web services, iphone, ruby on rails</description>
                <link>https://micropyramid.com</link>
                <category domain="micropyramid.com">
                MicroPyramid | Web Development | Mobile App Development
                </category>
                <copyright>Copyright 2014 MicroPyramid Informatics Private Limited</copyright>
                <language>en-us</language>
                <image>
                <url>https://micropyramid.com/static/site/images/logo.png</url>
                <title>MicroPyramid | Web Development | Mobile App Development</title>
                <link>https://micropyramid.com</link>
                <description>MicroPyramid python development company.
                 Our ambit of service encompasses and is as vivid as e-commerce,
                 web applications, news portals, community and job portals design &amp;
                  development. We work on Python, Django, Mongodb, Responsive web design, CSS3,
                   JavaScript, Jquery, Angularjs, Amazon web services, iphone, ruby on rails</description>
                </image>
                    '''
    if 'category' in request.GET.keys():
        posts = Post.objects.filter(status='P', category__name__icontains=request.GET.get('category')).order_by('-updated_on')[:10]
    else:
        posts = Post.objects.filter(status='P').order_by('-updated_on')[:10]

    for post in posts:

        nowtuple = post.updated_on.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        published_date = utils.formatdate(nowtimestamp)

        xml = xml + '<item><title><![CDATA[' + post.title + ']]></title>'
        xml = xml + '<description><![CDATA[' + post.get_content() + ']]></description>'
        xml = xml + '<link>https://micropyramid.com/blog/' + post.slug + '/</link>'
        xml = xml + '<category domain="micropyramid.com"><![CDATA[' + post.category.name + ']]></category>'
        xml = xml + '<comments>https://micropyramid.com/blog/' + post.slug + '/</comments>'
        xml = xml + '<pubDate>' + published_date + '</pubDate>'
        xml = xml + '<guid>https://micropyramid.com/blog/' + post.slug + '/</guid></item>'

    xml = xml + '</channel></rss>'

    return HttpResponse(xml, content_type="text/xml")

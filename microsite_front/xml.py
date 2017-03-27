import time
from email import utils
from django.http.response import HttpResponse
from pages.models import Page, Menu
from micro_blog.models import Category, Post
import math


def sitemap_xml(request, **kwargs):
    country = request.COUNTRY_CODE
    if kwargs:
        country = kwargs['country_name']

    # pages, blog categories, blog posts

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
             <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
             http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'''

    xml = xml + '<url><loc>https://micropyramid.com/' + str(country) + '/</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    menus = Menu.objects.filter(status="on", url__isnull=False).exclude(title='Python Development').exclude(url__in=['/', 'blog'])
    for menu in menus:
        if menu.url and str(menu.url) != 'none':
            if country == 'us':
                xml = xml + '<url><loc>https://micropyramid.com/' + menu.url + '</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'
            else:
                xml = xml + '<url><loc>https://micropyramid.com/' + str(country) + '/' + menu.url + '/</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'
    categories = Category.objects.filter(is_display=True)
    for category in categories:
        if category.post_set.filter(status='P').exists():
            xml = xml + '<url><loc>https://micropyramid.com/blog/category/' + category.slug + '/'
            xml = xml + '/</loc><changefreq>daily</changefreq><priority>0.85</priority>/</url>'

    posts = Post.objects.filter(status="P").order_by('-published_on')
    for post in posts:
        xml = xml + '<url><loc>https://micropyramid.com/blog/' + post.slug + '/</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    no_pages = int(math.ceil(float(posts.count()) / 10))
    for page_num in range(1, no_pages+1):
        xml = xml + '<url><loc>https://micropyramid.com/blog/' + str(page_num) + '/</loc><changefreq>daily</changefreq><priority>0.85</priority></url>'

    xml = xml + '<url><loc>https://micropyramid.com/sitemap/</loc><changefreq>daily</changefreq><priority>0.5</priority></url>'
    xml = xml + '</urlset>'

    return HttpResponse(xml, content_type="text/xml")


def rss(request):

    xml = '''<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
                <channel>
                <atom:link href="https://micropyramid.com/rss.xml" rel="self" type="application/rss+xml" />
                <title>MicroPyramid | Web Development | Mobile App Development</title>
                <description>MicroPyramid python development company.
                  MicroPyramid python development company.
                  Our ambit of service encompasses and is as vivid as e-commerce,
                  web applications, news portals, community and job portals design &amp;
                  development. We work on Python, Django, nodejs, Mongodb, Responsive web design, CSS3,
                  JavaScript, Jquery, Angularjs, Amazon web services</description>
                <link>https://micropyramid.com</link>
                <category domain="micropyramid.com">
                MicroPyramid | Web Development | Mobile App Development
                </category>
                <copyright>Copyright 2014 MicroPyramid</copyright>
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
                 MicroPyramid python development company.
                  Our ambit of service encompasses and is as vivid as e-commerce,
                  web applications, news portals, community and job portals design &amp;
                  development. We work on Python, Django, nodejs, Mongodb, Responsive web design, CSS3,
                  JavaScript, Jquery, Angularjs, Amazon web services</description>
                <link>https://micropyramid.com</link>
                <category domain="micropyramid.com">
                MicroPyramid | Web Development | Mobile App Development
                </category>
                <copyright>Copyright 2014 MicroPyramid</copyright>
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
        posts = Post.objects.filter(status='P', category__name__icontains=request.GET.get('category')).order_by('-published_on')[:10]
    else:
        posts = Post.objects.filter(status='P').order_by('-published_on')[:10]

    for post in posts:

        nowtuple = post.updated_on.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        published_date = utils.formatdate(nowtimestamp)

        xml = xml + '<item><title><![CDATA[' + post.title + ']]></title>'
        xml = xml + '<description><![CDATA[' + post.excerpt + ']]></description>'
        xml = xml + '<link>https://micropyramid.com/blog/' + post.slug + '/</link>'
        xml = xml + '<category domain="micropyramid.com"><![CDATA[' + post.category.name + ']]></category>'
        xml = xml + '<comments>https://micropyramid.com/blog/' + post.slug + '/</comments>'
        xml = xml + '<pubDate>' + published_date + '</pubDate>'
        xml = xml + '<guid>https://micropyramid.com/blog/' + post.slug + '/</guid></item>'

    xml = xml + '</channel></rss>'

    return HttpResponse(xml, content_type="text/xml")


def facebook_rss(request):
    xml = '''<rss version="2.0"
             xmlns:content="http://purl.org/rss/1.0/modules/content/">
            <channel>
            <title>Django and Python Web Development | Application Development Services India – MicroPyramid</title>
            <link>https://micropyramid.com</link>
            <description>
              MicroPyramid python development company.
              Our ambit of service encompasses and is as vivid as e-commerce,
              web applications, news portals, community and job portals design &amp;
              development. We work on Python, Django, nodejs, Mongodb, Responsive web design, CSS3,
              JavaScript, Jquery, Angularjs, Amazon web services
            </description>
            <language>en-us</language>
            <lastBuildDate>2016-05-17T04:44:16Z</lastBuildDate>'''
    posts = Post.objects.filter(status='P').order_by('-published_on')[:50]

    for post in posts:
        if post.published_on:
            nowtuple = post.published_on.timetuple()
        else:
            nowtuple = post.updated_on.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        published_date = utils.formatdate(nowtimestamp)
        xml = xml + '<item><title>' + post.title + '</title>'
        xml = xml + '<link>https://micropyramid.com/blog/' + post.slug + '/</link>'
        xml = xml + '<guid>' + str(post.slug) + '</guid>'
        xml = xml + '<pubDate>' + published_date + '</pubDate>'
        xml = xml + '<author>' + post.user.get_full_name() + '</author>'
        xml = xml + '<description>' + post.title + '</description>'
        xml = xml + '<content:encoded><![CDATA[<!doctype html><html lang="en" prefix="op: http://media.facebook.com/op#">'
        xml = xml + '<head><meta charset="utf-8">'
        xml = xml + '<link rel="canonical" href="https://micropyramid.com/blog/' + post.slug + '/">'
        xml = xml + '<meta property="op:markup_version" content="v1.0">'
        xml = xml + '</head><body><article>'
        xml = xml + '<header>'
        xml = xml + str(post.title) + ' - Micropyramid'
        xml = xml + '</header>'
        xml = xml + '<p>' + post.excerpt + '</p>'
        xml = xml + '</article></body></html>]]>'
        xml = xml + '</content:encoded></item>'

    xml = xml + '</channel></rss>'

    return HttpResponse(xml, content_type="text/xml")

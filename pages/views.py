from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from pages.models import Page, Menu
from pages.forms import MenuForm, PageForm
from django.db.models.aggregates import Max
import itertools
from micro_blog.models import Category, Post
from django.template.defaultfilters import slugify


@login_required
def pages(request):
    pagelist = Page.objects.all().order_by('id')
    return render(request, 'admin/content/page/page-list.html', {'pages': pagelist})


@login_required
def new_page(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        validate_page = PageForm(request.POST)
        if validate_page.is_valid():
            page = validate_page.save(commit = False)
            page.slug = slugify(request.POST.get('slug'))
            page.save()
            page.category.add(*request.POST.getlist('category'))
            data = {"error": False, 'response': 'Page created successfully'}
        else:
            data = {"error": True, 'response': validate_page.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    if request.user.is_superuser:
        c = {}
        c.update(csrf(request))
        return render(
            request,
            'admin/content/page/new-page.html',
            {
                'csrf_token': c['csrf_token'],
                'categories': categories
            })
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def delete_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.user.is_superuser:
        page.delete()
        return HttpResponseRedirect('/portal/content/page/')
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def edit_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        validate_page = PageForm(request.POST, instance=page)
        if validate_page.is_valid():
            page = validate_page.save(commit = False)
            page.slug = slugify(request.POST.get('slug'))
            page.save()
            page.category.clear()
            page.category.add(*request.POST.getlist('category'))

            data = {"error": False, 'response': 'Page updated successfully'}
        else:
            data = {"error": True, 'response': validate_page.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    if request.user.is_superuser:
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/content/page/edit-page.html',
                      {'page': page, 'csrf_token': c['csrf_token'], 'categories': categories})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def delete_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.user.is_superuser:
        menu.delete()
        return HttpResponseRedirect('/portal/content/menu/')
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def change_menu_status(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if menu.status == "on":
        menu.status = "off"
    else:
        menu.status = "on"
    menu.save()
    return HttpResponseRedirect('/portal/content/menu/')


@login_required
def change_page_status(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if page.is_active:
        page.is_active = False
    else:
        page.is_active = True
    page.save()
    return HttpResponseRedirect('/portal/content/page/')


@login_required
def menu(request):
    iterator = itertools.count()
    menu_list = Menu.objects.filter(parent=None).order_by('lvl')
    return render(request, 'admin/content/menu/menu-list.html',
                  {'menu_list': menu_list, 'iterator': iterator})


@login_required
def add_menu(request):
    if request.method == 'POST':
        validate_menu = MenuForm(request.POST)
        if validate_menu.is_valid():
            new_menu = validate_menu.save(commit=False)
            if request.POST.get('status', ''):
                new_menu.status = 'on'

            menu_count = Menu.objects.filter(parent=new_menu.parent).count()
            new_menu.lvl = menu_count + 1
            if request.POST.get('url'):
                new_menu.url = request.POST.get('url').rstrip('/')

            new_menu.save()
            data = {"error": False, 'response': 'Menu created successfully'}
        else:
            data = {"error": True, 'response': validate_menu.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    if request.user.is_superuser:
        c = {}
        c.update(csrf(request))
        parent = Menu.objects.filter(parent=None).order_by('lvl')
        return render(request, 'admin/content/menu/new-menu-item.html',
                      {'parent': parent, 'csrf_token': c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def edit_menu(request, pk):
    if request.method == 'POST':
        menu_instance = get_object_or_404(Menu, pk=pk)
        current_parent = menu_instance.parent
        current_lvl = menu_instance.lvl
        validate_menu = MenuForm(request.POST, instance=menu_instance)

        if validate_menu.is_valid():
            updated_menu = validate_menu.save(commit=False)
            if updated_menu.parent != current_parent:
                try:
                    if updated_menu.parent.id == updated_menu.id:
                        data = {'error': True, 'response': {
                            'parent': 'you can not choose the same as parent'}}
                        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
                except Exception:
                    pass

                lnk_count = Menu.objects.filter(
                    parent=updated_menu.parent).count()
                updated_menu.lvl = lnk_count + 1
                lvlmax = Menu.objects.filter(
                    parent=current_parent).aggregate(Max('lvl'))['lvl__max']
                if lvlmax != 1:
                    for i in Menu.objects.filter(parent=current_parent, lvl__gt=current_lvl, lvl__lte=lvlmax):
                        i.lvl = i.lvl-1
                        i.save()
            if request.POST.get('url'):
                updated_menu.url = request.POST.get('url').rstrip('/')
            else:
                updated_menu.url = 'none'

            if request.POST.get('status', ''):
                updated_menu.status = 'on'

            updated_menu.save()

            data = {'error': False, 'response': 'updated successfully'}
        else:
            data = {'error': True, 'response': validate_menu.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    if request.user.is_superuser:
        parent = Menu.objects.filter(parent=None).order_by('lvl')
        current_menu = get_object_or_404(Menu, pk=pk)
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/content/menu/edit-menu-item.html',
                      {'csrf_token': c['csrf_token'], 'current_menu': current_menu, 'parent': parent})
    else:
        return render_to_response('admin/accessdenied.html')


def site_page(request, slug):
    # pages_slugs = ['web-development', 'web-design', 'testing', 'crm', 'server-maintenance']
    # if slug in pages_slugs:
    #     return render(request, 'site/pages/' + slug + '.html')
    # return render(request, '404.html', status=404)
    pages = Page.objects.filter(slug=slug)
    if pages:
        page = pages[0]
        posts = []
        if page.category.all():
            posts = Post.objects.filter(category__in=page.category.all(), status='P').order_by('-published_on')[:3]
        return render(request, 'site/page.html', {'page': page, 'posts': posts})
    else:
        return render(request, '404.html', status=404)

from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from pages.models import Page, Menu
from micro_blog.models import Country
from pages.forms import MenuForm, PageForm, PageNewForm
from django.db.models.aggregates import Max
import itertools
from micro_blog.models import Category, Post
from micro_blog.forms import customPageCountryInlineFormSet
from django.template.defaultfilters import slugify
from django.forms.models import inlineformset_factory, modelformset_factory
from django.db.models import Q
from django.core.urlresolvers import reverse


@login_required
def pages(request):
    pagelist = Page.objects.filter(parent=None).order_by('id')
    return render(request, 'admin/content/page/page-list.html', {'pages': pagelist})


@login_required
def new_page(request):
    categories = Category.objects.all()
    countries = Country.objects.all()
    if request.method == 'POST':
        validate_page = PageNewForm(request.POST)
        print (request.POST)
        if validate_page.is_valid():
            # page = Page.objects.create(name=request.POST['name'],
            #                            slug=request.POST['name'],
            #                            meta_description=request.POST['meta_description'],
            #                            meta_title=request.POST['meta_title'],
            #                            keywords=request.POST['keywords'],
            #                            content=request.POST['content'], )
            page = validate_page.save(commit=False)
            page.parent = None
            page.slug = slugify(request.POST.get('slug'))
            page.is_default = True
            if request.POST.get('country'):
                page.country_id = request.POST.get('country')
            else:
                country = Country.objects.get(name='India')
                page.country = country
            page.save()
            # for country in countries.exclude(name__iexact='India'):
            #     slug = str(country.code) + '/' + slugify(request.POST.get('slug'))
            #     Page.objects.create(title=request.POST.get('country'), country=country, parent=page, slug=slug)
            page.category.add(*request.POST.getlist('category'))
            data = {"error": False, 'response': 'Page created successfully'}
        else:
            print (validate_page.errors)
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
                'categories': categories,
                'countries': countries
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


def update_dict_keys(temp, name, keys):
    for key in keys:
        changed_key = name + '-' + key
        temp[changed_key] = temp[key]
        del temp[key]
    return temp


@login_required
def edit_page(request, pk):
    page = get_object_or_404(Page, pk=pk)
    categories = Category.objects.all()
    countries = Country.objects.all().order_by('id')
    PageCountryFormSet = inlineformset_factory(Page, Page,
                                            fields=('title', 'content', 'slug', 'meta_title', 'meta_description', 'keywords', 'is_active', 'is_default'),
                                            formset=customPageCountryInlineFormSet,
                                            extra=len(countries),
                                            )
    if request.method == 'POST':
        pagecountry_formset = PageCountryFormSet(request.POST)
        print (len(pagecountry_formset.forms))
        if pagecountry_formset.is_valid():
            print ("hello")
            print ("valid")
            print (request.POST)
            i= 0 
            for each in pagecountry_formset:
                if each.cleaned_data:
                    print ("hello")
                    print (each.cleaned_data)
                    print (i)
                    page_obj = each.save(commit=False)
                    if not page_obj.country:
                        page_obj.country = countries[i]
                    page_obj.save()
                    print ("page")
                    print (page_obj.parent)
                    if not page_obj.parent:
                        print ("inside parent")
                        print (page_obj.id)
                        if str(page_obj.id) != str(pk):
                            print ("inside pk")
                            page_obj.parent = page
                    page_obj.save()
                    i += 1
                else:
                    print (each.errors)
            # new_forms = pagecountry_formset.save_new()
            # for each in new_forms:
            #     each.parent = page
            #     each.save()
            # page_obj = pagecountry_formset.save()
            print ("save")
            print (page)
            # page = validate_page.save(commit = False)
            # page.slug = slugify(request.POST.get('slug'))
            # page.save()
            # page.category.clear()
            # page.category.add(*request.POST.getlist('category'))
            return HttpResponseRedirect(reverse('pages:pages'))
        else:
            pagecountry_formset = PageCountryFormSet(request.POST)
            print ("not valid")
            print (request.POST)
            if pagecountry_formset.errors:
                print (pagecountry_formset.errors)
    else:
        pagecountry_formset = PageCountryFormSet(request.POST)

    if request.user.is_superuser:
        c = {}
        c.update(csrf(request))
        if page.country:
            page_country_ids = Page.objects.filter(Q(pk=pk) | Q(parent=page)).values_list('country')
            country_ids = [{'country_id': country.id} for country in Country.objects.exclude(id__in=page_country_ids).order_by('id')]
        else:
            country_ids = [{'country_id': country.id} for country in Country.objects.all().order_by('id')]
        country_ids = [{'country_id': country.id} for country in Country.objects.all().order_by('id')]
        if request.method == 'POST':
            PageCountryFormSet = PageCountryFormSet(request.POST, initial=country_ids)
        else:
            PageCountryFormSet = PageCountryFormSet(queryset=Page.objects.filter(Q(pk=pk) | Q(parent=page)).order_by('id'), initial=country_ids)
        return render(request, 'admin/content/page/edit-page.html',
                      {'page': page, 'csrf_token': c['csrf_token'], 'categories': categories,
                       'countries': countries, 'pagecountry_formset': PageCountryFormSet, 'country_ids': country_ids})
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
    language_code = request.LANGUAGE_CODE
    pages = Page.objects.filter(slug=slug, country__code=language_code)
    if not pages:
        pages = Page.objects.filter(slug=slug, is_default=True)
    if pages:
        page = pages[0]
        posts = []
        if page.category.all():
            posts = Post.objects.filter(category__in=page.category.all(), status='P').order_by('-published_on')[:3]
        return render(request, 'site/page.html', {'page': page, 'posts': posts})
    else:
        return render(request, '404.html', status=404)

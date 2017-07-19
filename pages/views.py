from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from pages.models import Page, Menu
from micro_blog.models import Country
from pages.forms import MenuForm, PageForm
from django.db.models.aggregates import Max
from micro_blog.models import Category, Post
from django.template.defaultfilters import slugify
from django.utils.http import is_safe_url
from urllib.parse import unquote
from django.conf import settings
from microsite.utils import *


@login_required
def pages(request):
    pagelist = Page.objects.filter(parent=None).order_by('id')
    return render(request, 'admin/content/page/page-list.html', {'pages': pagelist})


@login_required
def new_page(request):
    categories = Category.objects.all()
    countries = Country.objects.all()
    if request.method == 'POST':
        validate_page = PageForm(request.POST)
        if validate_page.is_valid():
            page = validate_page.save(commit=False)
            page.parent = None
            page.slug = slugify(request.POST.get('slug'))
            page.is_default = True
            if request.POST.get('country'):
                page.country_id = request.POST.get('country')
            else:
                country = Country.objects.get(name__iexact='US')
                page.country = country
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


# @login_required
# def edit_page(request, pk):
#     page = get_object_or_404(Page, pk=pk)
#     categories = Category.objects.all()
#     countries = Country.objects.all().order_by('id')
#     PageCountryFormSet = inlineformset_factory(Page, Page,
#                                             form=PageForm,
#                                             formset=customPageCountryInlineFormSet,
#                                             extra=len(countries),
#                                             max_num=len(countries),
#                                             )
#     if request.method == 'POST':
#         pagecountry_formset = PageCountryFormSet(request.POST)
#         if pagecountry_formset.is_valid():
#             i= 1
#             for each in pagecountry_formset:
#                 print (each.prefix)
#                 form_id = each.prefix.replace('form-','')
#                 if each.cleaned_data:
#                     page_obj = each.save(commit=False)
#                     page_obj.country_id = each.data['id_country_'+str(form_id)]
#                     page_obj.save()
#                     if not page_obj.parent:
#                         if str(page_obj.id) != str(pk):
#                             page_obj.parent = page
#                     page_obj.save()
#                     i += 1
#                 else:
#                     pass
#                 print (i)
#             return HttpResponseRedirect(reverse('pages:pages'))
#         else:
#             pagecountry_formset = PageCountryFormSet(request.POST)
#             if pagecountry_formset.errors:
#                 pass
#     else:
#         pagecountry_formset = PageCountryFormSet(request.POST)

#     if request.user.is_superuser:
#         c = {}
#         c.update(csrf(request))
#         country_ids = [{'country_id': country.id} for country in Country.objects.all().order_by('id')]
#         if request.method == 'POST':
#             PageCountryFormSet = PageCountryFormSet(request.POST, initial=country_ids)
#         else:
#             PageCountryFormSet = PageCountryFormSet(queryset=Page.objects.filter(Q(pk=pk) | Q(parent=page)).order_by('country_id'), initial=country_ids)
#         return render(request, 'admin/content/page/edit-page.html',
#                       {'page': page, 'csrf_token': c['csrf_token'], 'categories': categories,
#                        'countries': countries, 'pagecountry_formset': PageCountryFormSet, 'country_ids': country_ids})
#     else:
#         return render_to_response('admin/accessdenied.html')

@login_required
def edit_page(request, pk):
    country = request.GET.get('country') if request.GET.get('country') else request.POST.get('country_id')
    page = Page.objects.filter(pk=pk, country__slug=country).first()
    if not page:
        page = Page.objects.filter(parent_id=pk, country__slug=country).first()
    if not page:
        page = ''
    categories = Category.objects.all()
    countries = Country.objects.all()
    if request.method == 'POST':
        if page:
            validate_page = PageForm(request.POST, instance=page)
        else:
            validate_page = PageForm(request.POST)
        if validate_page.is_valid():
            edit_page = validate_page.save(commit=False)
            edit_page.slug = slugify(request.POST.get('slug'))

            if request.POST.get('is_default', '') == 'true':
                edit_page.is_default = True
            else:
                edit_page.is_default = False
            country = Country.objects.filter(slug=country).first()
            edit_page.country = country
            edit_page.save()
            if str(edit_page.id) != str(pk):
                edit_page.parent_id = pk
                edit_page.save()

            edit_page.category.clear()
            edit_page.category.add(*request.POST.getlist('category'))

            data = {"error": False, 'response': 'Page updated successfully'}
        else:
            data = {"error": True, 'response': validate_page.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    if request.user.is_superuser:
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/content/page/edit-page.html',
                      {'page': page, 'csrf_token': c['csrf_token'], 'categories': categories,
                       'countries': countries})
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
    countries = Country.objects.all()
    country_slug = request.POST.get('country') if request.POST.get('country') else 'usa'
    menu_list = Menu.objects.filter(parent=None, country__slug=country_slug).order_by('lvl')
    return render(request, 'admin/content/menu/menu-list.html',
                  {'menu_list': menu_list, 'countries': countries, 'country_slug': country_slug})


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
        countries = Country.objects.all()
        return render(request, 'admin/content/menu/new-menu-item.html',
                      {'parent': parent, 'csrf_token': c['csrf_token'],
                       'countries': countries})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def edit_menu(request, pk):
    country = request.GET.get('country') if request.GET.get('country') else request.POST.get('country_id')
    menu_instance = Menu.objects.filter(pk=pk, country__slug=country).first()
    if not menu_instance:
        each = Menu.objects.filter(pk=pk).first()
        if each:
            menu_instance = Menu.objects.filter(title=each.title, country__slug=country).first()
    if request.method == 'POST':
        current_parent = menu_instance.parent
        current_lvl = menu_instance.lvl
        if menu_instance:
            validate_menu = MenuForm(request.POST, instance=menu_instance)
        else:
            validate_menu = MenuForm(request.POST)
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
        parent = Menu.objects.filter(parent=None, country__slug=country).order_by('lvl')
        countries = Country.objects.all()
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/content/menu/edit-menu-item.html',
                      {'csrf_token': c['csrf_token'], 'current_menu': menu_instance,
                       'parent': parent, 'countries': countries})
    else:
        return render_to_response('admin/accessdenied.html')


def site_page(request, slug):
    # pages_slugs = ['web-development', 'web-design', 'testing', 'crm', 'server-maintenance']
    # if slug in pages_slugs:
    #     return render(request, 'site/pages/' + slug + '.html')
    # return render(request, '404.html', status=404)
    if 'country' in request.session.keys() and request.session['country']:
        country_code = request.session['country']
    else:
        country_code = request.COUNTRY_CODE
    country = Country.objects.filter(code=slug)
    if country:
        if country[0].code == settings.COUNTRY_CODE:
            return HttpResponseRedirect('/')
        return render(request, 'site/index.html', {
            'google_analytics_code': settings.GOOGLE_ANALYTICS_CODE})

    page = Page.objects.filter(slug=slug, country__code=country_code, is_active=True).first()
    if not page:
        page = Page.objects.filter(slug=slug).first()
        if page:
            page = Page.objects.filter(title__iexact=page.title, country__code=country_code, is_active=True).first()
            return HttpResponseRedirect('/' + page.country.code + '/' + page.slug +'/')
    if not page:
        page = Page.objects.filter(slug=slug, is_default=True, is_active=True)
    if page:
        posts = Post.objects.filter(status='P').order_by('-published_on')
        if page.category.all():
            posts = Post.objects.filter(category__in=page.category.all(), status='P').order_by('-published_on')
        return render(request, 'site/page.html', {'page': page, 'posts': posts})
    else:
        return render(request, '404.html', status=404)

def get_country_code_from_path(path):
    country_code_prefix_re = re.compile(r'^/([\w-]+)(/|$)')
    regex_match = country_code_prefix_re.match(path)

    if regex_match:
        country_code = regex_match.group(1)
        if Country.objects.filter(code=country_code):
            return country_code
    return None



def set_country(request):

    next = request.POST.get('next', request.GET.get('next'))
    if ((next or not request.is_ajax()) and
            not is_safe_url(next, request.get_host())):
        next = request.META.get('HTTP_REFERER')
        if next:
            next = unquote(next)  # HTTP_REFERER may be encoded.
        if not is_safe_url(next, request.get_host()):
            next = '/'
        if request.POST.get('country'):
            path = request.META.get('HTTP_REFERER').replace(request.scheme+'://' + request.get_host(), '')

            country_code = get_country_code_from_path(path)
            if country_code:
                path = request.META.get('HTTP_REFERER').replace(request.scheme+'://' + request.get_host(), '').replace('/'+country_code, '')
            if request.POST.get('country') == settings.COUNTRY_CODE:
                next = path
            else:
                next = '/' + request.POST.get('country') + path
    response = HttpResponseRedirect(next) if next else HttpResponse(status=204)
    if request.method == 'POST':
        country_code = request.POST.get('country')
        if country_code:
            request.session['country'] = country_code
            if hasattr(request, 'session'):
                request.session['_country'] = country_code
            else:
                response.set_cookie(
                    settings.COUNTRY_COOKIE_NAME, country_code,
                    max_age=settings.COUNTRY_COOKIE_AGE,
                    path=settings.COUNTRY_COOKIE_PATH,
                    domain=settings.COUNTRY_COOKIE_DOMAIN,
                )
    return response

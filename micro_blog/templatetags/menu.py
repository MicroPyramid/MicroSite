from django import template
from micro_blog.models import Tags, Category, Post, Post_Slugs
from pages.models import Menu
from django.db.models import Count, Prefetch

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_tags(context):
    return Tags.objects.annotate(Num=Count('rel_posts')).filter(Num__gt = 0, rel_posts__status='P')[:20]


@register.assignment_tag(takes_context=True)
def get_categories(context):
    has_blog_posts_categories = []
    categories = Category.objects.filter(is_display=True)
    for category in categories:
        if Post.objects.filter(category_id=category.id, status='P').exists():
            has_blog_posts_categories.append(category)
    return has_blog_posts_categories


@register.assignment_tag(takes_context=True)
def get_latest_posts(context):
    return Post.objects.filter(status='P').order_by(
        '-published_on'
    ).select_related("user").prefetch_related(
        Prefetch(
            "slugs",
            queryset=Post_Slugs.objects.filter(is_active=True),
            to_attr="active_slugs"
        )
    )[:3]


@register.assignment_tag(takes_context=True)
def get_menus(context):
    # menu_list = Menu.objects.filter(status="on").prefetch_related(
    #     Prefetch("menu_set", queryset=Menu.objects.filter(
    #         status="on").order_by('lvl'), to_attr="active_children"
    #     )
    # )
    menus = []
    menu_list = Menu.objects.filter(parent=None, status='on').order_by('lvl')
    for menu in menu_list:
        if menu.menu_set.filter(status='on'):
            menus.append(menu)
    return menus


@register.assignment_tag(takes_context=True)
def get_child_menus(context):
    menus = []
    menu_list = Menu.objects.filter(status="on", parent__isnull=False).exclude(parent__title='Contact Us').order_by('lvl')
    for menu in menu_list:
        if not menu.menu_set.filter(status='on'):
            menus.append(menu)
    return menus


@register.assignment_tag(takes_context=True)
def get_single_level_menus(context):
    menus = []
    menu_list = Menu.objects.filter(parent=None, status='on').order_by('lvl')
    for menu in menu_list:
        if not menu.menu_set.filter(status='on'):
            menus.append(menu)
    return menus

@register.assignment_tag(takes_context=True)
def get_all_menus(context):
    menu_list = Menu.objects.filter(status="on", parent=None).prefetch_related(
        Prefetch("menu_set", queryset=Menu.objects.filter(
            status="on").order_by('lvl'), to_attr="active_children"
        )
    )
    return menu_list.order_by('lvl')
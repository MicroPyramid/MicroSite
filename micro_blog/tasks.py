from celery.decorators import task
import sendgrid
from django.conf import settings
from micro_blog.models import Subscribers, Post, Category
from .send_grid import *
import datetime
from micro_admin.models import User
from django.template import loader


@task
def create_contact_in_category(category_name, email_address):
    '''
    Checks whether the category exists on not if it does then it will create a contact and save in
    database under sendgrid_user_id field and then add contact to list. If not create a category list
    then contact then adds contact to the new category
    list which eliminates the duplicates, also if any contact or list already exists then it return
    the object which avoids creating duplicates.

    Tested Cases:
    existing category new user -PASS
    existing category existing user -PASS
    new category existing user - PASS
    new catergory new user -PASS
    '''

    contact_lists = get_contact_lists()
    if category_name in contact_lists:
        contact_id = create_contact(email_address)
        CONTACTS_ENDPOINT = "https://api.sendgrid.com/v3/contactdb/lists/" + contact_lists[category_name] + \
            "/" + "recipients/" + contact_id
        response = requests.post(CONTACTS_ENDPOINT, headers=headers)
    else:
        contact_list_id = create_contact_list(category_name)
        contact_id = create_contact(email_address)
        CONTACTS_ENDPOINT = "https://api.sendgrid.com/v3/contactdb/" + \
            "lists/{0}/recipients/{1}".format(contact_list_id, contact_id)
        response = requests.post(CONTACTS_ENDPOINT, headers=headers)


@task
def sending_mail_to_subscribers():
    blog_posts = Post.objects.filter(published_on=datetime.datetime.today(), status='P')
    subscribers = Subscribers.objects.filter(blog_post=True)
    for blog_post in blog_posts:
        blog_url = 'https://www.micropyramid.com/blog/' + str(blog_post.slug) + '/'

        for subscriber in subscribers:
            sg = sendgrid.SendGridClient(settings.SG_USER, settings.SG_PWD)
            contact_msg = sendgrid.Mail()
            contact_msg.set_subject("New Blog Post | MicroPyramid")

            message_reply = 'Hello ' + str(subscriber.email) + ',\n\n'

            message_reply = '<p>New blog post has been created by ' + str(blog_post.author) + \
                ' with the name ' + str(blog_post.title) + ' in the category ' + str(blog_post.category.name) + '.</p>'

            message_reply = message_reply + 'Regards<br>'
            message_reply = message_reply + 'The MicroPyramid Team.<br>'
            contact_msg.set_html(message_reply)
            contact_msg.set_from("hello@micropyramid.com")
            contact_msg.add_to(subscriber.email)
            sg.send(contact_msg)


@task
def report_on_blog_post_published_limit():
    import datetime
    date = datetime.date.today()
    start_week = date - \
        datetime.timedelta(date.weekday()) - datetime.timedelta(1)
    end_week = start_week + datetime.timedelta(6)
    posts = Post.objects.filter(published_on__range=(start_week, end_week))
    blog_posts = Post.objects.filter(created_on__range=(start_week, end_week))
    from django.db.models import Sum, Count, Q, F
    incomplete_categories = Category.objects.filter(blog_posts__published_on__range=(start_week, end_week)).annotate(total_blog_posts=Count('blog_posts')).filter(total_blog_posts__lt=F('min_published_blogs'))
    complete_categories = Category.objects.filter(blog_posts__published_on__range=(start_week, end_week)).annotate(total_blog_posts=Count('blog_posts')).filter(total_blog_posts__gte=F('min_published_blogs'))
    users = User.objects.filter(user_roles='Admin', email='nikhila@micropyramid.com')
    formatted_start_week = datetime.datetime.strptime(
        str(start_week), "%Y-%m-%d").strftime("%d-%m-%Y")
    formatted_end_week = datetime.datetime.strptime(
        str(end_week), "%Y-%m-%d").strftime("%d-%m-%Y")
    min_blogposts = 0
    for user in users:
        sg = sendgrid.SendGridClient('peeljobs', '73etywgeugwqey56')
        contact_msg = sendgrid.Mail()
        temp = loader.get_template('admin/blogposts_report.html')
        rendered = temp.render({'posts': posts, 'blog_posts': blog_posts, 'start_week': start_week, 'end_week': end_week, 'user': user, 'complete_categories': complete_categories, 'incomplete_categories': incomplete_categories})
        contact_msg.set_html(rendered)
        contact_msg.set_text("Report")
        contact_msg.set_subject('Blog Post Report '+ formatted_start_week + ' - ' + formatted_end_week + ' - MicroPyramid')
        contact_msg.set_from("hello@micropyramid.com")
        contact_msg.add_to(user.email)
        sg.send(contact_msg)
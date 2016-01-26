from celery.decorators import task
import sendgrid
from django.conf import settings
from micro_admin.models import User
from micro_blog.models import Subscribers, Post
from .send_grid import *
import datetime


# A periodic task that will run every minute (the symbol "*" means every)
@task()
def daily_report():
    api_user = settings.SG_USER
    api_key = settings.SG_PWD
    user = User.objects.all()
    sg = sendgrid.SendGridClient(api_user, api_key)
    for usr in user:
        message = sendgrid.Mail()
        message.add_to(usr.email)
        message.set_from("report@reports.micropyramid.com")
        message.set_subject("Your Daily Report")
        message.set_html("Please provide your daily report")
        message.set_text('Daily Report')
        sg.send(message)


@task
def create_contact_in_category(category_name, email_address):
    '''
    Checks whether the category exists on not if it does then it will create a contact and save in
    database under sendgrid_user_id field and then add contact to list. If not create a category list then contact then adds contact to the new category
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
        CONTACTS_ENDPOINT = "https://api.sendgrid.com/v3/contactdb/lists/" + contact_lists[category_name]+"/" + "recipients/"+contact_id+""
        response = requests.post(CONTACTS_ENDPOINT, headers=headers)
        print response.status_code
    else:
        contact_list_id = create_contact_list(category_name)
        contact_id = create_contact(email_address)
        CONTACTS_ENDPOINT = "https://api.sendgrid.com/v3/contactdb/" + "lists/{0}/recipients/{1}".format(contact_list_id, contact_id)
        response = requests.post(CONTACTS_ENDPOINT, headers=headers)
        print response.status_code


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

            message_reply = '<p>New blog post has been created by ' + str(blog_post.author) + ' with the name ' + str(blog_post.title) + ' in the category '
            message_reply += str(blog_post.category.name) + '.</p>' + '<p>Please <a href="' + blog_url + '">click here</a> to view the blog post in the site.</p>'

            message_reply = message_reply + 'Regards<br>'
            message_reply = message_reply + 'The MicroPyramid Team.<br>'
            contact_msg.set_html(message_reply)
            contact_msg.set_from("hello@micropyramid.com")
            contact_msg.add_to(subscriber.email)
            sg.send(contact_msg)

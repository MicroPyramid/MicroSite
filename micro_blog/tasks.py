from celery.task.schedules import crontab
from celery.decorators import periodic_task,task
from celery.utils.log import get_task_logger
from datetime import datetime
from django.core.mail import send_mail
import sendgrid


# A periodic task that will run every minute (the symbol "*" means every)
@task()
def scraper_example():
    print "hello"
    params={
    'api_user':'micropyramid',
    'api_key':'wiej4djs3o5s',
    'to':'nikhila@micropyramid.com',
    'toname':'Destination',
    'subject':'hello',
    'text':'hello',
    'from' :  'inbound@micropyramid.bymail.in'
    'filters': {
        'templates': {
            'settings': {
                'enabled': 1,
                'template_id': '7e52e53a-3ffc-4b3d-b82e-2abebd31d1ad'
            }
        }
    }
    }
    response = request.POST('https://api.sendgrid.com/api/mail.send.json',params)
    print response
    send_mail('hello', 'hai', 'inbound@micropyramid.bymail.in', ['nikhila@micropyramid.com'], fail_silently=False)
    print "send"



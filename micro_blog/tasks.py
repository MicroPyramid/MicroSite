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
    send_mail('hello', 'hai', 'nikhila@micropyramid.com', ['nikhila@micropyramid.com'], fail_silently=False)
    print "send"
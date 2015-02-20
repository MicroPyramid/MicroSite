from celery.task.schedules import crontab
from celery.decorators import periodic_task,task
from celery.utils.log import get_task_logger
from datetime import datetime
from django.core.mail import send_mail
import sendgrid
import requests
from django.conf import settings
from micro_admin.models import User


# A periodic task that will run every minute (the symbol "*" means every)
@task()
def daily_report():
	api_user =settings.SG_USER
	api_key =settings.SG_PWD
	user = User.objects.all()
	sg = sendgrid.SendGridClient(api_user,api_key)
	for usr in user:
		message = sendgrid.Mail()
		message.add_to(usr.email)
		message.set_from("report@micropyramid.bymail.in")
		message.set_subject("Your Daily Report")
		message.set_html("Please provide your daily report")
		message.set_text('Daily Report')
		sg.send(message)


import smtplib
from email.message import EmailMessage
import codecs
from typing import *
from datetime import datetime
import logging
from django.conf import settings
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_HOST_USER =  settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = settings.EMAIL_PORT

HTMLFile = codecs.open("user/mail_template.html", 'r', "utf-8").read()
HTMLFileInvite = codecs.open("user/mail_template_invite.html", 'r', "utf-8").read()

def send_verify_email (user, link):
    content = f"Thanks {user.last_name} {user.first_name} for starting the new account creation process. We want to make sure it's really you. Please enter the following verification code when prompted. If you don’t want to create an account, you can ignore this message."
    title = 'Email Verification'
    index = HTMLFile.format(title=title,link=link,content=content)
    logging.getLogger().error(link) 
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD) 
        for email in set([user.email]):
            msg = EmailMessage()
            msg['Subject'] = "Verify Email Account | Minh Duc - HCMUS" 
            msg['From'] = EMAIL_HOST_USER 
            msg['To'] = email
            msg.set_content(index,subtype='html')
            smtp.send_message(msg)
        

def send_invite_email (email, link, groupName):
    content = f"We want to invite you to our group {groupName}. Please enter the following verification code when prompted. If you don’t want to, you can ignore this message."
    title = 'Group Invitation'
    index = HTMLFileInvite.format(title=title,link=link,content=content)
    logging.getLogger().error(link) 
    
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD) 
        for email in set([email]):
            msg = EmailMessage()
            msg['Subject'] = "Group Invitation | Minh Duc - HCMUS" 
            msg['From'] = EMAIL_HOST_USER 
            msg['To'] = email
            msg.set_content(index,subtype='html')
            smtp.send_message(msg)
        

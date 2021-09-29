from django.core.mail import EmailMessage
from django.conf import settings


import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'],from_email=settings.EMAIL_FROM, body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()
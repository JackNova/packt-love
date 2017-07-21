import logging
from google.appengine.api import mail
from app_config import config

USER_EMAIL = config['USER_EMAIL']


def send_email(book_title, book_description, book_image=None):
    message = mail.EmailMessage(sender="packt-love <%s>" % USER_EMAIL,
                                subject="Got book: %s" % book_title)

    message.to = "Me <%s>" % USER_EMAIL
    message.html = """<html><head></head><body>
    There's a new book for you!
    <strong>%s</strong>
    <img src="%s" />
    <p>%s</p>
    </body></html>""" % (book_title, book_image, book_description)

    message.send()


def send_error_no_content_email(subject, body):
    message = mail.EmailMessage(sender="packt-love <%s>" % USER_EMAIL,
                                subject="Got book: %s" % subject)

    message.to = "Me <%s>" % USER_EMAIL
    message.html = """<html><head></head><body>
    <strong>%s</strong>
    <p>%s</p>
    </body></html>""" % (subject, body)

    message.send()

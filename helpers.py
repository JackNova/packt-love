from lxml import html
import logging
import urllib2
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


def fetch_and_get_dom(request_url):
    response = urllib2.urlopen(request_url, timeout=45)
    raw_html = response.read()
    logging.info(raw_html)
    dom = html.fromstring(raw_html)
    return dom


def scrape(url, *args):
    dom = fetch_and_get_dom(url)
    results = []
    for xpression in args:
        x = dom.xpath(xpression)
        if len(x) > 0:
            try:
                results.append(x[0].text_content().strip())
            except:
                results.append(x[0].strip())
        else:
            logging.error("cant'find path %s in content" % xpression)
            results.append(None)

    return tuple(results)

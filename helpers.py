try:
    from lxml import html
except ImportError:
    import sys
    from app_config import config
    sys.path.insert(0, config['ALTERNATIVE_LOCAL_PYTHON_MODULES_PATH'])
    from lxml import html

import urllib2
from google.appengine.api import mail
from app_config import config

USER_EMAIL = config['USER_EMAIL']


def send_email(book_title, book_description, book_image):
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


def fetch_and_get_dom(request_url):
    response = urllib2.urlopen(request_url, timeout=45)
    raw_html = response.read()
    dom = html.fromstring(raw_html)
    return dom


def scrape(url, *args):
    dom = fetch_and_get_dom(url)
    results = []
    for xpression in args:
        x = dom.xpath(xpression)
        try:
            results.append(x[0].text_content().strip())
        except:
            results.append(x[0].strip())

    return tuple(results)

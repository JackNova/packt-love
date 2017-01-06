import webapp2
from helpers import scrape, send_email, send_error_no_content_email
from app_config import config
import logging
import urllib2
import urllib
import cookielib
from google.appengine.ext import ereporter
from google.appengine.api import taskqueue

ereporter.register_logger()

login_details = {
    "email": config["PACKT_EMAIL"],
    "password": config["PACKT_PASSWORD"],
    "op": "Login",
    "form_id": "packt_user_login_form",
    "form_build_id": ""
}

login_error = """Sorry, you entered an invalid email
    address and password combination."""

cj = cookielib.CookieJar()
http_handler = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(http_handler)

url = 'https://www.packtpub.com/packt/offers/free-learning'
get_book_url_path = "//a[contains(@class, 'twelve-days-claim')]/@href"
book_title_path = "//div[contains(@class, 'dotd-title')]"
new_form_id_path = "//input[@type='hidden'][starts-with(@id, 'form')][starts-with(@value, 'form')]/@value"
image_url_path = "//img[contains(@class, 'bookimage')]/@src"
book_description_path = "//*[@id='deal-of-the-day']/div/div/div[2]/div[3]"


class TaskHandler(webapp2.RequestHandler):

    def post(self):
        # scrape essential informations

        (get_book_url,
            book_title,
            new_form_id,
            image_url,
            book_description) = scrape(url,
                                       get_book_url_path,
                                       book_title_path,
                                       new_form_id_path,
                                       image_url_path,
                                       book_description_path)

        if new_form_id:
            login_details["form_build_id"] = new_form_id

        logging.info("""get_book_url: %s \n
            book_title: %s \n new_form_id: %s \n image_url: %s""" % (
            get_book_url, book_title, new_form_id, image_url))
        logging.info('book_description: \n %s' % book_description)

        if get_book_url is None:
            logging.error("impossible to get data. No need to continue")
            send_error_no_content_email("Error getting new book", """Getting the new book has
                been impossible. The offer seems to be suspended.
                You could retry manually by visiting the root
                page of the application on appengine.
                The task is not going to be retried authomatically.""")
        else:
            # login
            login_payload = urllib.urlencode(login_details)
            login_request = urllib2.Request(
                url, login_payload,
                {'content-type': 'application/x-www-form-urlencoded'})
            login_response = opener.open(login_request, timeout=45)
            login_failed = login_error in login_response.read()

            if login_failed:
                logging.error('login failed')
                self.error(401)
                return

            # grab book
            grab_book = opener.open(
                'https://www.packtpub.com' + get_book_url, timeout=45)
            grab_book_response = grab_book.read()

            send_email(book_title, book_description, 'https:'+image_url)

        self.response.write('done')


class MainHandler(webapp2.RequestHandler):

    def get(self):
        taskqueue.add(url='/task')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/task', TaskHandler)
], debug=True)

import webapp2
from model import scrape, curl
from app_config import config
import logging
import urllib2
import urllib
from cookielib import CookieJar
from google.appengine.ext import ndb

url = 'https://www.packtpub.com/packt/offers/free-learning'
login_error = 'Sorry, you entered an invalid email address and password combination.'


class Credentials(ndb.Model):
    cookies = ndb.PickleProperty(indexed=False, repeated=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    created = ndb.DateTimeProperty(auto_now_add=True)


class PacktLoginRequestHandler(webapp2.RequestHandler):

    def post(self):
        cj = CookieJar()
        http_handler = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(http_handler)

        # just need the new_form_id for logging in
        raw_html = curl(url)
        new_form_id, = scrape(
            raw_html,
            "//input[@type='hidden'][starts-with(@id, 'form')][starts-with(@value, 'form')]/@value"
        )

        login_details = {
            "email": config["PACKT_EMAIL"],
            "password": config["PACKT_PASSWORD"],
            "op": "Login",
            "form_id": "packt_user_login_form",
            "form_build_id": ""
        }

        if new_form_id:
            login_details["form_build_id"] = new_form_id

        # login
        login_payload = urllib.urlencode(login_details)
        login_request = urllib2.Request(
            url, login_payload,
            {'content-type': 'application/x-www-form-urlencoded'}
        )
        login_response = opener.open(login_request, timeout=45)
        login_failed = login_error in login_response.read()

        if login_failed:
            logging.error('login failed')
            self.error(401)
            return

        record = Credentials(id=config["PACKT_EMAIL"])
        cookie_list = [c for c in cj]
        record.cookies = cookie_list
        record.put()

        logging.info("login succeded")
        logging.info("credentials have been saved: ")
        logging.info(cookie_list)

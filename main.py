import webapp2
from model import scrape, send_email, curl, scrape_many
from app_config import config
import logging
import urllib2, urllib, cookielib
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

login_error = 'Sorry, you entered an invalid email address and password combination.'

cj = cookielib.CookieJar()
http_handler = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(http_handler)

url = 'https://www.packtpub.com/packt/offers/free-learning'

def login():

	cj = cookielib.CookieJar()
	http_handler = urllib2.HTTPCookieProcessor(cj)
	opener = urllib2.build_opener(http_handler)

	# just need the new_form_id for logging in
	raw_html = curl(url)
	new_form_id, = scrape(raw_html,
		"//input[@type='hidden'][starts-with(@id, 'form')][starts-with(@value, 'form')]/@value")

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
	login_request = urllib2.Request(url, login_payload, {'content-type': 'application/x-www-form-urlencoded'})
	login_response = opener.open(login_request, timeout=45)
	login_failed = login_error in login_response.read()

	if login_failed:
		logging.error('login failed')
		self.error(401)
		return

	logging.info("login succeded")

	return opener

class PurchaseFreeEbookTask(webapp2.RequestHandler):
	def post(self):
		# scrape essential informations
		raw_html = curl(url)
		get_book_url, book_title, new_form_id, image_url, book_description = scrape(raw_html,
			"//a[contains(@class, 'twelve-days-claim')]/@href",
			"//div[contains(@class, 'dotd-title')]",
			"//input[@type='hidden'][starts-with(@id, 'form')][starts-with(@value, 'form')]/@value",
			"//img[contains(@class, 'bookimage')]/@src",
			"//*[@id='deal-of-the-day']/div/div/div[2]/div[3]")

		if new_form_id:
			login_details["form_build_id"] = new_form_id

		logging.info('get_book_url: %s \n book_title: %s \n new_form_id: %s \n image_url: %s' % (get_book_url, book_title, new_form_id, image_url))
		logging.info('book_description: \n %s' % book_description)

		# login
		login_payload = urllib.urlencode(login_details)
		login_request = urllib2.Request(url, login_payload, {'content-type': 'application/x-www-form-urlencoded'})
		login_response = opener.open(login_request, timeout=45)
		login_failed = login_error in login_response.read()

		if login_failed:
			logging.error('login failed')
			self.error(401)
			return

		# grab book
		grab_book = opener.open('https://www.packtpub.com' + get_book_url, timeout=45)
		grab_book_response = grab_book.read()

		send_email(book_title, book_description, 'https:'+image_url)

		self.response.write('done')


class SchedulePurchaseFreeEBook(webapp2.RequestHandler):
	def get(self):
		taskqueue.add(url='/task/purchase-free-ebook')

class DownloadPurchasedEBooksTask(webapp2.RequestHandler):
	def post(self):
		opener = login()

		# get all my purchased ebooks ids
		my_ebooks = opener.open('https://www.packtpub.com/account/my-ebooks', timeout=45)
		my_ebooks_response = my_ebooks.read()
		ebooks_ids, = scrape_many(my_ebooks_response, "//div[contains(@class, 'product-line')]/@nid")
		logging.info('my ebooks are following: %s' % ebooks_ids)
		self.response.write(ebooks_ids)

		# for each ebook id schedule download of all resources
		

		self.response.write('done')

class ScheduleDownloadPurchasedEBooks(webapp2.RequestHandler):
	def get(self):
		taskqueue.add(url='/task/download-purchased-ebooks')
		

app = webapp2.WSGIApplication([
	('/schedule-purchase-free-ebook', SchedulePurchaseFreeEBook),
	('/task/purchase-free-ebook', PurchaseFreeEbookTask),
	('/schedule-download-purchased-ebooks', ScheduleDownloadPurchasedEBooks),
	('/task/download-purchased-ebooks', DownloadPurchasedEBooksTask)
], debug=True)

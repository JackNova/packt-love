try:
    from lxml import html
except ImportError:
    import sys
    from app_config import config
    sys.path.insert(0, config['ALTERNATIVE_LOCAL_PYTHON_MODULES_PATH'])
    from lxml import html
    
import urllib2
try:
    from google.appengine.api import mail
except Exception, e:
    pass
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

def curl(request_url):
    response = urllib2.urlopen(request_url, timeout=45)
    raw_html = response.read()
    return raw_html

def scrape(raw_html, *args):
	dom = html.fromstring(raw_html)
	results = []
	for xpression in args:
		x = dom.xpath(xpression)
		try:
			results.append(x[0].text_content().strip())
		except:
			results.append(x[0].strip())
			
	return tuple(results)

def scrape_many(raw_html, *xpressions):
    dom = html.fromstring(raw_html)
    results = []
    for xpression in xpressions:
        r = dom.xpath(xpression)
        try:
            results.append([x.text_content().strip() for x in r])
        except:
            results.append([x.strip() for x in r])

    return tuple(results)

def generate_download_urls(product_id):
    base_ebook_url = "https://www.packtpub.com/ebook_download/" + product_id + '/'
    xs = [base_ebook_url + x for x in ['pdf', 'epub', 'mobi']]
    xs.append("https://www.packtpub.com/code_download/" + product_id + '/')
    return set(xs)
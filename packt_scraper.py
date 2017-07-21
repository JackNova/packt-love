from lxml import html
import urllib2
import logging

url = 'https://www.packtpub.com/packt/offers/free-learning'
get_book_url_path = "//*[@id='free-learning-form']/@action"
book_title_path = "//div[contains(@class, 'dotd-title')]"
new_form_id_path = "//input[@type='hidden'][starts-with(@id, 'form')][starts-with(@value, 'form')]/@value"
image_url_path = "//img[contains(@class, 'bookimage')]/@src"
book_description_path = "//*[@id='deal-of-the-day']/div/div/div[2]/div[3]"


def fetch_and_get_text(request_url):
    response = urllib2.urlopen(request_url, timeout=45)
    raw_html = response.read()
    return raw_html


def scrape(page_text, *args):
    dom = html.fromstring(page_text)
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


if __name__ == '__main__':
    with open('fixtures/page.html') as page:
        txt = page.read()
        print scrape(txt, get_book_url_path,
                     book_title_path, new_form_id_path,
                     image_url_path, book_description_path)

from helpers import scrape
from fixtures import raw_html

def test_scrape():
    get_book_url, book_title, new_form_id, image_url, book_description = scrape(raw_html,
            "//a[contains(@class, 'twelve-days-claim')]/@href",
            "//div[contains(@class, 'dotd-title')]",
            "//input[@type='hidden'][starts-with(@id, 'form')][starts-with(@value, 'form')]/@value",
            "//img[contains(@class, 'bookimage')]/@src",
            "//*[@id='deal-of-the-day']/div/div/div[2]/div[3]")

    assert get_book_url == '/freelearning-claim/13250/21478'
    assert book_title == 'Machine Learning with R'
    assert new_form_id == 'form-7fb58741bd0c31a875c542ffc232268d'
    assert image_url == '//d1ldz4te4covpm.cloudfront.net/sites/default/files/imagecache/dotd_main_image/2148OS.jpg'
    assert book_description == "Today's free eBook is simple - it shows you how to get started with Machine Learning using R. Taking you through some potentially tricky concepts and mathematics, you'll soon learn how to apply Machine Learning principles to produce some real-world wins. What's holding you back? Try your hand with some neat Machine Learning techniques and tools today."
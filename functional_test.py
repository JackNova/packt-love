from model import scrape, scrape_many, generate_download_urls
from fixtures import raw_html, my_ebooks_page

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

def test_scrape_my_ebooks():
    test, = scrape_many(my_ebooks_page, "//div[contains(@class, 'product-line')]/@nid")
    assert set(test) == set(['13250', '19681', '19148', '15523', '16885', '16730', '10957', '15929', '14276', '17695', '14448', '14300', '7021', '17832', '18890', '16501', '13163', '16854', '16698', '17260', '18017', '13308', '19084', '11639', '11390', '17965', '10840', '15570', '16942', '11449', '15933', '15443', '16018', '18901', '13316', '16703', '19884', '9888', '17857', '16024', '14880', '18909', '21043', '11359', '19291', '18048', '12292', '14770', '8261', '15098', '15986', '16141', '11576', '19364', '18606', '16146', '14939', '11036', '17594', '11484', '14773', '16921', '18133', '15621', '9630', '18068', '13946', '16634', '15427', '19427', '11723', '19086', '15023', '12364', '13887', '20590', '16292', '16383', '17246', '14216', '17910', '15936', '14577', '11955', '14374', '11083', '9480', '13277', '14267', '15983', '11271', '16831', '14817', '12011', '10504', '7915', '6471', '12266', '11703', '5317', '8162', '13337', '18660', '16393', '12589', '11393', '9908', '10751', '13077', '4217', '4719', '10546', '12663', '12842', '9918', '13416', '11353', '12055', '11762', '11593', '8853', '10413', '10244', '9610', '11317', '11444', '8795', '12381', '13301', '8991', '13272', '11334', '9498', '9830', '11610', '12073', '9788', '10087', '12384', '10155', '14152', '10151', '10724', '12091', '7645', '9592', '4704', '11049', '10847', '13628', '11570', '10581', '10606', '6477'])

def test_generate_download_urls():
    product_id = '13250'
    base_ebook_url = "https://www.packtpub.com/ebook_download/" + product_id + '/'
    code_url = "https://www.packtpub.com/code_download/" + product_id + '/'
    xs = [base_ebook_url + x for x in ['pdf', 'epub', 'mobi']]
    xs.append(code_url)
    assert generate_download_urls(product_id) == set(xs)
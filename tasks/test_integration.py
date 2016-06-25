import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from packt_login import Credentials
from cookielib import Cookie, CookieJar


class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        pass

    def test_cookie_store(self):
        cj = CookieJar()
        test_email = "test@google.com"
        test_cookies = [Cookie(version=0, name='Name', value='1',
                               port=None, port_specified=False,
                               domain='www.example.com',
                               domain_specified=False,
                               domain_initial_dot=False,
                               path='/', path_specified=True, secure=False,
                               expires=None,
                               discard=True, comment=None, comment_url=None,
                               rest={'HttpOnly': None},
                               rfc2109=False)]
        for c in test_cookies:
            cj.set_cookie(c)
        x = Credentials(id=test_email)
        cookie_list = [c for c in cj]
        x.cookies = cookie_list
        x.put()

        y = Credentials.get_by_id(test_email)
        self.assertIsNotNone(y)
        self.assertEquals(y.key.id(), test_email)
        stored_credentials_dict = [sc.__dict__ for sc in y.cookies]
        self.assertEquals(stored_credentials_dict,
                          [sc.__dict__ for sc in test_cookies])

    def test_credentials_date(self):
        test_cookies = [Cookie(version=0, name='Name', value='1',
                               port=None, port_specified=False,
                               domain='www.example.com',
                               domain_specified=False,
                               domain_initial_dot=False,
                               path='/', path_specified=True, secure=False,
                               expires=None,
                               discard=True, comment=None, comment_url=None,
                               rest={'HttpOnly': None},
                               rfc2109=False)]
        c = Credentials(id="example@google.com")
        c.cookies = test_cookies
        c.put()
        old_created_date = c.created
        old_updated_date = c.updated
        c.cookies = []
        c.put()
        self.assertEquals(c.created, old_created_date)
        self.assertNotEquals(c.created, c.updated)
        self.assertNotEquals(c.updated, old_updated_date)
        assert c.created < c.updated

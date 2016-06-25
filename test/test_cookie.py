import urllib2
import urllib
import cookielib
from string_cookie_jar import StringCookieJar
import requests
import unittest


class TestCookieJar(unittest.TestCase):

    def setUp(self):
        pass

    def test_cookies(self):
        # launch a stub server that responds with a
        # predictable set-cookie header

        # call dump on the cookiejar and
        # check that all cookies are present
        pass

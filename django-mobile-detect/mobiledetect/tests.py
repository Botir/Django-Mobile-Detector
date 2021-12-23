from django.test import TestCase
from django.test.client import RequestFactory
from mobiledetect.detection import Detection

# user_agents_desktop = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
user_agents_android = 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36'
user_agents_iphone = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
user_agents_tablet = 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'


class UtilsTest(TestCase):

    def test_ua_mobile_android(self):
        request = RequestFactory(HTTP_USER_AGENT=user_agents_android).get('')
        detector = Detection(request)
        self.assertTrue(detector.is_mobile())

    def test_ua_mobile_ios(self):
        request = RequestFactory(HTTP_USER_AGENT=user_agents_iphone).get('')
        detector = Detection(request)
        self.assertTrue(detector.is_mobile())

    def test_ua_mobile_tablet(self):
        request = RequestFactory(HTTP_USER_AGENT=user_agents_tablet).get('')
        detector = Detection(request)
        self.assertTrue(detector.is_tablet())


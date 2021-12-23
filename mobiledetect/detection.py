import re
from .headers import DeviceHeader
from .user_agent import UserAgnet
from .constants import MOBILE_HEADERS, TABLET_DEVICES, get_extended_rule, get_mobile_rule

class Detection(object):

    # Mobile detection type.
    DETECTION_TYPE_MOBILE = 'mobile'

    # Extended detection type.
    DETECTION_TYPE_EXTENDED = 'extended'

    def __init__(self, request):
        self.device_header = DeviceHeader(request.META)
        self.user_agent = UserAgnet(self.device_header.http_headers, self.device_header.cloud_front_headers)

    def get_user_agent(self):
        """
        Retrieve the User-Agent name
        """
        return self.user_agent.name


    def is_mobile(self, user_agent=None, http_headers=None):
        """
        Check if the device is mobile.
        Returns true if any type of mobile device detected, including special ones
        """
        if http_headers:
            self.device_header.change(http_headers)
        if user_agent:
            self.user_agent.change(user_agent)

        # Check specifically for cloudfront headers if the useragent is 'Amazon CloudFront'
        if self.user_agent.name == 'Amazon CloudFront':
            if "HTTP_CLOUDFRONT_IS_MOBILE_VIEWER" in self.device_header.cloud_front_headers and self.device_header.cloud_front_headers[
                'HTTP_CLOUDFRONT_IS_MOBILE_VIEWER'] == 'true':
                return True

        self.set_detection_type(self.DETECTION_TYPE_MOBILE)

        if self.check_http_headers_for_mobile():
            return True
        else:
            return self.match_detection_rules()

    def is_tablet(self, user_agent=None, http_headers=None):
        """
        Check if the device is a tablet.
        Return true if any type of tablet device is detected.
        """


        # Check specifically for cloudfront headers if the useragent == 'Amazon CloudFront'
        if self.user_agent == 'Amazon CloudFront':
            if "HTTP_CLOUDFRONT_IS_TABLET_VIEWER" in self.device_header.cloud_front_headers and \
                    self.device_header.cloud_front_headers['HTTP_CLOUDFRONT_IS_TABLET_VIEWER'] == 'true':
                return True
        self.set_detection_type(self.DETECTION_TYPE_MOBILE)
        for _regex in TABLET_DEVICES:
            if self.match(_regex, user_agent):
                return True

    def set_detection_type(self, detection_type):
        """
        Set the detection type. Must be one of self.DETECTION_TYPE_MOBILE or
        self.DETECTION_TYPE_EXTENDED. Otherwise, nothing is set.
        """
        if detection_type is None:
            detection_type = self.DETECTION_TYPE_MOBILE

        if detection_type != self.DETECTION_TYPE_MOBILE and detection_type != self.DETECTION_TYPE_EXTENDED:
            return None

        self.detection_type = detection_type

    def check_http_headers_for_mobile(self):
        """
        Check the HTTP headers for signs of mobile.
        This is the fastest mobile check possible; it's used
        inside is_mobile() method.
        """
        http_headers = self.device_header.http_headers
        for mobile_header in MOBILE_HEADERS:
            match_type = MOBILE_HEADERS[mobile_header]
            if mobile_header in http_headers:
                if 'matches' in match_type and isinstance(match_type['matches'], list):
                    for _match in match_type['matches']:
                        if http_headers[mobile_header].find(_match) != -1:
                            return True
                    return False

                return False

        return False

    def match_detection_rules(self, user_agent=None):
        # Begin general search.
        rules = self.get_rules()

        for _regex in rules:
            if not _regex:
                continue
            if self.match(_regex, user_agent):
                return True
        else:
            return False

    def get_rules(self):
        """
        Retrieve the current set of rules.
        """
        if self.detection_type == self.DETECTION_TYPE_EXTENDED:
            return get_extended_rule()
        else:
            return get_mobile_rule()

    def match(self, match, user_agents=None):
        """
        Some detection rules are relative (not standard),
        because of the diversity of devices, vendors and
        their conventions in representing the User-Agent or
        the HTTP headers.
        This method will be used to check custom regexes against
        the User-Agent string.
        """
        matches = re.findall(re.compile(match), user_agents if user_agents else self.user_agent.name)
        if matches and len(matches) > 0:
            self.matching_regex = match
            self.matches_array = matches
            return True
        else:
            return False

    def get_device_type(self):
        pass

def detect(request):
    return Detection(request)

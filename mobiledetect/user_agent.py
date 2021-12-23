# import HTTP headers
from .constants import UA_HTTP_HEADERS

class UserAgnet:
    """
    With User-Agent string combined with specific HTTP headers to detect the mobile environment.
    """

    def __init__(self, http_headers, cloud_front_headers=None):
        """
        Parameters
        ----------
        http_headers : str
            Only HTTP headers.
        cloud_front_headers : str
            CLOUDFRONT headers
            (default is none)
        """
        # self.name is user agent name
        self.name = None
        self.parse_user_agent(http_headers, cloud_front_headers)

    def change(self, user_agent):
        if user_agent and user_agent != "":
            self.name = self.__prepare_user_agent(user_agent)

    def parse_user_agent(self, http_headers, cloud_front_headers=None):
        """
        parse user agent from http headers or CloudFront.
        """
        for alt_header in UA_HTTP_HEADERS:
            if alt_header in http_headers:
                if self.name is None:
                    self.name = http_headers[alt_header]
                else:
                    self.name += " " + http_headers[alt_header]

        if self.name:
            self.name = self.__prepare_user_agent(self.name)
            return self.name

        if cloud_front_headers and len(cloud_front_headers) > 0:
            self.name = 'Amazon CloudFront'
            return self.name

        return self.name

    def __prepare_user_agent(self, user_agent):
        """
        change name user agent
        """
        user_agent = user_agent.strip()
        return user_agent[0:500]

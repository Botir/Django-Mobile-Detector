class DeviceHeader:
    """Class for get only save HTTP headers."""

    def __init__(self, request):
        """Specify the request as injection."""
        self.http_headers = dict()
        self.cloud_front_headers = dict()
        self.change(request)

    def change(self, headers):
        """Change http header"""
        self.parse_http_headers(headers)

        # In case we're dealing with CloudFront, we need to know.
        self.parse_cf_headers(headers)

    def parse_http_headers(self, headers):
        # Set the HTTP Headers. Must be Django-flavored. This method will reset existing headers.
        for key, value in headers.items():
            # Only save HTTP headers.
            if key[0:5] == 'HTTP_':
                self.http_headers[key] = value


    def parse_cf_headers(self, headers):
        # Only save CLOUDFRONT headers.
        # start with cloudfront-.
        for key, value in headers.items():
            if key[0:16] == 'http_cloudfront_':
                self.cloud_front_headers[key] = value



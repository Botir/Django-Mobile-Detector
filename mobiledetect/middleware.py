from .detection import Detection

class DetectMiddleware(object):

    def __init__(self, get_response=None):
        if get_response is not None:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        detector = Detection(request)

        request.device = dict()
        request.device['is_mobile'] = detector.is_mobile()
        request.device['is_tablet'] = detector.is_tablet()
        request.device['user_agent'] = detector.user_agent.name

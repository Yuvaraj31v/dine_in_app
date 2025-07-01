import uuid

from .filter import set_trace_id

class TraceIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        trace_id = str(uuid.uuid4())
        set_trace_id(trace_id)
        response = self.get_response(request)
        return response
# trace_filter.py
import logging
import threading

_local = threading.local()

def set_trace_id(trace_id):
    _local.trace_id = trace_id

def get_trace_id():
    return getattr(_local, 'trace_id', '-')

class TraceIDFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = get_trace_id()
        return True

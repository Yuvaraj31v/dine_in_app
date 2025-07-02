# trace_filter.py
import logging

from contextvars import ContextVar

_trace_id_var = ContextVar("trace_id", default="-")

def set_trace_id(trace_id):
    _trace_id_var.set(trace_id)

def get_trace_id():
    return _trace_id_var.get()

class TraceIDFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = get_trace_id()
        return True

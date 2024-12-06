from fastapi import Header

from .utils import trace_id_var


def get_trace_id(x_trace_id: str = Header(None)):
    return trace_id_var.get()

import decimal
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
from frappe.utils import format_timedelta
from werkzeug.wrappers import Response
from werkzeug.local import LocalProxy
import json
import frappe


#!======================================================================

def json_handler(obj):
    """serialize non-serializable data for json"""
    from collections.abc import Iterable
    from re import Match

    if isinstance(obj, (date, datetime, time)):
        return str(obj)

    elif isinstance(obj, timedelta):
        return format_timedelta(obj)

    elif isinstance(obj, decimal.Decimal):
        return float(obj)

    elif isinstance(obj, LocalProxy):
        return str(obj)

    elif isinstance(obj, frappe.model.document.BaseDocument):
        return obj.as_dict(no_nulls=True)

    elif isinstance(obj, Iterable):
        return list(obj)

    elif isinstance(obj, Match):
        return obj.string

    elif type(obj) == type or isinstance(obj, Exception):
        return repr(obj)

    elif callable(obj):
        return repr(obj)

    else:
        raise TypeError(
            f"""Object of type {type(obj)} with value of {repr(obj)} is not JSON serializable"""
        )
#!=================================================================================================
def api_response(status=True, data=None, message="", status_code=200,data_size=0):
    if data is None:
        data = {}
    response = Response()

    response.status_code = status_code
    response.mimetype = "application/json"
    response.data = json.dumps({"status": status, 
                                "message": message, 
                                "data_size": data_size,
                                "data": data
                                },
                               default=json_handler, separators=(",", ":"))

    return response



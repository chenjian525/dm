import sys
import json
import logging
from decimal import Decimal
from datetime import datetime, date
from tornado.options import options


def get_app_db_settings():
    return dict(db_host=options.db_host, db_name=options.db_name, db_port=options.db_port,
                db_username=options.db_username, db_password=options.db_password)


def set_logger():
    default_format = ('[%(asctime)s] [%(levelname)s] '
                      '[%(module)s: %(lineno)d] %(message)s')
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format=default_format,
        datefmt='%Y-%m-%d %H:%M:%S %z',
    )


def json_default(dt_fmt='%Y-%m-%d %H:%M:%S', date_fmt='%Y-%m-%d', decimal_fmt=str):
    def _default(obj):
        if isinstance(obj, datetime):
            return obj.strftime(dt_fmt)
        elif isinstance(obj, date):
            return obj.strftime(date_fmt)
        elif isinstance(obj, Decimal):
            return decimal_fmt(obj)
        else:
            raise TypeError('%r is not JSON serializable' % obj)

    return _default


def json_dumps(obj, dt_fmt='%Y-%m-%d %H:%M:%S', date_fmt='%Y-%m-%d', decimal_fmt=str, ensure_ascii=False):
    return json.dumps(obj, ensure_ascii=ensure_ascii, default=json_default(dt_fmt, date_fmt, decimal_fmt))

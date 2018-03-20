import os
import sys
import logging
from tornado.options import options, define
from dm.config import load_app_options


def set_logger():
    default_format = ('[%(asctime)s] [%(levelname)s] '
                      '[%(module)s: %(lineno)d] %(message)s')
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format=default_format,
        datefmt='%Y-%m-%d %H:%M:%S %z',
    )


if __name__ == '__main__':
    define('app_path', os.path.dirname(os.path.abspath(__file__)))  # app.py所在目录
    define('app_db', os.path.join(options.app_path, 'db/app.db'))

    load_app_options()  # 加载配置

    set_logger()

    # from op.controllers import ui_modules
    settings = {
        'template_path': os.path.join(options.app_path, 'templates'),
        'static_path': os.path.join(options.app_path, 'static'),
        'cookie_secret': options.cookie_secret,
        'debug': options.debug,
        'login_url': '/login',
        'xsrf_cookies': True,
    }

    from dm.controllers.handlers import handlers
    from dm.infra.application import setup_application
    setup_application(handlers, settings, use_mysql=True)

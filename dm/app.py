import os
from tornado.options import options, define
from dm.config import load_app_options
from dm.infra.utils import set_logger


if __name__ == '__main__':
    define('app_path', os.path.dirname(os.path.abspath(__file__)))  # app.py所在目录

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

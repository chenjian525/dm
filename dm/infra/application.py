import os
import time
import logging
import signal
from tornado.options import options
from tornado import web, ioloop, autoreload, httpserver

from dm.infra.db import mysql_client
from dm.infra.utils import get_app_db_settings


def setup_application(handlers, app_settings, use_mysql=True):
    app = web.Application(handlers, **app_settings)

    # 监听端口
    server = httpserver.HTTPServer(app, xheaders=True)
    server.listen(options.port, address="127.0.0.1")

    # 连接数据库
    if use_mysql:
        app.db = mysql_client(**get_app_db_settings())

    # 程序退出处理
    on_app_terminal(server, app)

    # debug 模式下，文件变更后程序将自动重启服务，在此之前需将 db 连接关掉
    def on_reload():
        if use_mysql:
            logging.info('close database connection')
            app.db.close()

    # 监听配置文件
    if options.mode == 'dev':
        autoreload.watch(os.path.join(options.app_path, '../../eggs/conf/dev.py'))
    autoreload.add_reload_hook(on_reload)

    # 启动 loop
    logging.info('application started on port:%s', options.port)
    ioloop.IOLoop.instance().start()


MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 2


def on_app_terminal(server, application):

    def sig_handler(sig, _):
        logging.warning('Caught signal: %s', sig)
        ioloop.IOLoop.instance().add_callback(shutdown)

    def shutdown():
        logging.info('Stopping http server')
        server.stop()

        if options.mode != 'dev':
            logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)

        io_loop_instance = ioloop.IOLoop.instance()

        deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

        def stop_loop():
            now = time.time()
            if now < deadline and options.mode != 'dev':
                io_loop_instance.add_timeout(now + 1, stop_loop)
            else:
                io_loop_instance.stop()
                logging.info('Close database connection')
                if hasattr(application, 'db'):
                    application.db.close()
                    logging.info('Shutdown')
        stop_loop()

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    if hasattr(signal, 'SIGQUIT'):
        signal.signal(signal.SIGQUIT, sig_handler)

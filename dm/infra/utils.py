from tornado.options import options


def get_app_db_settings():
    host = options.db_host + ':' + str(options.db_port)
    return dict(db_host=host, db_name=options.db_name,
                db_username=options.db_username, db_password=options.db_password)

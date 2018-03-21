from tornado.options import options


def get_app_db_settings():
    return dict(db_host=options.db_host, db_name=options.db_name, db_port=options.db_port,
                db_username=options.db_username, db_password=options.db_password)

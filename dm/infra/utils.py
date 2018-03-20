from tornado.options import options


def get_app_db_settings():
    host = options.db_host + ':' + str(options.db_port)
    return dict(mysql_host=host, mysql_database=options.db_name,
                mysql_user=options.db_username, mysql_password=options.db_password)

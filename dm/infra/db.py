import sys
import inspect
import sqlite3
from tornado.web import HTTPError

from dm.infra import torndb


class DBConnection(object):
    def __init__(self, **kwargs):
        self.db = get_db(**kwargs)

    @property
    def is_valid(self):
        return self.db.is_valid

    def close(self):
        self.db.close()

    def get_tables(self):
        return self.db.get_tables()

    def get_columns(self, table_name):
        return self.db.get_columns(table_name)


class MYSQLConnection(object):
    def __init__(self, **kwargs):
        if kwargs.get('db_host') and kwargs.get('db_port'):
            db_host = ':'.join([kwargs.get('db_host'), str(kwargs.get('db_port'))])
        else:
            db_host = kwargs.get('db_host')

        self.conn = torndb.Connection(
            host=db_host,
            database=kwargs.get('db_name'),
            user=kwargs.get('db_username'),
            password=kwargs.get('db_password'),
            time_zone='+8:00',
            charset='utf8mb4',
            read_timeout=10,
            write_timeout=15,
        )

    @property
    def is_valid(self):
        return getattr(self.conn, '_db') is not None

    def close(self):
        self.conn.close()

    def get_tables(self):
        res = self.conn.query('show tables')
        return [i for j in res for i in j.values()]

    def get_columns(self, table_name):
        res = self.conn.query('desc %s' % table_name)
        return [(i['Field'], i['Type']) for i in res]


def sqlite3_client(db_path):
    s3 = sqlite3.connect(db_path)
    return s3


def mysql_client(**kwargs):
    if kwargs.get('db_host') and kwargs.get('db_port'):
        db_host = ':'.join([kwargs.get('db_host'), str(kwargs.get('db_port'))])
    else:
        db_host = kwargs.get('db_host')

    return torndb.Connection(
        host=db_host,
        database=kwargs.get('db_name'),
        user=kwargs.get('db_username'),
        password=kwargs.get('db_password'),
        time_zone='+8:00',
        charset='utf8mb4',
        read_timeout=10,
        write_timeout=15,
    )


def get_db(**kwargs):
    type_name = kwargs['db_type']
    name = type_name.upper() + 'Connection'
    for t in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if t[0] == name:
            return t[1](**kwargs)

    raise HTTPError(400, '%s 类型数据库未添加相应处理，请联系管理员' % type_name)

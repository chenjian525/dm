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

    def get_columns(self, table_name, include_type=True):
        return self.db.get_columns(table_name, include_type)

    def get_data_by_time_limit_sentence(self, table_name, parsed_arguments):
        return self.db.get_data_by_time_limit_sentence(table_name, parsed_arguments)


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

    def get_columns(self, table_name, include_type=True):
        res = self.conn.query('desc %s' % table_name)
        if include_type:
            return [(i['Field'], i['Type']) for i in res]
        else:
            return [i['Field'] for i in res]

    def get_data_by_time_limit_sentence(self, table_name, parsed_arguments):
        sql = 'select %s from %s where %s'
        normal_cols, date_limit_cols, *_ = parsed_arguments
        normal_cols.extend(i[0] for i in date_limit_cols)
        col_section = ', '.join(normal_cols)
        date_limit_cols = [(i[0], i[1], self.conn._db.literal(i[2])) for i in date_limit_cols]
        limit_section = ' and '.join(' '.join(i) for i in date_limit_cols)
        return sql % (table_name, col_section, limit_section)


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

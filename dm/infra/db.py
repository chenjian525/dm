import sys
import inspect
import sqlite3

from dm.infra import torndb


def sqlite3_client(db_path):
    s3 = sqlite3.connect(db_path)
    return s3


def mysql_client(mysql_host=None, mysql_database=None, mysql_user=None, mysql_password=None):
    return torndb.Connection(
        host=mysql_host,
        database=mysql_database,
        user=mysql_user,
        password=mysql_password,
        time_zone='+8:00',
        charset='utf8mb4',
        read_timeout=10,
        write_timeout=15,
    )


def get_client(type_name):
    name = type_name + '_client'
    for t in inspect.getmembers(sys.modules[__name__], inspect.isfunction):
        if t[0] == name:
            return t[1]


if __name__ == '__main__':
    print(get_client('mysql'))

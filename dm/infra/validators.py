import sys
import inspect
from voluptuous import Schema, REMOVE_EXTRA, All, In, Coerce, error


mysql_validate = Schema({
    'name': All(str, msg='数据库别名'),
    'db_type': All(str, In(['sqlite3', 'mysql', 'postgresql', 'mongodb']), msg='请传送正确的数据库类型'),
    'db_name': All(str, msg='数据库名'),
    'db_username': All(str, msg='数据库用户名'),
    'db_password': All(str, msg='密码'),
    'db_host': All(str, msg='请传送正确的数据库服务器地址'),
    'db_port': All(Coerce(int), msg='无效的数据库端口'),
}, extra=REMOVE_EXTRA, required=True)


def validate_arguments(args):
    def is_schema_instance(value):
        return isinstance(value, Schema)

    for v in inspect.getmembers(sys.modules[__name__], is_schema_instance):
        if v[0] == args['db_type'] + '_validate':
            return v[1](args)
    raise error.MatchInvalid('无效或不能处理的数据库类型,请联系管理员')

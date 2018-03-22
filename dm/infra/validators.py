import sys
import inspect
from tornado.web import HTTPError
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


def validate_add_task_args(columns, args):
    normal_columns = []
    date_limit_columns = []
    task_exec_limit_columns = []
    date_columns = [i[0] for i in columns if 'date' in i[1] or 'timestamp' in i[1]]
    for name in args:
        if name.endswith(('_eendd', '_sstartt')) and any(i in name for i in date_columns):
            if '_eendd' in name:
                name_ = name[:-6]
                date_limit_columns.append((name_, '<=', args['name']))
            else:
                name_ = name[:-8]
                date_limit_columns.append((name_, '>=', args['name']))

        if any(name == i[0] for i in columns):
            normal_columns.append(name)

        if name in ['exec_once', 'exec_per_minute']:
            task_exec_limit_columns.append((name, args['name']))

    if not normal_columns:
        raise HTTPError(400, '请勾选要查询的字段')
    if not date_limit_columns:
        raise HTTPError(400, '请用日期字段进行时间限制')
    if not task_exec_limit_columns:
        raise HTTPError(400, '请选择任务类型')

    return normal_columns, date_limit_columns, task_exec_limit_columns

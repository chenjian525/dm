from tornado.web import HTTPError
from tornado.ioloop import PeriodicCallback
import json

from dm.infra.db import DBConnection
from dm.controllers import BaseHandler
from dm.infra.validators import validate_arguments, validate_add_task_args


class Database(BaseHandler):
    def get(self):
        from dm.infra.utils import get_app_db_settings
        from dm.infra.db import mysql_client
        args = get_app_db_settings()
        args['db_name'] = 'dm'
        conn = mysql_client(**args)
        print(conn.query('desc reg_db'))
        print(self.db._db.literal('2018-03-25 14:23'))

        dbs = self.db.query('select * from reg_db')

        self.render('database/database.html', dbs=dbs, json=json)

    def post(self):
        args = self.plain_args()
        args = validate_arguments(args)

        try:
            conn = DBConnection(**args)
        except Exception as e:
            raise HTTPError(400, '无法链接数据库，请检查相关参数')
        else:
            if conn.is_valid:
                conn.close()
                self.db.execute('insert into reg_db(type, name, db_info) values(%s, %s, %s)', args['db_type'], args['name'], json.dumps(args))
                return self.write_ok('添加成功')
            else:
                raise HTTPError(400, '无法连接数据库，请检查相关参数')  # 连接不上时，会导致响应很慢；可异步测试连接，加个字段表示是否可用


class Tables(BaseHandler):
    def get(self, db_id):
        target_db = self.db.get('select * from reg_db where id=%s', db_id)
        if not target_db:
            raise HTTPError(404, '无效的数据库id')

        info = json.loads(target_db.db_info)
        db_connection = DBConnection(**info)
        tables = db_connection.get_tables()
        self.render('database/tables.html', tables=tables, db_id=db_id, db_type=target_db.type,
                    name=target_db.name, db_name=info.get('db_name'))


class OneTable(BaseHandler):
    def get(self, db_id, table_name):
        target_db = self.db.get('select * from reg_db where id=%s', db_id)
        if not target_db:
            raise HTTPError(404, '无效的数据库id')

        info = json.loads(target_db.db_info)
        db_connection = DBConnection(**info)
        columns = db_connection.get_columns(table_name)

        self.render('database/table.html', db_id=db_id, name=target_db.name, db_name=info.get('db_name'),
                    table_name=table_name, columns=columns, db_type=target_db.type)

    def post(self, db_id, table_name):
        args = {k: v for k, v in self.plain_args().item() if v}
        target_db = self.db.get('select * from reg_db where id=%s', db_id)
        if not target_db:
            raise HTTPError(404, '无效的数据库id')

        info = json.loads(target_db.db_info)
        db_connection = DBConnection(**info)
        columns = db_connection.get_columns(table_name)
        parsed_arguments = validate_add_task_args(columns, args)
        exe_type = parsed_arguments[2]
        periodic_time = 0 if 'exe_once' in exe_type else exe_type[1]
        sql_sentence = db_connection.get_data_by_time_limit_sentence(table_name, parsed_arguments)
        self.db.execute('insert into task(db_id, table_name, sql_sentence, periodic_time, next_exec_time, exec_times, '
                        'exec_type, status) values(%s, %s, %s, %s, NOW(), 0, %s, 1)', db_id, table_name,
                        sql_sentence, periodic_time, 0 if not periodic_time else 1)
        self.write_ok('创建成功')

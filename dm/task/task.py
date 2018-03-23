from concurrent import futures
from datetime import datetime, timedelta

from dm.infra.utils import json_dumps


class Executor(object):
    _instance = None

    def __new__(cls):
        if not getattr(cls, '_instance'):
            cls._instance = futures.ThreadPoolExecutor(max_workers=100)

        return cls._instance


class Task(object):
    executor = Executor()

    def __init__(self, db, data_db, task):
        self.db = db
        self.data_db = data_db
        self.task = task

    def __call__(self):
        self.executor.submit(self.get_data)
        # self.get_data()

    def get_data(self):
        res = self.data_db.query(self.task.sql_sentence)
        self.data_db.close()
        # self.executor.map(self.stored_data, res)
        for data in res:
            self.stored_data(data)

    def stored_data(self, data):
        row_id = self.db.execute('insert into reg_db_data(db_id, table_name, data) values(%s, %s, %s)',
                                 self.task.db_id, self.task.table_name, json_dumps(data))
        if row_id:
            if self.task.exec_type == 0:
                self.db.execute('update task set status=0, exec_times=exec_times+1, exec_status=0 where id=%s', self.task.id)
            else:
                exec_time = datetime.now() + timedelta(minutes=self.task.periodic_time)
                self.db.execute('update task set exec_times=exec_times+1, next_exec_time=%s, exec_status=0 where id=%s',
                                exec_time, self.task.id)

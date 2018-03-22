import json
import asyncio
from datetime import datetime, timedelta

from dm.infra.db import DBConnection, mysql_client
from dm.config import load_app_options
from dm.infra.utils import get_app_db_settings


@asyncio.coroutine
def main():
    load_app_options()
    db = mysql_client(**get_app_db_settings())

    while True:
        tasks = db.query('select task.*, reg_db.* from task t, reg_db r where t.status=1 '
                         'and t.next_exec_time<=NOW() and t.db_id=r.id')
        for task in tasks:
            info = json.loads(task.db_info)
            data_db = DBConnection(**info)
            task = Task(db, data_db, task.sql_sentence)
            yield from task()
            if task.exec_type == 0:
                db.execute('update task set status=0, exec_times=exec_times+1 where id=%s', task.id)
            else:
                exec_time = datetime.now() + timedelta(minutes=task.periodic_time)
                db.execute('update task set exec_time=exec_times+1, next_exec_time=%s where id=%s', exec_time, task.id)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main)

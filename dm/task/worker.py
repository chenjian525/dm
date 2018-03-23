import json
import logging

from dm.infra.db import DBConnection, mysql_client
from dm.config import load_app_options
from dm.infra.utils import get_app_db_settings
from dm.task.task import Task, Executor
from dm.task import on_task_terminal
from dm.infra.utils import set_logger


def main():
    set_logger()

    logging.info('-------  task start  -------')

    load_app_options()
    db = mysql_client(**get_app_db_settings())

    running = [True]
    on_task_terminal(running)

    while running:
        tasks = db.query('select t.*, r.db_info from task t, reg_db r where t.status=1 and t.exec_status=0 '
                         'and t.next_exec_time<=NOW() and t.db_id=r.id')
        for task in tasks:
            logging.info('get task: %s' % task.sql_sentence)
            db.execute('update task set exec_status=1 where id=%s', task.id)
            info = json.loads(task.db_info)
            data_db = DBConnection(**info)
            new_db = mysql_client(**get_app_db_settings())
            task = Task(new_db, data_db, task)
            task()

    logging.info('停止接收task，请等待所有任务完成')

    Executor().shutdown(wait=True)

    db.close()
    logging.info('-------  task closed  -------')


if __name__ == '__main__':
    main()

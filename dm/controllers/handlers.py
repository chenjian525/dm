from tornado.web import url

from dm.controllers.database import database


handlers = [
    url(r'/dbs', database.Database, name='dbs'),
    url(r'/dbs/(\d+)/tables', database.Tables, name='db_tables'),
    url(r'/dbs/(\d+)/tables/(\w+)', database.OneTable, name='table'),
]

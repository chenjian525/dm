from tornado.web import url

from dm.controllers.database import database


handlers = [
    url(r'/dbs', database.Database),
    url(r'/dbs/(\d+)/tables', database.Table),
    url(r'/dbs/(\d+)/tables/(\w+)', database.OneTable),
]

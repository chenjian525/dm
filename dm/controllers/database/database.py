from dm.controllers import BaseHandler
import json

from dm.infra.db import get_client


class Database(BaseHandler):
    def get(self):
        dbs = self.db.query('select * from reg_db')

        self.render('database/database.html', dbs=dbs, json=json)

    def post(self):
        pass


class Table(BaseHandler):
    def get(self):
        pass


class OneTable(BaseHandler):
    def get(self):
        pass

    def post(self):
        pass

from dm.controllers import BaseHandler
import json

from dm.infra.db import get_client
from dm.infra.validators import validate_arguments


class Database(BaseHandler):
    def get(self):

        # dbs = self.db.query('select * from reg_db')
        dbs = []

        self.render('database/database.html', dbs=dbs, json=json)

    def post(self):
        args = self.plain_args()
        args = validate_arguments(args)
        db_client = get_client(args['db_type'])
        try:
            db_client(**args)
        except Exception as e:
            pass


class Table(BaseHandler):
    def get(self):
        pass


class OneTable(BaseHandler):
    def get(self):
        pass

    def post(self):
        pass

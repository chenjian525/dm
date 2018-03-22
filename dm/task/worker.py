from tornado.options import options

from dm.infra.db import DBConnection, mysql_client
from dm.config import load_app_options
from dm.infra.utils import get_app_db_settings


def main():
    db = mysql_client(**get_app_db_settings())
    pass

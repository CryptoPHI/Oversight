"""
    Set up defaults and read oversight.conf
"""
import sys
import os
from ccoin_config import CoinConfig

default_oversight_config = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../oversight.conf')
)
oversight_config_file = os.environ.get('OVERSIGHT_CONFIG', default_oversight_config)
oversight_cfg = CoinConfig.tokenize(oversight_config_file)
oversight_version = "1.0.1"
min_coind_proto_version_with_oversight_ping = 70701


def get_coin_conf():
    home = os.environ.get('HOME')

    coin_conf = os.path.join(home, ".muecore/mue.conf")
    if sys.platform == 'darwin':
        coin_conf = os.path.join(home, "Library/Application Support/MueCore/mue.conf")

    coin_conf = oversight_cfg.get('coin_conf', coin_conf)

    return coin_conf


def get_network():
    return oversight_cfg.get('network', 'mainnet')


def sqlite_test_db_name(sqlite_file_path):
    (root, ext) = os.path.splitext(sqlite_file_path)
    test_sqlite_file_path = root + '_test' + ext
    return test_sqlite_file_path


def get_db_conn():
    import peewee
    env = os.environ.get('OVERSIGHT_ENV', 'production')

    # default values should be used unless you need a different config for development
    db_host = oversight_cfg.get('db_host', '127.0.0.1')
    db_port = oversight_cfg.get('db_port', None)
    db_name = oversight_cfg.get('db_name', 'oversight')
    db_user = oversight_cfg.get('db_user', 'oversight')
    db_password = oversight_cfg.get('db_password', 'oversight')
    db_charset = oversight_cfg.get('db_charset', 'utf8mb4')
    db_driver = oversight_cfg.get('db_driver', 'sqlite')

    if (env == 'test'):
        if db_driver == 'sqlite':
            db_name = sqlite_test_db_name(db_name)
        else:
            db_name = "%s_test" % db_name

    peewee_drivers = {
        'mysql': peewee.MySQLDatabase,
        'postgres': peewee.PostgresqlDatabase,
        'sqlite': peewee.SqliteDatabase,
    }
    driver = peewee_drivers.get(db_driver)

    dbpfn = 'passwd' if db_driver == 'mysql' else 'password'
    db_conn = {
        'host': db_host,
        'user': db_user,
        dbpfn: db_password,
    }
    if db_port:
        db_conn['port'] = int(db_port)

    if driver == peewee.SqliteDatabase:
        db_conn = {}

    db = driver(db_name, **db_conn)

    return db


coin_conf = get_coin_conf()
network = get_network()
db = get_db_conn()

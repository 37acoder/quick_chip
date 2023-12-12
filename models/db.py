from peewee import MySQLDatabase
import config

mysql_db = MySQLDatabase(
    config.db_name,
    host=config.db_host,
    port=config.db_port,
    user=config.db_user,
    password=config.db_password,
)

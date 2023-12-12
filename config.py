import os

db_name = "chip"
db_host = "localhost" or os.environ.get("DB_HOST")
db_port = 3306 or os.environ.get("DB_PORT")
db_user = "root" or os.environ.get("DB_USER")
db_password = "" or os.environ.get("DB_PASSWORD")

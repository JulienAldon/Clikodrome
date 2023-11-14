from src.configuration import options
import pymysql.cursors

connection = pymysql.connect(
    host=options.db_host,
    user=options.db_user,
    password=options.db_password,
    database=options.database,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()
cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
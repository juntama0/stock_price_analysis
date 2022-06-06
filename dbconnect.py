import psycopg2

# DB接続情報
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'postgres'


# DB接続関数
def get_connection():
    return psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'
        .format(
        user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, dbname=DB_NAME
    ))


conn = get_connection()
cur = conn.cursor()

# SQL実行（tbl_sampleから全データを取得）
cur.execute('SELECT * FROM t_securities_code')
rows = cur.fetchall()
print(rows)

cur.close()
conn.close()
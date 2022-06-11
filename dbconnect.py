import psycopg2


# DB接続関数
def get_connection():
    # DB接続情報
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASS = 'postgres'

    return psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'
        .format(
        user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, dbname=DB_NAME
    ))

def select_sql(select_sql):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # SQL実行（tbl_sampleから全データを取得）
        cur.execute(select_sql)
        rows = cur.fetchall()

        cur.close()
        conn.close()
        print("SELECT SUCCESS")
    except Exception as e:
        print("SELECT FAILURE")
        print(e)
    return rows


def insert_sql(insert_sql):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # SQL実行（テーブルにデータを挿入）
        cur.execute(insert_sql)
        # コミット
        conn.commit()

        cur.close()
        conn.close()
        print("INSERT SUCCESS")
    except Exception as e:
        print("INSERT FAILURE")
        print(e)




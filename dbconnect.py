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

# 証券コードを取得処理
def select_sql_securities_code(cursor):
    # 証券コード取得SQL
    SELECT_SQL_SECURITIES_CODE = "SELECT pk_securities_code ,company_name FROM T_SECURITIES_CODE"
    cursor.execute(SELECT_SQL_SECURITIES_CODE)
    result_list = cursor.fetchall()

    return result_list

# 決算発表日情報を取得
def select_sql_announcement_ymd(cursor):
    # 決算発表日取得SQL
    SELECT_SQL_ANNOUNCEMENT_YMD = "SELECT pk_securities_code, pk_year, pk_quarterly_settlement, announcement_of_financial_statements_ymd, next_day_announcement_of_financial_statements_ymd FROM t_announcement_of_financial_statements ORDER BY pk_securities_code, pk_year, pk_quarterly_settlement"
    cursor.execute(SELECT_SQL_ANNOUNCEMENT_YMD)
    result_list = cursor.fetchall()

    return result_list


# 株価情報をINSERT
def insert_stock_price(connection,cursor,stock_price_list):
    # 株価データ挿入SQL
    INSERT_SQL_STOCK_PRICE = "INSERT INTO t_announcement_of_financial_statements_stock_price (pk_securities_code, pk_year, pk_quarterly_settlement, stock_price, next_day_stock_price, growth_rate) VALUES ({pk_securities_code}, {pk_year}, {pk_quarterly_settlement}, {stock_price}, {next_day_stock_price}, {growth_rate});"

    for stock_price_set in stock_price_list:
        # INSERTのVALUESをセットする
        complete_insert_sql_stock_price = INSERT_SQL_STOCK_PRICE.format(**{ \
            "pk_securities_code" : stock_price_set[0] \
            , "pk_year" : stock_price_set[1]\
            , "pk_quarterly_settlement" : stock_price_set[2]\
            , "stock_price" : stock_price_set[3]\
            , "next_day_stock_price" : stock_price_set[4]\
            , "growth_rate" : stock_price_set[5]
            })
        # SQL実行
        cursor.execute(complete_insert_sql_stock_price)

    # コミット
    connection.commit()

# 対象の四半期の上昇率を取得
def select_sql_growth_rate(cursor,year,quarterly_settlement):
    # 返却用リスト
    result_list = []

    # 上昇率取得SQL
    SELECT_SQL_GROWTH_RATE = "SELECT growth_rate FROM t_announcement_of_financial_statements_stock_price WHERE pk_year = '{pk_year}' AND pk_quarterly_settlement = '{pk_quarterly_settlement}'"
    complete_select_sql_growth_rate = SELECT_SQL_GROWTH_RATE.format(**{"pk_year" : year, "pk_quarterly_settlement" : quarterly_settlement})
    # SQL実行
    cursor.execute(complete_select_sql_growth_rate)
    select_sql_growth_rate_list = cursor.fetchall()
    for growth_rate_tuple in select_sql_growth_rate_list:
        result_list.append(growth_rate_tuple[0])

    return result_list

# 証券コードを取得
def select_sql_stock_code_all(cursor):
    # 証券コード取得SQL
    SELECT_SQL_STOCK_CODE = "SELECT stock_code FROM t_stock_code;"
    cursor.execute(SELECT_SQL_STOCK_CODE)
    stockCodeList = cursor.fetchall()

    return stockCodeList

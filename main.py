import dbconnect
import library as lib
import datetime as dt
import time

#お試しsql
INSERT_STOCK_PRICE_SQL = \
    "INSERT INTO T_SECURITIES_CODE( " \
    "pk_securities_code" \
    ",company_name) " \
    "VALUES( " \
    "'9999' " \
    ",'0000' " \
    ")"

if __name__ == "__main__":
    # 開始時間
    start_time = time.time()

    # DB接続開始
    conn = dbconnect.get_connection()
    cur = conn.cursor()

    # 証券コードリスト（('証券コード','企業名')のリスト）を取得
    securities_code_list = dbconnect.select_sql_securities_code(cur)

    # 企業の決算発表日情報をDBに格納

    # 各企業の決算発表日情報をDBから取得
    announcement_ymd_list = dbconnect.select_sql_announcement_ymd(cur)

    # 各企業の第一四半期の決算発表日を使用し、決算発表日とその翌日の株価を取得（必要があれば実行。基本は最初の一回だけで良い）
    #stock_price_list = lib.fetch_stock_price(announcement_ymd_list)

    # 株価情報をDBに格納（まだデータを格納していなければ実行。基本は重複エラーになるため実行しない）
    #dbconnect.insert_stock_price(conn,cur,stock_price_list)

    # 1Qの上昇率を取得
    growth_rate_list_quarter1 = dbconnect.select_sql_growth_rate(cur,'2021','1')
    print(growth_rate_list_quarter1)

    lib.create_growth_comparizon_scatter_plot(growth_rate_list_quarter1,growth_rate_list_quarter1,'2021','1')



    #cur.execute(SELECT_SECURITIES_CODE_SQL)
    #securities_code_list = cur.fetchall()

    # DB接続終了
    cur.close()
    conn.close()

    # 終了時間
    end_time = time.time()
    print(end_time - start_time)

    '''
    # 証券コードリスト（('証券コード','企業名')のリスト）
    securities_code_list = dbconnect.select_sql(SELECT_SECURITIES_CODE_SQL)

    # 株価の検索処理
    price = lib.get_average_stock_price("7203", dt.date(2021, 6, 8))
    print(price)

    dbconnect.insert_sql(INSERT_STOCK_PRICE_SQL)
    '''

    '''
    i = 0
    for securities_code_tuple in securities_code_list:
        if i < 10:
            print(lib.get_average_stock_price(securities_code_tuple[0],dt.date(2021,6,8)))
            i = i + 1
    '''
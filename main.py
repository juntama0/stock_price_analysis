import dbconnect
import library as lib
import datetime as dt

# 証券コード取得SQL
SELECT_SQL_SECURITIES_CODE = "SELECT pk_securities_code ,company_name FROM T_SECURITIES_CODE"
# 決算発表日取得SQL
SELECT_SQL_ANNOUNCEMENT_YMD = "SELECT * FROM t_announcement_of_financial_statements"


# 株価データ挿入SQL
INSERT_STOCK_PRICE_SQL = ""

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
    # DB接続開始
    conn = dbconnect.get_connection()
    cur = conn.cursor()

    # 証券コードリスト（('証券コード','企業名')のリスト）を取得
    cur.execute(SELECT_SQL_SECURITIES_CODE)
    securities_code_list = cur.fetchall()

    # 企業の決算発表日情報をDBに格納

    # 各企業の決算発表日情報をDBから取得
    cur.execute(SELECT_SQL_ANNOUNCEMENT_YMD)
    announcement_ymd_list = cur.fetchall()

    # 各企業の第一四半期の決算発表日を使用し、決算発表日とその翌日の株価を取得
    lib.insert_stock_price(announcement_ymd_list)

    # 後で消す
    print(announcement_ymd_list)
    print(securities_code_list)



    #cur.execute(SELECT_SECURITIES_CODE_SQL)
    #securities_code_list = cur.fetchall()



    # DB接続終了
    cur.close()
    conn.close()





    '''
    # 証券コードリスト（('証券コード','企業名')のリスト）
    securities_code_list = dbconnect.select_sql(SELECT_SECURITIES_CODE_SQL)

    # 

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

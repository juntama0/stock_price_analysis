import dbconnect
import library as lib
import datetime as dt

# 証券コード取得SQL
SELECT_SECURITIES_CODE_SQL = \
    "SELECT " \
    "pk_securities_code " \
    ",company_name " \
    "FROM T_SECURITIES_CODE"
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
    # 証券コードリスト（('証券コード','企業名')のリスト）
    securities_code_list = dbconnect.select_sql(SELECT_SECURITIES_CODE_SQL)
    print(securities_code_list)

    # 株価の検索処理
    price = lib.get_average_stock_price("7203", dt.date(2021, 6, 8))
    print(price)

    dbconnect.insert_sql(INSERT_STOCK_PRICE_SQL)



    '''
    i = 0
    for securities_code_tuple in securities_code_list:
        if i < 10:
            print(lib.get_average_stock_price(securities_code_tuple[0],dt.date(2021,6,8)))
            i = i + 1
    '''

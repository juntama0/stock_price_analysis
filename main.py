import dbconnect
import library as lib
import datetime as dt

# 証券コード取得SQL
SELECT_SECURITIES_CODE_SQL = 'SELECT * FROM t_securities_code'


if __name__ == '__main__':
    # 証券コードリスト（('証券コード','企業名')のリスト）
    securities_code_list = dbconnect.select_sql(SELECT_SECURITIES_CODE_SQL)
    print(securities_code_list)

    # 株価の検索処理
    price = lib.get_average_stock_price('7203', dt.date(2021, 6, 8))
    print(price)

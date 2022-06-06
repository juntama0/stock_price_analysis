import dbconnect


# 証券コード取得SQL
SELECT_SECURITIES_CODE_SQL = 'SELECT * FROM t_securities_code'


if __name__ == '__main__':
    #証券コードリスト（('証券コード','企業名')のリスト）
    securities_code_list = dbconnect.select_sql(SELECT_SECURITIES_CODE_SQL)
    print(securities_code_list)

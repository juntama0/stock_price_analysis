import dbconnect
import library as lib
import datetime as dt
import time


if __name__ == "__main__":
    # 開始時間
    start_time = time.time()

    # DB接続開始
    conn = dbconnect.get_connection()
    cur = conn.cursor()
    print("DB接続完了")

    # 証券コードリスト（('証券コード',)のリスト）を取得
    #securities_code_list = dbconnect.select_sql_securities_code(cur)
    print("証券コードリスト取得完了")

    # 決算発表日情報のリストを取得（[(証券コード,年度,クォータ,決算発表日,翌営業日の決算発表日),(,,,,,)]のリスト）
    #announcement_ymd_list = lib.get_announcement_ymd_list(securities_code_list)
    print("決算発表時間が15時以降となっている銘柄の決算発表日情報を取得")

    # 企業の決算発表日情報をDBに格納
    #dbconnect.insert_announcement_ymd(conn, cur, announcement_ymd_list)

    # 各企業の決算発表日情報をDBから取得([(証券コード,年度,クォータ,決算発表日,翌営業日の決算発表日),(,,,,,)]のリスト)
    announcement_ymd_list = dbconnect.select_sql_announcement_ymd(cur)
    print("決算発表日情報取得完了")

    # 各企業の第一四半期の決算発表日を使用し、決算発表日とその翌日の株価を取得（必要があれば実行。基本は最初の一回だけで良い）
    stock_price_list = lib.fetch_stock_price(announcement_ymd_list)
    print("株価リスト取得完了")

    # 株価情報をDBに格納（まだデータを格納していなければ実行。基本は重複エラーになるため実行しない）
    dbconnect.insert_stock_price(conn,cur,stock_price_list)
    print("DBに株価情報を格納完了")

    # 1Qの上昇率を取得
    #growth_rate_list_quarter1 = dbconnect.select_sql_growth_rate(cur,'2021','1')

    # 前回と今回の上昇率に関する散布図を描画
    #lib.create_growth_comparizon_scatter_plot(growth_rate_list_quarter1,growth_rate_list_quarter1,'2021','1')



    #cur.execute(SELECT_SECURITIES_CODE_SQL)
    #securities_code_list = cur.fetchall()

    # DB接続終了
    cur.close()
    conn.close()

    # 終了時間
    end_time = time.time()
    print("実行時間：" + str(round(end_time - start_time)) + "秒")


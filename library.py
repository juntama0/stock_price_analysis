# ライブラリをインポート
from pandas_datareader import data
import datetime
from datetime import timedelta
import psycopg2
import time
from bs4 import BeautifulSoup
import numpy
import matplotlib.pyplot as plt
import dbconnect


# その日の株価を取得
def get_stock_price(securities_code,ymd):# ymdは日付型（例：'2022-01-01'）
    start_time = time.time()
    start = ymd
    end = ymd

    try:
        # 証券コードを検索用に整形
        search_securities_code = securities_code + ".JP"
        # 株価を取得
        df = data.DataReader(search_securities_code,"stooq",start,end)
        # dataframeの
        dataframe = df.head()
        # 対象の日付をstr型に変換
        str_ymd = ymd.strftime("%Y-%m-%d")
        # dataframeの中にある対象の日付のデータにアクセス
        stock_price_data_group = dataframe.loc[str_ymd]

        # その日の高値
        high_stock_price = stock_price_data_group[1]
        # その日の安値
        low_stock_price = stock_price_data_group[2]
        # その日の平均株価(小数点は丸め込み)
        average_stock_price = round((high_stock_price + low_stock_price) / 2)

        end_time = time.time()
        print("証券コード：" + securities_code + ",日付：" + str(ymd) + "の株価取得タイム：" + str(end_time - start_time))

        return average_stock_price
    except Exception as e:
        print(e)
        return 0


# 25日間の平均株価を取得
def get_average_stock_price_25(securities_code,ymd):# ymdは日付型（例：'2022-01-01'）
    start = ymd - timedelta(25)
    end = ymd

    try:
        # 証券コードを検索用に整形
        search_securities_code = securities_code + ".JP"
        # 株価を取得
        df = data.DataReader(search_securities_code,"stooq",start,end)

        # 株価データの個数を取得
        dataframe_row_num = len(df['High'])
        # 全ての株価の高値と安値の合計値
        total_stock_price = df['High'].sum() +df['Low'].sum()
        # 25日の平均株価を算出
        average_stock_price_25 =  total_stock_price / (dataframe_row_num * 2) # 2は2列分の意

        return average_stock_price_25
    except Exception as e:
        print(e)
        return 0


# 決算発表日の株価と上昇率を取得
def fetch_stock_price(announcement_ymd_list):
    # 返却用のリスト（決算発表日株価、決算発表日翌日の株価、上昇率のリスト）
    return_list = []
    for announcement_ymd_tuple in announcement_ymd_list:
        # 一時格納用株価リスト
        stock_price_list = []

        # 証券コードを取得
        securities_code = announcement_ymd_tuple[0]

        # 決算発表日を日付型に変換
        announcement_ymd = announcement_ymd_tuple[3]
        announcement_ymd_datetime = datetime.datetime.strptime(announcement_ymd, "%Y%m%d")

        # 決算発表日の翌日を日付型に変換
        announcement_next_day_ymd = announcement_ymd_tuple[4]
        announcement_next_day_ymd_datetime = datetime.datetime.strptime(announcement_next_day_ymd, "%Y%m%d")

        # 決算発表日の株価を取得
        announcement_stock_price = get_stock_price(securities_code,announcement_ymd_datetime)
        # 決算発表日の翌日の株価を取得
        announcement_next_day_stock_price = get_stock_price(securities_code, announcement_next_day_ymd_datetime)
        # 上昇率を算出
        growth_rate = round((announcement_next_day_stock_price - announcement_stock_price) / announcement_stock_price, 3)

        # 決算発表日から25日前までの平均株価を取得
        average_stock_price_25 = get_average_stock_price_25(securities_code,announcement_ymd_datetime)
        # 決算発表日の株価と25日平均株価の乖離率を取得
        deviation_rate_average_stock_price_25 = round((average_stock_price_25 - announcement_stock_price) / announcement_stock_price, 3)

        print("平均："+str(average_stock_price_25) + ",株価："+str(announcement_stock_price) + ",乖離率：" + str(deviation_rate_average_stock_price_25))

        # 一時格納用株価リストに格納
        stock_price_list.append(announcement_ymd_tuple[0])
        stock_price_list.append(announcement_ymd_tuple[1])
        stock_price_list.append(announcement_ymd_tuple[2])
        stock_price_list.append(announcement_stock_price)
        stock_price_list.append(announcement_next_day_stock_price)
        stock_price_list.append(growth_rate)
        stock_price_list.append(deviation_rate_average_stock_price_25)
        # 返却用リストに格納
        return_list.append(stock_price_list)

    return return_list


# 散布図を作成
def create_growth_comparizon_scatter_plot(previous_growth_rate_list,growth_rate_list,year,quarter):# 上昇率の単位は％
    x_list = numpy.array(previous_growth_rate_list)
    y_list = numpy.array(growth_rate_list)
    plt.xlim(-0.20,0.20)
    plt.ylim(-0.20,0.20)
    plt.title("Year:" + year + " Quarter:" + quarter,fontsize=15)
    plt.xlabel("This growth rate",fontsize=15)
    plt.ylabel("Previous growth rate",fontsize=15)
    plt.grid(True)
    plt.tick_params(labelsize=10)
    # グラフの描画
    plt.scatter(x_list,y_list,s=5,c="b",marker="D",alpha=0.5)
    plt.show()

'''
#LINE証券の企業情報詳細ページにアクセスし、過去１年間の決算情報を取得（20220605 maeda）要修正。mainメソッドは関数を呼び出すだけ。
def getKessanYMD():
    # 決算日情報（Q、決算年月日、決算発表時間）を保持する配列
    kessanInfoList = []
    # スクレイピングの許可は確認済み
    url = "https://trade.line-sec.co.jp/stock/detail/"

    # postgreSQLへの接続を確立
    conn = dbconnect.get_connection()
    cur = conn.cursor()

    # 証券コード取得メソッドの呼び出し
    stockCodeList = dbconnect.select_sql_stock_code_all(cur)

    #postgreSQLの接続をclose
    if conn is not None:
        cur.close()
        conn.close()

    # 証券コードリストの要素分、決算日情報の取得処理を繰り返す
    for stockCode in stockCodeList:
        try:
            # 検索する
            soup = BeautifulSoup(requests.get(url + stockCode).content, "html.parser")
            # サーバーに負荷を掛けないように1秒止める
            time.sleep(1)
            # class = _5wW_WUの存在確認
            checkClass = soup.find(True, class_ = "_5wW_WU")
            # class = _5wW_WU が存在する場合、class = "_5wW_H1" を抽出する。存在しない場合次の証券コードへ。
            if checkClass is not None:
                settlementInfo = soup.find_all(True, class_ = "_5wW_H1")
'''
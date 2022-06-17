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
def get_25_average_stock_price(securities_code,ymd):# ymdは日付型（例：'2022-01-01'）
    start = ymd - timedelta(25)
    end = ymd

    try:
        # 証券コードを検索用に整形
        search_securities_code = securities_code + ".JP"
        # 株価を取得
        df = data.DataReader(search_securities_code,"stooq",start,end)
        # dataframe
        dataframe = df.head(25)
        print(type(dataframe))

        # 対象の日付をstr型に変換
        str_ymd = ymd.strftime("%Y-%m-%d")
        # dataframeの中にある対象の日付のデータにアクセス
        stock_price_data_group = dataframe.loc[str_ymd]
        print(df['Open'][0])


        # その日の高値
        high_stock_price = stock_price_data_group[1]
        # その日の安値
        low_stock_price = stock_price_data_group[2]
        # その日の平均株価(小数点は丸め込み)
        average_stock_price = round((high_stock_price + low_stock_price) / 2)

        return average_stock_price
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
        growth_rate = round((announcement_next_day_stock_price - announcement_stock_price) / announcement_stock_price * 100,1)

        # 決算発表日から25日前の日付を取得
        #get_average_stock_price

        # 一時格納用株価リストに格納
        stock_price_list.append(announcement_ymd_tuple[0])
        stock_price_list.append(announcement_ymd_tuple[1])
        stock_price_list.append(announcement_ymd_tuple[2])
        stock_price_list.append(announcement_stock_price)
        stock_price_list.append(announcement_next_day_stock_price)
        stock_price_list.append(growth_rate)
        # 返却用リストに格納
        return_list.append(stock_price_list)

    return return_list

#date = datetime.datetime.strptime('20220616', "%Y%m%d")
#fetch_stock_price([('1301', '2021', '1', '20210112', '20210113')])

#get_25_average_stock_price('7201',date)

# 散布図を作成
def create_growth_comparizon_scatter_plot(previous_growth_rate_list,growth_rate_list,year,quarter):# 上昇率の単位は％
    x_list = numpy.array(previous_growth_rate_list)
    y_list = numpy.array(growth_rate_list)
    plt.xlim(-20.0,20.0)
    plt.ylim(-20.0,20.0)
    plt.title("Year:" + year + " Quarter:" + quarter,fontsize=20)
    plt.xlabel("This growth rate",fontsize=20)
    plt.ylabel("Previous growth rate",fontsize=20)
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

##########################
# 以下の関数は参考。後ほど削除
##########################
# ライブラリをインポート
'''
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.firefox import service as ff
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from selenium import webdriver



#日経経済新聞のサイトから、指定した日付に決算発表を行う企業の銘柄コードを取得
def getStockCode(kessanHappyoYmd):
    year = kessanHappyoYmd[0:4]
    month = kessanHappyoYmd[4:6]
    day = kessanHappyoYmd[6:8]
    pageNo = 1

    # 銘柄コードと決算発表日の配列を作成
    codeAndKessanDayList = []

    while True:
        # URLを取得
        url = "https://www.nikkei.com/markets/kigyo/money-schedule/kessan/?ResultFlag=1&SearchDate1=" \
              + year + "%E5%B9%B4" + month + "&SearchDate2="+day+"&Gcode=%20&hm=" + str(pageNo)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15 "}

        # 検索する
        soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
        # サーバーに負荷を掛けないように1秒止める
        time.sleep(1)

        # テーブル全体の決算データ
        kessanDataTable = []
        # テーブルを指定
        table = soup.findAll("table", {"class": "cmn-table_style2"})[0]
        rows = table.findAll("tr")
        # 行番号を定義
        rowNo = 0

        # テーブル各行のデータを取得
        for row in rows:
            kessanDataRow = []
            for cell in row.findAll(['td', 'th']):
                kessanDataRow.append(cell.get_text())
            # 最初の行は項目名のため、リストに追加しない
            if rowNo != 0:
                codeAndKessanDayList.append(kessanDataRow[1])
                kessanDataTable.append(kessanDataRow)
            rowNo = rowNo + 1

        # 1ページに表示される検索結果数がMax（50件）でない場合、次のページ検索を行わない。
        if len(kessanDataTable) < 50:
            break
        pageNo = pageNo + 1
    return codeAndKessanDayList

#セレニウムでLINE証券の企業情報詳細ページにアクセスし、前回のAI予想を取得
def getStockPriceForecastFromLineShoken(stockCodeList):
    kessanNameList = ['決算1Q','決算2Q','決算3Q','決算通期']

    #ドライバの設定
    firefox_servie = ff.Service(executable_path="/Users/jun/Program/geckodriver")
    driver = webdriver.Firefox(service=firefox_servie)

    #返却するリスト
    resultList = []

    for stockCode in stockCodeList:
        try:
            #URLを設定
            url = "https://trade.line-sec.co.jp/stock/detail/" + stockCode
            driver.get(url)
            time.sleep(1)

            #決算予想のリンクリスト
            kessanForecastlinkList = driver.find_elements(By.XPATH,"//article/a")
            #決算予想未取得フラグ
            kessanUnacquiredFlg = True
            #業績修正予想未取得フラグ
            gyosekiUnacquiredFlg = True

            for link in kessanForecastlinkList:
                # クリックしたい要素までスクロール
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                #報告の種類名を取得（決算XQor業績修正）
                reportName= link.find_element(By.CLASS_NAME,"_5wW_x3").text

                if (reportName in kessanNameList and kessanUnacquiredFlg) or (reportName == "業績修正" and gyosekiUnacquiredFlg):
                    #決算予想のリンクをクリック
                    link.click()
                    time.sleep(1)

                    # 決算予想結果
                    forecastResultPath = driver.find_element(By.CLASS_NAME, "_3rF_Ga")
                    fororecastResult = forecastResultPath.find_element(By.TAG_NAME,"p").text

                    # 企業名
                    kigyoNameLink = driver.find_element(By.CLASS_NAME, "_3rF_nN")
                    kigyoName = kigyoNameLink.find_element(By.TAG_NAME,"h1").text

                    #報告種類が決算
                    if reportName in kessanNameList:
                        result = [stockCode,kigyoName,"決算",fororecastResult]
                        kessanUnacquiredFlg = False

                    #報告種類が業績修正
                    elif reportName == "業績修正":
                        result = [stockCode,kigyoName, "業績修正", fororecastResult]
                        gyosekiUnacquiredFlg = False

                    # 返却用のリストに結果を格納
                    resultList.append(result)

                    #前のページに戻る
                    driver.back()
                    time.sleep((1))

        except Exception as e:
            print(e)
    #ブラウザを閉じる
    driver.close()

    return resultList

#メールの送信
def sendMail(sendAddress,password,fromAddress,toAddress,message):
    sendAddress = sendAddress
    password = password
    subject = 'LINE証券株価予測まとめ'
    bodyText = message
    fromAddress = fromAddress
    toAddress = toAddress

    # SMTPサーバに接続
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.login(sendAddress, password)

    # メール作成
    msg = MIMEText(bodyText)
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Date'] = formatdate()

    # 作成したメールを送信
    smtpobj.send_message(msg)
    smtpobj.close()

'''
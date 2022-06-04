# ライブラリをインポート
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
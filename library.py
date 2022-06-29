# ライブラリをインポート
from pandas_datareader import data
import datetime
from datetime import timedelta
import time
import numpy
import matplotlib.pyplot as plt
from selenium.webdriver.firefox import service as ff
from selenium.webdriver.common.by import By
from selenium import webdriver
import workdays
import jpholiday



# その日の株価を取得
def get_stock_price(securities_code,ymd):# ymdは日付型（例：'2022-01-01'）
    start_time = time.time()
    start = ymd
    end = ymd
    # 取得サイトを指定(yahoo or stooq)
    site = "yahoo"

    try:
        if site == "yahoo":
            # 証券コードを検索用に整形
            search_securities_code = securities_code + ".T"
            # yahooから株価を取得
            df = data.DataReader(search_securities_code, site, start, end)
        elif site == "stooq":
            # 証券コードを検索用に整形
            search_securities_code = securities_code + ".jp"
            # yahooから株価を取得
            df = data.DataReader(search_securities_code, site, start, end)
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

ymd = datetime.datetime.strptime('20220621', "%Y%m%d")
test = get_stock_price('7203',ymd)
print(test)


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
        if dataframe_row_num == 0:
            average_stock_price_25 = 0
        else:
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

        # 決算発表日から25日前までの平均株価を取得
        average_stock_price_25 = round(get_average_stock_price_25(securities_code,announcement_ymd_datetime))
        if announcement_stock_price == 0:
            deviation_rate_average_stock_price_25 = 0
            growth_rate = 0
        else:
            # 上昇率を算出
            growth_rate = round( (announcement_next_day_stock_price - announcement_stock_price) / announcement_stock_price, 3)
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


# 翌営業日を取得
def get_next_working_day(datetime):
    next_working_day = datetime + timedelta(days=1)
    # 翌日が土日もしくは祝日の場合
    while next_working_day.weekday() >= 5 or jpholiday.is_holiday(next_working_day):
        next_working_day = next_working_day +timedelta(days=1)

    return next_working_day


# 決算発表日の情報を取得（引数はタプルのリスト[('9999',),('9999',)]）
def get_announcement_ymd_list(securities_code_list):
    # ドライバの設定
    firefox_servie = ff.Service(executable_path="/Users/jun/Program/geckodriver")
    driver = webdriver.Firefox(service=firefox_servie)

    # 返却するリスト
    return_list = []

    for securities_code in securities_code_list:
        try:
            # URLを設定
            url = "https://trade.line-sec.co.jp/stock/detail/" + securities_code[0]
            driver.get(url)
            time.sleep(1)

            # もっと見るボタンの要素を取得
            if len(driver.find_elements(By.CLASS_NAME,"SWx__P"))>0:
                motto_miru_button = driver.find_element(By.CLASS_NAME,"SWx__P")
                driver.execute_script("arguments[0].scrollIntoView(true);", motto_miru_button)
                motto_miru_button.click()
                #time.sleep(3)

            # 決算予想ブロック
            settlement_day_list = driver.find_elements(By.XPATH, "//article/a")

            # 一つ前の決算結果の格納リスト
            previous_settlement_inf_list = ['9999','2099','0Q','20990101','20990101']

            for settlement_day_block in settlement_day_list:
                # "決算"もしくは"業績報告"の文字列取得
                announcement_genre = settlement_day_block.find_element(By.CLASS_NAME,"_5wW_ZM").text
                # 決算発表時間が書かれている文字列を取得
                announcement_time_text = settlement_day_block.find_element(By.CLASS_NAME,"_5wW_uB").text
                # 決算発表時間を取得
                announcement_time = announcement_time_text[11:13]

                # 報告種別が"決算"かつ決算発表時間が15時以降の銘柄を取得（翌日株価と比較するため）
                if announcement_genre == "決算" and int(announcement_time) >= 15:
                    # 年度情報が書いてある文字列を取得
                    year_text = settlement_day_block.find_element(By.CLASS_NAME,"_5wW_Jg").text
                    year = year_text[0:4]

                    # 決算発表日を取得（YYYY/MM/DD）
                    announcement_date_slash = announcement_time_text[0:10]
                    # 日付型に変換
                    announcement_date_datetime = datetime.datetime.strptime(announcement_date_slash, '%Y/%m/%d')
                    # 決算発表日の翌営業日を取得
                    next_annoucement_date_datetime = get_next_working_day(announcement_date_datetime)

                    #決算発表日、決算発表日の翌営業日をString型に変換
                    announcement_date = announcement_date_datetime.strftime('%Y%m%d')
                    next_annoucement_date = next_annoucement_date_datetime.strftime('%Y%m%d')

                    # クォータを取得
                    quarter_text = settlement_day_block.find_element(By.CLASS_NAME,"_5wW_Va").text
                    if quarter_text == "通期":
                        quarter = "4Q"
                    else:
                        quarter = quarter_text

                    # 結果を格納
                    settlement_inf_list = [securities_code[0],year,quarter,announcement_date,next_annoucement_date]

                    # 取得結果が重複していなければ、各銘柄の決算発表日情報リストを返却リストに格納
                    if not previous_settlement_inf_list[0:3] == settlement_inf_list[0:3]:
                        return_list.append(settlement_inf_list)

                    # 結果を一つ前の結果リストに格納
                    previous_settlement_inf_list = settlement_inf_list

        except Exception as e:
            print(e)
    # ブラウザを閉じる
    driver.close()
    return return_list

'''
# LINE証券の企業情報詳細ページにアクセスし、過去１年間の決算情報を取得（20220605 maeda）要修正。mainメソッドは関数を呼び出すだけ。
def get_settlement_ymd(securities_code_list):
    # 決算日情報（証券コード、年度、クォータ、決算公表日、決算公表日の翌営業日）を保持する配列
    settlement_info_list = []

    for stockCode in securities_code_list:

        # タプルの要素を文字列に変換する
        stock_code_str = "".join(stockCode)

        try:
            # URLを設定print(settlement_quarter)
            url = "https://trade.line-sec.co.jp/stock/detail/" + stock_code_str

            # ドライバの設定（geckodriver は /usr/local/bin/に配置している）
            driver = webdriver.Firefox()
            driver.get(url)
            time.sleep(1)

            # もっとみるボタンが存在する場合、ボタンをクリックする
            settlement_button = driver.find_elements(By.XPATH, "//article/div/div/button")
            if not len(settlement_button) == 0:
                for button_to_click in settlement_button:
                    # クリックしたいボタンまで画面をスクロール
                    driver.execute_script("arguments[0].scrollIntoView(true);", button_to_click)
                    button_to_click.click()
                    time.sleep(1)

            # 決算予想のリンクリスト
            kessan_forecast_link_list = driver.find_elements(By.XPATH, "//article/a")

            for link in kessan_forecast_link_list:
                # 報告の種類名を取得（決算or業績修正）
                settlement_category = link.find_element(By.CLASS_NAME, "_5wW_ZM").text

                # 決算だがQがない場合の検証のため取得
                report_name = link.find_element(By.CLASS_NAME, "_5wW_x3").text

                # 決算クオーターを取得（通期or1Qor2Qor3QorNone）
                # if not settlement_category == "業績修正":
                if (settlement_category == "決算") and ("Q" in report_name or "通期" in report_name):
                    settlement_quarter = link.find_element(By.CLASS_NAME, "_5wW_Va").text
                else:
                    settlement_quarter = ""

                # 決算年度を取得
                settlement_year = link.find_element(By.CLASS_NAME, "_5wW_Jg").text

                # 決算発表日と時間を取得
                settlement_published_date_time = link.find_element(By.CLASS_NAME, "_5wW_uB").text
                time.sleep(1)

                # データ整形。決算クオーターが"通期"の場合、"4Q"に置換する。
                if settlement_quarter == "通期":
                    settlement_quarter = "4"

                # データ整形。クォータに含まれている"Q"を取り除く。
                settlement_quarter = settlement_quarter.replace("Q", "")

                # データ整形。決算年度のみを切り出す。
                settlement_year = settlement_year[0:4]

                # データ整形。決算公表日と決算公表時間を分割する。
                settlement_published_date = settlement_published_date_time[0:11]
                settlement_published_time = settlement_published_date_time[11:]

                # データ整形。決算公表日に含まれている"/"を取り除く。
                settlement_published_date = settlement_published_date.replace("/", "")

                # データ整形。決算公表日の末尾に" "が入ってる場合は無視する。
                if settlement_published_date[-1] == " ":
                    settlement_published_date = settlement_published_date[:-1]

                # 決算公表日の翌営業日を求めるために、文字列を日付型にする。
                settlement_published_date_tmp = datetime.datetime.strptime(settlement_published_date, '%Y%m%d')

                # 決算公表日の翌日を求める
                settlement_published_date_tmp = settlement_published_date_tmp + timedelta(days=1)

                # 土日祝を判定し、翌営業日を取得する
                while True:
                    # 祝日の場合
                    if jpholiday.is_holiday(settlement_published_date_tmp):
                        settlement_published_date_tmp = settlement_published_date_tmp + timedelta(days=1)
                        continue
                    # 土日の場合
                    elif settlement_published_date_tmp.weekday() >= 5:
                        settlement_published_date_tmp = settlement_published_date_tmp + timedelta(days=1)
                        continue
                    # 平日の場合
                    else:
                        settlement_published_next_date = settlement_published_date_tmp
                        break

                # 翌営業日を文字列型にする
                settlement_published_next_date = settlement_published_next_date.strftime("%Y%m%d")

                # 決算カテゴリが"決算"かつ決算公表時間が"15:00"の場合、返却用リストにデータを格納する。
                if (settlement_category == "決算") and (settlement_published_time == "15:00"):
                    settlement_info_result = [stock_code_str, settlement_year, settlement_quarter,
                                              settlement_published_date, settlement_published_next_date]
                    settlement_info_list.append(settlement_info_result)
                # 決算カテゴリが"業績修正"かつ決算公表時間が"15:00"の場合、次の要素へ処理を移る。
                elif (settlement_category == "業績修正") and (settlement_published_time == "15:00"):
                    continue
                # 決算公表時間が15:00でない場合、次の要素へ処理を移る。
                elif settlement_published_time is not "15:00":
                    continue

            # ブラウザを閉じる
            driver.close()

        except Exception as e:
            print(e)

    return settlement_info_list

'''
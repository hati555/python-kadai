import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

### Chromeを起動する関数
def set_driver(driver_path,headless_flg):

    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg==True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    #options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)

### main処理
def main():
    # ログ出力上書きモードでファイルオープン
    f = open('mynavilog.txt','w')
#    search_keyword="高収入"
    # driverを起動
    driver=set_driver("chromedriver.exe",False)
     # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    # ポップアップを閉じる
    # driver.execute_script('document.querySelector(".karte-close").click()')
    # time.sleep(2)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    # コンソールから入力を求める
    word = input("検索条件を入力してください >>> ")
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(word)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    
    # 表示ページ
    page = 1

    #
    df = pd.DataFrame({'copy':[],'status':[],'name':[]})
    
    # nページ分繰り返し
    while True:
        try:
            if len(driver.find_elements_by_css_selector(".iconFont--arrowLeft")) > 0:
                f.write('今{0}ページ目'.format(page))
                # 検索結果の一番上の会社名を取得
                name_list=driver.find_elements_by_class_name("cassetteRecruit__name")
                copy_list=driver.find_elements_by_class_name("cassetteRecruit__copy")
                status_list=driver.find_elements_by_class_name("labelEmploymentStatus")
                # 1ページ分繰り返し
    #            print("{},{},{}".format(len(copy_list),len(status_list),len(name_list)))
                for name,copy,status in zip(name_list,copy_list,status_list):
    #                print(name.text)
    #                print(copy.text)
    #                print(status.text)
                    series = pd.Series([copy.text, status.text, name.text],['copy','status','name_list'])
                    df = df.append(series, ignore_index = True)

                btn = driver.find_element_by_css_selector(".iconFont--arrowLeft").get_attribute("href")
                print("next url:{}".format(btn))
                driver.get(btn)
                page+=1
                driver.implicitly_wait(10)
                print("Moving to next page......")
                time.sleep(10)                
            else:
                # CSV出力
                df.to_csv("mynavi_data.csv")
                f.write('全ページ取得終了！！！')

                print("全ページ取得終了！！！")
                f.close()
                break
        except IOError:
            f.write('IOエラー！！！')
            print("IOエラー！！！")
            # 処理を継続
            
### 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
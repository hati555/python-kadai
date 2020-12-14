### 検索ツールサンプル
### これをベースに課題の内容を追記してください
import csv

### 課題1

# 検索ソース
#source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search():
    #CSV読込
    f = open("searchdata.csv","r")
    reader = csv.reader(f)
    source = [ e for e in reader ]
    f.close()
        
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    
    ### ここに検索ロジックを書く
    if word in source:
        print("{}が見つかりした".format(word))
    else:
        print("ありませんでした。")
        source.append(word)
        print(source)

if __name__ == "__main__":
    search()
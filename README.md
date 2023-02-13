## 環境
```
python -V                                                                                  [main]
Python 3.9.13

pip list                                                                                   [main]
Package            Version
------------------ -----------
beautifulsoup4     4.11.1
certifi            2022.9.24
charset-normalizer 2.1.1
contourpy          1.0.6
cycler             0.11.0
fonttools          4.38.0
gensim             4.2.0
idna               3.4
ipadic             1.0.0
kiwisolver         1.4.4
matplotlib         3.6.2
mecab-python3      1.0.5
numpy              1.23.3
oauthlib           3.2.2
packaging          21.3
Pillow             9.2.0
pip                22.3
pyparsing          3.0.9
python-dateutil    2.8.2
requests           2.28.1
requests-oauthlib  1.3.1
scipy              1.9.3
setuptools         58.1.0
six                1.16.0
smart-open         6.2.0
soupsieve          2.3.2.post1
torch              1.12.1
torchaudio         0.12.1
torchvision        0.13.1
tweepy             4.10.1
typing_extensions  4.3.0
urllib3            1.26.12
wordcloud          1.8.2.2
```

## 環境構築手順
python（3.9.13）のインストール

mecabのインストール

ipadic辞書のインストール

mecab-ipadic-NEologd辞書のインストール

辞書インストール後コードのMeCab.Tagger部分の引数のpathを書き換える

twitterAPIのアクセスキー取得

APIのアクセスキー取得後configファイルを作成し設定する

↓config.py
```
API_KEY='API_KEY'
API_KEY_SECRET='API_KEY_SECRET'
BEARER_TOKEN='BEARER_TOKEN'
ACCESS_TOKEN='ACCESS_TOKEN'
ACCSESS_TOKEN_SECRET='ACCSESS_TOKEN_SECRET'
```

## 作成したファイル
config.py
- ここにTwitterAPIで使用するkeyなどを記載

tweets.py
- main.py実行時にツイートを収集してCSVに記述する部分の処理

python analysys.py
- ファイル名を引数に取ることで個別のDCG計算可能

python main.py
- ツイート収集→タイトル入力でDCG計算

python auto_analysys-toCSV.py
- コード内に自動でDCG値を算出したい日付のcsvファイルとタイトル群を複数入れることで自動実行可能
- Word2Vecのパラメータを変動した結果をCSVファイルへ出力可能
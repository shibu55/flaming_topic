# 環境
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

# 環境構築手順
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

# 作成したファイル
config.py
- ここにTwitterAPIで使用するkeyなどを記載

tweets.py
- main.py実行時にツイートを収集してCSVに記述する部分の処理

analysys.py
- ファイル名を引数に取ることで個別のDCG計算可能

main.py
- ツイート収集→タイトル入力でDCG計算

auto_analysys-toCSV.py
- コード内に自動でDCG値を算出したい日付のcsvファイルとタイトル群を複数入れることで自動実行可能
- Word2Vecのパラメータを変動した結果をCSVファイルへ出力可能

all_analysys.py
- コード内に自動でDCG値を算出したい日付のcsvファイルとタイトル群を複数入れることで自動実行可能

# 実行方法
## main.py
```
python main.py
```
ツイート収集処理実行前に入力2回必要（ツイートデータの収集期間を指定可能）

入力後ツイート収集
```
何日前から(1~6): 1
何日前まで(0~5): 0
```

過去x日分の炎上を含むツイートを収集したcsvファイルがdataフォルダに作成される

（ここまでtweets.py）
（ここからanalysys.py）

収集したツイートをもとにいいね数やリツイート数があるツイートのみを含む`text.txt`を出力

`text.txt`を分かち書きした結果を`wakati.txt`に出力

「炎上トピック」と「炎上」をアンド検索した結果から上位頻出単語を出力（baseline手法の結果）

`DCG値を計算するタイトルを入力:`と表示後，記事タイトルを入力するとDCG値とヒット数を確認可能

`wakati.txt`の内容をもとにベクトル化しトピックの類似単語出力（提案手法の結果）

### 出力例
```
shibutani 14:09:02 : /Users/shibutani/h-shibutani/引き継ぎ/dev % python main.py                                                                                   [main]
何日前から(1~6): 1
何日前まで(0~5): 0
97
(↑リクエスト回数)
最後のページに到達しました
（baseline手法）
炎上トピック：批判
1: 土下座
2: 人気
3: 公開
4: コメント
5: 反論
6: ユーチューバー
7: レジ
8: トラブル
9: 路上
10: カノックスター
11: 殺到
12: 無視
13: 作品
14: 引用
15: 全員
DCG値を計算するタイトルを入力: レジトラブルで炎上の人気ユーチューバー　店前の路上で土下座する動画公開　批判コメントに反論
ヒット数: 9
ヒットした単語: 土下座, 人気, 公開, コメント, 反論, ユーチューバー, レジ, トラブル, 路上
DCGスコア: 4.254494511770458
（提案手法）
炎上トピック：批判
1: 動画
2: 人気
3: 反論
4: 公開
5: コメント
6: 土下座
7: ニュース
8: トラブル
9: ユーチューバー
10: 路上
11: スポニチアネックス
12: カノックスター
13: レジ
14: 迷惑
15: 再生
DCG値を計算するタイトルを入力: レジトラブルで炎上の人気ユーチューバー　店前の路上で土下座する動画公開　批判コメントに反論
ヒット数: 10
ヒットした単語: 動画, 人気, 反論, 公開, コメント, 土下座, トラブル, ユーチューバー, 路上, レジ
DCGスコア: 4.472875539792207
```


### *注意
ツイート収集のリクエストの上限回数に達すると１５分程度ツイート収集ができなくなります

## analysys.py
```
python analysys.py csvファイルまでのpath
```

引数に指定したファイルに対してmain.pyの後半と同様の処理を実行
### 出力例
```
shibutani 14:15:45 : /Users/shibutani/h-shibutani/引き継ぎ/dev % python analysys.py data/tweets_炎上_02-12_14-08-02-13_14-08.csv
炎上トピック：批判
1: 土下座
2: 人気
3: 公開
4: コメント
5: 反論
6: ユーチューバー
7: レジ
8: トラブル
9: 路上
10: カノックスター
11: 殺到
12: 無視
13: 作品
14: 引用
15: 全員
DCG値を計算するタイトルを入力: レジトラブルで炎上の人気ユーチューバー　店前の路上で土下座する動画公開　批判コメントに反論
ヒット数: 9
ヒットした単語: 土下座, 人気, 公開, コメント, 反論, ユーチューバー, レジ, トラブル, 路上
DCGスコア: 4.254494511770458
炎上トピック：批判
1: 反論
2: 公開
3: 人気
4: コメント
5: トラブル
6: ユーチューバー
7: ニュース
8: 路上
9: 土下座
10: 動画
11: スポニチアネックス
12: カノックスター
13: 謝罪
14: レジ
15: 再生
DCG値を計算するタイトルを入力: レジトラブルで炎上の人気ユーチューバー　店前の路上で土下座する動画公開　批判コメントに反論
ヒット数: 10
ヒットした単語: 反論, 公開, 人気, コメント, トラブル, ユーチューバー, 路上, 土下座, 動画, レジ
DCGスコア: 4.466184029564828
```

## auto_analysys-toCSV.py
```
python auto_analysys-toCSV.py
```
指定した複数のファイル，タイトルに対してanalysys.pyを自動実行

パラメータを変動可能でパラメータごとの結果をCSVファイルに出力

ファイル名指定場所

```
cf = csv_file('ここにcsvのファイル名を書く')
```


パラメータの変動実験等を一括で行いたい時に使用

### 使用している変数
`file_names_all`

自動実行するCSVファイルを指定する（複数指定可能）

`titles_all`

実行するファイルに対してDCG値を計算するタイトル群を格納する

`vector_size_list`

実行時に変動させるベクトルサイズの値を複数設定可能

`min_count_list`

実行時に変動させる最小頻度の値を複数設定可能

`window_list`

実行時に変動させるウインドウサイズの値を複数設定可能

## all_analysys.py
```
python all_analysys.py
```

auto_analysys-toCSV.pyのcsv出力，パラメータ変動なしバージョン
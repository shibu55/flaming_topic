import tweepy
import datetime
import csv
import config


class make_csv:
    def __init__(self,filename):
        self.file='./data/'+filename
        # csvファイルの作成とヘッダーの書き込み
        with open(self.file,mode="w",encoding="utf-8") as file:
            writer=csv.writer(file) # writerオブジェクトを作成
            header=[
                "text",
                "tweet_id",
                "post_date",
                "retweet",
                "favorite",
                ] # ヘッダー
            writer.writerow(header) # ヘッダーを書き込む
    def make(self,tweet):
        # csvファイルの作成とヘッダーの書き込み
        with open(self.file,mode="a",encoding="utf-8") as file:
            writer=csv.writer(file) # writerオブジェクトを作成

            text = str(tweet.text).replace('\n','')
            if text.find(','):
                text.replace(',','，')

            body=[
                text,
                tweet.id,
                tweet.created_at + datetime.timedelta(hours=+9),
                tweet.public_metrics['retweet_count'],
                tweet.public_metrics['like_count'],
                ]
            writer.writerow(body) # を書き込む


def generate_csv(word, file_name):
    API_KEY = config.API_KEY
    API_KEY_SECRET = config.API_KEY_SECRET
    BEARER_TOKEN = config.BEARER_TOKEN
    ACCESS_TOKEN = config.ACCESS_TOKEN
    ACCSESS_TOKEN_SECRET = config.ACCSESS_TOKEN_SECRET

    #https://docs.tweepy.org/en/stable/client.html
    client = tweepy.Client(bearer_token = BEARER_TOKEN, consumer_key = API_KEY, consumer_secret = API_KEY_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCSESS_TOKEN_SECRET)


    first_flg = True

    now = datetime.datetime.now()
    start_time = now  - datetime.timedelta(days = 2) - datetime.timedelta(hours = 9)
    end_time = start_time + datetime.timedelta(days = 1)

    QUERY = word + ' -is:retweet'

    mc = make_csv(file_name)
    for i in range(200):
        #1回目のリクエストと2回目以降のリクエストパラメータが違うためフラグ管理

        # print("first_flg: " + str(first_flg))

        MAX_RESULTS = 100
        if first_flg == True:
            #1回目リクエスト
            tweets = client.search_recent_tweets(query = QUERY, tweet_fields = ["public_metrics","created_at"], max_results = MAX_RESULTS, start_time = start_time, end_time = end_time)
            #初回フラグを落とす
            first_flg = False
        else:
            #2回目移行リクエスト
            tweets = client.search_recent_tweets(query = QUERY, tweet_fields = ["public_metrics","created_at"], max_results = MAX_RESULTS, start_time = start_time, end_time = end_time, next_token=next_token)

        tweets_data = tweets.data
        if tweets_data != None:
            for tweet in tweets_data:
                mc.make(tweet)
        else:
            print("該当がありませんでした")

        try:
            next_token = tweets.meta['next_token']
            # print("next_token: " + next_token)
        except KeyError:
            #next_tokenが取得できない（最後のリクエスト）の場合はループ終了
            print(i)
            print("最後のページに到達しました")
            break

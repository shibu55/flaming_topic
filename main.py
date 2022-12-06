from tweets import generate_csv
from analysys import search_topic
import datetime


def main():
    now = datetime.datetime.now()
    
    word = input("Tweet収集に用いるキーワードを入力: ")
    from_date = input("何日前から(1~6): ")
    to_date = input("何日前まで(0~5): ")
    start_time = now  - datetime.timedelta(days = int(from_date)) - datetime.timedelta(minutes = 1)
    end_time = now  - datetime.timedelta(days = int(to_date)) - datetime.timedelta(minutes = 1)
    file_name = 'tweets_{0}_{1}-{2}.csv'.format(word,start_time.strftime('%m-%d_%H-%M'),end_time.strftime('%m-%d_%H-%M'))

    start_time = start_time - datetime.timedelta(hours = 9)
    end_time = end_time - datetime.timedelta(hours = 9) 

    generate_csv(word, file_name, start_time, end_time)
    word = input("検索するキーワードを入力： ")
    target_file = './data/'+file_name
    search_topic(word, target_file)
    
if __name__ == "__main__":
    main()
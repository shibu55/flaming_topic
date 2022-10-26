from tweets import generate_csv
from analysys import search_topic
import datetime


def main():
    now = datetime.datetime.now()
    word = input("Tweet収集に用いるキーワードを入力: ")
    file_name = 'tweets_{0}_{1}.csv'.format(word,now.strftime('%Y-%m-%d_%H-%M'))

    generate_csv(word, file_name)
    word = input("検索するキーワードを入力： ")
    target_file = './data/'+file_name
    search_topic(word, target_file)
    
if __name__ == "__main__":
    main()
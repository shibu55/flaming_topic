from gensim.models import word2vec
import sys
import logging
import MeCab
import csv
import re

def extract_text_from_csv(file_name):
    text_list = [] 
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        for row in reader:
            # いいねorリツイートがあるツイートのみ解析
            if int(row[3]) or int(row[4]):
                text_list.append(row[0]) #取得したい列番号を指定（0始まり）
            # 無差別解析
            # text_list.append(row[0]) #取得したい列番号を指定（0始まり）

    # 先頭行(ヘッダー)を削除しておく
    # del text_list[0]

    result = ''
    for text in text_list:
        text = re.sub('^RT @[0-9a-zA-Z_]{1,15}: ', '', text)
        text = re.sub('^@[0-9a-zA-Z_]{1,15} ', '', text)
        # 英数字の削除
        text = re.sub('[a-zA-Z0-9_]','',text)
        # 記号の削除
        text = re.sub('[!-/:-@[-`{-~]','',text)
        result += text
        result += '\n'

    f = open('./data/text.txt', 'w')
    f.writelines(result)
    f.close()



def wakati():
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    tagger = MeCab.Tagger('-Owakati')

    fi = open('./data/text.txt', 'r')
    fo = open('./data/wakati.txt', 'w')

    line = fi.readline()
    while line:
        result = tagger.parse(line)
        fo.write(result) # skip first \s
        line = fi.readline()

    fi.close()
    fo.close()


def search_topic(word, file_name):
    extract_text_from_csv(file_name)
    wakati()

    sentences = word2vec.LineSentence('./data/wakati.txt')
    sg=1
    vector_size=100
    min_count=10
    window=10
    model = word2vec.Word2Vec(sentences, sg=sg, vector_size=vector_size, min_count=min_count, window=window)

    print('sg = %d, vector_size = %d, min_count = %d, window = %d' % (sg, vector_size, min_count, window))
    print('(word, similarity)')

    for i in model.wv.most_similar(word):
        print(i)

def main():
    args = sys.argv
    file_name = args[1]

    word = input("検索するキーワードを入力： ")
    search_topic(word, file_name)

if __name__ == "__main__":
    main()
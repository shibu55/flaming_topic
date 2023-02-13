# coding:utf-8
from gensim.models import word2vec
import sys
import MeCab
import collections
import csv
import re
import math
import requests
from bs4 import BeautifulSoup

def extract_text_from_csv(file_name):
    text_list = []
    is_metrics_filtering = True
    
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)

        for row in reader:
            if is_metrics_filtering:
                # いいねorリツイートがあるツイートのみ解析
                if not(int(row[3]) or int(row[4])):
                    row[0] = ''
            # 診断メーカーと炎上万博は予測する炎上と関連がないため排除
            if '#shindanmaker' in row[0]:
                row[0] = ''
            if '万博' in row[0]:
                row[0] = ''
            text_list.append(row[0])

    result = ''
    for text in text_list:
        text = re.sub('^RT @[0-9a-zA-Z_]{1,15}: ', '', text)
        text = re.sub('^@[0-9a-zA-Z_]{1,15} ', '', text)
        # 英数字の削除
        text = re.sub('[a-zA-Zａ-ｚＡ-Ｚ0-9_]','',text)
        # 記号の削除
        text = re.sub('[（）「」!-/:-@[-`{-~]','',text)
        result += text
        result += '\n'

    f = open('./data/text.txt', 'w')
    f.writelines(result)
    f.close()

def wakati():
    # 分かち書き用
    tagger = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd -Owakati')
    # 品詞取得用
    chasen = MeCab.Tagger ('-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd -Ochasen')

    fi = open('./data/text.txt', 'r')
    fo = open('./data/wakati.txt', 'w')

    line = fi.readline()
    words = []
    while line:
        result = tagger.parse(line)
        fo.write(result)
        res = chasen.parse(line)
        res = res.splitlines()
        for r in res:
            word_info = r.split()
            # EOFで処理が止まることを避けるため
            if len(word_info)>3:
                # 頻度計算のため名詞のみ取り出し
                if (word_info[3].startswith("名詞")) and (len(word_info[0])>1):
                    # stopwordsの設定
                    if not(word_info[0] in ["炎上状態", "仕事", "感じ", "記事", "最近", "ネタ", "tweet", "炎上商法", "日本", "界隈", "ニュース", "ファン", "覚悟", "案件", "なん", "好き", "お願い", "今年", "来年", "去年", "問題", "炎上", "発言", "万博", "ツイート", "もの","これ","ため","それ","ところ","よう","炎上","動画","商法","こと","質問","箱","人","さん","そう","みたい","もの","ちゃん","さん","やつ","ところ","たち","くん","あれ","みんな","自分"]):
                        words.append(word_info[0])
        line = fi.readline()
    # print('上位頻出単語（全体）')
    c = collections.Counter(words)
    common_words = c.most_common(30)
    # print(common_words)
    most_common_word = common_words[0][0]
    print('炎上トピック：'+most_common_word)

    fi.close()
    fo.close()
    # トピックによる絞り込み頻度検索（baseline手法）
    get_common_words(most_common_word)
    return most_common_word

def get_common_words(most_common_word):
    tagger = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd -Owakati')
    chasen = MeCab.Tagger ('-d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd -Ochasen')

    fi = open('./data/text.txt', 'r')
    line = fi.readline()
    words = []
    while line:
        result = tagger.parse(line)
        # 炎上トピックがツイートに含まれるときのみ頻度解析
        if most_common_word in result:
            res = chasen.parse(line)
            res = res.splitlines()
            for r in res:
                word_info = r.split()
                if len(word_info)>3:
                    if word_info[3].startswith("名詞") and (len(word_info[0])>1):
                        if not(word_info[0] in ["炎上状態", "仕事", "感じ", "記事", "最近", "ネタ", "tweet", "炎上商法", "日本", "界隈", "ニュース", "ファン", "覚悟", "案件", "なん", "好き", "お願い", "今年", "来年", "去年", "案件", "問題", "発言", "万博", "ツイート", "もの","これ","ため","それ","ところ","よう","炎上","動画","商法","こと","質問","箱","人","さん","そう","みたい","もの","ちゃん","さん","やつ","ところ","たち","くん","あれ","みんな","自分"]):
                            words.append(word_info[0])
        line = fi.readline()
    # print('上位頻出単語（アンド検索）')
    c = collections.Counter(words)
    common_words = c.most_common(51)
    # print(common_words)
    rank_words = []
    for word in common_words:
        rank_words.append(word[0])
    for index, item in enumerate(rank_words[1:16]):
        print(str(index+1)+': '+item)

    calculate_by_dcg(rank_words[1:16])

    fi.close()

def search_topic(file_name):
    # csvからツイート取り出し
    extract_text_from_csv(file_name)

    # 形態素解析と頻度計算
    most_common_word = wakati()

    sentences = word2vec.LineSentence('./data/wakati.txt')
    # Word2Vecのパラメータ設定
    sg=1
    vector_size=800
    min_count=8
    window=10
    model = word2vec.Word2Vec(sentences, sg=sg, vector_size=vector_size, min_count=min_count, window=window)

    print('炎上トピック：'+most_common_word)

    # トピックとなり得ない口語表現を排除
    stopwords = ['これ', 'やん', 'やろ', 'すぎる', 'すぎ', 'さん', 'そう']
    results = []
    for item in model.wv.most_similar(most_common_word, topn=30):
        # 一文字の単語はトピックとして扱わない
        if (len(item[0])>1) and not(item[0] in stopwords):
            results.extend(item)

    rank_words = []
    it = iter(results)
    for i, j in zip(it, it):
        rank_words.append(i)
        # print(i, j)

    for index, item in enumerate(rank_words[0:15]):
        print(str(index+1)+': '+item)
    calculate_by_dcg(rank_words[0:15])

def calculate_by_dcg(rank_words):
    text = input("DCG値を計算するタイトルを入力: ")
    
    # 英数字の削除
    text = re.sub('[a-zA-Z0-9０-９_]','',text)
    # 記号の削除
    text = re.sub('[!-/:-@[-`{-~]','',text)
    
    o_tagger = MeCab.Tagger('-Owakati -d /opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd')
    o_tagger_i = MeCab.Tagger('-Owakati -d /opt/homebrew/lib/mecab/dic/ipadic')

    # タイトルに対する形態素解析
    # タイトルは短いので二種類の辞書を使用
    wakati = o_tagger.parse(text)
    wakati_i = o_tagger_i.parse(text)
    w = wakati + ' ' + wakati_i
    
    # 形態素解析した結果を集合化
    text_word_set = set(w.split(' '))
    result = 0
    hit_count = 0
    hit_words = []
    # DCG値の計算
    for index, item in enumerate(rank_words):
        point = 0
        if item in text_word_set:
            hit_words.append(item)
            hit_count += 1
            point = 1/math.log2(index+2)
        result += point

    print('ヒット数: '+str(hit_count))
    print('ヒットした単語: ' + ", ".join(hit_words))
    print('DCGスコア: '+str(result))

# 本文の取得に使用（最終的に実験では使用していない）
# def get_text_in_web_site(url):
#     html=requests.get(url).text
#     soup=BeautifulSoup(html,"html.parser")
#     for script in soup(["script", "style"]):
#         script.decompose()

#     text=soup.get_text()

#     lines= [line.strip() for line in text.splitlines()]

#     text="\n".join(line for line in lines if line)
#     return text

def main():
    args = sys.argv
    file_name = args[1]

    search_topic(file_name)

if __name__ == "__main__":
    main()
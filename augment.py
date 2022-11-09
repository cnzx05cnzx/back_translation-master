import time
# import synonyms
import requests
import random
from hashlib import md5
import pkuseg
import json

f = open('stopwords/hit_stopwords.txt', encoding='utf-8')
stop_words = list()
for stop_word in f.readlines():
    stop_words.append(stop_word[:-1])


def get_trans(query, from_lang='en', to_lang='zh'):
    # Set your own appid/appkey.
    appid = '111'
    appkey = '111'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # print(result)
    return result['trans_result'][0]['dst']


# 回译
def all_trans(query):
    res_end = []
    res_begin = []
    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    lang_list = ['en', 'jp', 'fra', 'kor', 'ru']
    try:
        for temp in lang_list:
            time.sleep(random.randint(0, 1))
            res_begin.append(get_trans(query, 'zh', temp))

        for temp in zip(res_begin, lang_list):
            res_end.append(get_trans(temp[0], temp[1], 'zh'))
    except:
        return res_end
    return res_end


# 获取同义词
def get_synonyms(word):
    return synonyms.nearby(word)[0]


# 同义词替换
def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        s_words = get_synonyms(random_word)
        if len(s_words) >= 1:
            synonym = random.choice(s_words)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break

    sentence = ''.join(new_words)

    return sentence


# 同义词随机插入
def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    sentence = ''.join(new_words)
    return sentence


def add_word(new_words):
    s_words = []
    counter = 0
    while len(s_words) < 1:
        random_word = new_words[random.randint(0, len(new_words) - 1)]
        s_words = get_synonyms(random_word)
        counter += 1
        if counter >= 10:
            return
    random_synonym = random.choice(s_words)
    random_idx = random.randint(0, len(new_words) - 1)
    new_words.insert(random_idx, random_synonym)


# 随机交换
def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    sentence = ''.join(new_words)
    return sentence


def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words) - 1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words) - 1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    return new_words


# 随机删除
def random_deletion(words, p):
    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words) - 1)
        return words[rand_int]
    sentence = ''.join(new_words)
    return sentence


# 音近词替换
def sound_replacement(words, n, vocab):
    n = random.randint(n//2, n)
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        s_words = vocab[random_word] if random_word in vocab else []
        if len(s_words) >= 1:
            synonym = random.choice(s_words)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break

    sentence = ''.join(new_words)

    return sentence





if __name__ == "__main__":


    # res = all_trans('童话说雨后终会出现彩虹，却不曾说过它也会转瞬成空')
    # seg = pkuseg.pkuseg()
    temp = list('童话说雨后终会出现彩虹，却不曾说过它也会转瞬成空')
    print(temp)
    # res = synonym_replacement(temp, 2)
    # res = random_insertion(temp, 2)
    # res = random_swap(temp, 2)
    res = random_deletion(temp, 0.1)

    print(res)

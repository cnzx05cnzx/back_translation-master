from random import shuffle

import augment
import argparse
import pandas as pd
import csv
import pkuseg
import json

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=False, default='./before/B.csv', type=str, help="原始数据的输入文件目录")
ap.add_argument("--output", required=False, default='./after/B.csv', type=str, help="增强数据后的输出文件目录")
ap.add_argument("--alpha", required=False, default=0.15, type=float, help="改动数据在句中占比")
args = ap.parse_args()


# 回译增强语句
def back_trans(train_orig, output_file):
    lines = pd.read_csv(train_orig)
    writer = open(output_file, 'w', encoding='utf-8', newline="")

    #  2.基于文件对象构建csv写入对象
    csv_write = csv.writer(writer)
    csv_write.writerow(['A', 'B', 'C', 'D', 'E', 'F', 'content'])

    print("正在使用回译生成增强语句...")
    for i, line in lines.iterrows():

        sentence = line['content']
        # print(sentence)
        aug_sentences = augment.all_trans(sentence)
        for aug_sentence in aug_sentences:
            csv_write.writerow([line[0], line[1], line[2], line[3], line[4], line[5], aug_sentence])
        # 是否写入原句子
        # csv_write.writerow([line[0], line[1], line[2], line[3], line[4], line[5], sentence])
        print('finish {} sentence'.format(i))
    writer.close()
    print("已生成增强语句!")


# 简单eda增强语句
def eda(train_orig, output_file, alpha):
    lines = pd.read_csv(train_orig)
    writer = open(output_file, 'w', encoding='utf-8', newline="")

    #  2.基于文件对象构建csv写入对象
    csv_write = csv.writer(writer)
    csv_write.writerow(['A', 'B', 'C', 'D', 'E', 'F', 'content'])

    seg = pkuseg.pkuseg()

    # 同义词替换sr  插入ri  交换rs   删除rd  扩充句子数目
    augment_cnt = {
        'sr': 2,
        'ri': 2,
        'rs': 2,
        'rd': 2
    }

    print("正在使用eda生成增强语句...")
    for i, line in lines.iterrows():
        sentence = line['content']
        seg_list = seg.cut(sentence)
        seg_list = " ".join(seg_list)
        words = list(seg_list.split())
        num_words = len(words)

        # 改变词数量
        n_cnt = max(1, int(alpha * num_words))
        augmented_sentences = []

        # 同义词替换sr
        for _ in range(augment_cnt['sr']):
            a_words = augment.synonym_replacement(words, n_cnt)
            augmented_sentences.append(a_words)

        # 随机插入ri
        for _ in range(augment_cnt['ri']):
            a_words = augment.random_insertion(words, n_cnt)
            augmented_sentences.append(a_words)

        # 随机交换rs
        for _ in range(augment_cnt['rs']):
            a_words = augment.random_swap(words, n_cnt)
            augmented_sentences.append(a_words)

        # 随机删除rd,这里的参数是alpha,而不是改动词语数量
        for _ in range(augment_cnt['rd']):
            a_words = augment.random_deletion(words, alpha)
            augmented_sentences.append(a_words)

        # shuffle(augmented_sentences)

        for aug_sentence in augmented_sentences:
            csv_write.writerow([line[0], line[1], line[2], line[3], line[4], line[5], aug_sentence])

        # 是否写入原句子
        # csv_write.writerow([line[0], line[1], line[2], line[3], line[4], line[5], sentence])
        print('finish {} sentence'.format(i))
    writer.close()
    print("已生成增强语句!")


def sound_noise(train_orig, output_file, alpha=0.15):
    with open('confusion/soundConfusion.json', "r", encoding='utf-8') as f:
        sound_dict = json.load(f)

    lines = pd.read_csv(train_orig)
    writer = open(output_file, 'w', encoding='utf-8', newline="")

    #  2.基于文件对象构建csv写入对象
    csv_write = csv.writer(writer)
    csv_write.writerow(['content'])

    augment_cnt = 2

    print("正在生成噪声语句...")
    for i, line in lines.iterrows():
        sentence = line['content']
        seg_list = list(sentence)
        seg_list = " ".join(seg_list)
        words = list(seg_list.split())
        num_words = len(words)

        # 改变词数量
        n_cnt = max(1, int(alpha * num_words))
        augmented_sentences = []

        # 同义词替换sr
        for _ in range(augment_cnt):
            a_words = augment.sound_replacement(words, n_cnt, sound_dict)
            augmented_sentences.append(a_words)

        for aug_sentence in augmented_sentences:
            csv_write.writerow([aug_sentence])

        # 是否写入原句子
        # csv_write.writerow([line[0], line[1], line[2], line[3], line[4], line[5], sentence])
        print('finish {} sentence'.format(i))
    writer.close()
    print("已生成基于声音的噪声语句!")


if __name__ == "__main__":
    # back_trans(args.input, args.output)
    # eda(args.input, args.output, args.alpha)

    sound_noise(args.input, args.output, args.alpha)

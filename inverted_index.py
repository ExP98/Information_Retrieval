from bs4 import BeautifulSoup           # parse html pages
import sys                              # getsizeof
import uuid                             # to create unique file names
import glob                             # to get the family of path names
import os                               # to create dir
import shutil                           # to delete dir
from text_processing import stemming
from tfidf import tfidf_index
from collections import OrderedDict


def process_docs(block_size, index_file):
    files = glob.glob('data/*.sgm')

    block_file_names = []
    tokens = []
    doc_id = 0
    doc_dict = dict()

    for file in files:
        soup = BeautifulSoup(open(file), 'html.parser')
        documents = soup.find_all('reuters')

        for doc in documents:
            doc_len = 0
            if doc.body is not None and doc.body.text is not None:
                text = doc.body.text

                if (sys.getsizeof(tokens) / 1024) < block_size:
                    new_tokens = [(t, doc_id) for t in stemming(text)]
                    doc_len += len(new_tokens)
                    tokens += new_tokens
                else:
                    block_file_names += spimi_index(tokens)
                    tokens = [(t, doc_id) for t in stemming(text)]
                    doc_len += len(tokens)

            doc_dict[doc_id] = doc_len
            doc_id += 1

    block_file_names += spimi_index(tokens)
    merge(block_file_names, index_file)
    save_doc_stats(doc_dict)
    tfidf_index(flag_fast=True)
    print("INDEX was built", index_file)


def save_doc_stats(doc_d):
    print('doc_d size ', sys.getsizeof(doc_d) / 1024 / 1024, 'MB')
    with open("index/doc_stats.bin", "w") as wf:
        wf.write(str(len(doc_d)) + '\n')
        for k in doc_d.keys():
            wf.write(f"{k} | {doc_d[k]}\n")


def spimi_index(tokens):
    index_dict = dict()
    for term, doc_id in tokens:
        if term not in index_dict.keys():
            index_dict[term] = {doc_id: 1}
        else:
            if doc_id not in index_dict[term].keys():
                index_dict[term][doc_id] = 1
            else:
                index_dict[term][doc_id] += 1
    index_dict = OrderedDict(sorted(index_dict.items()))

    print('Block, size: ', sys.getsizeof(index_dict) / 1024 / 1024, ' MB; len: ', len(index_dict))
    return [write_block_to_disk(index_dict)]


def write_block_to_disk(index_dict):
    with open("temp/" + str(uuid.uuid4()) + ".bin", "w") as wf:
        for k in index_dict.keys():
            wf.write(f"{k} | {index_dict[k]}\n")
    return wf.name


def get_next_line(handler):
    line = handler.readline()
    if not line:
        return None, []
    line = line.split(' | ')
    term = line[0]

    item_list_str = [x.split(':') for x in line[1][1:-2].split(',')]
    item_list = [(int(it[0]), int(it[1])) for it in item_list_str]
    dc = dict()
    for it1, it2 in item_list:
        dc[it1] = it2
    return term, dc


def merge_two_files(file_name1, file_name2, res='-1'):
    f1 = open(file_name1, 'r')
    f2 = open(file_name2, 'r')
    if res == '-1':
        file_name_res = "temp/" + str(uuid.uuid4())
    else:
        file_name_res = res
    f_res = open(file_name_res, 'w')

    t1, d1 = get_next_line(f1)
    t2, d2 = get_next_line(f2)

    while (t1 is not None) & (t2 is not None):
        if t1 == t2:
            for k in d2.keys():
                if k not in d1.keys():
                    d1[k] = d2[k]
                else:
                    d1[k] += d2[k]

            f_res.write(f"{t1} | {d1}\n")
            t1, d1 = get_next_line(f1)
            t2, d2 = get_next_line(f2)
        elif t1 < t2:
            f_res.write(f"{t1} | {d1}\n")
            t1, d1 = get_next_line(f1)
        elif t1 > t2:
            f_res.write(f"{t2} | {d2}\n")
            t2, d2 = get_next_line(f2)
    if t1 is None:
        while t2 is not None:
            f_res.write(f"{t2} | {d2}\n")
            t2, d2 = get_next_line(f2)
    if t2 is None:
        while t1 is not None:
            f_res.write(f"{t1} | {d1}\n")
            t1, d1 = get_next_line(f1)

    f1.close()
    f2.close()
    f_res.close()
    return file_name_res


def merge(filenames_list, index_file):
    stack = []
    for fn in filenames_list:
        stack.append(fn)

    f1 = stack.pop()
    while stack:
        f2 = stack.pop()
        if stack:
            f1 = merge_two_files(f1, f2)
        else:
            f1 = merge_two_files(f1, f2, res=index_file)
    shutil.rmtree('temp/')
    os.mkdir('temp/')


def get_posting_by_term(query_term, index_file='index/tfidf_index.out'):
    pos = set()
    with open(index_file, 'r') as ind_f:
        for line in ind_f:
            line_list = line.split(' | ')
            if line_list[0] == query_term:
                item_list_str = [x.split(':') for x in line_list[1][1:-2].split(',')]
                pos = set([int(it[0]) for it in item_list_str])
    return pos


def get_doc_ids(index_file='index/tfidf_index.out'):
    pos = set()
    with open(index_file, 'r') as ind_f:
        for line in ind_f:
            line_list = line.split(' | ')
            item_list_str = [x.split(':') for x in line_list[1][1:-2].split(',')]
            pos |= set([int(it[0]) for it in item_list_str])
    return pos

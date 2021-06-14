from bs4 import BeautifulSoup
import pickle
import sys
import uuid
import glob
import os
import shutil
from text_processing import stemming
from collections import OrderedDict


def process_docs(block_size, index_file):
    files = glob.glob('short_data/*.sgm')

    block_file_names = []
    tokens = []
    doc_id = 0

    for file in files:
        soup = BeautifulSoup(open(file), 'html.parser')
        documents = soup.find_all('reuters')

        for doc in documents:
            if doc.body is not None and doc.body.text is not None:
                text = doc.body.text

                if (sys.getsizeof(tokens) / 1024) < block_size:
                    tokens += [(t, doc_id) for t in stemming(text)]
                else:
                    block_file_names += spimi_index(tokens)
                    tokens = []
                doc_id += 1
    block_file_names += spimi_index(tokens)
    tokens = []
    print(block_file_names)
    merge(block_file_names, index_file)
    print("END of process_docs")


def spimi_index(tokens):
    index_dict = dict()
    for term, doc_id in tokens:
        if term not in index_dict.keys():
            index_dict[term] = {doc_id}
        else:
            index_dict[term].add(doc_id)
    index_dict = OrderedDict(sorted(index_dict.items()))

    print('getsizeof, MB', sys.getsizeof(index_dict) / 1024 / 1024)
    print(len(index_dict))
    return [write_block_to_disk(index_dict)]


def write_block_to_disk(index_dict):
    with open("temp/" + str(uuid.uuid4()) + ".bin", "w") as wf:
        for k in index_dict.keys():
            wf.write(f"{k}: {index_dict[k]}\n")
    return wf.name


def get_next_line(handler):
    line = handler.readline()
    if not line:
        return None, []
    line = line.split(':')
    term = line[0]
    id_list = [int(x) for x in line[1][2:-2].split(',')]
    return term, id_list


def merge_two_files(file_name1, file_name2, res='-1'):
    f1 = open(file_name1, 'r')
    f2 = open(file_name2, 'r')
    if res == '-1':
        file_name_res = "temp/" + str(uuid.uuid4())
    else:
        file_name_res = res
    f_res = open(file_name_res, 'w')

    t1, l1 = get_next_line(f1)
    t2, l2 = get_next_line(f2)

    while (t1 is not None) & (t2 is not None):
        if t1 == t2:
            f_res.write(f"{t1}: {set(l1) | set(l2)}\n")
            t1, l1 = get_next_line(f1)
            t2, l2 = get_next_line(f2)
        elif t1 < t2:
            f_res.write(f"{t1}: {set(l1)}\n")
            t1, l1 = get_next_line(f1)
        elif t1 > t2:
            f_res.write(f"{t2}: {set(l2)}\n")
            t2, l2 = get_next_line(f2)
    if t1 is None:
        while t2 is not None:
            f_res.write(f"{t2}: {set(l2)}\n")
            t2, l2 = get_next_line(f2)
    if t2 is None:
        while t1 is not None:
            f_res.write(f"{t1}: {set(l1)}\n")
            t1, l1 = get_next_line(f1)

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


def get_inverted_index(index_file):
    with open(index_file, 'rb') as load_file:
        inverted_index = pickle.load(load_file, encoding='latin1')
    load_file.close()
    return dict(inverted_index)


# def print_info():
#     files = ["index/index_stemming.pkl"]
#     for file_name in files:
#         inverted_index = get_inverted_index(file_name)
#         count = sum(len(post) for post in inverted_index.values())
#
#         with open("index/collection_stats.pkl", 'rb') as stats_files:
#             n, doc_length_dict, avg_doc_length = pickle.load(stats_files)
#         stats_files.close()
#
#         print("Stats for " + file_name)
#         print("Number of distinct terms: " + str(len(inverted_index)))
#         print("Number of tokens: " + str(count))
#         print("Number of documents processed (including empty): " + str(n))
#         print("Average document length: " + str(avg_doc_length) + " words")


process_docs(2**10, 'index/index.out')
# print_info()

from math import log
import sys


def get_doc_len_by_id(doc_id, stats_file='index/doc_stats.bin'):
    num = None
    with open(stats_file, 'r') as f:
        next(f)
        for line in f:
            line_list = line.split(' | ')
            if int(line_list[0]) == doc_id:
                num = int(line_list[1])
    return num


def get_docs_count(stats_file='index/doc_stats.bin'):
    c = -1
    with open(stats_file, 'r') as f:
        c = f.readline()
    return int(c)


def get_docs_len(stats_file='index/doc_stats.bin'):
    d = dict()
    with open(stats_file, 'r') as f:
        next(f)
        for _line in f:
            line_list = _line.split(' | ')
            d[int(line_list[0])] = int(line_list[1])
    return d


def tfidf_index(ind_file='index/index.out',
                new_ind_file='index/tfidf_index.out',
                stats_file='index/doc_stats.bin',
                flag_fast=False):
    doc_count = get_docs_count(stats_file)

    if flag_fast:
        doc_lengths = get_docs_len(stats_file)
        print(sys.getsizeof(doc_lengths) / 1024 / 1024, 'MB')

    f_newind = open(new_ind_file, 'w')
    counter = 0

    with open(ind_file, 'r') as f_ind:
        for line in f_ind:
            if counter % 1000 == 0:
                print(counter)
            counter += 1

            doc_line = line.split(' | ')
            term = doc_line[0]

            item_list_str = [x.split(':') for x in doc_line[1][1:-2].split(',')]
            item_list = [(int(it[0]), int(it[1])) for it in item_list_str]

            temp_dict = dict()
            for doc_id, nt in item_list:
                if flag_fast:
                    d_len = doc_lengths[doc_id]
                else:
                    d_len = get_doc_len_by_id(doc_id, stats_file)

                tf = nt / d_len
                idf = log(doc_count / len(item_list))
                temp_dict[doc_id] = round(tf * idf, 5)
            f_newind.write(f"{term} | {temp_dict}\n")
    f_newind.close()
    print("TF-IDF index was built!")


# tfidf_index(ind_file='index/short_index.out', new_ind_file='index/tfidf_short_index.out', flag_fast=True)
# print(get_docs_count())
# print(get_doc_len_by_id(2))

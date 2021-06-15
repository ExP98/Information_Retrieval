from inverted_index import *
from text_processing import *

index_file = 'index/tfidf_index.out'


def get_ind(lst, elem):
    if lst.__contains__(elem):
        ind = lst.index(elem)
    else:
        ind = None
    return ind


def srep(_str):
    _str = _str.replace(" or ", " OR ")
    _str = _str.replace(' | ', ' OR ')
    _str = _str.replace(' and ', ' AND ')
    _str = _str.replace(' & ', ' AND ')
    _str = _str.replace(' not ', ' NOT ')
    _str = _str.replace('not ', ' NOT ')
    _str = _str.replace('NOT ', ' NOT ')
    _str = _str.replace(' ~ ', ' NOT ')
    _str = _str.replace(' ~', ' NOT ')
    _str = _str.replace('~', ' NOT ')
    return _str


def show_best_matches(num, term_list, doc_id_set, index_file='index/tfidf_index.out'):
    doc_d = dict()
    with open(index_file, 'r') as ind_f:
        for line in ind_f:
            line_list = line.split(' | ')
            if line_list[0] in term_list:
                item_list_str = [x.split(':') for x in line_list[1][1:-2].split(',')]
                pos = [(int(it[0]), float(it[1])) for it in item_list_str]
                for doc_id, tfidf in pos:
                    if doc_id in doc_id_set:
                        if doc_id not in doc_d.keys():
                            doc_d[doc_id] = tfidf
                        else:
                            doc_d[doc_id] += tfidf
    res_list = sorted(doc_d.items(), key=lambda item: item[1], reverse=True)
    if len(res_list) > num:
        res_list = res_list[:num]
    return res_list


def parsing_query():
    doc_id_set = get_doc_ids()
    oper = ["AND", "NOT", "OR"]
    print("\nTo exit write exit()\nPossible operators: AND, and, &; OR, or, |; NOT, not, ~\nNO brackets!")
    print("Example: health OR aid AND not care")
    print("Example: ~Moscow | Berlin & Rome")

    while True:
        query_string = input("\nQuery: ")
        if query_string == "exit()":
            sys.exit()

        query_string = srep(query_string)
        q_list = query_string.split()
        print(q_list)
        q_list_not_oper = []
        for i, elem in enumerate(q_list):
            if elem not in oper:
                q_list_not_oper.append(elem)
                try:
                    q = word_stemming(elem)
                    res = get_posting_by_term(q)
                    if len(res) > 0:
                        q_list[i] = res
                    else:
                        print(q, 'is not in index')
                        parsing_query()
                except Exception:
                    print('Exception')
                    parsing_query()

        ind = get_ind(q_list, "NOT")
        # to avoid while 0 (because ind of 'NOT' might be 0th)
        while ind is not None:
            tmp = doc_id_set - set(q_list[ind + 1])
            q_list.pop(ind)
            q_list[ind] = tmp
            ind = get_ind(q_list, "NOT")

        ind = get_ind(q_list, "AND")
        while ind:
            tmp = set(q_list[ind - 1]) & set(q_list[ind + 1])
            q_list.pop(ind)
            q_list.pop(ind)
            q_list[ind - 1] = tmp
            ind = get_ind(q_list, "AND")

        ind = get_ind(q_list, "OR")
        while ind:
            tmp = set(q_list[ind - 1]) | set(q_list[ind + 1])
            q_list.pop(ind)
            q_list.pop(ind)
            q_list[ind - 1] = tmp
            ind = get_ind(q_list, "OR")
        print('Count of docs: ', len(q_list[0]))
        num = 5
        print('Best ', num, ' by sum of tf-idf: ', show_best_matches(num, q_list_not_oper, q_list[0]))
        # print('doc IDs: ', q_list[0])


# parsing_query()


# single_word_query()
# multiple_and_word_query()           # for example (without quotes): "health care aids"
# multiple_or_word_query()
# not_word_query()

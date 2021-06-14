from inverted_index import *
from text_processing import *

index_file = 'index/index.out'


def single_word_query():
    while True:
        query = input("\nTo exit write exit()\nEnter one word as a query: ")
        if query == "exit()":
            break
        if len(query.split()) > 1:
            print("This is not a single word")
            break
        else:
            query = word_stemming(query)
            res = get_posting_by_term(query)
            if len(res) > 0:
                print('posting list', res)
                print('doc IDs:', res)
                print('count of docs', len(res))
            else:
                print('Selected word is not indexed')


def multiple_and_word_query():
    print("\nTo exit write exit()")
    while True:
        query = input("\nAND query (without AND, list the words separated by spaces): ")
        if query == "exit()":
            break
        terms = [word_stemming(w) for w in query.split()]
        matches = set()
        for term in terms:
            res = get_posting_by_term(term)

            if not matches:
                matches = res
            else:
                matches &= res
        if len(matches) > 0:
            print('count of docs:', len(matches))
            print('doc IDs: ', matches)
        else:
            print('Nothing was found ')


def multiple_or_word_query():
    print("\nTo exit write exit()")
    while True:
        query = input("\nOR query (without OR, list the words separated by spaces): ")
        if query == "exit()":
            break
        terms = [word_stemming(w) for w in query.split()]
        matches = set()
        for term in terms:
            res = get_posting_by_term(term)
            matches |= res
        if len(matches) > 0:
            print('count of docs:', len(matches))
            print('doc IDs: ', matches)
        else:
            print('Nothing was found ')


def not_word_query():
    doc_id_set = get_doc_ids()
    print("\nTo exit write exit()")
    while True:
        query = input("\nNOT query (without NOT, list the words separated by spaces): ")
        if query == "exit()":
            break
        if len(query.split()) > 1:
            print("This is not a single word")
            break
        else:
            query = word_stemming(query)
            res = get_posting_by_term(query)
            diff_id = doc_id_set - res
            print('len: all, res, &, diff:', len(doc_id_set), len(res), len(doc_id_set & res), len(diff_id))

            print('count of docs:', len(diff_id))
            # print('doc IDs: ', diff_id)


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


def parsing_query():
    doc_id_set = get_doc_ids()
    oper = ["AND", "NOT", "OR"]
    print("\nTo exit write exit()\nPossible operators: AND, and, &; OR, or, |; NOT, not, ~\nNO brackets!")
    print("Example: health OR aid AND not care")
    print("Example: ~Moscow | Berlin & Rome")

    while True:
        query_string = input("\nQuery: ")
        if query_string == "exit()":
            break

        query_string = srep(query_string)
        q_list = query_string.split()
        print(q_list)
        for i, elem in enumerate(q_list):
            if elem not in oper:
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
            print(q_list[ind + 1])
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
        # print('doc IDs: ', q_list[0])


# parsing_query()


# single_word_query()
# multiple_and_word_query()           # for example (without quotes): "health care aids"
# multiple_or_word_query()
# not_word_query()

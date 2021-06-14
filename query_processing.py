from inverted_index import *
from text_processing import *

index_file = "index/index_stemming.pkl"


def single_word_query():
    inverted_index = get_inverted_index(index_file)
    while True:
        query = input("\nTo exit write exit()\nEnter one word as a query: ")
        if query == "exit()":
            break
        if len(query.split()) > 1:
            print("This is not a single word")
            break
        else:
            query = word_stemming(query)
            if query in inverted_index.keys():
                print('inv ind', inverted_index[query])
                doc_ids_set = set([x[0] for x in inverted_index[query]])
                doc_count = len(doc_ids_set)
                print('doc IDs:', doc_ids_set)
                print('count of docs', doc_count)
            else:
                print('Selected word is not indexed')


def multiple_and_word_query():
    inverted_index = get_inverted_index(index_file)
    while True:
        query = input("\nTo exit write exit()\n"
                      "AND query (without AND, list the words separated by spaces): ")
        if query == "exit()":
            break
        terms = [word_stemming(w) for w in query.split()]
        matches = set()
        for term in terms:
            if term in inverted_index.keys():
                id_to_add = set([x[0] for x in inverted_index[term]])
                if not matches:
                    matches = id_to_add
                else:
                    matches &= id_to_add
        print('count of docs:', len(matches))
        print('doc IDs: ', matches)


def multiple_or_word_query():
    inverted_index = get_inverted_index(index_file)
    while True:
        query = input("\nTo exit write exit()"
                      "\nOR query (without OR, list the words separated by spaces): ")
        if query == "exit()":
            break
        terms = [word_stemming(w) for w in query.split()]
        matches = set()
        for term in terms:
            if term in inverted_index.keys():
                matches |= set([x[0] for x in inverted_index[term]])

        print('count of docs:', len(matches))
        print('doc IDs: ', matches)


def not_word_query():
    inverted_index = get_inverted_index(index_file)

    with open('index/all_articles.pkl', 'rb') as load_file:
        arts = pickle.load(load_file, encoding='latin1')
    load_file.close()
    all_doc_id_set = set(arts.keys())

    while True:
        query = input("\nTo exit write exit()"
                      "\nNOT query (without NOT, list the words separated by spaces): ")
        if query == "exit()":
            break
        if len(query.split()) > 1:
            print("This is not a single word")
            break
        else:
            query = word_stemming(query)
            if query in inverted_index.keys():
                query_ids = set([x[0] for x in inverted_index[query]])
                print(len(all_doc_id_set), len(query_ids))
                diff_id = all_doc_id_set - query_ids
                print(len(all_doc_id_set & query_ids))
            else:
                diff_id = set()
            print('count of docs:', len(diff_id))
            # print('doc IDs: ', diff_id)


def get_ind(l, elem):
    if l.__contains__(elem):
        ind = l.index(elem)
    else:
        ind = None
    return ind


def parsing_query():
    inverted_index = get_inverted_index(index_file)

    with open('index/all_articles.pkl', 'rb') as load_file:
        arts = pickle.load(load_file, encoding='latin1')
    load_file.close()
    all_doc_id_set = set(arts.keys())

    oper = ["AND", "NOT", "OR"]

    while True:
        query_string = input("\nTo exit write exit()\nQuery: ")
        if query_string == "exit()":
            break

        q_list = query_string.split()
        for i, elem in enumerate(q_list):
            if elem not in oper:
                q = word_stemming(elem)
                if q in inverted_index.keys():
                    q_list[i] = set(x[0] for x in inverted_index[q])
                else:
                    print(q, 'is not in index')
                    parsing_query()

        ind = get_ind(q_list, "NOT")
        while ind:
            tmp = all_doc_id_set - set(q_list[ind + 1])
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
        print('doc IDs: ', q_list[0])


# parsing_query('Moscow OR Berlin OR Rome')
# parsing_query('health AND care AND aids')
# parsing_query('health AND care OR aids')


parsing_query()


# single_word_query()
# multiple_and_word_query()           # for example (without quotes): "health care aids"
# multiple_or_word_query()
# not_word_query()

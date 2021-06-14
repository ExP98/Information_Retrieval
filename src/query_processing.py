from inverted_index import *
from text_processing import *

index_file = "../index/index_stemming.pkl"


def single_word_query():
    inverted_index = get_inverted_index(index_file)
    while True:
        query = input("Enter one word as a query: ")
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
        query = input("\nAND query (without AND, list the words separated by spaces): ")
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
        query = input("\nOR query (without OR, list the words separated by spaces): ")
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

    with open('../index/all_articles.pkl', 'rb') as load_file:
        arts = pickle.load(load_file, encoding='latin1')
    load_file.close()
    all_doc_id_set = set(arts.keys())

    while True:
        query = input("\nNOT query (without NOT, list the words separated by spaces): ")
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


# single_word_query()
# multiple_and_word_query()           # for example (without quotes): "health care aids"
# multiple_or_word_query()
not_word_query()
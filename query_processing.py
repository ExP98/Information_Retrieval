from inverted_index import *
from text_processing import *

index_file = "index/index_stemming.pkl"


def single_word_query():
    inverted_index = get_inverted_index(index_file)
    while True:
        query = input("Enter a single keyword search query: ")
        if len(query.split()) > 1:
            print("This is not a single word")
            break
        else:
            query = word_stemming(query)
            if query in inverted_index.keys():
                doc_ids_set = set([x[0] for x in inverted_index[query]])
                doc_count = len(doc_ids_set)
                print('doc IDs:', doc_ids_set)
                print('count of docs', doc_count)

                # with open("all_articles", 'rb') as all_articles:
                #     d = pickle.load(all_articles)
                # all_articles.close()

                # if doc_count > 5:
                #     for _id in list(doc_ids_set)[:5]:
                #         print('\n!!!\n', _id, '\n', d[_id])
            else:
                print('keyword is not in index')


def multiple_and_word_query():
    inverted_index = get_inverted_index(index_file)
    while True:
        query = input("Enter a multiple AND search query: ")
        if query == "exit()":
            break
        terms = [word_stemming(w) for w in query.split()]
        matches = set()
        print('TERMS: ', terms, len(terms))
        for term in terms:
            if term in inverted_index.keys():
                id_to_add = set([x[0] for x in inverted_index[term]])
                if not matches:
                    matches = id_to_add
                else:
                    matches = matches & id_to_add

        print('count of docs:', len(matches))
        print('doc IDs: ', matches)


def multiple_or_word_query():
    inverted_index = get_inverted_index(index_file)
    while True:
        query = input("Enter a multiple OR search query: ")
        if query == "exit()":
            break
        terms = [word_stemming(w) for w in query.split()]
        matches = set()
        for term in terms:
            if term in inverted_index.keys():
                matches |= set([_[0] for _ in inverted_index[term]])

        print('count of docs:', len(matches))
        print('doc IDs: ', matches)

        # with open("all_articles", 'rb') as all_articles:
        #     d = pickle.load(all_articles)
        # all_articles.close()
        #
        # if len(matches) > 5:
        #     for i in list(matches)[:5]:
        #         print('\nID: ', i, '\n', d[i])


# single_word_query()
multiple_and_word_query()
# multiple_or_word_query()

from src.inverted_index import get_inverted_index
import pickle

# inverted_index = get_inverted_index('index/index_stemming.pkl')
#
# all_doc_id_set = set()
#
# for k in inverted_index.keys():
#     all_doc_id_set |= set(inverted_index[k][0])
#
# print(len(all_doc_id_set))
# print(all_doc_id_set)


with open('index/all_articles.pkl', 'rb') as load_file:
    arts = pickle.load(load_file, encoding='latin1')
load_file.close()

all_ids = set(arts.keys())

print(all_ids)
print(len(all_ids))



def print_info():
    files = ["index/index_stemming.pkl"]
    for file_name in files:
        inverted_index = get_inverted_index(file_name)
        count = sum(len(post) for post in inverted_index.values())

        with open("index/collection_stats.pkl", 'rb') as stats_files:
            n, doc_length_dict, avg_doc_length = pickle.load(stats_files)
        stats_files.close()

        print("Stats for " + file_name)
        print("Number of distinct terms: " + str(len(inverted_index)))
        print("Number of tokens: " + str(count))
        print("Number of documents processed (including empty): " + str(n))
        print("Average document length: " + str(avg_doc_length) + " words")


# print_info()

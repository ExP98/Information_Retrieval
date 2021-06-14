from bs4 import BeautifulSoup
import pickle
import sys
import uuid
import glob
import os
from text_processing import stemming


def process_docs(block_size, index_file):
    files = glob.glob('short_data/*.sgm')
    n = 0
    block_file_names = []
    doc_length_dict = {}
    for file in files:
        soup = BeautifulSoup(open(file), 'html.parser')
        documents = soup.find_all('reuters')
        n += len(documents)
        tokens = []

        for doc in documents:
            if doc.body is not None and doc.body.text is not None:
                text = doc.body.text
                doc_id = int(doc['newid'].encode("utf-8"))
                doc_length_dict[doc_id] = len(text.split())
                tokens = tokens + stemming(text, doc_id)
        block_file_names = block_file_names + spimi_index(tokens, block_size)
    print('file names: ', block_file_names)
    collection_statistics(n, doc_length_dict)
    merge_blocks(block_file_names, index_file)
    print("END of process_docs")


def spimi_index(tokens, block_size):
    index_dict = {}
    output_files = []
    for token in tokens:
        if (sys.getsizeof(index_dict) / 1024) < block_size:
            index_dict = add_to_dictionary(token, index_dict)
        else:
            print('getsizeof', sys.getsizeof(index_dict) / 1024 / 1024)
            output_files = output_files + [write_block_to_disk(index_dict)]
            index_dict.clear()
            index_dict = add_to_dictionary(token, index_dict)

    print('getsizeof', sys.getsizeof(index_dict) / 1024 / 1024)
    if index_dict.keys():
        output_files = output_files + [write_block_to_disk(index_dict)]
    return output_files


def add_to_dictionary(token, index_dict):
    if token[0] in index_dict.keys():
        if token[1][0] not in index_dict[token[0]]:
            index_dict[token[0]].append(token[1])
        else:
            index = index_dict[token[0]].index(token[1][0])
            index_dict[token[0]][index][1] += 1
    else:
        index_dict[token[0]] = [token[1]]
    return index_dict


def write_block_to_disk(index_dict):
    with open("temp/" + str(uuid.uuid4()), "wb") as output_file:
        pickle.dump(index_dict, output_file, protocol=pickle.HIGHEST_PROTOCOL)
    output_file.close()
    return output_file.name


def collection_statistics(n, doc_length_dict):
    total_docs_length = 0
    for key, value in doc_length_dict.items():
        total_docs_length += value
    avg_doc_length = total_docs_length / n
    with open("index/collection_stats.pkl", "wb") as stats_file:
        pickle.dump((n, doc_length_dict, avg_doc_length), stats_file, protocol=pickle.HIGHEST_PROTOCOL)
    stats_file.close()


def merge_blocks(block_file_names, index_file):
    for block_path in block_file_names:
        inverted_index = {}

        with open(block_path, 'rb') as block_file:
            block = pickle.load(block_file, encoding='latin1')
        block_file.close()

        if os.path.isfile(index_file):
            with open(index_file, 'rb') as output_file:
                index = pickle.load(output_file, encoding='latin1')
            output_file.close()

            for dictionary in [index, block]:
                for key, value in dictionary.items():
                    inverted_index.setdefault(key, []).extend(value)
        else:
            inverted_index = block

        with open(index_file, "wb") as output_file:
            pickle.dump(inverted_index, output_file, protocol=pickle.HIGHEST_PROTOCOL)
        output_file.close()
        os.remove(block_path)


def get_inverted_index(index_file):
    with open(index_file, 'rb') as load_file:
        inverted_index = pickle.load(load_file, encoding='latin1')
    load_file.close()
    return dict(inverted_index)


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


# process_docs(2**10, 'index/index_stemming.pkl')
# print_info()

from inverted_index import process_docs

index_file = 'index/index.out'
Kbyte_limit = 2**10
process_docs(Kbyte_limit, index_file)

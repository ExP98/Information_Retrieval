from src.inverted_index import process_docs
from src.text_processing import stemming

index_file = "index/index_stemming.pkl"
Kbyte_limit = 2**10
process_docs(Kbyte_limit, stemming, index_file)

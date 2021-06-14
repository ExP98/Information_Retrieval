import glob
import pickle
from bs4 import BeautifulSoup


files = glob.glob('../data/*.sgm')
print(files)
doc_dictionary = dict()
for file in files:
    soup = BeautifulSoup(open(file), 'html.parser')
    documents = soup.find_all('reuters')

    for doc in documents:
        if doc.body is not None and doc.body.text is not None:
            text = doc.body.text
            doc_id = int(doc['newid'].encode("utf-8"))
            doc_dictionary[doc_id] = text

with open('../index/all_articles.pkl', "wb") as output_file:
    pickle.dump(doc_dictionary, output_file, protocol=pickle.HIGHEST_PROTOCOL)
output_file.close()

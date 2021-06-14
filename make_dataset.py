import glob
from bs4 import BeautifulSoup


files = glob.glob('data/*.sgm')
doc_dictionary = dict()
for file in files:
    soup = BeautifulSoup(open(file), 'html.parser')
    documents = soup.find_all('reuters')

    for doc in documents:
        if doc.body is not None and doc.body.text is not None:
            text = doc.body.text
            doc_id = int(doc['newid'].encode("utf-8"))
            doc_dictionary[doc_id] = text

with open('index/all_articles.txt', "w") as output_file:
    for k in doc_dictionary.keys():
        output_file.write(f"ID {k}: {doc_dictionary[k]}\n")

print("All articles were written to file")

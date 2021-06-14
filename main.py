import pickle

with open("index/all_articles.pkl", 'rb') as all_articles:
    d = pickle.load(all_articles)
all_articles.close()

print(d[20477])
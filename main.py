import pickle

with open("index/collection_stats.pkl", 'rb') as all_articles:
    d = pickle.load(all_articles)
all_articles.close()

print(d)
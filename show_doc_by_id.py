import pickle


def show_doc_by_id():
    with open("index/all_articles.pkl", 'rb') as all_articles:
        d = pickle.load(all_articles)
    all_articles.close()

    print('To finish the session write exit()\nWrite docID to see the doc text')
    while True:
        query = input("docID: ")
        if query == "exit()":
            break
        if query.isdigit():
            if int(query) in d.keys():
                print(d[int(query)])
            else:
                print('doc with selected ID was not found')
        else:
            print("Got not int")


show_doc_by_id()

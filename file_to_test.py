import pickle
import sys
import re
import uuid
import collections


d = {b'fan': [(2992, 1, 0)], b'resent': [(2992, 1, 0)], b'affairs.': [(2992, 1, 0)], b'makoto': [(2992, 1, 0)],
     b'kuroda,': [(2992, 1, 0)], b'criticism,': [(2992, 1, 0)], b'businessmen.': [(2992, 1, 0)],
     b'nervous': [(2992, 1, 0)], b'walli': [(2992, 1, 0)], b'postal': [(2992, 1, 0)], b'for,': [(2992, 1, 0)],
     b'receive,': [(2992, 1, 0)], b'sure.': [(2992, 1, 0)], b'further,': [(2992, 1, 0)],
     b'singapor': [(2993, 1, 0), (2994, 1, 0)], b'activity,': [(2993, 1, 0)], b'non-bank': [(2993, 1, 0), (2993, 1, 0)],
     b"singapore'": [(2994, 1, 0)], b'(mas)': [(2994, 1, 0)], b'ma': [(2994, 1, 0)], b'bulletin': [(2994, 1, 0)],
     b'broadly-bas': [(2994, 1, 0)], b'year-on-year': [(2994, 1, 0)], b"china'": [(2995, 1, 0)],
     b'performance.': [(2995, 1, 0)], b'readjust': [(2995, 1, 0)], b'unsal': [(2995, 1, 0)],
     b'cost-effici': [(2995, 1, 0)], b'tightness.': [(2996, 1, 0)], b'full,': [(2996, 1, 0)],
     b'finland': [(2997, 1, 0)], b'ltcb': [(2997, 1, 0)], b'(nioc)': [(2998, 1, 0)], b'discounts,': [(2998, 1, 0)],
     b'nioc': [(2998, 1, 0)], b'formulas.': [(2998, 1, 0)], b'oman': [(2998, 1, 0)], b'dubai': [(2998, 1, 0)],
     b'discount,': [(2998, 1, 0), (2998, 1, 0)], b'colder': [(2998, 1, 0)], b'self-impos': [(2998, 1, 0)],
     b'futures,': [(2998, 1, 0)], b'cheating,"': [(2998, 1, 0)], b'singapore.': [(2998, 1, 0)], b'vlcc': [(2998, 1, 0)],
     b'arrangements.': [(2998, 1, 0)], b'<ici.l>': [(2999, 1, 0)], b'lister': [(2999, 1, 0), (2999, 1, 0)],
     b'l': [(2999, 1, 0)], b'messel': [(2999, 1, 0)], b'manufacturer,': [(2999, 1, 0)], b'dyer': [(2999, 1, 0)],
     b'silk': [(2999, 1, 0)], b'wool': [(2999, 1, 0)], b'fibres.': [(2999, 1, 0)], b'natwest': [(3000, 1, 0)],
     b'aaa.': [(3000, 1, 0)], b'underwriting.': [(3000, 1, 0)]}
print(len(d.keys()), sys.getsizeof(d))

d = collections.OrderedDict(sorted(d.items()))

with open("temp/" + str(uuid.uuid4()) + ".bin", "w") as wf:
    for k in d.keys():
        ids = [x[0] for x in d[k]]
        wf.write(f"{k}: {ids}\n")

with open('temp/out.bin', 'r') as fr:
    for line in fr:
        ll = line[:-1].split(':')
        key_word = ll[0]
        posting_list = [int(x) for x in ll[1][2:-1].split(',')]

# try:
#     file = open("out.bin", "wb")
#
#     try:
#         pickle.dump(book1, file)
#         pickle.dump(book2, file)
#         pickle.dump(book3, file)
#         pickle.dump(book4, file)
#     finally:
#         file.close()
#
# except FileNotFoundError:
#     print("Невозможно открыть файл")

from inverted_index import *

process_docs(2**10, 'index/short_index.out')

# d = OrderedDict()
# l = [('behavior', {1894: 1, 2553: 1}), ('behaviour', {2987: 1}), ('behind', {1866: 1, 2405: 1, 2479: 1, 2724: 1, 3010: 2, 3021: 1, 3045: 1, 3133: 1, 3219: 1, 3274: 1, 3294: 1, 3309: 1, 3326: 1, 3335: 1, 3536: 1}), ('beleagur', {2051: 1, 2077: 1}), ('beleggineng', {3453: 1}), ('belfastbas', {3246: 1}), ('belgian', {1808: 1, 1941: 2, 1964: 1, 2058: 1, 2708: 4, 2818: 3, 2852: 1, 2954: 2, 2957: 2, 2958: 2, 3153: 1, 3190: 2, 3508: 3}), ('belgium', {1941: 2, 1984: 1, 2014: 1, 2058: 1, 2116: 1, 2256: 1, 2455: 2, 2708: 2, 2943: 1}), ('belgiumluxembourg', {1945: 1}), ('belgoluxembourg', {1931: 1, 3170: 1}), ('belief', {1828: 1, 2071: 1, 2562: 1, 2812: 1, 2923: 1, 3274: 2})]
# # l = [('workforc', {8958: 1, 8973: 1}), ('workpractic', {8958: 2}), ('world', {8986: 1}), ('written', {8958: 1}), ('year', {8950: 1, 8951: 2, 8952: 2, 8958: 1, 8962: 1, 8966: 2, 8981: 1, 8982: 2, 8991: 1, 8992: 3, 8998: 2, 8999: 1}), ('yen', {8986: 1}), ('yesterday', {8956: 1, 8996: 1}), ('yet', {8986: 1}), ('york', {8983: 2}), ('zeebregt', {8958: 2})]
# for item in l:
#     d[item[0]] = item[1]
# print(d)
#
# with open("temp/" + str(uuid.uuid4()) + ".bin", "w") as wf:
#     for k in d.keys():
#         wf.write(f"{k} | {d[k]}\n")
# print(wf.name)


# file_names = ['temp/b6a918d3-9df5-4f8a-9ed6-75b19db2a1f2.bin', 'temp/c8c18ddc-f2cc-4111-a122-dcc8dfb42a3c.bin']
#
#
# def get_next_line(handler):
#     line = handler.readline()
#     if not line:
#         return None, []
#     line = line.split(' | ')
#     term = line[0]
#
#     item_list_str = [x.split(':') for x in line[1][1:-2].split(',')]
#     item_list = [(int(it[0]), int(it[1])) for it in item_list_str]
#     dc = dict()
#     for it1, it2 in item_list:
#         dc[it1] = it2
#     return term, dc
#
#
# def _merge_two_files(file_name1, file_name2, res='-1'):
#     f1 = open(file_name1, 'r')
#     f2 = open(file_name2, 'r')
#     if res == '-1':
#         file_name_res = "temp/" + str(uuid.uuid4())
#     else:
#         file_name_res = res
#     f_res = open(file_name_res, 'w')
#
#     t1, d1 = get_next_line(f1)
#     t2, d2 = get_next_line(f2)
#
#     while (t1 is not None) & (t2 is not None):
#         if t1 == t2:
#             for k in d2.keys():
#                 if k not in d1.keys():
#                     d1[k] = d2[k]
#                 else:
#                     d1[k] += d2[k]
#
#             f_res.write(f"{t1} | {d1}\n")
#             t1, d1 = get_next_line(f1)
#             t2, d2 = get_next_line(f2)
#         elif t1 < t2:
#             f_res.write(f"{t1} | {d1}\n")
#             t1, d1 = get_next_line(f1)
#         elif t1 > t2:
#             f_res.write(f"{t2} | {d2}\n")
#             t2, d2 = get_next_line(f2)
#     if t1 is None:
#         while t2 is not None:
#             f_res.write(f"{t2} | {d2}\n")
#             t2, d2 = get_next_line(f2)
#     if t2 is None:
#         while t1 is not None:
#             f_res.write(f"{t1} | {d1}\n")
#             t1, d1 = get_next_line(f1)
#
#     f1.close()
#     f2.close()
#     f_res.close()
#     return file_name_res
#
#
# # f1 = open(file_names[0], 'r')
# # f2 = open(file_names[1], 'r')
# # f_res = open('temp/res.out', 'w')
#
# # print(get_next_line(f1))
#
# _merge_two_files(file_names[0], file_names[1], 'temp/merge.out')

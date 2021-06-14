# import pickle
# import sys
# import re
# import uuid
# import collections
#
#
# # with open('temp/2ea17ebd-1637-47eb-bff0-087917131594.bin', 'r') as fr:
# #     print(sys.getsizeof(fr))
# #     for line in fr:
# #         ll = line[:-1].split(':')
# #         key_word = ll[0]
# #         posting_list = [int(x) for x in ll[1][2:-1].split(',')]
#
#
# file_names = ['temp/2ea17ebd-1637-47eb-bff0-087917131594.bin', 'temp/21e40e48-add1-4ead-b14c-9f5753a9a685.bin',
#               'temp/25e1fdc1-3220-4a88-8b12-b9400629aabb.bin', 'temp/477a168a-1a98-44a0-a460-eeba789cf9a3.bin',
#               'temp/f536d33f-ce4e-4d62-9b1d-407116d60b8d.bin']
#
#
# def get_next_line(handler):
#     line = handler.readline()
#     if not line:
#         return None, []
#     line = line.split(':')
#     term = line[0]
#     id_list = [int(x) for x in line[1][2:-2].split(',')]
#     return term, id_list
#
#
# def merge_two_files(file_name1, file_name2, res='-1'):
#     f1 = open(file_name1, 'r')
#     f2 = open(file_name2, 'r')
#     if res == '-1':
#         file_name_res = "temp/" + str(uuid.uuid4())
#     else:
#         file_name_res = res
#     f_res = open(file_name_res, 'w')
#
#     t1, l1 = get_next_line(f1)
#     t2, l2 = get_next_line(f2)
#
#     while (t1 is not None) & (t2 is not None):
#         if t1 == t2:
#             f_res.write(f"{t1}: {set(l1) | set(l2)}\n")
#             t1, l1 = get_next_line(f1)
#             t2, l2 = get_next_line(f2)
#         elif t1 < t2:
#             f_res.write(f"{t1}: {set(l1)}\n")
#             t1, l1 = get_next_line(f1)
#         elif t1 > t2:
#             f_res.write(f"{t2}: {set(l2)}\n")
#             t2, l2 = get_next_line(f2)
#     if t1 is None:
#         while t2 is not None:
#             f_res.write(f"{t2}: {set(l2)}\n")
#             t2, l2 = get_next_line(f2)
#     if t2 is None:
#         while t1 is not None:
#             f_res.write(f"{t1}: {set(l1)}\n")
#             t1, l1 = get_next_line(f1)
#
#     f1.close()
#     f2.close()
#     f_res.close()
#     return file_name_res
#
#
# def merge(filenames_list, index_file):
#     stack = []
#     for fn in filenames_list:
#         stack.append(fn)
#
#     f1 = stack.pop()
#     while stack:
#         f2 = stack.pop()
#         if stack:
#             f1 = merge_two_files(f1, f2)
#         else:
#             f1 = merge_two_files(f1, f2, res=index_file)
#     shutil.rmtree('temp/')
#     os.mkdir('temp/')
#
# merge(file_names, 'res.out')
import json
from pprint import pprint
from cla import User
user = User('eshmargunov')

# print(User(214895).id_groups())
if __name__ == '__main__':
    print(user.mutual_friend_class())
# print(user.mutual_friend_class())
# final_list = []
# print(user.id_unique_groups())
# for i in user.id_unique_groups():
#     user.groups_getById(i)
#     try:
#         for a in user.groups_getById(i)['response']:
#             json_group = {
#                 'name': a['name'],
#                 'gid': a['id'],
#                 'members_count': a['members_count']
#             }
#             final_list.append(json_group)
#     except KeyError:
#         time.sleep(1)
#
# # with open("newsafr2.json", "w", encoding='utf_8_sig') as datafile:
# #     json.dump(final_list, datafile, ensure_ascii=False)
# pprint(final_list)
# print(len(final_list))

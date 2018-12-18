import requests
import time
import sys
import json
from pprint import pprint

print('Введите токен:')  # 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
token = input()


class User:

    def __init__(self, user_id):
        self.user_id = user_id
        if str(user_id).isdigit():
            self.user_id = user_id
        else:
            params = {
                'user_ids': user_id,
                'access_token': token,
                'v': '5.92'
            }
            response = requests.get('https://api.vk.com/method/users.get', params)
            user_data = response.json()
            try:
                self.user_id = user_data['response'][0]['id']
            except KeyError:
                sys.exit('Данного пользователя не существует')

    def get_groups(self):
        params = {
            'user_id': self.user_id,
            'extended': 1,
            'fields': 'members_count',
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/groups.get',
                                params)
        print('.')
        return response.json()

    def get_friends(self):
        params = {
            'user_id': self.user_id,
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/friends.get',
                                params)
        print('.')
        return response.json()

    def groups_get_by_id(self, group_id):

        params = {
            'group_ids': group_id,
            'fields': 'members_count',
            'access_token': token,
            'v': '5.92'
        }
        response = requests.get('https://api.vk.com/method/groups.getById',
                                params)
        print('.')
        return response.json()

    def id_groups(self):
        id_groups = []
        user_friends = User(self.user_id).get_groups()
        if 'error' in user_friends and 'error_code' in user_friends['error'] and user_friends['error'][
            'error_code'] == 7:
            return 'error_code = 7'
        elif 'error' in user_friends and 'error_code' in user_friends['error'] and user_friends['error'][
            'error_code'] == 6:
            time.sleep(1)
            return 'error_code = 6'
        elif 'error' in user_friends and 'error_code' in user_friends['error'] and user_friends['error'][
            'error_code'] == 18:
            time.sleep(1)
            print('Пользователь id{} был удален или забанен'.format(self.user_id))
            return 'error_code = 18'
        elif 'error' in user_friends and 'error_code' in user_friends['error'] and user_friends['error'][
            'error_code'] == 30:
            print('Этот профиль приватный')
            sys.exit()
        else:
            for i in user_friends['response']['items']:
                id_groups.append(i['id'])
            return id_groups

    def mutual(self):
        id_groups_user = User(self.user_id).id_groups()
        friends_user = User(self.user_id).get_friends()['response']['items']
        for i in friends_user:
            friend = User(i).id_groups()
            if friend == 'error_code = 6':
                friends_user.append(i)
            elif friend == 'error_code = 7':
                print('Пользователь id{} закрыл группы'.format(i))
            else:
                id_groups_user = list(set(id_groups_user) - set(friend))
        return id_groups_user

    def id_unique_groups(self):
        final_list = []
        unique_groups = User(self.user_id).mutual()
        for a in unique_groups:
            info = User(self.user_id).groups_get_by_id(a)
            if 'error' in info:
                unique_groups.append(a)
                time.sleep(1)
            else:
                for i in info['response']:
                    if 'error' in i:
                        unique_groups.append(a)
                        time.sleep(1)
                    else:
                        json_group = {
                            'name': i['name'],
                            'gid': i['id'],
                            'members_count': i['members_count']
                        }
                        final_list.append(json_group)
        with open("newsafr2.json", "w", encoding='utf_8_sig') as datafile:
            json.dump(final_list, datafile, ensure_ascii=False, indent=4)
        pprint(final_list)

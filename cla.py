import requests
import time

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


class User:

    def __init__(self, name_user):
        self.name_user = name_user

    def name_parsing(self):
        try:
            user_id = User(self.name_user).utils_resolve_screen_name(self.name_user)['response']['object_id']
        except TypeError:
            user_id = self.name_user
        return user_id

    def utils_resolve_screen_name(self, screen_name):
        params = {
            'screen_name': screen_name,
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                                params)
        print('.')
        return response.json()

    def get_groups(self):  # группы пользователя
        params = {
            'user_id': User(self.name_user).name_parsing(),
            'extended': 1,
            'fields': 'members_count',
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/groups.get',
                                params)
        print('.')
        return response.json()

    def get_friends(self):  # друзья пользователя
        params = {
            'user_id': User(self.name_user).name_parsing(),
            'access_token': token,
            'v': '5.92'
        }

        response = requests.get('https://api.vk.com/method/friends.get',
                                params)
        print('.')
        return response.json()

    def groups_get_by_id(self, group_id):  # Инфа о сообществе

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

    def id_groups(self):  # id групп пользователя
        id_groups = []
        user_friends = User(self.name_user).get_groups()
        if 'error' in user_friends and 'error_code' in user_friends['error'] and user_friends['error'][
            'error_code'] == 7:
            print('error_code = 7')
            return 'error_code = 7'
        elif 'error' in user_friends and 'error_code' in user_friends['error'] and user_friends['error'][
            'error_code'] == 6:
            print('error_code = 6')
            return 'error_code = 6'
        else:
            for i in user_friends['response']['items']:
                id_groups.append(i['id'])
            return id_groups

    def mutual_friend_class(self):
        id_groups_user = User(self.name_user).id_groups()  # id моих групп
        print("id_groups_user", id_groups_user)  # НЕ НУЖНО
        friends_user = User(self.name_user).get_friends()['response']['items']  # id друзей
        print('friends_user', friends_user)  # НЕ НУЖНО
        for i in friends_user:
            print('i', i)  # НЕ НУЖНО
            id_groups_friend = []
            print('User(i).id_groups()', User(i).id_groups())  # НЕ НУЖНО
            if User(i).id_groups() == 'error_code = 7':
                print('123')
            if User(i).id_groups() == 'error_code = 6':
                time.sleep(2)
                friends_user.append(i)
            else:
                id_groups_friend.append(User(i).id_groups())
                # print('id_groups_friend', id_groups_friend)  # НЕ НУЖНО
                id_groups_user = list(set(id_groups_user) - set(id_groups_friend[0]))
                print('id_groups_user', id_groups_user)  # НЕ НУЖНО
                # id_groups_user = id_groups_user_1
        return id_groups_user

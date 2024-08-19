import requests
import re

class VKMethods:
    def __init__(self, logger, token=None):
        self.token = token
        self.logger = logger
    async def like_vk_post(self, url):
        self.logger.info('Лайкаю пост..')
        if not 'vk.com' in url:
            return 0
        if '-' in url:
            group = True
        else:
            group = False
        if 'wall' in url:
            type = 'post'
        elif 'video' in url:
            type = 'video'
        elif 'photo' in url:
            type = 'photo'
        elif 'audio' in url:
            type = 'audio'
        elif 'note' in url:
            type = 'note'
        elif 'market' in url:
            type = 'market'
        elif 'photo_comment' in url:
            type = 'photo_comment'
        elif 'video_comment' in url:
            type = 'video_comment'
        elif 'topic_comment' in url:
            type = 'topic_comment'
        elif 'market_comment' in url:
            type = 'market_comment'
        elif 'clip' in url:
            type = 'clip'

        url = url.replace('https://vk.com/', '').split('_')
        owner_id = re.findall('\\d+', url[0])[0]
        if group:
            owner_id = '-'+owner_id
        post_id = re.findall("\\d+", url[1])[0]
        response = requests.get(
            f'''https://api.vk.com/method/likes.add?type={type}&owner_id={owner_id}&item_id={post_id}&access_token={self.token}&v=5.131'''
            )
        self.logger.info(f'Ответ вк: {response.json()}')
        if response.json().get('response').get('likes'):
            return 1
        return 0

    async def join_vk_group(self, url):
        self.logger.info('Присоединяюсь к группе..')
        if not 'vk.com' in url:
            return 0
        group_id = url.split('/')[-1].replace('club', '')
        response = requests.get(f'https://api.vk.com/method/groups.join?group_id={group_id}&access_token={self.token}&v=5.131')
        self.logger.info(f'Ответ вк: {response.json()}')
        if response.json().get('response') == 1:
            return 1
        else:
            return 0

    async def add_vk_friend(self, url):
        self.logger.info('Добавляю в друзья')
        if not 'vk.com' in url:
            return 0
        user_id = url.split('/')[-1].replace('id', '')
        response = requests.get(f'https://api.vk.com/method/friends.add?user_id={user_id}&access_token={self.token}&v=5.131')
        self.logger.info(f'Ответ ВК: {response.json()}')
        if response.json().get('response') == 1:
            return 1
        else:
            return 0

    async def get_vk_post(self, url):
        self.logger.info('Получаю информацию о посте')
        if not 'vk.com' in url:
            return 0
        post_id = url.split('_')[-1]
        response = requests.get(
            f'https://api.vk.com/method/wall.getById?posts={post_id}&access_token={self.token}&v=5.131')
        self.logger.info(f'Ответ ВК: {response.json()}')
        if 'response' in response.json():
            return 1
        else:
            return 0
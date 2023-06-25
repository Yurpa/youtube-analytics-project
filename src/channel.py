from googleapiclient.discovery import build
import json
import os


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.info = Channel.info(self.__channel_id)

        self.title = self.info['items'][0]['snippet']['title']
        self.channel_info = self.info['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/{self.info['items'][0]['snippet']['customUrl']}"
        self.subscriber_count = self.info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.info['items'][0]['statistics']['videoCount']
        self.view_count = self.info['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} {self.url}'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=Channel.info(self.__channel_id).api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return print(json.dumps(channel, indent=2, ensure_ascii=False))

    @staticmethod
    def info(channel_id):
        channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        data = json.dumps(channel, indent=2, ensure_ascii=False)
        return json.loads(data)

    @classmethod
    def get_service(cls):
        return Channel.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, data):
        information = {'id канала': self.__channel_id,
                       'название канала': self.title,
                       'описание канала': self.channel_info,
                       'ссылка на канал': self.url,
                       'количество подписчиков': self.subscriber_count,
                       'количество видео': self.video_count,
                       'общее количество просмотров': self.view_count}
        with open(data, 'w', encoding='utf-8') as file:
            json.dump(information, file, indent=4, ensure_ascii=False)

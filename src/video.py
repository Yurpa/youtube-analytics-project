from src.channel import Channel


class Video(Channel):
    """Video class"""

    def __init__(self, video_id: str):
        self.video_id = video_id

        self.info = self.info(self.video_id)
        try:
            self.title = self.info['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count: int = self.info['items'][0]['statistics']['viewCount']
            self.like_count: int = self.info['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title}, {self.url}, {self.view_count}, {self.like_count})"

    @staticmethod
    def info(video_id):
        video_response = Channel.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id
                                                    ).execute()
        return video_response


class PLVideo(Video):
    """Playlist"""
    channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)

        self.video_id = video_id
        self.playlist_id = playlist_id

        self.info_play(self.video_id, self.playlist_id)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title}, {self.url}, {self.view_count}, {self.like_count})"

    @staticmethod
    def info_play(video_id, playlist_id):
        playlists = Channel.youtube.playlists().list(channelId=PLVideo.channel_id,
                                                  part='contentDetails,snippet',
                                                  maxResults=50,
                                                  ).execute()
        for playlist in playlists['items']:
            if playlist['id'] == playlist_id:
                Video.info(video_id)

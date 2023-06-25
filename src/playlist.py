import datetime

import isodate

from src.channel import Channel
from src.video import PLVideo, Video


class PlayList:
    """Playlist class"""
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id

        self.info_playlist = self.info_playlist(self.playlist_id)

        self.title = self.info_playlist['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.info_playlist['id']}"

        self.video_id_playlist = []

    @staticmethod
    def info_playlist(playlist_id):
        playlists = Channel.youtube.playlists().list(channelId=PLVideo.channel_id,
                                                     part='contentDetails,snippet',
                                                     maxResults=50,
                                                     ).execute()

        for playlist in playlists['items']:
            if playlist['id'] == playlist_id:
                return playlist

    @property
    def total_duration(self):
        """Overall duration of videos"""
        playlist_videos = Channel.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                               part='contentDetails',
                                                               maxResults=50,
                                                               ).execute()
        self.video_id_playlist: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        time_all = datetime.timedelta(seconds=0)

        for item in self.video_id_playlist:
            videos = Video.info(item)['items']
            for video in videos:
                iso_8601_duration = video['contentDetails']['duration']
                duration = isodate.parse_duration(iso_8601_duration)
                time_all += duration
        return time_all

    def show_best_video(self):
        """best viewed"""
        total_video = {}
        for item in self.video_id_playlist:
            video = Video.info(item)['items'][0]['statistics']['viewCount']
            total_video[item] = int(video)
        best_video = max(total_video.items(), key=lambda k: k[1])

        return f"https://youtu.be/{best_video[0]}"

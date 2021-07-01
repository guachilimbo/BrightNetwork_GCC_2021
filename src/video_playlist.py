"""A video playlist class."""
from .video_library import VideoLibrary

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
        self.name = name.upper()
        self.user_name = name
        self.videos_included = []

    def add_video(self, video_id):
        vid = VideoLibrary.get_video(video_id)
        self.videos_included.append(vid)
        return self.videos_included




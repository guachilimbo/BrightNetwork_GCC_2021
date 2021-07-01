"""A video player class."""

from .video_library import VideoLibrary
import random
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_video = []
        self.flag = 0
        self.pause = False
        self.playlist_lst = []
        self.playlist_names_lst = []
        self.playlist_found = False
        self.video_in_playlist = False
        self.found_videos = []
        self.video_in_library = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        video_lst = self._video_library.get_all_videos()
        vid_info = []
        for vid in video_lst:
            vid_info.append(f"  {vid.title} ({vid.video_id}) [{' '.join(vid.tags)}]")
        vid_info.sort()
        print("Here's a list of all available videos:")
        print('\n'.join(vid_info))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        all_id = []
        for vid in self._video_library.get_all_videos():
            all_id.append(vid.video_id)
        if video_id not in all_id:
            return print("Cannot play video: Video does not exist")
        elif self.flag == 0:
            requested_video = self._video_library.get_video(video_id)
            self.flag = 1
            self.current_video = requested_video
            self.pause = False
            return print(f"Playing video: {requested_video.title}")
        else:
            requested_video = self._video_library.get_video(video_id)
            out = f"Stopping video: {self.current_video.title}\nPlaying video: {requested_video.title}"
            self.current_video = requested_video
            self.pause = False
            return print(out)

    def stop_video(self):
        """Stops the current video."""
        if self.flag == 0:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self.current_video.title}")
            self.flag = 0
            self.current_video = []

    def play_random_video(self):
        """Plays a random video from the video library."""
        all_id = []
        for vid in self._video_library.get_all_videos():
            all_id.append(vid.video_id)
        if not all_id:
            print("No videos available")
        else:
            VideoPlayer.play_video(self, random.choice(all_id))

    def pause_video(self):
        """Pauses the current video."""
        if self.flag == 0:
            print("Cannot pause video: No video is currently playing")
        elif not self.pause:
            print(f"Pausing video: {self.current_video.title}")
            self.pause = True
        else:
            print(f"Video already paused: {self.current_video.title}")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.flag == 0:
            print("Cannot continue video: No video is currently playing")
        else:
            if self.pause:
                print(f"Continuing video: {self.current_video.title}")
                self.pause = False
            else:
                print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.flag == 0:
            print("No video is currently playing")
        else:
            vid = self.current_video
            if self.pause:
                print(f"Currently playing: {vid.title} ({vid.video_id}) [{' '.join(vid.tags)}] - PAUSED")
            else:
                print(f"Currently playing: {vid.title} ({vid.video_id}) [{' '.join(vid.tags)}]")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in self.playlist_names_lst:
            self.playlist_lst.append(Playlist(playlist_name))
            self.playlist_names_lst.append(playlist_name.upper())
            print(f"Successfully created new playlist: {playlist_name}")
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        self.playlist_found = False
        for playlist in self.playlist_lst:
            if playlist_name.upper() == playlist.name:
                self.playlist_found = True
                requested_video = self._video_library.get_video(video_id)
                if requested_video is None:
                    print(f"Cannot add video to {playlist_name}: Video does not exist")
                elif requested_video not in playlist.videos_included:
                    playlist.videos_included.append(requested_video)
                    print(f"Added video to {playlist_name}: {requested_video.title} ")
                else:
                    print(f"Cannot add video to {playlist_name}: Video already added")
                break
        if self.playlist_found is False:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if not self.playlist_lst:
            print("No playlists exist yet")
        else:
            all_playlists = []
            for playlist in self.playlist_lst:
                all_playlists.append(f"  {playlist.user_name} ")
            all_playlists.sort()
            print("Showing all playlists:")
            print('\n'.join(all_playlists))

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        self.playlist_found = False
        for playlist in self.playlist_lst:
            if playlist_name.upper() == playlist.name:
                self.playlist_found = True
                print(f"Showing playlist: {playlist_name}")
                if not playlist.videos_included:
                    print(f"  No videos here yet")
                else:
                    for vid in playlist.videos_included:
                        print(f"  {vid.title} ({vid.video_id}) [{' '.join(vid.tags)}]")

                break
        if self.playlist_found is False:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.upper() not in self.playlist_names_lst:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            self.video_in_playlist = False
            for playlist in self.playlist_lst:
                if playlist_name.upper() == playlist.name:
                    requested_video = self._video_library.get_video(video_id)
                    if not requested_video:
                        print(f"Cannot remove video from {playlist_name}: Video does not exist")
                    else:
                        for video in playlist.videos_included:
                            if video.video_id == video_id:
                                self.video_in_playlist = True
                                print(f"Removed video from {playlist_name}: {video.title}")
                                playlist.videos_included.remove(video)
                            break
                        if self.video_in_playlist is False:
                            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        self.playlist_found = False
        for playlist in self.playlist_lst:
            if playlist.name == playlist_name.upper():
                self.playlist_found = True
                playlist.videos_included.clear()
                print(f"Successfully removed all videos from {playlist_name}")
                break
        if self.playlist_found is False:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        self.playlist_found = False
        for playlist in self.playlist_lst:
            if playlist.name == playlist_name.upper():
                self.playlist_found = True
                self.playlist_lst.remove(playlist)
                del playlist
                print(f"Deleted playlist: {playlist_name}")
        if self.playlist_found is False:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        self.found_videos = []
        self.video_in_library = False
        for vid in self._video_library.get_all_videos():
            if search_term.lower() in vid.title.lower():
                self.found_videos.append(vid)
                self.video_in_library = True
            self.found_videos.sort(key=lambda x: x.title)
        if self.video_in_library is False:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for count, vid in enumerate(self.found_videos):
                print(f"  {count + 1}) {vid.title} ({vid.video_id}) [{' '.join(vid.tags)}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            ask = input('\n')
            if ask.isnumeric() and int(ask) - 1 <= count:
                requested_id = self.found_videos[int(ask) - 1].video_id
                self.play_video(requested_id)


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        self.found_videos = []
        self.video_in_library = False
        for vid in self._video_library.get_all_videos():
            if "#" not in video_tag:
                break
            elif video_tag.lower() in vid.tags:
                self.found_videos.append(vid)
                self.video_in_library = True
            self.found_videos.sort(key=lambda x: x.title)
        if self.video_in_library is False:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for count, vid in enumerate(self.found_videos):
                print(f"  {count + 1}) {vid.title} ({vid.video_id}) [{' '.join(vid.tags)}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            ask = input()
            if ask.isnumeric() and int(ask) - 1 <= count:
                requested_id = self.found_videos[int(ask) - 1].video_id
                self.play_video(requested_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")

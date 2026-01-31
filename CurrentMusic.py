from time import time

import requests
import urllib3

import config
from format_ordinal import format_ordinal

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CurrentMusic:
    def __init__(self):
        self.reset()
        self.displayed_id = None

    def reset(self):
        self.id = None
        self.title = None
        self.artist = None
        self.genre = None
        self.plays = None
        self.minutes_ago = None
        self.started_at = None
        self.ends_at = None
        self.comment = None
        self.song_changed = True

    def get_song_info(self):
        return f"\t{self.artist} - {self.title} ({self.genre})\n\t  🔁{format_ordinal(self.plays + 1)} listen\n\t  {self.comment}"

    def update(self):
        try:
            response = requests.get(
                f"{config.SUBSONIC_SERVER}/rest/getNowPlaying",
                params={
                    "u": config.SUBSONIC_USERNAME,
                    "p": config.SUBSONIC_PASSWORD,
                    "v": "1.13.0",
                    "c": "music-presence",
                    "f": "json",
                },
                verify=False,  # Certificate check
            )
        except requests.exceptions.RequestException:
            print("Cannot connect to Subsonic server")
            return

        if response.status_code != 200:
            print("Error getting music", response.text)
            return

        try:
            json = response.json()["subsonic-response"]
        except requests.exceptions.JSONDecodeError:
            print("Cannot parse response", response.text)
            return

        if len(json["nowPlaying"]) == 0:
            self.reset()
            return

        if json["status"] == "ok" and len(json["nowPlaying"]) > 0:
            nowPlayingEntry = json["nowPlaying"]["entry"]
            nowPlayingList = [
                player
                for player in nowPlayingEntry
                if player["username"] == config.SUBSONIC_USERNAME
            ]

            if len(nowPlayingList) == 0:
                self.id = None
                self.reset()
                return

            nowPlaying = nowPlayingList[0]

            self.song_changed = (
                nowPlaying["id"] != self.id
                or nowPlaying["playCount"] != self.plays
                or nowPlaying["minutesAgo"] != self.minutes_ago
            )

            self.id = nowPlaying["id"]
            self.artist = nowPlaying["artist"]
            self.title = nowPlaying["title"]
            self.genre = (
                ""
                if len(nowPlaying["genres"]) == 0
                else nowPlaying["genres"][0]["name"]
            )
            self.plays = nowPlaying["playCount"]
            self.minutes_ago = nowPlaying["minutesAgo"]
            if self.song_changed:
                self.started_at = time() - self.minutes_ago * 60
                self.ends_at = self.started_at + nowPlaying["duration"]
            self.comment = nowPlaying["comment"]

            if time() >= self.ends_at:
                print("Song ended")
                self.reset()
                return

            if self.displayed_id != nowPlaying["id"]:
                print(self.get_song_info())

            self.check_exclusion()

            self.displayed_id = nowPlaying["id"]

    def check_exclusion(self):
        genre = self.genre
        song_id = self.id
        if genre in config.EXCLUDED_GENRES:
            self.reset()
            if self.displayed_id != song_id:
                print(f"This song is excluded from genre {genre}")
            return True
        return False

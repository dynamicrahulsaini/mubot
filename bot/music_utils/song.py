from typing import Union
from dataclasses import dataclass
from discord import Member, User


@dataclass
class Song:
    url: str
    title: str
    duration: int
    requester: Union[User, Member]

    def __init__(self, url: str, title: str, duration: int, requester: Union[User, Member]):
        self.url = url
        self.title = title
        self.duration = duration
        self.requester = requester
    
    def from_song_info(song_info: dict, requester: Union[User, Member]):
        return Song(song_info["url"], song_info["title"], song_info["duration"], requester)

from dataclasses import dataclass

@dataclass()
class User:
    user_url: str
    user_first_name: str
    user_last_name: str

@dataclass()
class Meme:
    url: str
    likes: int
    author: User



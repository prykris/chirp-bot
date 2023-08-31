from typing import Dict
from dataclasses import dataclass, asdict


@dataclass
class Tweet:
    id: str
    user: str
    text: str
    time: str

    @staticmethod
    def from_dict(data: Dict[str, str]) -> 'Tweet':
        return Tweet(id=data['id'], user=data['user'], text=data['text'], time=data['time'])

    def to_dict(self):
        return asdict(self)
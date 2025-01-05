import dataclasses

import requests
from monkeytype.authorization import Authorization

class Users:
    def __init__(self, auth: Authorization):
        self.auth = auth


    def get_personal_bests(self, mode: str, mode2: int | str | None = None):
        return PersonalBests.from_dict(requests.get(url=f"{self.auth.users}/personalBests", params={
            'mode': mode,
            'mode2': mode2
        }, headers=self.auth.auth_header).json())


@dataclasses.dataclass
class PersonalBest:
    acc: float
    consistency: float
    difficulty: str
    language: str
    lazy_mode: bool
    numbers: bool
    punctuation: bool
    raw: float
    timestamp: int
    wpm: float

    @classmethod
    def from_dict(cls, dict_: dict):
        return cls(
            acc=dict_['acc'],
            consistency=dict_['consistency'],
            difficulty=dict_['difficulty'],
            language=dict_['language'],
            lazy_mode=dict_['lazyMode'],
            numbers=dict_['numbers'],
            punctuation=dict_['punctuation'],
            raw=dict_['raw'],
            timestamp=dict_['timestamp'],
            wpm=dict_['wpm']
        )


@dataclasses.dataclass
class PersonalBests:
    personal_beats: dict[str, PersonalBest]
    message: str

    @classmethod
    def from_dict(cls, dict_):
        personal_beats = {}
        for mode, personal_bests in dict_["data"].items():
            for personal_best in personal_bests:
                personal_beats[mode] = PersonalBest.from_dict(personal_best)

        return cls(
            personal_beats=personal_beats,
            message=dict_['message']
        )
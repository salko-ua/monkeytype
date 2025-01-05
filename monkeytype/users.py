import dataclasses
from pprint import pprint
from datetime import datetime
import requests
from monkeytype.authorization import Authorization


class Users:
    def __init__(self, auth: Authorization):
        self.auth = auth

    def get_personal_bests(self, mode: str, mode2: int | str | None = None):
        """
        Fetches the user's personal bests from the API based on the provided mode and optional
        secondary mode. Handles the response and constructs appropriate objects.

        :param mode: The primary mode for fetching the personal bests. Represents how the data
            is categorized or filtered.
        :type mode: str

        :param mode2: An optional secondary mode for further filtering or categorizing the
            personal bests. Can be an integer, string, or None if not provided by the user.
        :type mode2: int | str | None

        :return: A `PersonalBests` object constructed from the response if the data is
            available. If the secondary mode is not provided, a `PersonalBests` object
            is derived from the primary data only. Returns `None` if no data is found.
        :rtype: Union[PersonalBests, None]
        """
        response = requests.get(url=f"{self.auth.users}/personalBests", params={
            'mode': mode,
            'mode2': mode2
        }, headers=self.auth.auth_header)
        json = response.json()
        headers = response.headers

        if json["data"] is None:
            return None

        if mode2 is None:
            return PersonalBests.from_dict([json, headers])

        return PersonalBests(
            personal_beats={PersonalBest.from_dict(json["data"][0])},
            message=json["message"],
            limits=Limits.from_dict(headers)
        )


@dataclasses.dataclass
class Limits:
    x_ratelimit_limit: int
    x_ratelimit_remaining: int
    x_ratelimit_reset: int

    @classmethod
    def from_dict(cls, dict_: dict):
        return cls(
            x_ratelimit_limit=int(dict_["x-ratelimit-limit"]),
            x_ratelimit_remaining=int(dict_["x-ratelimit-remaining"]),
            x_ratelimit_reset=int(dict_["x-ratelimit-reset"])
        )


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
    limits: Limits

    @classmethod
    def from_dict(cls, list_of_dicts: list[dict]):
        json = list_of_dicts[0]
        header = list_of_dicts[1]

        personal_beats = {}
        for mode, personal_bests in json["data"].items():
            for personal_best in personal_bests:
                personal_beats[mode] = PersonalBest.from_dict(personal_best)

        return cls(
            personal_beats=personal_beats,
            message=json['message'],
            limits=Limits.from_dict(header)
        )

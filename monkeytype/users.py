import dataclasses
from pprint import pprint
from datetime import datetime
import requests
from monkeytype.authorization import Authorization


class Users:
    def __init__(self, auth: Authorization):
        self.auth = auth


    def check_name(self, name: str):
        """
        - Token is not required but recommended.
        Checks if a given username is available.
        If token empty can`t return uid, it will be ""

        :param name: The username to be checked for availability.
        :type name: str
        :return: A CheckName object constructed from the API response.
        :rtype: CheckName
        """
        response = requests.get(url=f"{self.auth.users}/checkName/{name}", headers=self.auth.auth_header)
        json = response.json()
        headers = response.headers

        return CheckName.from_dict(json, headers)

    def get_personal_bests(self, mode: str, mode2: int | str | None = None):
        """
        - Token is required.
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
            return PersonalBests.from_dict(json, headers)

        return PersonalBests(
            personal_beats={PersonalBest.from_dict(json["data"][0])},
            message=json["message"],
            limits=Limits.from_dict(headers)
        )

    def get_tags(self):
        # TODO:
        response = requests.get(url=f"{self.auth.users}/tags", headers=self.auth.auth_header)
        json = response.json()
        return json

    def get_stats(self):
        response = requests.get(url=f"{self.auth.users}/stats", headers=self.auth.auth_header)
        json = response.json()
        headers = response.headers
        return PersonalStats.from_dict(json, headers)

    def get_profile(self, uid_or_username: str | int):
        response = requests.get(url=f"{self.auth.users}/{uid_or_username}/profile", headers=self.auth.auth_header)
        json = response.json()
        return json


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
class CheckName:
    uid: str | None
    available: bool
    message: str
    limits: Limits

    @classmethod
    def from_dict(cls, json: dict, header: dict):
        if json["data"]:
            uid = json["data"]["uid"]
        else:
            uid = None

        return cls(
            uid=uid,
            available=False if json["message"] == "Username unavailable" else True,
            message=json["message"],
            limits=Limits.from_dict(header)
        )

@dataclasses.dataclass
class PersonalStats:
    uid: str
    completed_tests: int
    started_tests: int
    time_typing: bool
    message: str
    limits: Limits

    @classmethod
    def from_dict(cls, json: dict, header: dict):
        if json["message"] == "Unauthorized":
            raise "Unauthorized"

        return cls(
            uid=json["data"]["_id"],
            completed_tests=json["data"]["completedTests"],
            started_tests=json["data"]["startedTests"],
            time_typing=json["data"]["timeTyping"],
            message=json["message"],
            limits=Limits.from_dict(header)
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
    personal_beats: dict[str, PersonalBest] | None
    time: dict[str, PersonalBest] | None
    words: dict[str, PersonalBest] | None
    message: str
    limits: Limits

    @classmethod
    def from_dict(cls, json: dict, header: dict):
        personal_beats = {}
        for mode, personal_bests in json["data"].items():
            for personal_best in personal_bests:
                personal_beats[mode] = PersonalBest.from_dict(personal_best)

        return cls(
            personal_beats=personal_beats,
            time=personal_beats["time"] if "time" in personal_beats else None,
            words=personal_beats["words"] if "words" in personal_beats else None,
            message=json['message'],
            limits=Limits.from_dict(header)
        )



@dataclasses.dataclass
class Profile:

    @classmethod
    def from_dict(cls, json: dict, header: dict):
        pass
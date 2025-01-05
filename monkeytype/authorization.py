from dataclasses import dataclass


@dataclass
class Authorization:
    token: str
    users = "https://api.monkeytype.com/users"

    @property
    def auth_header(self) -> dict:
        return {"Authorization": f"ApeKey {self.token}"}
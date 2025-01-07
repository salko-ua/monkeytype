from dataclasses import dataclass


@dataclass
class Authorization:
    token: str | None = None
    users = "https://api.monkeytype.com/users"

    @property
    def auth_header(self) -> dict:
        if not self.token:
            return {}

        return {"Authorization": f"ApeKey {self.token}"}
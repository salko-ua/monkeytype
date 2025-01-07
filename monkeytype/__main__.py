from monkeytype.authorization import Authorization
from monkeytype.users import Users
from pprint import pprint


monkey = Authorization()
users = Users(monkey)

pprint(users.get_personal_bests("time").personal_beats["15"].acc)
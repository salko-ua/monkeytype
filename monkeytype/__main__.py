from monkeytype.authorization import Authorization
from monkeytype.users import Users
from pprint import pprint
import os

monkey = Authorization(os.getenv("MONKEYTYPE_TOKEN"))
users = Users(monkey)

pprint(users.get_stats())
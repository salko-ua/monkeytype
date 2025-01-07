from monkeytype.authorization import Authorization
from monkeytype.users import Users
from pprint import pprint

token=''

monkey = Authorization(token)
users = Users(monkey)

pprint(users.get_personal_bests("time"))
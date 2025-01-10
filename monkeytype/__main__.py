from monkeytype.authorization import Authorization
from monkeytype.users import Users
from pprint import pprint


monkey = Authorization("Njc3ZGE4NGIzM2VlMjdhYTEyYjYxYjViLm1nRkxkQlUzVlRERXFFRURrSFpoalNpLUVMbFFUbVFz")
users = Users(monkey)

pprint(users.get_tags())
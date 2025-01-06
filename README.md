## MonkeyType Library python

Example of usage
```python
from monkeytype.authorization import Authorization
from monkeytype.users import Users

token=''

# Get auth
monkey = Authorization(token)
# It sorted by categories
# Categories in api it`s class in python
# Users has methods (check_name, get_personal_bests ..) like in https://api.monkeytype.com/docs
users = Users(monkey)

# Example of usage method get_personal_bests
print(users.get_personal_bests("time")
```


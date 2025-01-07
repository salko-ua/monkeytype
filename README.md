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
# Temp docs
# Users has methods
# methods has any data after they was called and has limits\
# example
bests = users.get_personal_bests("time") # get personal best by time
ex1 = bests.limits.x_ratelimit_limit
ex2 = bests.limits.x_ratelimit_reset
ex3 = bests.limits.x_ratelimit_remaining
another_data = bests.personal_beats["15"].acc # for example
```


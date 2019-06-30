from functools import partial

from django.conf import settings

import jwt

ALGO = 'HS256'

encode = partial(jwt.encode, key=settings.JWT_SECRET, algorithm=ALGO)
decode = partial(jwt.decode, key=settings.JWT_SECRET, verify=True, algorithms=[ALGO])

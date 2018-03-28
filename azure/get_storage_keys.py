#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import pandas as pd

from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, get_storage_key

users = pd.read_json("users.json", orient="records")

storage_keys = dict()
storage_keys["admin"] = get_storage_key(STORAGE_ACCOUNT_TEMPLATE.format("admin"), RG_TEMPLATE.format("admin"))

for _, row in users.iterrows():
    row = dict(row)
    user = row["user"]
    user_account = STORAGE_ACCOUNT_TEMPLATE.format(user)
    user_rg = RG_TEMPLATE.format(user)
    user_key = get_storage_key(user_account, user_rg)
    storage_keys[user] = user_key
    print(user, "done")

json.dump(storage_keys, open("storage_keys.json", "w"), indent=4, sort_keys=True)

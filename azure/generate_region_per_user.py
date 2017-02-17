#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import json

student_cnt = 81

# GPU 6-core machines is the limit
# eastus: 24
# southcentralus: 20 + 24
# westeurope: 20
# southeastasia: 20

regions = ["eastus"] * 17 + ["southcentralus"] * 44 + ["westeurope"] * 20
assert len(regions) == student_cnt

users = pd.read_json("users.json", orient="records")

region_by_user = {}

for idx, (_, row) in enumerate(users.iterrows()):
    row = dict(row)
    user = row["user"]
    region_by_user[user] = regions[idx]

json.dump(region_by_user, open("regions.json", "w"), indent=4, sort_keys=True)

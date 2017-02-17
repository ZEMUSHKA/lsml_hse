#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import json

student_cnt = 81

# GPU 6-core machines is the limit
# eastus: 24 (148 NC cores)
# southcentralus: 24 (148 NC cores) + 20 (124 NV cores)
# westeurope: 20 (124 NV cores)
# southeastasia: 20 (124 NV cores)

# Dv2 limits (ticket in progress)
# eastus: 24 (288 cores)
# southcentralus: 44 (528 cores)
# westeurope: 20 (240 cores)
# southeastasia: 20 (240 cores)

regions = ["eastus"] * 17 + ["southcentralus"] * 44 + ["westeurope"] * 20
gpus_kind = ["Standard_NC6"] * 17 + ["Standard_NC6"] * 24 + ["Standard_NV6"] * 20 + ["Standard_NV6"] * 20
assert len(regions) == student_cnt == len(gpus_kind)

users = pd.read_json("users.json", orient="records")

region_by_user = dict()
gpu_by_user = dict()
region_by_user["admin"] = "eastus"
gpu_by_user["admin"] = "Standard_NC6"

for idx, (_, row) in enumerate(users.iterrows()):
    row = dict(row)
    user = row["user"]
    region_by_user[user] = regions[idx]
    gpu_by_user[user] = gpus_kind[idx]


json.dump(region_by_user, open("regions.json", "w"), indent=4, sort_keys=True)
json.dump(gpu_by_user, open("gpus.json", "w"), indent=4, sort_keys=True)

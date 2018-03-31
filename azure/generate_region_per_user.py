#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import pandas as pd

# GPU 6-core limits
# eastus: 24 (148 NC cores)
# southcentralus: 24 (148 NC cores) + 20 (124 NV cores)
# westeurope: 19 (114 NV cores) + 8 (48 NC cores)
# southeastasia: 20 (124 NV cores)

# Ev3 12-core limits
# eastus: 24 (288 cores)
# southcentralus: 44 (528 cores)
# westeurope: 27 (324 cores)
# southeastasia: 20 (240 cores)

regions = ["eastus"] * 17 + \
          ["southcentralus"] * 44 + \
          ["westeurope"] * 27

gpus_kind = ["Standard_NC6"] * 17 + \
            ["Standard_NC6"] * 24 + \
            ["Standard_NV6"] * 20 + \
            ["Standard_NV6"] * 19 + \
            ["Standard_NC6"] * 8

users = pd.read_json("users.json", orient="records")
assert len(regions) == len(users) == len(gpus_kind)

region_by_user = dict()
gpu_by_user = dict()
region_by_user["admin"] = "eastus"
gpu_by_user["admin"] = "Standard_NC6"
region_by_user["test"] = "southeastasia"
gpu_by_user["test"] = "Standard_NV6"

for idx, (_, row) in enumerate(users.iterrows()):
    row = dict(row)
    user = row["user"]
    region_by_user[user] = regions[idx]
    gpu_by_user[user] = gpus_kind[idx]


json.dump(region_by_user, open("regions.json", "w"), indent=4, sort_keys=True)
json.dump(gpu_by_user, open("gpus.json", "w"), indent=4, sort_keys=True)

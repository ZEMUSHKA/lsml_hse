#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import pandas as pd

import utils

# users = pd.read_json("users.json", orient="records")

users = json.load(open("sber.json"))
users = pd.DataFrame(users.keys(), columns=["user"])

subscription_id = utils.get_subscription_id()
VM_NAME = "cluster1"
start = "2018-05-08T00:00:00Z"
end = "2018-05-25T00:00:00Z"
interval = "PT24H"

df = []

for idx, (_, row) in enumerate(users.iterrows()):
    row = dict(row)
    user = row["user"]
    rg_name = utils.get_student_resource_group(user)
    print user, rg_name
    out = utils.get_cpu_usage(subscription_id, rg_name, VM_NAME, start, end, interval)
    if out is not None:
        out = dict(out)
        out["student"] = user
        df.append(out)

df = pd.DataFrame(df)
df = df[sorted(df.columns)]
df.to_excel("cpu_report1_fintech.xlsx")

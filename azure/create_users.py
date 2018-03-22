#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json
import pandas as pd
from utils import generate_pass, STUDENT_COUNT, AD_DOMAIN

users = []

for idx in range(STUDENT_COUNT):
    password = generate_pass()
    user = "student{}".format(idx + 1)
    out = subprocess.check_output(
        """
        az ad user create \
        --user-principal-name "{u}@{d}" \
        --display-name "{u}" \
        --password {p} \
        --mail-nickname "{u}"
        """.format(p=password, u=user, d=AD_DOMAIN),
        shell=True
    )
    out = json.loads(out)
    userId = out["objectId"]
    users.append([user, password, userId])
    print user, "done"

df = pd.DataFrame(users, columns=["user", "password", "userId"])
df.to_json("users.json", orient="records")

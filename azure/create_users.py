#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import subprocess

import pandas as pd

from utils import check_output_wrapper

# import pandas as pd
# pd.read_json("users.json", orient="records").to_excel("users.xlsx")

from utils import generate_pass, STUDENT_COUNT, AD_DOMAIN

users = []

for idx in range(STUDENT_COUNT):
    # if (idx + 1) <= 81:
    #     continue
    password = generate_pass()
    user = "student{}".format(idx + 1)
    out = check_output_wrapper(
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
    print(user, "done")

df = pd.DataFrame(users, columns=["user", "password", "userId"])
df.to_json("users.json", orient="records")

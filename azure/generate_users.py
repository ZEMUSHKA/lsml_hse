#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import random
import subprocess
import json
import pandas as pd

student_cnt = 2
pass_chars = string.letters + string.digits
pass_size = 16


def generate_pass():
    return ''.join((random.choice(pass_chars)) for _ in range(pass_size))

users = []

for idx in range(student_cnt):
    password = generate_pass()
    user = "student{}".format(idx + 1)
    out = subprocess.check_output(
        """
        az ad user create \
        --user-principal-name "{u}@zimovnovgmail.onmicrosoft.com" \
        --display-name "{u}" \
        --password {p} \
        --mail-nickname "{u}"
        """.format(p=password, u=user),
        shell=True
    )
    out = json.loads(out)
    userId = out["objectId"]
    users.append([user, password, userId])

df = pd.DataFrame(users, columns=["user", "password", "userId"])
df.to_json("users.json", orient="records")

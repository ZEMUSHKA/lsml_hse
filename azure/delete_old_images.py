#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

import pandas as pd

from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, get_storage_key

users = pd.read_json("users.json", orient="records")

CONTAINER = "images"
PATTERN = "ubuntugpu2.vhd"

for _, row in users.iterrows():
    row = dict(row)
    user = row["user"]
    userId = row["userId"]
    resGrName = RG_TEMPLATE.format(user)
    storName = STORAGE_ACCOUNT_TEMPLATE.format(user)
    userKey = get_storage_key(storName, resGrName)
    subprocess.check_output(
        """
        az storage blob delete \
        --container-name {cont} \
        --account-key {key} \
        --account-name {acc} \
        --name {fn}
        """.format(cont=CONTAINER, fn=PATTERN, acc=storName, key=userKey),
        shell=True
    )
    print(user, "done")

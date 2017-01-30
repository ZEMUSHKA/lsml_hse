#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess
from utils import get_storage_key

RES_GR_TEMPLATE = "{0}_resources"
STORAGE_ACCOUNT_TEMPLATE = "{0}lsmlhse645221"

users = pd.read_json("users.json", orient="records")

for _, row in users.iterrows():
    row = dict(row)
    user = row["user"]
    userId = row["userId"]
    resGrName = RES_GR_TEMPLATE.format(user)
    storName = STORAGE_ACCOUNT_TEMPLATE.format(user)
    userKey = get_storage_key(storName, resGrName)
    subprocess.check_output(
        """
        az storage blob delete \
        --container-name {cont} \
        --account-key {key} \
        --account-name {acc} \
        --name {fn}
        """.format(cont="images", fn="ubuntugpu2.vhd", acc=storName, key=userKey),
        shell=True
    )
    print user, "done"
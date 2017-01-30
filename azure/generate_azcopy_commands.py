#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE
from utils import get_storage_key

users = pd.read_json("users.json", orient="records")

ADMIN_STORAGE_ACCOUNT = STORAGE_ACCOUNT_TEMPLATE.format("admin")
ADMIN_RG = RG_TEMPLATE.format("admin")
CONTAINER = "images"
PATTERN = "ubuntugpu.vhd"

admin_key = get_storage_key(ADMIN_STORAGE_ACCOUNT, ADMIN_RG)

with open("azcopy.bat", "w", buffering=0) as f:
    for _, row in users.iterrows():
        row = dict(row)
        user = row["user"]
        user_account = STORAGE_ACCOUNT_TEMPLATE.format(user)
        user_rg = RG_TEMPLATE.format(user)
        user_key = get_storage_key(user_account, user_rg)
        command = \
            """md "C:\\Users\\andrey\\Desktop\\AzureTemp\\{d}"\r\n\
start "AzCopy {s} to {d}" "C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\AzCopy\\AzCopy.exe" \
            /Source:https://{s}.blob.core.windows.net/{cont} \
            /Dest:https://{d}.blob.core.windows.net/{cont} \
            /SourceKey:{sk} \
            /DestKey:{dk} \
            /Pattern:{p}\
            /V:"C:\\Users\\andrey\\Desktop\\AzureTemp\\{d}-log.txt"\
            /Z:"C:\\Users\\andrey\\Desktop\\AzureTemp\\{d}"\r\n""".format(
                s=ADMIN_STORAGE_ACCOUNT,
                d=user_account,
                sk=admin_key,
                dk=user_key,
                p=PATTERN,
                cont=CONTAINER
            )
        f.write(command)
        print user, "done"

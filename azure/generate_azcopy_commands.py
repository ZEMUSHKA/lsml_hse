#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess
import json

users = pd.read_json("users.json", orient="records")

RES_GR_TEMPLATE = "{0}_resources"
STORAGE_ACCOUNT_TEMPLATE = "{0}lsmlhse645221"
admin_account = "adminlsml"
admin_rg = "admin_resources"
PATTERN = "ubuntugpu2.vhd"


def get_storage_key(account, rg):
    out = subprocess.check_output(
        """
        az storage account keys list \
        --name {n} \
        --resource-group {g}
        """.format(n=account, g=rg),
        shell=True
    )
    out = json.loads(out)
    key = out["keys"][0]["value"]
    return key

admin_key = get_storage_key(admin_account, admin_rg)

with open("azcopy.bat", "w", buffering=0) as f:
    for _, row in users.iterrows():
        row = dict(row)
        user = row["user"]
        user_account = STORAGE_ACCOUNT_TEMPLATE.format(user)
        user_rg = RES_GR_TEMPLATE.format(user)
        user_key = get_storage_key(user_account, user_rg)
        command = \
            """md "C:\Users\andrey\Desktop\AzureTemp\{d}"\r\n\
            start "AzCopy {s} to {d}" "C:\Program Files (x86)\Microsoft SDKs\Azure\AzCopy\AzCopy.exe" \
            /Source:https://{s}.blob.core.windows.net/images \
            /Dest:https://{d}.blob.core.windows.net/images \
            /SourceKey:{sk} \
            /DestKey:{dk} \
            /Pattern:{p}\
            /V:"C:\Users\andrey\Desktop\AzureTemp\{d}-log.txt"\
            /Z:"C:\Users\andrey\Desktop\AzureTemp\{d}"\r\n""".format(
                s=admin_account,
                d=user_account,
                sk=admin_key,
                dk=user_key,
                p=PATTERN
            )
        f.write(command)
        print user, "done"

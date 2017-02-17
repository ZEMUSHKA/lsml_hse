#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess
from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, region_by_user

users = pd.read_json("users.json", orient="records")

for idx, (_, row) in enumerate(users.iterrows()):
    # if idx < 10:
    #     continue
    row = dict(row)
    user = row["user"]
    userId = row["userId"]
    rgName = RG_TEMPLATE.format(user)
    region = region_by_user[user]
    # create res gr
    subprocess.check_output(
        """
        az group create \
        -n "{n}" \
        -l "{l}"
        """.format(n=rgName, l=region),
        shell=True
    )
    # assign user to his res gr
    subprocess.check_output(
        """
        az role assignment create \
        --assignee {userId} \
        --role Contributor \
        --resource-group {rg}
        """.format(userId=userId, rg=rgName),
        shell=True
    )
    # create storage account
    storName = STORAGE_ACCOUNT_TEMPLATE.format(user)
    subprocess.check_output(
        """
        az storage account create \
        -l {l} \
        -n {n} \
        -g {g} \
        --sku Standard_LRS
        """.format(l=region, n=storName, g=rgName),
        shell=True
    )
    # create container for images
    subprocess.check_output(
        """
        az storage container create \
        -n images \
        --account-name {s}
        """.format(s=storName),
        shell=True
    )
    print user, "done"

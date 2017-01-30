#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess
from utils import REGION, RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE

users = pd.read_json("users.json", orient="records")

for _, row in users.iterrows():
    row = dict(row)
    user = row["user"]
    userId = row["userId"]
    resGrName = RG_TEMPLATE.format(user)
    # create res gr
    subprocess.check_output(
        """
        az group create \
        -n "{n}" \
        -l "{l}"
        """.format(n=resGrName, l=REGION),
        shell=True
    )
    # assign user to his res gr
    subprocess.check_output(
        """
        az role assignment create \
        --assignee {userId} \
        --role Contributor \
        --resource-group {rg}
        """.format(userId=userId, rg=resGrName),
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
        """.format(l=REGION, n=storName, g=resGrName),
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

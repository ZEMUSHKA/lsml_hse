#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

import pandas as pd

from utils import AD_GROUP, get_ad_group_id

subprocess.check_output(
    """
    az ad group create \
    --display-name {g} \
    --mail-nickname {g}
    """.format(g=AD_GROUP),
    shell=True
)

users = pd.read_json("users.json", orient="records")
group_id = get_ad_group_id(AD_GROUP)

for _, row in users.iterrows():
    row = dict(row)
    userId = row["userId"]
    subprocess.check_output(
        """
        az ad group member add \
        --group {g} \
        --member-id {u}
        """.format(g=AD_GROUP, u=userId),
        shell=True
    )
    print(row["user"], "added to group")

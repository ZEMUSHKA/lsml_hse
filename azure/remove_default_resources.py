#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import subprocess
from utils import RG_TEMPLATE

users = pd.read_json("users.json", orient="records")

for idx, (_, row) in enumerate(users.iterrows()):
    if idx < 3:
        continue
    row = dict(row)
    user = row["user"]
    resGrName = RG_TEMPLATE.format(user)
    # create res gr
    subprocess.check_output(
        """
        az group delete \
        -n "{n}"
        """.format(n=resGrName),
        shell=True
    )
    print user, "done"

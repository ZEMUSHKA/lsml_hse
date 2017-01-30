#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json


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

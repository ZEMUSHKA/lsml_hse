#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import subprocess

import numpy as np
import pandas as pd

from utils import timeit


@timeit
def get_vm_list():
    out = subprocess.check_output(
        """
        az vm list
        """,
        shell=True
    )
    out = json.loads(out)
    return out


@timeit
def get_vm_status(vm_ids):
    out = subprocess.check_output(
        """
        az vm show -d --ids {0}
        """.format(" ".join(vm_ids)),
        shell=True
    )
    out = json.loads(out)
    return out


vm_list = get_vm_list()
vm_ids = [x["id"] for x in vm_list]
vm_statuses = get_vm_status(vm_ids)

df = []
for vm in vm_statuses:
    rg = vm["resourceGroup"]
    vm_size = vm["hardwareProfile"]["vmSize"]
    power_state = vm["powerState"]
    is_deallocated = int(power_state == "VM deallocated")
    df.append([rg, vm_size, is_deallocated, 1 - is_deallocated])

df = pd.DataFrame(df, columns=["resourceGroup", "vmSize", "deallocated", "running"])

df = pd.pivot_table(
    df,
    index=["resourceGroup", "vmSize"],
    values=["deallocated", "running"],
    aggfunc=[np.sum],
    fill_value=0)

df.to_excel("report.xlsx")

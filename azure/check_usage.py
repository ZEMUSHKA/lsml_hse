#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json
from utils import timeit
import pandas as pd
import numpy as np


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
vm_ids = map(lambda x: x["id"], vm_list)
vm_statuses = get_vm_status(vm_ids)

df = []
for vm in vm_statuses:
    rg = vm["resourceGroup"]
    vm_size = vm["hardwareProfile"]["vmSize"]
    power_state = vm["powerState"]
    is_deallocated = power_state == "VM deallocated"
    df.append([rg, vm_size, int(is_deallocated), int(~is_deallocated)])

df = pd.DataFrame(df, columns=["resourceGroup", "vmSize", "deallocated", "running"])

df = pd.pivot_table(
    df,
    index=["vmSize", "resourceGroup"],
    values=["deallocated", "running"],
    aggfunc=[np.sum],
    fill_value=0)

df.to_excel("report.xlsx")

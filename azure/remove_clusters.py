#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import subprocess

from joblib import Parallel, delayed

import utils
from utils import RG_TEMPLATE, check_output_wrapper

finished_students = [

]


def get_vm_status(VM, RG):
    out = check_output_wrapper(
        """
        az vm show -d -n {0} -g {1}
        """.format(VM, RG),
        shell=True
    )
    if out.strip() == "":
        return None
    out = json.loads(out)
    power_state = out["powerState"]
    return power_state


def list_disks_for_rg(RG):
    out = check_output_wrapper(
        """
        az disk list -g {0}
        """.format(RG),
        shell=True
    )
    if out == "":
        return []
    out = json.loads(out)
    return out


def safe_remove(VM, RG):
    assert len(VM) > 0
    assert len(RG) > 0
    vm_status = get_vm_status(VM, RG)
    if vm_status == "VM deallocated":
        try:
            utils.remove_vm_and_disks(VM, RG)
            print("Removed", VM, RG)
        except:
            print("Error removing", VM, RG)
    elif vm_status == "VM running":
        print("Didn't remove running VM", VM, RG)
        return
    elif vm_status is None:
        print("Already removed", VM, RG)
    else:
        print("Unknown status", VM, RG, vm_status)
        return
    # remove orphaned disks
    disks = list_disks_for_rg(RG)
    disks = [x for x in disks if x["name"].startswith(VM)]
    disks = [x["id"] for x in disks]
    if disks:
        print("Removing orphaned disks")
        for disk in disks:
            print(disk)
        utils.remove_disks(disks)


Parallel(n_jobs=10, backend="threading")(
    delayed(safe_remove)(
        "cluster{0}".format(idx),
        RG_TEMPLATE.format("student{0}".format(student_id))
    )
    for idx in [1, 2, 3]
    for student_id in finished_students
)

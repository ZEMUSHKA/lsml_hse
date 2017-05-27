#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
from utils import RG_TEMPLATE
from joblib import Parallel, delayed
import subprocess
import json


finished_students = [
    5,
    46,
    33,
    4,
    58,
    30,
    43,
    20,
    17,
    45,
    69,
    32,
    70,
    57,
    71,
    42,
    61,
    41,
    67,
    59,
    60,
    21,
    75,
    9,
    15,
    14,
    50,
    47,
    23,
    38,
    13,
    29,
    10,
    79,
    55,
    53,
    77,
    40,
    25,
    52,
    39
]


def get_vm_status(VM, RG):
    out = subprocess.check_output(
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


def safe_remove(VM, RG):
    vm_status = get_vm_status(VM, RG)
    if vm_status == "VM deallocated":
        try:
            utils.remove_vm_and_disks(VM, RG)
            print "Removed", VM, RG
        except:
            print "Error removing", VM, RG
    elif vm_status == "VM running":
        print "Didn't remove running VM", VM, RG
    elif vm_status is None:
        print "Already removed", VM, RG
    else:
        print "Unknown status", VM, RG, vm_status


Parallel(n_jobs=10, backend="threading")(
    delayed(safe_remove)(
        "cluster{0}".format(idx),
        RG_TEMPLATE.format("student{0}".format(student_id))
    )
    for idx in [1, 2, 3]
    for student_id in finished_students
)

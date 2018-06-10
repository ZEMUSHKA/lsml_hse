#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import subprocess
from joblib import Parallel, delayed

from utils import remove_disks, check_output_wrapper


def list_orphaned_disks():
    out = check_output_wrapper(
        """
        az disk list
        """,
        shell=True
    )
    if out.strip() == "":
        return None
    out = json.loads(out)
    out = [x for x in out if x["managedBy"] is None]
    out = [x["id"] for x in out]
    return out


orphaned = list_orphaned_disks()
print(len(orphaned))
for elem in orphaned:
    print(elem)

batch_size = 5
Parallel(n_jobs=10, backend="threading")(
    delayed(remove_disks)(orphaned[start:start + batch_size])
    for start in range(0, len(orphaned), batch_size)
)

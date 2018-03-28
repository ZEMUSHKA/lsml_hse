#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import subprocess

from utils import remove_disks


def list_orphaned_disks():
    out = subprocess.check_output(
        """
        az disk list
        """,
        shell=True
    )
    if out.strip() == "":
        return None
    out = json.loads(out)
    out = [x for x in out if x["ownerId"] is None]
    out = [x["id"] for x in out]
    return out


orphaned = list_orphaned_disks()
remove_disks(orphaned)

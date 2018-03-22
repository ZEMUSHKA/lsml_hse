#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from utils import STUDENT_COUNT, AD_DOMAIN

for idx in range(STUDENT_COUNT):
    user = "student{}".format(idx + 1)
    subprocess.check_output(
        """
        az ad user delete \
        --upn-or-object-id "{u}@{d}" \
        """.format(u=user, d=AD_DOMAIN),
        shell=True
    )
    print user, "deleted"

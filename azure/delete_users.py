#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from utils import STUDENT_COUNT, AD_DOMAIN, check_output_wrapper

for idx in range(STUDENT_COUNT):
    user = "student{}".format(idx + 1)
    check_output_wrapper(
        """
        az ad user delete \
        --upn-or-object-id "{u}@{d}" \
        """.format(u=user, d=AD_DOMAIN),
        shell=True
    )
    print(user, "deleted")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json
from utils import timeit
import pandas as pd
import numpy as np


@timeit
def create_image(RG_NAME, IMAGE_NAME, SOURCE, REGION):
    subprocess.check_output(
        """
        az image create \
            -g {RG_NAME} \
            -n {IMAGE_NAME} \
            --source "{SOURCE}" \
            --os-type linux \
            -l {REGION}
        """.format(**locals()),
        shell=True
    )
    create_image_lock(RG_NAME, IMAGE_NAME)
    assign_role_to_student_group(IMAGE_NAME)


@timeit
def create_image_lock(RG_NAME, IMAGE_NAME):
    subprocess.check_output(
        """
        az lock create -t CanNotDelete -n lock -g {RG_NAME} --parent-resource-path "" --resource-name "{IMAGE_NAME}" \
        --resource-provider-namespace "" --resource-type "Microsoft.Compute/images"
        """.format(**locals()),
        shell=True
    )


@timeit
def assign_role_to_student_group(IMAGE_NAME):
    # for students group
    subprocess.check_output(
        """
        az role assignment create \
            --role Contributor \
            --assignee "3cf12edd-00e1-4c10-85a3-7f1b34e57cb4" \
            --scope "/subscriptions/62e31321-0aac-47b0-b396-f7f518e91cb2/resourceGroups/admin_resources/providers/Microsoft.Compute/images/{IMAGE_NAME}"
        """.format(**locals()),
        shell=True
    )


for region in ["eastus", "southcentralus", "westeurope", "southeastasia"]:
    create_image("admin_resources",
                 "ubuntu_gpu_image1_{0}".format(region),
                 "https://lsml1{0}.blob.core.windows.net/images/ubuntugpu.vhd".format(region),
                 region)
    for clIdx in [1, 2, 3]:
        create_image("admin_resources",
                     "cluster{1}_image1_{0}".format(region, clIdx),
                     "https://lsml1{0}.blob.core.windows.net/images/cluster{1}.vhd".format(region, clIdx),
                     region)

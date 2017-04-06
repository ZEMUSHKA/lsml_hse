#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json
from utils import timeit
import pandas as pd
import numpy as np


@timeit
def create_image(RG_NAME, IMAGE_NAME, SOURCE):
    subprocess.check_output(
        """
        az image create \
            -g {RG_NAME} \
            -n {IMAGE_NAME} \
            --source "{SOURCE}" \
            --os-type linux
        """.format(**locals()),
        shell=True
    )
    create_image_lock(RG_NAME, IMAGE_NAME)


@timeit
def create_image_lock(RG_NAME, IMAGE_NAME):
    subprocess.check_output(
        """
        az lock create -t CanNotDelete -n lock -g {RG_NAME} --parent-resource-path "" --resource-name "{IMAGE_NAME}" \
        --resource-provider-namespace "" --resource-type "Microsoft.Compute/images"
        """.format(**locals()),
        shell=True
    )


for region in ["eastus", "southcentralus", "westeurope", "southeastasia"]:
    create_image("admin_resources",
                 "ubuntu_gpu_image1_{0}".format(region),
                 "https://lsml1{0}.blob.core.windows.net/images/ubuntugpu.vhd".format(region))
    for clIdx in [1, 2, 3]:
        create_image("admin_resources",
                     "cluster{1}_image1_{0}".format(region, clIdx),
                     "https://lsml1{0}.blob.core.windows.net/images/cluster{1}.vhd".format(region, clIdx))

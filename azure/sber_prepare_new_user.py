#!/usr/bin/env python
# -*- coding: utf-8 -*-
# switch to sber: az account set --subscription "ФКН ВШЭ"
# switch to sponsored: az account set --subscription "Sponsorship 2017"
import json
import subprocess
from joblib import Parallel, delayed

from utils import get_subscription_id, check_output_wrapper

j = json.load(open("sber.json"))


def make_user(user, settings):
    resource_group = settings["resource_group"]
    storage_account = settings["storage_account"]
    region = settings["region"]

    # create res gr
    check_output_wrapper(
        """
        az group create \
        -n "{n}" \
        -l "{l}"
        """.format(n=resource_group, l=region),
        shell=True
    )

    print("WARN: Add user '{0}' as contributor to '{1}' manually!".format(user, resource_group))
    # # assign user to his res gr
    # check_output_wrapper(
    #     """
    #     az role assignment create \
    #     --assignee {user} \
    #     --role Contributor \
    #     --resource-group {rg}
    #     """.format(user=user, rg=resource_group),
    #     shell=True
    # )

    # create storage account
    check_output_wrapper(
        """
        az storage account create \
        -l {l} \
        -n {n} \
        -g {g} \
        --sku Standard_LRS
        """.format(l=region, n=storage_account, g=resource_group),
        shell=True
    )

    # grant images access
    images = [
        "cluster1_image1_eastus",
        "cluster2_image1_eastus",
        "cluster3_image1_eastus",
        "ubuntu_gpu_image1_eastus"
    ]
    for image in images:
        pass
        # check_output_wrapper(
        #     """
        #     az role assignment create \
        #         --role Contributor \
        #         --assignee "{user}" \
        #         --scope "/subscriptions/{s}/resourceGroups/admin_resources/providers/Microsoft.Compute/images/{image}"
        #     """.format(image=image, user=user, s=get_subscription_id()),
        #     shell=True
        # )
    print("WARN: Add user '{0}' as contributor to 'admin_resources' manually!".format(user))

    print(user, "done")


Parallel(n_jobs=10, backend="threading")(
    delayed(make_user)(user, settings) for user, settings in j.items()
)

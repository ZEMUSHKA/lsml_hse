#!/usr/bin/env python
# -*- coding: utf-8 -*-
# switch to sber: az account set --subscription "ФКН ВШЭ"
# switch to sponsored: az account set --subscription "Sponsorship 2017"
import json
import subprocess

from utils import get_subscription_id

j = json.load(open("sber.json"))

for user, settings in j.iteritems():
    resource_group = settings["resource_group"]
    storage_account = settings["storage_account"]
    region = settings["region"]

    # create res gr
    subprocess.check_output(
        """
        az group create \
        -n "{n}" \
        -l "{l}"
        """.format(n=resource_group, l=region),
        shell=True
    )

    print "WARN: Add user '{0}' as contributor to '{1}' manually!".format(user, resource_group)
    # # assign user to his res gr
    # subprocess.check_output(
    #     """
    #     az role assignment create \
    #     --assignee {user} \
    #     --role Contributor \
    #     --resource-group {rg}
    #     """.format(user=user, rg=resource_group),
    #     shell=True
    # )

    # create storage account
    subprocess.check_output(
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
        print "WARN: Add user '{0}' as contributor to '{1}' manually!".format(user, image)
        # subprocess.check_output(
        #     """
        #     az role assignment create \
        #         --role Contributor \
        #         --assignee "{user}" \
        #         --scope "/subscriptions/{s}/resourceGroups/admin_resources/providers/Microsoft.Compute/images/{image}"
        #     """.format(image=image, user=user, s=get_subscription_id()),
        #     shell=True
        # )

    print user, "done"

##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from joblib import Parallel, delayed

import utils
from utils import VNET_NAME, SUBNET_NAME, NSG_NAME, cloud_init_fill_template, CLUSTER_IMAGE, RG_NAME, REGION, CLUSTER_VM

parser = argparse.ArgumentParser()
parser.add_argument("--create_shared", action="store_true", help="create shared resources")
parser.add_argument("--create_aux", action="store_true", help="create aux resources, only once per script run")
parser.add_argument("--jobs", type=int, action="store", help="number of parallel jobs")
args = parser.parse_args()

VM_SIZE = "Standard_E4_v3"

RESIZE_OS_DISK = False
OS_DISK_SIZE = 511

if args.create_shared:
    utils.create_shared(RG_NAME, REGION, VNET_NAME, NSG_NAME, SUBNET_NAME)


def create_cluster_node(idx, user_pass):
    IP_NAME = "ip_cluster{0}".format(idx)
    NIC_NAME = "nic_cluster{0}".format(idx)
    INT_DNS_NAME = CLUSTER_VM.format(idx)
    OS_DISK_NAME = "cluster{0}_os_disk".format(idx)
    VM_NAME = INT_DNS_NAME
    IP = "10.0.1.2{0}".format(idx)

    if idx != 1:
        IP_NAME = None

    if args.create_aux:
        # create public IP
        if IP_NAME is not None:
            utils.create_public_ip(IP_NAME, RG_NAME)

        # Create network card with fixed private IP
        utils.create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP)

    # create VM https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-windows-sizes
    IMAGE_NAME = "/subscriptions/" + utils.get_subscription_id() + \
                 "/resourceGroups/" + RG_NAME + "/providers/Microsoft.Compute/images/" + \
                 CLUSTER_IMAGE.format(idx)
    data_disks = "255 255 255 255"

    if idx == 1:
        cloud_init_fn = cloud_init_fill_template("configs/cloud_init_cluster_master_template.txt", user_pass)
    else:
        cloud_init_fn = "configs/cloud_init_cluster_slave.txt"
    utils.create_vm(VM_NAME, RG_NAME, REGION, IMAGE_NAME, NIC_NAME, VM_SIZE, None, OS_DISK_NAME,
                    user_pass, cloud_init_fn, data_disks, "Standard_LRS")

    if RESIZE_OS_DISK:
        utils.deallocate_vm(VM_NAME, RG_NAME)
        utils.resize_managed_disk(RG_NAME, OS_DISK_NAME, OS_DISK_SIZE)
        utils.start_vm(VM_NAME, RG_NAME)


user_pass = utils.generate_pass()
Parallel(n_jobs=args.jobs or 3, backend="threading")(
    delayed(create_cluster_node)(idx, user_pass) for idx in [1, 2, 3]
)

print("cluster1 public IP: {}".format(utils.get_public_ip("ip_cluster1", RG_NAME)))
print("password:", user_pass)

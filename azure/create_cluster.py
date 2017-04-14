##!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, VNET_NAME, SUBNET_NAME, NSG_NAME, region_by_user
import argparse
from joblib import Parallel, delayed

parser = argparse.ArgumentParser()
parser.add_argument("--user", action="store", help="account name, for example student1", required=True)
parser.add_argument("--ssh_key", action="store", help="ssh public key, for example ~/.ssh/id_rsa_azure.pub",
                    required=True)
parser.add_argument("--create_shared", action="store_true", help="create shared resources")
parser.add_argument("--create_aux", action="store_true", help="create aux resources, only once per script run")
args = parser.parse_args()

STUDENT_NAME = args.user
RG_NAME = RG_TEMPLATE.format(STUDENT_NAME)
STORAGE_ACCOUNT = STORAGE_ACCOUNT_TEMPLATE.format(STUDENT_NAME)
region = region_by_user[STUDENT_NAME]

CREATE_VM_FROM_IMAGE = True
RESIZE_OS_DISK = False
OS_DISK_SIZE = 511

if args.create_shared:
    # create vnet and subnet
    utils.create_vnet(VNET_NAME, RG_NAME, region, SUBNET_NAME)

    # create network security group
    utils.create_nsg(NSG_NAME, RG_NAME, region)

    # create SSH and Jupyter rules
    utils.allow_incoming_port(NSG_NAME, RG_NAME, "allow_ssh", 22, 1000)


def create_cluster_node(idx):
    IP_NAME = "ip_cluster{0}".format(idx)
    NIC_NAME = "nic_cluster{0}".format(idx)
    INT_DNS_NAME = "cluster{0}".format(idx)
    OS_DISK_NAME = "cluster{0}_os_disk".format(idx)
    VM_NAME = INT_DNS_NAME
    IP = "10.0.1.2{0}".format(idx)

    if args.create_aux:
        # create public IP
        utils.create_public_ip(IP_NAME, RG_NAME)

        # Create network card with fixed private IP
        utils.create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP)

    # create VM
    VM_SIZE = "Standard_D12_v2"  # https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-windows-sizes
    PUB_KEY = args.ssh_key

    if CREATE_VM_FROM_IMAGE:
        IMAGE_NAME = "/subscriptions/" + utils.get_subscription_id() + \
                     "/resourceGroups/admin_resources/providers/Microsoft.Compute/images/" + \
                     "cluster{0}".format(idx) + "_image1_" + region
        data_disks = "127 127 127 127 127 127 127 127"
        if idx == 1:
            cloud_init_fn = "cloud_init_cluster_master.txt"
        else:
            cloud_init_fn = "cloud_init_cluster_slave.txt"
        utils.create_vm(VM_NAME, RG_NAME, region, IMAGE_NAME, NIC_NAME, VM_SIZE, PUB_KEY, OS_DISK_NAME,
                        cloud_init_fn, data_disks)
    else:
        IMAGE_NAME = "Canonical:UbuntuServer:14.04.4-LTS:latest"
        utils.create_vm(VM_NAME, RG_NAME, region, IMAGE_NAME, NIC_NAME, VM_SIZE, PUB_KEY, OS_DISK_NAME)

    if RESIZE_OS_DISK:
        utils.deallocate_vm(VM_NAME, RG_NAME)
        utils.resize_managed_disk(RG_NAME, OS_DISK_NAME, OS_DISK_SIZE)
        utils.start_vm(VM_NAME, RG_NAME)

Parallel(n_jobs=3, backend="threading")(
    delayed(create_cluster_node)(idx) for idx in [1, 2, 3]
)

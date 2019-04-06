##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import utils
from utils import VNET_NAME, SUBNET_NAME, NSG_NAME, cloud_init_fill_template, RG_NAME, REGION, UBUNTUGPU_IMAGE

parser = argparse.ArgumentParser()
parser.add_argument("--create_shared", action="store_true", help="create shared resources")
parser.add_argument("--create_aux", action="store_true", help="create aux resources, only once per script run")
args = parser.parse_args()

VM_SIZE = "Standard_NC6"

RESIZE_OS_DISK = False
OS_DISK_SIZE = 1023

if args.create_shared:
    utils.create_shared(RG_NAME, REGION)

IP_NAME = "ip_ubuntugpu"
NIC_NAME = "nic_ubuntugpu"
INT_DNS_NAME = "ubuntugpu"
OS_DISK_NAME = "ubuntugpu_os_disk"
IP = "10.0.1.10"

if args.create_aux:
    # create public IP
    utils.create_public_ip(IP_NAME, RG_NAME)

    # Create network card with fixed private IP
    utils.create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP)

# create VM
VM_NAME = INT_DNS_NAME

IMAGE_NAME = "/subscriptions/" + utils.get_subscription_id() + \
             "/resourceGroups/" + RG_NAME + "/providers/Microsoft.Compute/images/" + UBUNTUGPU_IMAGE
data_disks = "255 255 255 255"

user_pass = utils.generate_pass()
cloud_init_fn = cloud_init_fill_template("configs/cloud_init_ubuntugpu_template.txt", user_pass)
utils.create_vm(VM_NAME, RG_NAME, REGION, IMAGE_NAME, NIC_NAME, VM_SIZE, None, OS_DISK_NAME,
                user_pass, cloud_init_fn, data_disks)

if RESIZE_OS_DISK:
    utils.deallocate_vm(VM_NAME, RG_NAME)
    utils.resize_managed_disk(RG_NAME, OS_DISK_NAME, OS_DISK_SIZE)
    utils.start_vm(VM_NAME, RG_NAME)

print("ubuntugpu public IP: {}".format(utils.get_public_ip(IP_NAME, RG_NAME)))
print("password:", user_pass)

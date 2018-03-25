##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import utils
from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, VNET_NAME, SUBNET_NAME, NSG_NAME, region_by_user, \
    gpus_by_user, cloud_init_fill_template

parser = argparse.ArgumentParser()
parser.add_argument("--user", action="store", help="account name, for example student1", required=True)
parser.add_argument("--create_shared", action="store_true", help="create shared resources")
parser.add_argument("--create_aux", action="store_true", help="create aux resources, only once per script run")
args = parser.parse_args()

student_name = args.user
rg_name = RG_TEMPLATE.format(student_name)
storage_account = STORAGE_ACCOUNT_TEMPLATE.format(student_name)
region = region_by_user[student_name]

RESIZE_OS_DISK = False
OS_DISK_SIZE = 1023

if args.create_shared:
    utils.create_shared(rg_name, region)

IP_NAME = "ip_ubuntugpu"
NIC_NAME = "nic_ubuntugpu"
INT_DNS_NAME = "ubuntugpu"
OS_DISK_NAME = "ubuntugpu_os_disk"
IP = "10.0.1.10"

if args.create_aux:
    # create public IP
    utils.create_public_ip(IP_NAME, rg_name)

    # Create network card with fixed private IP
    utils.create_nic_with_private_ip(NIC_NAME, rg_name, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP)

# create VM
VM_NAME = INT_DNS_NAME
vm_size = gpus_by_user[student_name]

IMAGE_NAME = "/subscriptions/" + utils.get_subscription_id() + \
             "/resourceGroups/admin_resources/providers/Microsoft.Compute/images/ubuntu_gpu_image1_" + region
data_disks = "255 255 255 255"

user_pass = utils.generate_pass()
cloud_init_fn = cloud_init_fill_template("configs/cloud_init_ubuntugpu_template.txt", user_pass)
utils.create_vm(VM_NAME, rg_name, region, IMAGE_NAME, NIC_NAME, vm_size, None, OS_DISK_NAME,
                user_pass, cloud_init_fn, data_disks)

if RESIZE_OS_DISK:
    utils.deallocate_vm(VM_NAME, rg_name)
    utils.resize_managed_disk(rg_name, OS_DISK_NAME, OS_DISK_SIZE)
    utils.start_vm(VM_NAME, rg_name)

print "ubuntugpu public IP: {}".format(utils.get_public_ip("ip_ubuntugpu", rg_name))
print "password:", user_pass

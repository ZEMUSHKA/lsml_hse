##!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, VNET_NAME, SUBNET_NAME, NSG_NAME, region_by_user, gpus_by_user
import argparse

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
RESIZE_OS_DISK = True
OS_DISK_SIZE = 1000

if args.create_shared:
    # create vnet and subnet
    utils.create_vnet(VNET_NAME, RG_NAME, region, SUBNET_NAME)

    # create network security group
    utils.create_nsg(NSG_NAME, RG_NAME, region)

    # create SSH rule
    utils.allow_incoming_port(NSG_NAME, RG_NAME, "allow_ssh", 22, 1000)

IP_NAME = "ip_ubuntugpu"
NIC_NAME = "nic_ubuntugpu"
INT_DNS_NAME = "ubuntugpu"
IP = "10.0.1.10"

if args.create_aux:
    # create public IP
    utils.create_public_ip(IP_NAME, RG_NAME)

    # Create network card with fixed private IP
    utils.create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP)

# create VM
VM_NAME = INT_DNS_NAME
VM_SIZE = gpus_by_user[STUDENT_NAME]
PUB_KEY = args.ssh_key

if CREATE_VM_FROM_IMAGE:
    IMAGE_NAME = "ubuntugpu.vhd"
    utils.create_vm_from_image(VM_NAME, RG_NAME, region, NIC_NAME, IP_NAME, STORAGE_ACCOUNT, VM_SIZE, PUB_KEY, IMAGE_NAME, NSG_NAME)
else:
    pass

if RESIZE_OS_DISK:
    utils.deallocate_vm(VM_NAME, RG_NAME)
    utils.resize_os_disk(RG_NAME, VM_NAME, OS_DISK_SIZE)
    utils.start_vm(VM_NAME, RG_NAME)
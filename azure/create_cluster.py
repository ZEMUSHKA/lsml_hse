##!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
from utils import RG_TEMPLATE, STORAGE_ACCOUNT_TEMPLATE, VNET_NAME, SUBNET_NAME, NSG_NAME, region_by_user

STUDENT_NAME = "admin"
RG_NAME = RG_TEMPLATE.format(STUDENT_NAME)
STORAGE_ACCOUNT = STORAGE_ACCOUNT_TEMPLATE.format(STUDENT_NAME)
region = region_by_user[STUDENT_NAME]

CREATE_AUX_RESOURCES = False
CREATE_VM_FROM_IMAGE = True
RESIZE_OS_DISK = True
OS_DISK_SIZE = 500

if CREATE_AUX_RESOURCES:
    # create vnet and subnet
    utils.create_vnet(VNET_NAME, RG_NAME, region, SUBNET_NAME)

    # create network security group
    utils.create_nsg(NSG_NAME, RG_NAME, region)

    # create SSH and Jupyter rules
    utils.allow_incoming_port(NSG_NAME, RG_NAME, "allow_ssh", 22, 1000)

for idx in [1, 2, 3]:
    IP_NAME = "ip_cluster{0}".format(idx)
    NIC_NAME = "nic_cluster{0}".format(idx)
    INT_DNS_NAME = "cluster{0}".format(idx)
    VM_NAME = INT_DNS_NAME
    IP = "10.0.1.2{0}".format(idx)

    if CREATE_AUX_RESOURCES:
        # create public IP
        utils.create_public_ip(IP_NAME, RG_NAME)

        # Create network card with fixed private IP
        utils.create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP)

    # create VM
    VM_SIZE = "Standard_D12_v2"  # https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-windows-sizes
    PUB_KEY = "~/.ssh/id_rsa_azure.pub"
    DISK_SIZE = 1

    if CREATE_VM_FROM_IMAGE:
        IMAGE_NAME = "cluster{0}.vhd".format(idx)
        utils.create_vm_from_image(VM_NAME, RG_NAME, region, NIC_NAME, IP_NAME, STORAGE_ACCOUNT, VM_SIZE, PUB_KEY,
                                   DISK_SIZE, IMAGE_NAME)
    else:
        IMAGE_URN = "Canonical:UbuntuServer:14.04.4-LTS:latest"
        utils.create_vm(VM_NAME, RG_NAME, region, NIC_NAME, IP_NAME, STORAGE_ACCOUNT, VM_SIZE, PUB_KEY, IMAGE_URN,
                        NSG_NAME)

    if RESIZE_OS_DISK:
        utils.deallocate_vm(VM_NAME, RG_NAME)
        utils.resize_os_disk(RG_NAME, VM_NAME, OS_DISK_SIZE)
        utils.start_vm(VM_NAME, RG_NAME)
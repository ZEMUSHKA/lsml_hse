##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from joblib import Parallel, delayed

import utils
from utils import VNET_NAME, SUBNET_NAME, NSG_NAME, cloud_init_fill_template

parser = argparse.ArgumentParser()
parser.add_argument("--create_shared", action="store_true", help="create shared resources")
parser.add_argument("--create_aux", action="store_true", help="create aux resources, only once per script run")
args = parser.parse_args()

N_MACHINES = 13

student_name = "sirius"
rg_name = utils.get_student_resource_group(student_name)
storage_account = utils.get_student_storage_account(student_name)
region = utils.get_student_region(student_name)
vm_size = utils.get_student_gpu_size(student_name)

if args.create_shared:
    utils.create_shared(rg_name, region)

IP_NAME = "ip_ubuntugpu{}"
NIC_NAME = "nic_ubuntugpu{}"
INT_DNS_NAME = "ubuntugpu{}"
OS_DISK_NAME = "ubuntugpu_os_disk{}"
IP = "10.0.1.{}"


def create_aux(idx):
    # create public IP
    utils.create_public_ip(IP_NAME.format(idx), rg_name)

    # Create network card with fixed private IP
    utils.create_nic_with_private_ip(NIC_NAME.format(idx), rg_name,
                                     VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME.format(idx),
                                     INT_DNS_NAME.format(idx), IP.format(idx+10))


if args.create_aux:
    Parallel(n_jobs=5, backend="threading")(
        delayed(create_aux)(idx) for idx in range(N_MACHINES)
    )


def create_vm(idx, password):
    VM_NAME = INT_DNS_NAME.format(idx)

    IMAGE_NAME = "/subscriptions/" + utils.get_subscription_id() + \
                 "/resourceGroups/admin_resources/providers/Microsoft.Compute/images/ubuntu_gpu_image1_" + region
    data_disks = "255 255 255 255"

    user_pass = password
    cloud_init_fn = cloud_init_fill_template("configs/cloud_init_sirius_template.txt", user_pass, postfix=str(idx))
    utils.create_vm(VM_NAME, rg_name, region, IMAGE_NAME, NIC_NAME.format(idx), vm_size, None, OS_DISK_NAME.format(idx),
                    user_pass, cloud_init_fn, data_disks)

    print("{} public IP: {}".format(VM_NAME, utils.get_public_ip(IP_NAME.format(idx), rg_name)))


# create VMs
password = utils.generate_pass()
print("password:", password)
Parallel(n_jobs=5, backend="threading")(
    delayed(create_vm)(idx, password) for idx in range(N_MACHINES)
)

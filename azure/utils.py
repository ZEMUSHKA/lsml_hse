#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json
import time

RG_TEMPLATE = "{0}_resources"
STORAGE_ACCOUNT_TEMPLATE = "{0}lsmlhse645221"
VNET_NAME = "network"
SUBNET_NAME = "subnet"
NSG_NAME = "security_group"

region_by_user = json.loads(open("regions.json", "r").read())
gpus_by_user = json.loads(open("gpus.json", "r").read())


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts)
        return result
    return timed


@timeit
def get_storage_key(account, rg):
    out = subprocess.check_output(
        """
        az storage account keys list \
            --name {n} \
            --resource-group {g}
        """.format(n=account, g=rg),
        shell=True
    )
    out = json.loads(out)
    key = out["keys"][0]["value"]
    return key


@timeit
def create_vnet(VNET_NAME, RG_NAME, REGION, SUBNET_NAME):
    subprocess.check_output(
        """
        az network vnet create \
            -n {VNET_NAME} \
            -g {RG_NAME} \
            -l {REGION} \
            --address-prefix 10.0.0.0/16 \
            --subnet-name {SUBNET_NAME} \
            --subnet-prefix 10.0.1.0/24
        """.format(**locals()),
        shell=True
    )


@timeit
def create_nsg(NSG_NAME, RG_NAME, REGION):
    subprocess.check_output(
        """
        az network nsg create \
            -n {NSG_NAME} \
            -g {RG_NAME} \
            -l {REGION}
        """.format(**locals()),
        shell=True
    )


@timeit
def allow_incoming_port(NSG_NAME, RG_NAME, RULE_NAME, PORT, PRIORITY):
    subprocess.check_output(
        """
        az network nsg rule create \
            --access Allow \
            --nsg-name {NSG_NAME} \
            -g {RG_NAME} \
            --protocol Tcp \
            --name {RULE_NAME} \
            --source-address-prefix "*" \
            --source-port-range "*" \
            --direction InBound \
            --destination-port-range {PORT} \
            --destination-address-prefix "*" \
            --priority {PRIORITY}
        """.format(**locals()),
        shell=True
    )


@timeit
def create_public_ip(IP_NAME, RG_NAME):
    subprocess.check_output(
        """
        az network public-ip create \
            -n {IP_NAME} \
            -g {RG_NAME}
        """.format(**locals()),
        shell=True
    )


@timeit
def create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP):
    subprocess.check_output(
        """
        az network nic create \
            -n {NIC_NAME} \
            -g {RG_NAME} \
            --vnet-name {VNET_NAME} \
            --subnet {SUBNET_NAME} \
            --network-security-group {NSG_NAME} \
            --public-ip-address {IP_NAME} \
            --internal-dns-name {INT_DNS_NAME} \
            --private-ip-address {IP}
        """.format(**locals()),
        shell=True
    )


@timeit
def create_vm(VM_NAME, RG_NAME, REGION, IMAGE_NAME, NIC_NAME, VM_SIZE, PUB_KEY, OS_DISK_NAME):
    subprocess.check_output(
        """
        az vm create \
            -n {VM_NAME} \
            -g {RG_NAME} \
            -l {REGION} \
            --admin-username ubuntu \
            --image "{IMAGE_NAME}" \
            --nics {NIC_NAME} \
            --size {VM_SIZE} \
            --ssh-key-value {PUB_KEY} \
            --os-disk-name {OS_DISK_NAME} \
            --authentication-type ssh \
            --storage-sku Standard_LRS \
            --storage-caching "ReadWrite"
        """.format(**locals()),
        shell=True
    )


# @timeit
def deallocate_vm(VM_NAME, RG_NAME):
    subprocess.check_output(
        """
        az vm deallocate \
            -g {RG_NAME} \
            -n {VM_NAME}
        """.format(**locals()),
        shell=True
    )


# @timeit
def start_vm(VM_NAME, RG_NAME):
    subprocess.check_output(
        """
        az vm start \
            -g {RG_NAME} \
            -n {VM_NAME}
        """.format(**locals()),
        shell=True
    )


@timeit
def resize_managed_disk(RG_NAME, DISK_NAME, DISK_SIZE):
    subprocess.check_output(
        """
        az disk update \
            --resource-group {RG_NAME} \
            --name {DISK_NAME} \
            --size-gb {DISK_SIZE}
        """.format(**locals()),
        shell=True
    )


@timeit
def get_subscription_id():
    out = subprocess.check_output(
        """
        az account list
        """,
        shell=True
    )
    out = json.loads(out)
    out = filter(lambda x: x["isDefault"], out)[0]
    return out["id"]

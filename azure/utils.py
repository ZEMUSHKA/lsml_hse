#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json

REGION = "eastus"
RG_TEMPLATE = "{0}_resources"
STORAGE_ACCOUNT_TEMPLATE = "{0}lsmlhse645221"
VNET_NAME = "network"
SUBNET_NAME = "subnet"
NSG_NAME = "security_group"


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


def create_nsg(NSG_NAME, RG_NAME, REGION):
    subprocess.check_output(
        """
        az network nsg create \
            -n {NSG_NAME} \
            -g {RG_NAME} \
            -l {REGION}
        """.format(**locals())
    )


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


def create_public_ip(IP_NAME, RG_NAME):
    subprocess.check_output(
        """
        az network public-ip create \
            -n {IP_NAME} \
            -g {RG_NAME}
        """.format(**locals()),
        shell=True
    )


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


def create_vm_from_image(VM_NAME, RG_NAME, REGION, NIC_NAME, IP_NAME, STORAGE_ACCOUNT, VM_SIZE, PUB_KEY, DISK_SIZE, IMAGE_NAME):
    subprocess.check_output(
        """
        azure vm create \
            -n {VM_NAME} \
            -g {RG_NAME} \
            -l {REGION} \
            -u ubuntu \
            -p $(cat ssh_pass.txt) \
            --image-urn "https://"{STORAGE_ACCOUNT}".blob.core.windows.net/images/{IMAGE_NAME}" \
            --nic-names {NIC_NAME} \
            --public-ip-name {IP_NAME} \
            --storage-account-name {STORAGE_ACCOUNT} \
            --vm-size {VM_SIZE} \
            --ssh-publickey-file {PUB_KEY} \
            --os-type Linux \
            --data-disk-size {DISK_SIZE}
        """.format(**locals()),
        shell=True
    )

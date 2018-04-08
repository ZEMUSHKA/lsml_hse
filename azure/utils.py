#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
import string
import subprocess
import time

STUDENT_COUNT = 98
AD_DOMAIN = "zimovnovgmail.onmicrosoft.com"
AD_GROUP = "students"

RG_TEMPLATE = "{0}_resources"
STORAGE_ACCOUNT_TEMPLATE = "{0}lsmlhse645221"
VNET_NAME = "network"
SUBNET_NAME = "subnet"
NSG_NAME = "security_group"

region_by_user = json.loads(open("regions.json", "r").read())
gpus_by_user = json.loads(open("gpus.json", "r").read())


def load_sber_users():
    return json.load(open("sber.json"))


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result
    return timed


@timeit
def get_storage_key(account, rg):
    out = check_output_wrapper(
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
    check_output_wrapper(
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
    check_output_wrapper(
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
    check_output_wrapper(
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
    check_output_wrapper(
        """
        az network public-ip create \
            -n {IP_NAME} \
            -g {RG_NAME}
        """.format(**locals()),
        shell=True
    )


@timeit
def create_nic_with_private_ip(NIC_NAME, RG_NAME, VNET_NAME, SUBNET_NAME, NSG_NAME, IP_NAME, INT_DNS_NAME, IP):
    template = """
        az network nic create \
            -n {NIC_NAME} \
            -g {RG_NAME} \
            --vnet-name {VNET_NAME} \
            --subnet {SUBNET_NAME} \
            --network-security-group {NSG_NAME} \
            --internal-dns-name {INT_DNS_NAME} \
            --private-ip-address {IP} """
    if IP_NAME is not None:
        template += " --public-ip-address {IP_NAME} "
    check_output_wrapper(
        template.format(**locals()),
        shell=True
    )


@timeit
def create_vm(VM_NAME, RG_NAME, REGION, IMAGE_NAME, NIC_NAME, VM_SIZE, pub_key, OS_DISK_NAME,
              password, cloud_init_fn=None, data_disks=None, storage_type="Standard_LRS"):
    template = \
        """
        az vm create \
            -n {VM_NAME} \
            -g {RG_NAME} \
            -l {REGION} \
            --admin-username ubuntu \
            --image "{IMAGE_NAME}" \
            --nics {NIC_NAME} \
            --size {VM_SIZE} \
            --os-disk-name {OS_DISK_NAME} \
            --storage-sku {storage_type} \
            --storage-caching "ReadWrite" """

    if data_disks is not None:
        template += " --data-disk-sizes-gb {0} ".format(data_disks)
    if cloud_init_fn is not None:
        template += ' --custom-data "{0}" '.format(cloud_init_fn)

    if pub_key is not None:
        template += " --authentication-type ssh --ssh-key-value {0} ".format(pub_key)
    else:
        template += " --authentication-type password --admin-password {0}".format(password)

    check_output_wrapper(
        template.format(**locals()),
        shell=True
    )


# @timeit
def deallocate_vm(VM_NAME, RG_NAME):
    check_output_wrapper(
        """
        az vm deallocate \
            -g {RG_NAME} \
            -n {VM_NAME}
        """.format(**locals()),
        shell=True
    )


# @timeit
def start_vm(VM_NAME, RG_NAME):
    check_output_wrapper(
        """
        az vm start \
            -g {RG_NAME} \
            -n {VM_NAME}
        """.format(**locals()),
        shell=True
    )


def remove_vm(VM_NAME, RG_NAME):
    check_output_wrapper(
        """
        az vm delete \
            -g {RG_NAME} \
            -n {VM_NAME} \
            --yes
        """.format(**locals()),
        shell=True
    )


def remove_vm_and_disks(VM_NAME, RG_NAME):
    out = check_output_wrapper(
        """
        az vm list \
            -g {RG_NAME}
        """.format(**locals()),
        shell=True
    )
    out = json.loads(out)
    vm = [x for x in out if x["name"] == VM_NAME]
    assert len(vm) == 1
    vm = vm[0]
    storageProfile = vm["storageProfile"]
    data_disk_ids = [x.get("managedDisk", {}).get("id", None) for x in storageProfile.get("dataDisks", [])]
    os_disk_id = storageProfile.get("osDisk", {}).get("managedDisk", {}).get("id", None)
    all_disk_ids = data_disk_ids + [os_disk_id]
    all_disk_ids = [x for x in all_disk_ids if x is not None]

    print("Will delete disks:\n" + "\n".join(all_disk_ids))

    print("Removing VM...")
    remove_vm(VM_NAME, RG_NAME)

    print("Removing disks...")
    remove_disks(all_disk_ids)


def remove_disks(all_disk_ids):
    check_output_wrapper(
        """
        az disk delete \
            --ids {0} --yes
        """.format(" ".join(all_disk_ids)),
        shell=True
    )


@timeit
def resize_managed_disk(RG_NAME, DISK_NAME, DISK_SIZE):
    check_output_wrapper(
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
    out = check_output_wrapper(
        """
        az account list
        """,
        shell=True
    )
    out = json.loads(out)
    out = [x for x in out if x["isDefault"]][0]
    return out["id"]


@timeit
def create_shared(RG_NAME, region):
    # create vnet and subnet
    create_vnet(VNET_NAME, RG_NAME, region, SUBNET_NAME)

    # create network security group
    create_nsg(NSG_NAME, RG_NAME, region)

    # firewall rules
    allow_incoming_port(NSG_NAME, RG_NAME, "allow_ssh", 22, 1000)
    allow_incoming_port(NSG_NAME, RG_NAME, "allow_squid", 3128, 1010)
    allow_incoming_port(NSG_NAME, RG_NAME, "allow_jupyter", 9999, 1020)


def get_public_ip(IP_NAME, RG_NAME):
    out = check_output_wrapper(
        """
        az network public-ip show -n {IP_NAME} -g {RG_NAME}
        """.format(**locals()),
        shell=True
    )
    out = json.loads(out)
    return out["ipAddress"]


def resize_VM(VM_NAME, RG_NAME, NEW_SIZE):
    check_output_wrapper(
        """
        az vm resize \
        --resource-group {RG_NAME} \
        --name {VM_NAME} \
        --size {NEW_SIZE}
        """.format(**locals()),
        shell=True
    )


def generate_pass():
    numbers = [random.choice(string.digits) for _ in range(2)]
    big_letters = [random.choice(string.ascii_uppercase) for _ in range(7)]
    small_letters = [random.choice(string.ascii_lowercase) for _ in range(7)]
    p = numbers + big_letters + small_letters
    random.shuffle(p)
    return ''.join(p)


def get_ad_group_id(ad_group):
    out = check_output_wrapper(
        """
        az ad group show --group {g}
        """.format(g=ad_group),
        shell=True
    )
    out = json.loads(out)
    return out["objectId"]


def cloud_init_fill_template(template_fn, user_pass):
    result_fn = template_fn + "_filled.txt"
    with open(result_fn, "w") as f:
        f.write(open(template_fn).read().replace("###PASSWORD###", user_pass))
    return result_fn


def get_student_resource_group(student_name):
    if "@" in student_name:
        return load_sber_users()[student_name]["resource_group"]
    else:
        return RG_TEMPLATE.format(student_name)


def get_student_storage_account(student_name):
    if "@" in student_name:
        return load_sber_users()[student_name]["storage_account"]
    else:
        return STORAGE_ACCOUNT_TEMPLATE.format(student_name)


def get_student_region(student_name):
    if "@" in student_name:
        return load_sber_users()[student_name]["region"]
    else:
        return region_by_user[student_name]


def get_student_gpu_size(student_name):
    if "@" in student_name:
        return load_sber_users()[student_name]["gpu"]
    else:
        return gpus_by_user[student_name]


def check_output_wrapper(command, shell):
    # fix for windows
    return subprocess.check_output(
        command.strip() if isinstance(command, str) else command,
        shell=shell
    )


def list_disks_for_rg(RG):
    out = check_output_wrapper(
        """
        az disk list -g {0}
        """.format(RG),
        shell=True
    )
    if out == "":
        return []
    out = json.loads(out)
    return out


def remove_orphaned_disks(rg_name):
    disks = list_disks_for_rg(rg_name)
    disks = [x for x in disks if x["managedBy"] is None]
    disks = [x["id"] for x in disks]
    if disks:
        print("Removing orphaned disks:")
        for disk in disks:
            print(disk)
        remove_disks(disks)

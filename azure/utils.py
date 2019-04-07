#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
import string
import subprocess
import time

RG_NAME = "my_resources"
REGION = "eastus"

VNET_NAME = "network"
SUBNET_NAME = "subnet"
NSG_NAME = "security_group"

CLUSTER_VM = "cluster{0}"
UBUNTUGPU_VM = "ubuntugpu"

CLUSTER_IMAGE = CLUSTER_VM + "_image"
UBUNTUGPU_IMAGE = UBUNTUGPU_VM + "_image"


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts))
        return result
    return timed


@timeit
def get_storage_key(storage_account, rg_name):
    out = check_output_wrapper(
        """
        az storage account keys list \
            --name {storage_account} \
            --resource-group {rg_name}
        """.format(**locals()),
        shell=True
    )
    out = json.loads(out)
    key = out["keys"][0]["value"]
    return key


@timeit
def create_vnet(vnet_name, rg_name, region, subnet_name):
    check_output_wrapper(
        """
        az network vnet create \
            -n {vnet_name} \
            -g {rg_name} \
            -l {region} \
            --address-prefix 10.0.0.0/16 \
            --subnet-name {subnet_name} \
            --subnet-prefix 10.0.1.0/24
        """.format(**locals()),
        shell=True
    )


@timeit
def create_nsg(nsg_name, rg_name, region):
    check_output_wrapper(
        """
        az network nsg create \
            -n {nsg_name} \
            -g {rg_name} \
            -l {region}
        """.format(**locals()),
        shell=True
    )


@timeit
def allow_incoming_port(nsg_name, rg_name, rule_name, port, priority):
    check_output_wrapper(
        """
        az network nsg rule create \
            --access Allow \
            --nsg-name {nsg_name} \
            -g {rg_name} \
            --protocol Tcp \
            --name {rule_name} \
            --source-address-prefix "*" \
            --source-port-range "*" \
            --direction InBound \
            --destination-port-range {port} \
            --destination-address-prefix "*" \
            --priority {priority}
        """.format(**locals()),
        shell=True
    )


@timeit
def create_public_ip(ip_name, rg_name):
    check_output_wrapper(
        """
        az network public-ip create \
            -n {ip_name} \
            -g {rg_name}
        """.format(**locals()),
        shell=True
    )


@timeit
def create_nic_with_private_ip(nic_name, rg_name, vnet_name, subnet_name, nsg_name, ip_name, int_dns_name, ip):
    template = """
        az network nic create \
            -n {nic_name} \
            -g {rg_name} \
            --vnet-name {vnet_name} \
            --subnet {subnet_name} \
            --network-security-group {nsg_name} \
            --internal-dns-name {int_dns_name} \
            --private-ip-address {ip} """
    if ip_name is not None:
        template += " --public-ip-address {ip_name} "
    check_output_wrapper(
        template.format(**locals()),
        shell=True
    )


@timeit
def create_vm(vm_name, rg_name, region, image_name, nic_name, vm_size, pub_key, os_disk_name,
              password, cloud_init_fn=None, data_disks=None, storage_type="Standard_LRS"):
    template = \
        """
        az vm create \
            -n {vm_name} \
            -g {rg_name} \
            -l {region} \
            --admin-username ubuntu \
            --image "{image_name}" \
            --nics {nic_name} \
            --size {vm_size} \
            --os-disk-name {os_disk_name} \
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
def deallocate_vm(vm_name, rg_name):
    check_output_wrapper(
        """
        az vm deallocate \
            -g {rg_name} \
            -n {vm_name}
        """.format(**locals()),
        shell=True
    )


# @timeit
def start_vm(vm_name, rg_name):
    check_output_wrapper(
        """
        az vm start \
            -g {rg_name} \
            -n {vm_name}
        """.format(**locals()),
        shell=True
    )


def remove_vm(vm_name, rg_name):
    check_output_wrapper(
        """
        az vm delete \
            -g {rg_name} \
            -n {vm_name} \
            --yes
        """.format(**locals()),
        shell=True
    )


def remove_vm_and_disks(vm_name, rg_name):
    out = check_output_wrapper(
        """
        az vm list \
            -g {rg_name}
        """.format(**locals()),
        shell=True
    )
    out = json.loads(out)
    vm = [x for x in out if x["name"] == vm_name]
    assert len(vm) == 1
    vm = vm[0]
    storageProfile = vm["storageProfile"]
    data_disk_ids = [x.get("managedDisk", {}).get("id", None) for x in storageProfile.get("dataDisks", [])]
    os_disk_id = storageProfile.get("osDisk", {}).get("managedDisk", {}).get("id", None)
    all_disk_ids = data_disk_ids + [os_disk_id]
    all_disk_ids = [x for x in all_disk_ids if x is not None]

    print("Will delete disks:\n" + "\n".join(all_disk_ids))

    print("Removing VM...")
    remove_vm(vm_name, rg_name)

    print("Removing disks...")
    remove_disks(all_disk_ids)


def remove_disks(all_disk_ids):
    if not all_disk_ids:
        return
    check_output_wrapper(
        """
        az disk delete \
            --ids {0} --yes
        """.format(" ".join(all_disk_ids)),
        shell=True
    )


@timeit
def resize_managed_disk(rg_name, disk_name, disk_size):
    check_output_wrapper(
        """
        az disk update \
            --resource-group {rg_name} \
            --name {disk_name} \
            --size-gb {disk_size}
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
def create_shared(rg_name, region, vnet_name, nsg_name, subnet_name):
    # create vnet and subnet
    create_vnet(vnet_name, rg_name, region, subnet_name)

    # create network security group
    create_nsg(nsg_name, rg_name, region)

    # firewall rules
    allow_incoming_port(nsg_name, rg_name, "allow_ssh", 22, 1000)
    allow_incoming_port(nsg_name, rg_name, "allow_squid", 3128, 1010)
    allow_incoming_port(nsg_name, rg_name, "allow_jupyter", 9999, 1020)


def get_public_ip(ip_name, rg_name):
    out = check_output_wrapper(
        """
        az network public-ip show -n {ip_name} -g {rg_name}
        """.format(**locals()),
        shell=True
    )
    out = json.loads(out)
    return out["ipAddress"]


def resize_vm(vm_name, rg_name, new_size):
    check_output_wrapper(
        """
        az vm resize \
        --resource-group {rg_name} \
        --name {vm_name} \
        --size {new_size}
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


def cloud_init_fill_template(template_fn, user_pass, postfix=""):
    result_fn = template_fn + "_filled.txt" + postfix
    with open(result_fn, "w") as f:
        f.write(open(template_fn).read().replace("###PASSWORD###", user_pass))
    return result_fn


def check_output_wrapper(command, shell):
    # fix for windows
    return subprocess.check_output(
        command.strip() if isinstance(command, str) else command,
        shell=shell
    )


def list_disks_for_rg(rg_name):
    out = check_output_wrapper(
        """
        az disk list -g {0}
        """.format(rg_name),
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


def get_cpu_usage(subscription_id, rg_name, vm_name, start, end, interval):
    # example:
    # start = "2018-05-08T00:00:00Z"
    # end = "2018-05-25T00:00:00Z"
    # interval = "PT24H"
    out = ""
    try:
        out = check_output_wrapper(
            """
            az monitor metrics list \
            --resource "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Compute/virtualMachines/{vm_name}" \
            --metric "Percentage CPU" --start-time {start} --end-time {end} --interval {interval}
            """.format(**locals()),
            shell=True
        )
        out = json.loads(out)
        return list(map(lambda x: (x["timeStamp"], x["average"]), out["value"][0]["timeseries"][0]["data"]))
    except:
        print("couldn't get stat for", rg_name, vm_name)

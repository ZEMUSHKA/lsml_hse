##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import utils

parser = argparse.ArgumentParser()
parser.add_argument("--user", action="store", help="account name, for example student1", required=True)
parser.add_argument("--start", action="store_true", help="start ubuntugpu machines")
parser.add_argument("--stop", action="store_true", help="stop ubuntugpu machines")
parser.add_argument("--remove", action="store_true", help="remove ubuntugpu VM and disks")
args = parser.parse_args()

student_name = args.user
rg_name = utils.get_student_resource_group(student_name)

assert args.start or args.stop or args.remove
assert not (args.start and args.stop and args.remove)
if args.start:
    action_func = utils.start_vm
elif args.stop:
    action_func = utils.deallocate_vm
elif args.remove:
    action_func = utils.remove_vm_and_disks

if args.remove:
    # remove orphaned disks (to make sure)
    utils.remove_orphaned_disks(rg_name)

action_func("ubuntugpu", rg_name)

if args.start:
    print("ubuntugpu public IP: {}".format(utils.get_public_ip("ip_ubuntugpu", rg_name)))

##!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
from utils import RG_TEMPLATE
from joblib import Parallel, delayed
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--user", action="store", help="account name, for example student1", required=True)
parser.add_argument("--start", action="store_true", help="start cluster machines")
parser.add_argument("--stop", action="store_true", help="stop cluster machines")
parser.add_argument("--remove", action="store_true", help="remove cluster VMs and disks")
args = parser.parse_args()

STUDENT_NAME = args.user
RG_NAME = RG_TEMPLATE.format(STUDENT_NAME)

assert args.start or args.stop or args.remove
assert not (args.start and args.stop and args.remove)
if args.start:
    action_func = utils.start_vm
elif args.stop:
    action_func = utils.deallocate_vm
elif args.remove:
    action_func = utils.remove_vm_and_disks

Parallel(n_jobs=3, backend="threading")(
    delayed(action_func)("cluster{0}".format(idx), RG_NAME) for idx in [1, 2, 3]
)

if args.start:
    print "cluster1 public IP: {}".format(utils.get_public_ip("ip_cluster1", RG_NAME))
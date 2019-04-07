##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from joblib import Parallel, delayed

import utils
from utils import RG_NAME, CLUSTER_VM

parser = argparse.ArgumentParser()
parser.add_argument("--start", action="store_true", help="start cluster machines")
parser.add_argument("--stop", action="store_true", help="stop cluster machines")
parser.add_argument("--remove", action="store_true", help="remove cluster VMs and disks")
parser.add_argument("--jobs", type=int, action="store", help="number of parallel jobs")
args = parser.parse_args()

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
    utils.remove_orphaned_disks(RG_NAME)

Parallel(n_jobs=args.jobs or 3, backend="threading")(
    delayed(action_func)(CLUSTER_VM.format(idx), RG_NAME) for idx in [1, 2, 3]
)

if args.start:
    print("cluster1 public IP: {}".format(utils.get_public_ip("ip_cluster1", RG_NAME)))

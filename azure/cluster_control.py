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
args = parser.parse_args()

STUDENT_NAME = args.user
RG_NAME = RG_TEMPLATE.format(STUDENT_NAME)

assert args.start or args.stop
assert not (args.start and args.stop)
action_func = utils.deallocate_vm if args.stop else utils.start_vm

Parallel(n_jobs=3)(
    delayed(action_func)("cluster{0}".format(idx), RG_NAME) for idx in [1, 2, 3]
)

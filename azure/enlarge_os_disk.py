#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils
from utils import RG_TEMPLATE

STUDENT_NAME = "admin"
RG_NAME = RG_TEMPLATE.format(STUDENT_NAME)
VM_NAME = "ubuntugpu"
DISK_SIZE = 300

utils.deallocate_vm(VM_NAME, RG_NAME)
utils.resize_os_disk(RG_NAME, VM_NAME, DISK_SIZE)
utils.start_vm(VM_NAME, RG_NAME)

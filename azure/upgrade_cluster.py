##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from joblib import Parallel, delayed

import utils
from utils import RG_NAME, resize_vm, CLUSTER_VM

"""
README:
1. Stop All in Ambari && python cluster_control.py --stop
2. Run this script && python cluster_control.py --start
3. Change Ambari settings (run on cluster1 node)

curl 'http://localhost:8080/api/v1/clusters/Cluster/config_groups/2' -u admin:admin -H "X-Requested-By: ambari" -i  -X PUT --data '{"ConfigGroup":{"group_name":"MasterNode","description":"","tag":"YARN","hosts":[],"desired_configs":[]}}' --compressed
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.nodemanager.resource.cpu-vcores 16
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.scheduler.maximum-allocation-vcores 16
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.nodemanager.resource.memory-mb 98304
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.scheduler.maximum-allocation-mb 98304

4. Start All in Ambari
5. Change SparkContext settings

More workers:
    sc = get_spark_context(executorsPerNode=16, memoryPerExecutor=6144)
More memory per worker:
    sc = get_spark_context(executorsPerNode=8, memoryPerExecutor=12288)
Even more memory per worker (huge ALS workload maybe):
    sc = get_spark_context(executorsPerNode=4, memoryPerExecutor=24576)

"""

NEW_SIZE = "Standard_E16_v3"  # 16 cores, 128 GB memory

Parallel(n_jobs=3, backend="threading")(
    delayed(resize_vm)(CLUSTER_VM.format(idx), RG_NAME, NEW_SIZE) for idx in [1, 2, 3]
)

print("Done!")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from utils import timeit, check_output_wrapper, CLUSTER_IMAGE, UBUNTUGPU_IMAGE, REGION, RG_NAME

parser = argparse.ArgumentParser()
parser.add_argument("--storage_account", action="store", required=True)
args = parser.parse_args()


@timeit
def create_image(RG_NAME, IMAGE_NAME, SOURCE, REGION):
    check_output_wrapper(
        """
        az image create \
            -g {RG_NAME} \
            -n {IMAGE_NAME} \
            --source "{SOURCE}" \
            --os-type linux \
            -l {REGION}
        """.format(**locals()),
        shell=True
    )


create_image(RG_NAME,
             UBUNTUGPU_IMAGE,
             "https://{0}.blob.core.windows.net/images/ubuntugpu.vhd".format(args.storage_account),
             REGION)
for clIdx in [1, 2, 3]:
    create_image(RG_NAME,
                 CLUSTER_IMAGE.format(clIdx),
                 "https://{0}.blob.core.windows.net/images/cluster{1}.vhd".format(args.storage_account, clIdx),
                 REGION)

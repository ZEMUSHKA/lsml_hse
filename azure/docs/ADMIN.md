# Admin notes

## Flush disks
`parallel-ssh -i -t 0 -H "cluster1 cluster2 cluster3" "sudo sh -c \"sync && echo 3 > /proc/sys/vm/drop_caches\""`

## Benchmark
Using `N_KEYS = 200; MB_PER_KEY = 500; N_JOBS = 100` in `spark_demo.ipynb`
- Sequential write with `df.write.save("hdfs:///user/ubuntu/bigData.parquet")`
HDD: 7.5 min, SSD: 6.1 min
- Sequential read with `ss.read.parquet("hdfs:///user/ubuntu/bigData.parquet").rdd.map(lambda x: len(x)).distinct().count()`
HDD: 38 min, SSD: 11 min

## Tools

**(for admin)** Install AzCopy in Windows environment for blobs copy across storage accounts:
https://docs.microsoft.com/en-us/azure/storage/storage-use-azcopy

**(for admin)** Install Azure Storage Explorer:
http://storageexplorer.com

## New Images feature
https://docs.microsoft.com/en-us/azure/virtual-machines/linux/capture-image
```
az image create -g admin_resources -n ubuntu_gpu_image1
--source "https://adminlsmlhse645221.blob.core.windows.net/images/ubuntugpu.vhd"
--os-type linux
```

Can share images across subscription:
```
/subscriptions/<subscriptionId>/resourceGroups/admin_resources/providers/Microsoft.Compute/images/ubuntu_gpu_image1
```

## Managed disk resize (including OS disk)
https://docs.microsoft.com/en-us/azure/virtual-machines/linux/expand-disks

## Copy VHD images accross storage accounts (obsolete, use managed disks and images)
All images are copied to students' storage accounts with
`python generate_azcopy_commands.py` and running the resulting
`azcopy.bat` on Windows VM in Azure.

##  Mounting data disks
You can mount data disks with `./mount_disk.sh`.

## Create image from VM
Save all needed user files from home directory to /usr/local/backup, the user will be deleted.
  
Capture machine: https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-linux-capture-image

Azure CLI 2.0 commands for capturing:
```
Over SSH: sudo waagent -deprovision+user
az vm deallocate -g admin_resources -n ubuntugpu
az vm generalize -g admin_resources -n ubuntugpu
az vm capture -g admin_resources -n ubuntugpu --vhd-name-prefix ubuntugpu
```

## NC6 vs NV6 machine

Both work with NC6 image on Ubuntu 16.04.
Approx. same price.
M60 has less but faster cores and new architecture: 
https://www.quora.com/What-are-the-major-differences-between-the-Nvidia-Tesla-M60-and-K80

| Parameter     | NC6 (K80)     | NV6 (M60)    |
| ------------- |:-------------:|:------------:|
| ConvNet       | 14min 41s     | 8min 41s     |
| Memory        | 12GB          | 8GB          |


## On new ubuntu 14.04 machine
```
sudo apt-get update
sudo apt-get install language-pack-en
```

## HDP 2.5 cluster setup

Installation guide: http://docs.hortonworks.com/HDPDocuments/Ambari-2.4.2.0/bk_ambari-installation/content/download_the_ambari_repo_ubuntu14.html
Disable THP: 
```
sudo bash
echo never >/sys/kernel/mm/transparent_hugepage/enabled
```
Use cluster[1-3] nodes names.
Change `dfs.namenode.datanode.registration.ip-hostname-check` in `hdfs-site.xml`.



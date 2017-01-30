# Scripts and Wiki for Azure

## Start
Install Azure CLI and Azure CLI 2.0: 
https://docs.microsoft.com/en-us/cli/azure

Install AzCopy in Windows environment for blobs copy across storage accounts: 
https://docs.microsoft.com/en-us/azure/storage/storage-use-azcopy

Install Azure Storage Explorer: 
http://storageexplorer.com

## Ubuntu machine mount data disk after start (used in GPU machine)
```
# check drive name
lsblk

# create partition
(
echo o # Create a new empty DOS partition table
echo n # Add a new partition
echo p # Primary partition
echo 1 # Partition number
echo   # First sector (Accept default: 1)
echo   # Last sector (Accept default: varies)
echo w # Write changes
) | sudo fdisk /dev/sdc

# format partition
sudo mkfs.ext4 /dev/sdc1

# tune ext4 to reserve 0 blocks
sudo tune2fs -m 0 /dev/sdc1

# create mount point
sudo mkdir /mnt2

# add line to /etc/fstab (with sudo)
/dev/sdc1 /mnt2 ext4 defaults 0 2

# mount for the first time (will be automounted on reboot)
sudo mount /dev/sdc1

# change owner to your user
sudo chown -R ubuntu /mnt2
```

## Restore user files after VM creation (used in GPU machine)

```
# copy all files and directories including hidden
sudo chown -R ubuntu /usr/local/backup
cp -rT /usr/local/backup /home/ubuntu
```

## Create image from VM

Save all needed user files from home directory to /usr/local/backup, the user will be deleted.
  
Capture machine: https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-linux-capture-image

```
# Azure CLI 2.0 commands for capturing:
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

#!/usr/bin/env bash

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

# add line to /etc/fstab
echo "/dev/sdc1 /mnt2 ext4 defaults 0 2" | sudo tee -a /etc/fstab

# mount for the first time (will be automounted on reboot)
sudo mount /dev/sdc1

# change owner to your user
sudo chown -R ubuntu /mnt2
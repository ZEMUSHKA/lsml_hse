#!/usr/bin/env bash
#export STUDENT_NAME="student1"
#export RG_NAME=$STUDENT_NAME"_resources"
#export STORAGE_ACCOUNT=$STUDENT_NAME"lsmlhse645221"

export RG_NAME="admin_resources"
export STORAGE_ACCOUNT="adminlsml"

export VNET_NAME="student_network"
export SUBNET_NAME="student_subnet"
export REGION="eastus"
export NSG_NAME="student_security_group"
export IP_NAME="ip_ubuntugpu"
export NIC_NAME="nic_ubuntugpu"
export INT_DNS_NAME="ubuntugpu"
export VM_NAME=$INT_DNS_NAME

# create vnet and subnet
az network vnet create \
    -n $VNET_NAME \
    -g $RG_NAME \
    -l $REGION \
    --address-prefix 10.0.0.0/16 \
    --subnet-name $SUBNET_NAME \
    --subnet-prefix 10.0.1.0/24

# Create network security group
az network nsg create \
    -n $NSG_NAME \
    -g $RG_NAME \
    -l $REGION

# Create SSH and Jupyter rules
az network nsg rule create \
    --access Allow \
    --nsg-name $NSG_NAME \
    -g $RG_NAME \
    --protocol Tcp \
    --name allow_ssh \
    --source-address-prefix "*" \
    --source-port-range "*" \
    --direction InBound \
    --destination-port-range 22 \
    --destination-address-prefix "*" \
    --priority 1000

az network nsg rule create \
    --access Allow \
    --nsg-name $NSG_NAME \
    -g $RG_NAME \
    --protocol Tcp \
    --name allow_jupyter \
    --source-address-prefix "*" \
    --source-port-range "*" \
    --direction InBound \
    --destination-port-range 9999 \
    --destination-address-prefix "*" \
    --priority 1010

# Create public IP
az network public-ip create \
    -n $IP_NAME \
    -g $RG_NAME

# Create network card with fixed private IP
az network nic create \
    -n $NIC_NAME \
    -g $RG_NAME \
    --vnet-name $VNET_NAME \
    --subnet $SUBNET_NAME \
    --network-security-group $NSG_NAME \
    --public-ip-address $IP_NAME \
    --internal-dns-name $INT_DNS_NAME \
    --private-ip-address 10.0.1.10

# Create VM
#az vm create \
#    -n $VM_NAME \
#    -g $RG_NAME \
#    --image "https://"$STORAGE_ACCOUNT".blob.core.windows.net/images/ubuntu_gpu.vhd" \
#    --authentication-type ssh \
#    --nics $NIC_NAME \
#    --nsg $NSG_NAME \
#    --public-ip-address $IP_NAME \
#    --size Standard_NC6 \
#    --ssh-key-value ~/.ssh/id_rsa.pub \
#    --storage-type Standard_LRS \
#    --storage-account $STORAGE_ACCOUNT \
#    --custom-os-disk-type Linux

azure vm create \
    -n $VM_NAME \
    -g $RG_NAME \
    -l $REGION \
    --admin-username ubuntu \
    --image-urn "https://"$STORAGE_ACCOUNT".blob.core.windows.net/images/ubuntu_gpu.vhd" \
    --nic-names $NIC_NAME \
    --public-ip-name $IP_NAME \
    --storage-account-name $STORAGE_ACCOUNT \
    --vm-size Standard_NC6 \
    --ssh-publickey-file ~/.ssh/id_rsa.pub \
    --os-type Linux \
    --data-disk-size 1000
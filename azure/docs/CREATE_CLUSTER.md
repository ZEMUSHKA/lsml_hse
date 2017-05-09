# How to create a Hadoop cluster

We are using images for a ready-to-use HDP cluster.

**Always pull the latest version of this repository before running anything!**

**If commands below fail, maybe you need to update Azure CLI 2.0 to the latest version: `az component update`**

## If you need to recreate cluster

First remove all cluster machines (can be in any state, will be removed anyway):
```
python cluster_control.py —user student* —remove
```

Then proceed with all instructions below omitting `--create_shared` and `--create_aux` flags.

## Create instructions
Run `python create_cluster.py --user student* --ssh_key ~/.ssh/*.pub
--create_shared --create_aux` to create 3 cluster nodes on `10.0.1.[21-23]`
with private DNS names `cluster[1-3]`.

`--create_shared` flag creates shared resources like virtual network (need to do it once throughout the course).

`--create_aux` flag creates resources for virtual machines you create like IP address (need to do once per machine).

Create SOCKS proxy like here [Setup proxy for Chrome](SETUP_PROXY.md) for `cluster1` machine.

Also add
```
10.0.1.21	cluster1
10.0.1.22	cluster2
10.0.1.23	cluster3
```
to your /etc/hosts (Mac, Linux).
Instructions for Windows: https://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/

SSH to `cluster1` machine:
`ssh ubuntu@(paste public IP of virtual machine here) -i ~/.ssh/id_rsa_azure`.

**Wait for cloud-init to finish (this is crucial):**
```
ubuntu@cluster1:~$ cat /var/log/cloud-init-output.log
Cloud-init v. 0.7.5 finished at Tue, 11 Apr 2017 11:13:50 +0000. Datasource DataSourceAzureNet [seed=/dev/sr0].  Up 247.74 seconds
```

Open Ambari via proxy: `http://10.0.1.21:8080`, 
use `admin/admin` to authenticate.
Ambari is a Hadoop cluster management utility.
To start Hadoop cluster, select "Actions" -> "Start All".

Start Jupyter notebooks on `cluster1`:
```
tmux
./start_notebook.sh
```

Open Notebooks using `https://10.0.1.21:9999` via SOCKS proxy.
Ask admin for Notebook password.

## Cluster start/stop

Stop (deallocate) resources when you don't need them.
There will be no charges for VM usage, but all the data is still stored.

### Cluster machines start
```
1. python cluster_control.py --user student* --start
2. In Ambari select "Actions" -> "Start All", wait till it's done.
```

### Cluster machines stop
```
1. In Ambari select "Actions" -> "Stop All", wait till it's done.
2. python cluster_control.py --user student* --stop
```

## Known issues
* **(fixed with maintance mode)** Grafana fails to start automatically (because somehow it is already running),
probably a bug (https://github.com/grafana/grafana/issues/1990).

# How to create a Hadoop cluster

We are using images for a ready-to-use HDP cluster.

**Always pull the latest version of this repository before running anything!**

**If commands below fail, maybe you need to update Azure CLI 2.0 to the latest version**

## If you need to recreate cluster

First remove all cluster machines (can be in any state, will be removed anyway):
```
python cluster_control.py --remove
```

Then proceed with all instructions below omitting `--create_shared` and `--create_aux` flags.

## Create instructions

**If** you haven't created a cluster before, add `--create_shared` flag which creates shared resources like a virtual network (need to do it once throughout the course).

**If** you create these machines for the first time, add `--create_aux` flag which creates resources for virtual machines you create like IP address (need to do once per machine).

Run `python create_cluster.py` to create 3 cluster nodes on `10.0.1.[21-23]`
with private DNS names `cluster[1-3]` using necessary flags described above.

After the scipt finishes you will see a **public IP** for each cluster node and a **password** for everything on each machine.

Now ssh to `cluster1` machine (which is a master node). Run `ssh ubuntu@[public IP of cluster1]` and enter the password.

**Wait for cloud-init to finish (this is crucial):**

Run `tail -fn 100 /var/log/cloud-init-output.log` in remote shell and wait for
```
ALL DONE
...
Cloud-init v. 0.7.5 finished at Tue, 11 Apr 2017 11:13:50 +0000. Datasource DataSourceAzureNet [seed=/dev/sr0].  Up 247.74 seconds
```

`cluster1` machine has a squid http proxy to access cluster network. Use the following settings:
- host: a public IP of `cluster1`
- port: 3128
- user: ubuntu
- password: a passsword for `cluster1` generated after create script finishes

You can setup an http proxy in Google Chrome using a plugin described [here](SETUP_PROXY.md).

**Now it's time to start cluster components**:
- Open Ambari (a Hadoop cluster management utility) via http proxy `http://cluster1:8080`,
use `admin/admin` to authenticate.
- Start Hadoop cluster components by clicking "Actions" -> "Start All".

Start Jupyter notebooks on `cluster1`:
Run `tmux` and then inside tmux run: `./start_notebook.sh`

Open Notebooks using `https://cluster1:9999` via http proxy or `https://[public IP of cluster1]:9999` to access from the Internet.
Use generated password for `cluster1` to access Jupyter Notebooks.

## Cluster start/stop

Stop (deallocate) resources when you don't need them.
There will be no charges for VM usage, but all the data is still stored.

### Cluster machines start
1. `python cluster_control.py --start`
2. In Ambari select "Actions" -> "Start All", wait till it's done.

### Cluster machines stop
1. In Ambari select "Actions" -> "Stop All", wait till it's done.
2. `python cluster_control.py --stop`

## Ssh access to cluster2 and cluster3
We don't have enough public IPs for all nodes, but you can still access these nodes via `cluster1` node.
Run `ssh cluster2` in `cluster1` remote shell to access `cluster2`.

## Execute a command on all nodes
Run `parallel-ssh -i -t 0 -H "cluster1 cluster2 cluster3" "hostname"` in `cluster1` remote shell.

## Known issues
* **(fixed with maintance mode)** Grafana fails to start automatically (because somehow it is already running),
probably a bug (https://github.com/grafana/grafana/issues/1990).

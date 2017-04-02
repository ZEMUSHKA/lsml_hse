# How to create a Hadoop cluster

We are using images for a ready-to-use HDP cluster.

## Start instructions
Run `python create_cluster.py --user student* --ssh_key ~/.ssh/*.pub` to create 3 cluster nodes on `10.0.1.[21-23]`
with private DNS names `cluster[1-3]`.

Create SOCKS proxy like here [Setup proxy for Chrome](SETUP_PROXY.md) for `cluster1` machine.

Also add
```
10.0.1.21	cluster1
10.0.1.22	cluster2
10.0.1.23	cluster3
```
to your /etc/hosts (Mac, Linux).

Open Ambari via proxy: `http://10.0.1.21:8080`, 
use `admin/admin` to authenticate.
Ambari is a Hadoop cluster management utility.
To start Hadoop cluster, select "Actions" -> "Start All".

Copy necessary user settings:
```
# copy all files and directories including hidden
sudo chown -R ubuntu /usr/local/backup
cp -rT /usr/local/backup /home/ubuntu
```

Start Jupyter notebooks:
```
tmux
./start_notebook.sh
```

Open Notebooks using `https://10.0.1.21:9999` via SOCKS proxy.
Ask admin for Notebook password.

## Stop instructions
In Ambari select "Actions" -> "Stop All", wait till it's done.
Then use https://portal.azure.com to stop all cluster machines.

## Known issues
* **(fixed with maintance mode)** Grafana fails to start automatically (because somehow it is already running),
probably a bug (https://github.com/grafana/grafana/issues/1990).
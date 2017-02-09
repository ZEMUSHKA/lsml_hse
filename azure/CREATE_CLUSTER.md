# How to create a Hadoop cluster

We are using images for a ready-to-use HDP cluster.

## Instructions
Run `python create_cluster.py` to create 3 cluster nodes on `10.0.1.[21-23]` 
with private DNS names `cluster[1-3]`.

Resize disks for `cluster[1-3]` machines with `python enlarge_os_disk.py`.

After that is done, create SOCKS proxy over ssh with 
`ssh ubuntu@(paste public IP of cluster1 VM here) -ND 8157` (Mac, Linux),
this will give you access to internal network of the Hadoop cluster.
You can use newly created SOCKS proxy with FoxyProxy plugin for Chrome, 
just add a rule to use `localhost:8157` for `10.*` addresses.

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

Open Notebooks using `https://10.0.1.21:9999` via SOCKS proxy or public IP address.

## Known issues
* Grafana fails to start automatically (because somehow it is already running), 
probably a bug (https://github.com/grafana/grafana/issues/1990).
# How to create a GPU machine

We are using an image with installed TensorFlow, GPU drivers and stuff.
We will use both NV6 and NC6 machines in different regions!

**Always pull the latest version of this repository before running anything!**

**If commands below fail, maybe you need to update Azure CLI 2.0 to the latest version: `az component update`**


## If you need to recreate GPU machine

First remove it (can be in any state, will be removed anyway):
```
python ubuntugpu_control.py —user student* —remove
```

Then proceed with all instructions below omitting `--create_aux` flag.

## Create instructions (shared is already created in cluster script)
Run `python create_ubuntu_gpu.py --user student* --ssh_key ~/.ssh/*.pub --create_aux`.

`--create_aux` flag creates resources for virtual machines you create like IP address (need to do once per machine).

**Wait for cloud-init to finish (this is crucial):**
```
ubuntu@ubuntugpu:~$ cat /var/log/cloud-init-output.log
Cloud-init v. 0.7.8 finished at Mon, 08 May 2017 11:05:21 +0000. Datasource DataSourceAzureNet [seed=/dev/sr0].  Up 77.67 seconds
```

Create SOCKS proxy like here [Setup proxy for Chrome](SETUP_PROXY.md) for `ubuntugpu` machine.

Start Jupyter notebooks:
```
tmux
./start_notebook.sh
```

Open Notebooks using `https://10.0.1.10:9999` via SOCKS proxy.
Ask admin for Notebook password.

You can start/stop machine in Azure portal http://portal.azure.com

## GPU machine start/stop

Stop (deallocate) resources when you don't need them.
There will be no charges for VM usage, but all the data is still stored.

```
python ubuntugpu_control.py --user student* --start
python ubuntugpu_control.py --user student* --stop
```
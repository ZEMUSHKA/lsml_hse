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

Then proceed with all instructions below omitting `--create_shared` and `--create_aux` flags.

## Create instructions

**If** you haven't created a cluster, add `--create_shared` flag which creates shared resources like a virtual network (need to do it once throughout the course).

**If** you create this machine for the first time, add `--create_aux` flag which creates resources for virtual machines you create like IP address (need to do once per machine).

Run `python create_ubuntu_gpu.py --user student*` adding the necessary flags described above.

After the scipt finishes you will see a **public IP** of your new machine and a **password** for everything on that machine.

Now ssh to `ubuntugpu` machine. Run `ssh ubuntu@(paste public IP of virtual machine here)` and enter the password.

**Wait for cloud-init to finish on the remote machine (this is crucial):**

Run `tail -fn 100 /var/log/cloud-init-output.log` in remote shell and wait for
```
Cloud-init v. 0.7.8 finished at Mon, 08 May 2017 11:05:21 +0000. Datasource DataSourceAzureNet [seed=/dev/sr0].  Up 77.67 seconds
```

This machine has a squid http proxy to access its network. Use the following settings:
- host: a public IP of a virtual machine
- port: 3128
- user: ubuntu
- password: a passsword generated after create script finishes

You can setup an http proxy in Google Chrome using a plugin described [here](SETUP_PROXY.md).

Now start Jupyter notebooks (in remote shell):
Run `tmux` and then inside tmux run: `./start_notebook.sh`

Open Notebooks using `https://ubuntugpu:9999` via http proxy or `https://(paste public IP of virtual machine here):9999` to access from the Internet.
Use generated password to access Jupyter Notebooks.

You can start/stop machine in Azure portal http://portal.azure.com

## GPU machine start/stop

Stop (deallocate) resources when you don't need them.
There will be no charges for VM usage, but all the data is still stored.

```
python ubuntugpu_control.py --user student* --start
python ubuntugpu_control.py --user student* --stop
```
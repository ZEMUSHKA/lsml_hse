# How to create a GPU machine

We are using an image with installed TensorFlow, GPU drivers and stuff.
We will use both NV6 and NC6 machines in different regions!

## Create instructions (shared is already created in cluster script)
Run `python create_ubuntu_gpu.py --user student* --ssh_key ~/.ssh/*.pub --create_aux`.

Create SOCKS proxy like here [Setup proxy for Chrome](SETUP_PROXY.md) for `ubuntugpu` machine.

Start Jupyter notebooks:
```
tmux
./start_notebook.sh
```

Open Notebooks using `https://10.0.1.10:9999` via SOCKS proxy.
Ask admin for Notebook password.

You can start/stop machine in Azure portal http://portal.azure.com

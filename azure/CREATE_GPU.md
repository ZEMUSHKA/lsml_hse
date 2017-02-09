# How to create a GPU machine

We are using an image with installed TensorFlow, GPU drivers and stuff.
We will use both NV6 and NC6 machines in different regions!

## Instructions
Run `python create_ubuntu_gpu.py`.

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

# Scripts and Wiki for Azure

![](docs/azure_logo.png)

## First steps
* Accept your "Azure lab assignment" found in your email inbox:
    - click "Accept lab assignment"
    - log in with Microsoft Account on your email address (sign up if missing)
    - click "Setup Lab" to create Sponsored Subscription (filling in name, phone, etc)

* Install Azure CLI 2.0 (https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
and authenticate with `az login` in command line using your Microsoft Account.
If you've used Azure before, make sure that you switch to sponsored azure subscription with
`az account set --subscription SPONSORED_SUBSCRIPTION_ID`.

* Authenticate in http://portal.azure.com (Google Chrome is recommended) using your Microsoft Account.
This is the web interface for the things you can do with Azure CLI, like creating a Virtual Machine.

* Install Python 2 or 3. Execute `pip install joblib` or `pip3 install joblib` based on your Python version,
we will need this for setup scripts.

* If you use Windows install Putty ssh client (https://www.putty.org/) and Git (https://git-scm.com/).
On Linux you can use `ssh` and `git`.
Clone this repo running `git clone https://github.com/ZEMUSHKA/lsml_hse`, you will need all the scripts.

* Install AzCopy 8 (or 7) (https://docs.microsoft.com/ru-ru/azure/storage/common/storage-use-azcopy),
we will need it to copy prepared disk images to your account.

## Further reading
[How to create a Hadoop cluster](docs/CREATE_CLUSTER.md)

[How to create a machine with GPU](docs/CREATE_GPU.md)

[Admin notes](docs/ADMIN.md)

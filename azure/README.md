# Azure Wiki

![](docs/azure_logo.png)

## First steps
* Accept your "Azure lab assignment" found in your email inbox:
    - click "Accept lab assignment"
    - log in with Microsoft Account on your email address (sign up if missing)
    - click "Setup Lab" to create Sponsored Subscription (filling in name, phone, etc)

* Install Azure CLI 2.0 (https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
and authenticate with `az login` in command line using your Microsoft Account.
Make sure that you switch to sponsored azure subscription with
`az account set --subscription [SPONSORED_SUBSCRIPTION_ID]`.

* Authenticate in http://portal.azure.com (Google Chrome is recommended) using your Microsoft Account.
This is the web interface for the things you can do with Azure CLI, like creating a Virtual Machine.

* Install Python 2 or 3. Execute `pip install joblib` or `pip3 install joblib` based on your Python version,
we will need this for setup scripts.

* If you use Windows install Putty ssh client (https://www.putty.org/) and Git (https://git-scm.com/).
On Linux you can use `ssh` and `git`.
Clone this repo running `git clone https://github.com/ZEMUSHKA/lsml_hse` to get a bunch of useful scripts.

* Install AzCopy 8 (or 7) (https://docs.microsoft.com/ru-ru/azure/storage/common/storage-use-azcopy).
Create Resource Group **my_resources** in "East US" region and Storage Account in it (has unique name).
Go to that Storage Account -> Blobs and create a container called **images**.
Go to that Storage Account and get "key1" Key in "Access keys" settings.
Now execute (Windows example, you can create a small Windows VM to excute this)
`cd "C:\Program Files (x86)\Microsoft SDKs\Azure\AzCopy"` and `AzCopy.exe /Source:https://lsml1eastus.blob.core.windows.net/images /Dest:https://[STORAGE_ACCOUNT_NAME].blob.core.windows.net/images /S /DestKey:[KEY1_KEY]`
to copy all disk images you will need to your storage account.

* Create machine images from copied disk images with
`python create_images.py --storage_account [STORAGE_ACCOUNT_NAME]`

## Further reading
[How to create a Hadoop cluster](docs/CREATE_CLUSTER.md)

[How to create a machine with GPU](docs/CREATE_GPU.md)

[Admin notes](docs/ADMIN.md)

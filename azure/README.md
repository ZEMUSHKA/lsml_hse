# Scripts and Wiki for Azure

![](docs/azure_logo.png)

## First steps
1. Install Azure CLI 2.0 (tested with 2.0.29):
https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

2. Authenticate with `az login` in command line using your student credentials.

3. Authenticate in http://portal.azure.com (Google Chrome is recommended) using the same credentials.

4. Install Python 2 or 3

5. `pip install joblib` or `pip3 install joblib` based on your Python version

## How-To's
1. Clone this repo running: `git clone https://github.com/ZEMUSHKA/lsml_hse`
2. Switch to azure subscription we use if you've used azure before:
- ПМИ: `az account set --subscription "ФКН ВШЭ"`
- ФТиАД: `az account set --subscription "Sponsorship 2017"`
3. Use any of the below:

[How to create a Hadoop cluster](docs/CREATE_CLUSTER.md)

[How to create a machine with GPU](docs/CREATE_GPU.md)

[Admin notes](docs/ADMIN.md)

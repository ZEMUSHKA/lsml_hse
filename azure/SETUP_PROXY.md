# Setup proxy for Chrome

## Create proxy

Create SOCKS proxy via ssh with
`ssh ubuntu@(paste public IP of virtual machine here) -ND 8157` (Mac, Linux),
this will give you access to internal network of the virtual machine.

## Setup Chrome extension

You can use newly created SOCKS proxy with
[FoxyProxy plugin](https://chrome.google.com/webstore/detail/foxyproxy-standard/gcknhkkoolaabfmlnjonogaaifnjlfnp)
for Chrome.

In FoxyProxy extension add new proxy with address `localhost:8157`
as `SOCKS v5` proxy and check `SOCKS proxy?`.
On `URL Patterns` tab add rules for `10.*` and `cluster*`.
Then click on FoxyProxy icon and choose
`Use proxies based on their pre-defined patterns and priorities`.
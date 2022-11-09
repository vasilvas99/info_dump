# Setting i.f. static IPs on different OSes

## Windows

The next commands should be executed in powershell as administrator.

Backup the current network interface configuration by executing:

```powershell
netsh -c interface dump > network_if_backup.txt
```

Connect the RPI via a **straight-through** (normal) Ethernet cable to your PC/Laptop.

Find the name of the interface the RPI is connected to by running:

```powershell
netsh interface show interface
```

Example output:

```console
Admin State    State          Type             Interface Name
-------------------------------------------------------------------------
Enabled        Connected      Dedicated        Ethernet Instance 0
```

Here the interface name would be:  `Ethernet Instance 0`.

Now we are ready to set the static ip. Execute:

```powershell
netsh interface ip set address "<interface name>" static 192.168.7.3 255.255.255.0 192.168.7.1
```

After that you should be able to ping the RPI on `192.168.7.1`. You can now ssh to it or scrape the system info via the __"dump_info.py"__ script.

When you are done, you can restore your original network configuration by running:

```powershell
netsh exec network_if_backup.txt
```

## Linux

There are a lot of ways to manage network configs on Linux. Here we will assume the most common situation - the network profiles are managed by __NetworkManager__
and via __nmcli__.

Connect the RPI via a **straight-through** (normal) Ethernet cable to your PC/Laptop and find the name of the interface by running:

```bash
nmcli con show
```

Example output

```console
NAME               UUID                                  TYPE      DEVICE          
DHCP               3419bd9a-e620-4249-a162-a96279fd76b1  ethernet  enp0s13f0u3u1i5 
...
```
Here the name of the name of the interface of interest would be: `enp0s13f0u3u1i5`.
Also note the name of the current profile. E.g. `DHCP`.

Create a new static-ip profile for the identified interface:

```bash
sudo nmcli con add type ethernet con-name "static-ip" ifname <interface_name> ipv4.addresses 192.168.7.3/24 gw4 192.168.7.1
```

And set that profile as **up**:

```bash
sudo nmcli con up static-ip ifname <interface_name> 
```

Now your static-ip profile should be successfully set.


After that you should be able to ping the RPI on `192.168.7.1`. You can now ssh to it or scrape the system info via the __"dump_info.py"__ script.

When you are done, you can restore your original network configuration by running:


```bash
sudo nmcli con down static-ip ifname <interface_name> 
sudo nmcli con up <old_nmcli_profile> ifname <interface_name> 
```

Note: in my case `<old_nmcli_profile> = DHCP`, `<interface_name>=enp0s13f0u3u1i5`.



## MacOS

**TODO: Find a mac..**
# Info dump

A script that SSH's to a host an obtains relevant system information. 

## IP configurations

This script requires an ethernet connection to the remote device. In the case of an RPI the simplest possible configuration is a straight-trough (normal) Ethernet cable connecting the RJ45 ports of the Laptop/PC and the RPI4 and a static ip config on both the client and the remote device.

**You can find here how to set a static ip on different OSes: [Setting a static ip](/static_ips.md)**

## Usage

To setup the SSH credentials and other connection information edit the `dump_info_config.json` file.

```json
{
    "HOST": "192.168.7.1", # host ip address/hostname
    "PORT": "22", # ssh port
    "SSH_USER": "root", # ssh login username
    "SSH_PASS": "", # password
    "PING_TIMES": 1, # number of times the host would be ping-ed before ssh connection is attempted
    "DUMP_TO_FILE": "yes" # should the scraped info be dumped to a file  - <yes/no>
}
```

This script does not depend on a system installation of OpenSSH but rather uses the `paramiko` library that is a "pure-Python" implementation of the ssh protocol. That __should__ make it platform independent, as not all Windows clients have OpenSSH installed by default for example.

To install it:

```bash
pip3 install paramiko
```

Other than paramiko, there are no external dependencies.


## Running

After paramiko is installed and the json config file is appropriately edited, please run:

```bash
python dump_info.py
```

## Example output:

```json
{
  "cpu_info": [
    "processor = 0",
    "BogoMIPS = 108.00",
    "Features = fp asimd evtstrm crc32 cpuid",
    "CPU implementer = 0x41",
    "CPU architecture = 8",
    "CPU variant = 0x0",
    "CPU part = 0xd08",
    "CPU revision = 3",
    "",
    "processor = 1",
    "BogoMIPS = 108.00",
    "Features = fp asimd evtstrm crc32 cpuid",
    "CPU implementer = 0x41",
    "CPU architecture = 8",
    "CPU variant = 0x0",
    "CPU part = 0xd08",
    "CPU revision = 3",
    "",
    "processor = 2",
    "BogoMIPS = 108.00",
    "Features = fp asimd evtstrm crc32 cpuid",
    "CPU implementer = 0x41",
    "CPU architecture = 8",
    "CPU variant = 0x0",
    "CPU part = 0xd08",
    "CPU revision = 3",
    "",
    "processor = 3",
    "BogoMIPS = 108.00",
    "Features = fp asimd evtstrm crc32 cpuid",
    "CPU implementer = 0x41",
    "CPU architecture = 8",
    "CPU variant = 0x0",
    "CPU part = 0xd08",
    "CPU revision = 3",
    "",
    "Hardware = BCM2835",
    "Revision = d03114",
    "Serial = 100000007c38a9ed",
    "Model = Raspberry Pi 4 Model B Rev 1.4"
  ],
  "uname": "Linux 5.10.83-v8 aarch64",
  "os_release": [
    "BUILD_ID=\"20221107145736\"",
    "ID=leda",
    "IMAGE_VERSION=\"v0.0.23-95-gdd83f39\"",
    "NAME=\"Eclipse Leda\"",
    "PRETTY_NAME=\"Eclipse Leda 2022 (Hockenheim)\"",
    "VERSION=\"2022 (Hockenheim)\"",
    "VERSION_CODENAME=\"Hockenheim\"",
    "VERSION_ID=v0.0.23-95-gdd83f39"
  ],
  "hostname": "leda-c939",
  "eth0_MAC": "e4:5f:01:0e:c9:39",
  "eth0_IPv4": [
    "192.168.7.1"
  ],
  "wlan_MAC": "e4:5f:01:0e:c9:3b",
  "wlan0_IPv4": [
    ""
  ]
}
```
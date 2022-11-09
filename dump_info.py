import paramiko
import subprocess
import platform
import sys
import json

# Load config
with open("dump_info_config.json", "r") as json_fh:
    conf = json.load(json_fh)

HOST = conf["HOST"]
PORT = conf["PORT"]
USERNAME = conf["SSH_USER"]
PASSWORD = conf["SSH_PASS"]
PING_TIMES = conf["PING_TIMES"]
DUMP_TO_FILE = "y" in conf["DUMP_TO_FILE"].lower()


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def ping(host, retries=1):
    parameter = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", parameter, str(retries), host]
    response = subprocess.call(command)

    if response != 0:
        raise ConnectionError(
            f"Could not ping PI on ip {host}. Are you sure your PC network interface is configured correctly? Check static_ips.md for help."
        )


try:
    print(f"Trying to ping RPI {PING_TIMES} time(s)....")
    ping(HOST, retries=PING_TIMES)
    print("Success!")
except ConnectionError as ce:
    eprint(ce)
    exit(-1)

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Trying username-password based authentication")
    client.connect(
        HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        look_for_keys=False,
        allow_agent=False,
    )
except Exception as ex:
    eprint("Username-Password authentication failed. Exiting...")
    exit(-1)

print("=============================================")
print("Successful SSH authentication!")
print("=============================================")


def execute_single_command(bash_cmd: str):
    _, stdout, _ = client.exec_command(bash_cmd)
    return stdout.read().decode("ascii", "ignore").strip()


info_dict = {}
info_dict["cpu_info"] = (
    execute_single_command(r"cat /proc/cpuinfo")
    .replace("\t", "")
    .replace(":", " =")
    .split("\n")
)
info_dict["uname"] = execute_single_command(r"echo $(uname) $(uname -r) $(uname -p)")
info_dict["os_release"] = execute_single_command(r"cat /usr/lib/os-release").split("\n")
info_dict["hostname"] = execute_single_command(r"cat /etc/hostname")
info_dict["eth0_MAC"] = execute_single_command(r"cat /sys/class/net/eth0/address")
info_dict["eth0_IPv4"] = execute_single_command(r"ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'").split("\n")
info_dict["wlan_MAC"] = execute_single_command(r"cat /sys/class/net/wlan0/address")
info_dict["wlan0_IPv4"] = execute_single_command(r"ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'").split("\n")

client.close()
print("=============================================")
print("OS information obtained")
print("=============================================")
print(json.dumps(info_dict, indent=2))

if DUMP_TO_FILE:
    with open("system_info.json", "w") as fh:
        json.dump(info_dict, fh, indent=2)

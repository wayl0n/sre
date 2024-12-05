# katello_cli.py - Script that provides a user friendly Command Line Interface to the Katello API

### Usage
* Note katello_cli.py -h for more verbose help.  Username and Password are gathered either from an ENV variables or from user supplied input.
```
katello_cli.py [-h] [--list-act-keys] [--list-cv] [--list-cv-hosts] [--list-hosts] [--get-act-key GET_ACT_KEY] [--get-cv GET_CV] [--uid UID]
```

![Alt text](katello_cli_screenshot.png?raw=true "katello_cli help menu")

### Example returned data of --list-hosts

```
(env) Johnnys-MacBook-Pro% ./katello_cli.py --uid xxxxxxxx --list-hosts

Host NAME: kafka1001
Host ID: 15248
Host OS: Rocky 9.4
Host machine type OpenStack Nova
Host Content View: Rocky_9_KVM_x86-64
Host Registered through: katello001-us-proxy
*******
Host NAME: zookeeper2003
Host ID: 17488
Host OS: Rocky 8.10
Host machine type m6i.large
Host Content View: Rocky_8_Amzn_x86-64
Host Registered through: katello002-eu-proxy

```
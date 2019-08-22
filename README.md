# blackbox-trace

## Installation

You may use the provided script to streamline installation. Run the following
commands in the repository:

```bash
cd setup
bash install-audit.sh
```

Alternatively, use a package manager to install
[auditd](https://linux.die.net/man/8/auditd) along with audispd-plugins

```bash
sudo apt-get -qq update && apt-get -qq -y upgrade
sudo apt-get -qq install -y auditd audispd-plugins
```

Then, copy the audit rules into auditd's configuration directory and read the
defined rules into auditd using auditctl. The following commands are especially
helpful for resetting the original rules after changing them:

```bash
sudo cp audit.rules /etc/audit/rules.d
sudo auditctl -R /etc/audit/rules.d/audit.rules
```

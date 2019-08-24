# blackbox-trace

blackbox-trace is a tool which allows you to trace the system calls being made
by any process. It works by using the Linux Audit framework to track all system
calls being made by a given PID and allows you to fetch the most recent system
calls and the timestamps at which the calls were made. Read more about the Linux
Audit framework [here](https://wiki.archlinux.org/index.php/Audit_framework).
You may skip over the **Installation** section as it is specific to Arch Linux.
See [Further Notes](../../#further-notes) to learn more about the Linux Audit
framework tools used in blackbox-trace.

## Getting Started

These instructions will help you install blackbox-trace and start using it to
fetch the most recent system calls being made by a process.

### Automatic Installation

Use the provided script to streamline installation. Run the following commands
from inside the `blackbox-trace` directory and enter your password when prompted:

```bash
cd setup
sudo bash install-blackbox-trace.sh
```

Take the time to read [Configuring audit](../../#configuring-audit) under
[Manual Installation](../../#manual-installation). It contains commands which
will be helpful if you need to reconfigure the audit rules later. You may skip
the rest of [Manual Installation](../../#manual-installation). Also read
[MySQL Example prequisites](../../#mysql-example-prerequisites) under
[Manual Installation](../../#manual-installation) if you wish to run
[MySQL Example](../../#mysql-example) under [Usage](../../#usage).

### Manual Installation

Follow these instructions if you wish to manually install blackbox-trace.

#### Prerequisites

The following packages are required to run blackbox-trace:

- [auditd](https://packages.debian.org/stretch/auditd)
- [audispd-plugins](https://packages.debian.org/stretch/audispd-plugins)
- Python 3.5.3
- [python3-pip](https://packages.debian.org/stretch/python3-pip)

It is recommended that you use a package manager to install these packages. For
Debian 9 (Stretch):

```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y auditd audispd-plugins python3 python3-pip
```

The following Python packages which can also be found in
[`setup/requirements.txt`](./trace/requirements.txt) are also required to run
blackbox-trace:

- [psutil](https://pypi.org/project/psutil/)

It is recommended that you use pip to install these packages. Run the following
command from inside the `blackbox-trace` directory:

```bash
sudo pip3 install -r trace/requirements.txt
```

#### Configuring audit

Copy the audit rules into auditd's configuration directory and read the defined
rules into [auditd](https://linux.die.net/man/8/auditd)  using
[auditctl](https://linux.die.net/man/8/auditctl). The following commands are
especially helpful for resetting the original rules after changing them. Run all
of the following commands from inside the `blackbox-trace` directory and enter
your password when prompted:

```bash
sudo cp setup/audit.rules /etc/audit/rules.d
sudo auditctl -R /etc/audit/rules.d/audit.rules
```

#### MySQL Example prerequisites

The following packages are required to run [MySQL Example](../../#mysql-example)
under [Usage](../../#usage):

- [mysql-server](https://packages.debian.org/stretch/mysql-server)
- [mysql-client](https://packages.debian.org/stretch/mysql-client)

It is recommended that you use a package manager to install these packages. For
Debian 9 (Stretch):

```bash
sudo apt-get install -y mysql-server mysql-client
```

MySQL will start on boot time but you can also manually start it. For Debian 9
(Stretch):

```bash
sudo /etc/init.d/mysql start
```

Reference [MySQL](../../#mysql) under [Further Notes](../../#further-notes) if
you have issues with installation.

## Usage

This section contains example usages of `SystemCallTracer` from
[`trace/system_call_tracer.py`](./trace/system_call_tracer.py).

### Printing the last 50 system calls

The following Python code demonstrates how to use `SystemCallTracer` to print
the last 50 system calls made by a process. The process ID of the process to be
traced is represented in the following code as `TRACE_PID`.

```python
from systemcalltracer import SystemCallTracer
import time

# Initialize a system call tracer with the given pid
system_call_tracer = SystemCallTracer(TRACE_PID)

# Wait 1 second to give system_call_tracer time to start tracing system
# calls and print the last 50 system calls
time.sleep(1)
system_call_tracer.print_trace()
```

### Printing the last 50 system calls every second

See [`trace/continuous_trace.py`](./trace/continuous_trace.py) for an example of a
python script for printing the last 50 system calls every second. To run this
example, replace `TRACE_PID` in the following command with the process ID of the
process to be traced, run the command from inside the `blackbox-trace` directory,
and enter your password when prompted:

```bash
sudo python3 trace/continuous_trace.py TRACE_PID
```

### MySQL Example

Use [`trace/continuous_trace.py`](./trace/continuous_trace.py) to begin tracing
the MySQL daemon. Run the following command from inside the `blackbox-trace`
directory, and enter your password when prompted:

```bash
sudo python3 trace/continuous_trace.py $(pidof mysqld)
```

You should see the system call trace being printed every second. Now, you can
interact with MySQL to see what effect it has on the system call trace. You may
interact directly by connecting to the MySQL daemon with `sudo mysql` or you
may use
[`mysql_example/create_insert_script.sh`](./mysql_example/create_insert_script.sh)
to create `mysql_example/insert_script.sql`, a script which will create a
database, create a table, and insert values into that table. Run the following
command from inside the `blackbox-trace` directory to run 100 `INSERT` SQL
statements:

```bash
bash mysql_example/create_insert_script.sh 100
sudo mysql < mysql_example/insert_script.sql
```

## Further Notes

This section contains useful information for better understanding the different
components of blackbox-trace.

### Linux Audit framework

These are the manual pages for the Linux Audit framework tools used for
blackbox-trace:

- [auditd](https://linux.die.net/man/8/auditd)
- [auditctl](https://linux.die.net/man/8/auditctl)
- [ausearch](https://linux.die.net/man/8/ausearch)

### MySQL

Reference [this page](https://wiki.debian.org/MySql) for MySQL installation on
Debian 9 (Stretch).

## Acknowledgements

- **Kevin Hogan** for guiding me throughout the course of my research
- **Dr. James Purtilo** for giving me the opportunity to gain research
  experience

For more information about the software engineering team at the University of
Maryland, visit [https://seam.cs.umd.edu/](https://seam.cs.umd.edu/).

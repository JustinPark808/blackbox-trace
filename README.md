# blackbox-trace

blackbox-trace is a tool which allows you to trace the system calls being made
by any process. It works by using audit to track all system calls being made by
a given PID and allows you to fetch the most recent system calls and the
timestamps at which the calls were made.

## Installation

Use the provided script to streamline installation. Run the following commands
from inside the blackbox-trace directory and enter your password when prompted:

```bash
cd setup
bash install-blackbox-trace.sh
```

### Manual Installation

Run all of the following commands from inside the blackbox-trace directory and
enter your password when prompted:

#### Step 1.

Use a package manager to install [auditd](https://linux.die.net/man/8/auditd)
along with audispd-plugins:

```bash
sudo apt-get -qq update && apt-get -qq -y upgrade
sudo apt-get -qq install -y auditd audispd-plugins
```

#### Step 2.

Copy the audit rules into auditd's configuration directory and read the defined
rules into auditd using [auditctl](https://linux.die.net/man/8/auditctl). The
following commands are especially helpful for resetting the original rules after
changing them:

```bash
sudo cp setup/audit.rules /etc/audit/rules.d
sudo auditctl -R /etc/audit/rules.d/audit.rules
```

#### Step 3.

Install required modules for python3:

```bash
sudo pip3 -r trace/requirements.txt
```

## Usage

The following code demonstrates how to use SystemCallTracer to print the 50 most
recent system calls made by a process. The process ID of the process to be
traced is represented in the following code as `TRACE_PID`.

```python
from systemcalltracer import SystemCallTracer
import time

# Initialize a system call tracer with the given pid
system_call_tracer = SystemCallTracer(TRACE_PID)

# Wait 1 second to give system_call_tracer time to start tracing system
# calls and print the 50 most recent system calls
time.sleep(1)
system_call_tracer.print_trace()
```

See [trace/continuous_trace.py](../blob/master/trace/continuous_trace.py) for
an example of a python script for printing the 50 most recent system calls every
second. To run this example, replace `TRACE_PID` in the following command with
the process ID of the process to be traced, run the command from inside the
blackbox-trace directory, and enter your password when prompted:

```bash
python3 trace/continuous_trace.py TRACE_PID
```

## Acknowledgements

- **Kevin Hogan** for guiding me throughout the course of my research
- **Dr. James Purtilo** for giving me the opportunity to gain research
  experience

For more information about the software engineering team at the University of
Maryland, visit [https://seam.cs.umd.edu/](https://seam.cs.umd.edu/).

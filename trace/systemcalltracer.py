from collections import deque
from datetime import datetime
import psutil
import re
import subprocess
from subprocess import PIPE
import sys
import threading
import time

class SystemCallTracer:
    """System Call Tracer class.

    Traces the system calls being made by a process defined by a given
    pid. The run() method will be started and it will run in the
    background until the application exits.
    """

    def __init__(self, trace_pid):
        """ Constructor.

        Initialize system call sliding window sequence, and background
        thread necessary for tracing system calls.

        Args:
            trace_pid (int): pid of the process to trace.
        """
        # Check if the given pid exists
        if not psutil.pid_exists(trace_pid):
            print("The given pid does not exist!")
            sys.exit()

        #: int: the pid to trace
        self._trace_pid = trace_pid

        #: deque of str: the sequence of the 50 most recent system
        # calls ordered from oldest to newest
        self._syscall_sequence = deque('', 50)

        # Initialize and start background thread for tracing system
        # calls
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

        # Create a lock
        self._lock = threading.Lock()

    def _run(self):
        """ Trace system calls being made by the given pid.

        Counts the frequency of system calls and keeps track of the
        sequence in which system calls are made in a 5 second window.
        """
        # Add audit rules for tracing the given pid
        # TODO: Should we also track system calls made by child
        #       processes of the process being traced?
        #       i.e. add 'ppid={pid}' to AUDITCTL_COMMAND
        AUDITCTL_COMMAND = \
                'sudo auditctl -a always,exit -S all -F pid={pid}'.format(
                        pid=self._trace_pid)
        process = \
                subprocess.run(
                        AUDITCTL_COMMAND,
                        stdout=PIPE,
                        stderr=PIPE,
                        shell=True)

        # The format_str given to strftime() is the format in which
        # ausearch expects time arguments
        time_format_str = '%m/%d/%Y %H:%M:%S'
        last_traced_time = datetime.now().strftime(time_format_str)

        # Get the system calls made by the given pid as often as
        # possible
        # TODO: Implement realtime streaming from the audit log to
        #       process each event one by one
        while True:
            # Set the ausearch command
            AUSEARCH_COMMAND = \
                    'sudo ausearch --interpret --pid {pid} \
                    --start {last_traced_time}'.format(
                            pid=self._trace_pid,
                            last_traced_time=last_traced_time)

            # Run the ausearch command and get its output
            process = \
                    subprocess.run(
                            AUSEARCH_COMMAND,
                            stdout=PIPE,
                            stderr=PIPE,
                            shell=True)

            # Update the last traced time
            last_traced_time = datetime.now().strftime(time_format_str)

            # Get output from the ausearch command
            process_output = process.stdout.decode('utf-8').split('\n')

            # Parse each line of ausearch output for system calls and
            # acquire/release the lock to prevent access of the system
            # call sequence before it's finished updating
            # TODO: Figure out how to split the pattern string without
            #       the resulting tabs being included in the regex
            #       pattern
            pattern = \
                    re.compile(
                            '\((?P<calltime>\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d).*syscall=(?P<syscall>\S+)')
            with self._lock:
                for line in process_output:
                    # Search the current line for the regex pattern
                    match = pattern.search(line)

                    # If a match was found
                    if match is not None:
                        # Append the system call to _syscall_sequence
                        calltime = match.group('calltime')
                        syscall = match.group('syscall')
                        self._syscall_sequence.append((calltime, syscall))

    def print_trace(self):
        """ Print the last 50 system calls.

        Prints the sequence of the last 50 system calls ordered from oldest to
        newest and prints each system call with its call frequency.
        """
        # Acquire/release the lock to prevent access of the system call
        # sequence before it's finished printing
        with self._lock:
            print('**************************************************')
            print()
            print('Printing the last 50 system calls...')
            print()

            # Print last 50 system call sequence
            print('System call sequence:')
            for (calltime, syscall) in self._syscall_sequence:
                print(
                        '({calltime}, \'{syscall}\'), '.format(
                            calltime=calltime,
                            syscall=syscall),
                    end='')
            print()
            print()

            # Calculate system call frequencies
            syscall_frequencies = {}
            for _, syscall in self._syscall_sequence:
                syscall_frequencies[syscall] = \
                        syscall_frequencies.setdefault(syscall, 0) + 1

            # Print system call frequencies
            print('System call frequencies:')
            for key in sorted(syscall_frequencies):
                print(
                        '\'{syscall}\': {frequency}, '.format(
                            syscall=key,
                            frequency=syscall_frequencies[key]),
                    end='')
            print()
            print()

            print('**************************************************')
            print()

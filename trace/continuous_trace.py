#!/usr/bin/python3

import argparse
from systemcalltracer import SystemCallTracer
import time

def main():
    """Main function."""
    # Define the ArgumentParser to accept a pid
    parser = argparse.ArgumentParser(
            description='Print the 50 most recent system calls every second')
    parser.add_argument(
            'trace_pid',
            nargs=1,
            type=int,
            help='the pid to trace')

    # Parse the command line for the pid to trace
    trace_pid = parser.parse_args().trace_pid[0]

    # Initialize a system call tracer with the given pid
    system_call_tracer = SystemCallTracer(trace_pid)

    # Every second, print the 50 most recent system calls
    while True:
        time.sleep(1)
        system_call_tracer.print_trace()

# Run main function
if __name__ == '__main__':
    main()

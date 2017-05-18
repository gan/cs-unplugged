"""Control script for creating RenderDaemons."""
import os
import sys
import logging
import optparse
import multiprocessing
from RenderDaemon import RenderDaemon

def parse_args():
    """Command-line option parser for program control.

    For usage & options, type: "render.py -h".
    """
    opts = optparse.OptionParser(
        usage="{0} [options] input-data-set(s)".format(sys.argv[0]), description="Create, modify and kill render daemons.")
    opts.add_option("--daemon",
                    "-d",
                    action="store",
                    type="int",
                    help="The number of the daemon to apply the command too.",
                    default=None)
    options, arguments = opts.parse_args()
    return options, arguments

def get_daemon_pids():
    """Get the pids of all render daemons.

    Returns:
        An array of file names correlating to pidfiles.
    """
    pass


def check_pid(pid):
    """Check that process is still active.

    Args:
        pid: The process id of the process.
    Returns:
        True if the process exists and is active, False otherwise.
    """
    try:
        os.kill(pid, 0)  # kill actually means send UNIX signal.
    except OSError:
        return False
    else:
        return True


if __name__ == "__main__":
    options, arguments = parse_args()
    action = arguments[0]

    # Set-up directories
    pid_directory = os.path.join(os.getcwd(), "pidstore")
    if not os.path.exists(pid_directory):
        os.makedirs(pid_directory, exist_ok=True)
    logs_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_directory, exist_ok=True)

    logfile = os.path.join(logs_directory, "render.log")
    pidfile = os.path.join(pid_directory, "render_{}.pid".format(options.daemon))

    logging.basicConfig(filename=logfile)
    d = RenderDaemon(pidfile=pidfile)

    if action == "start":
        d.start()
    elif action == "stop":
        d.stop()
    elif action == "restart":
        d.restart()
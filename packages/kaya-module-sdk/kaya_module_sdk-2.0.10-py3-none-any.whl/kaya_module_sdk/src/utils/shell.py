import logging
from subprocess import PIPE, Popen

log = logging.getLogger("KayaPythonModuleSDK")


def shell_cmd(command: list, user=None):
    log.debug("")
    log.debug("Issuing system command: (%s)", command)
    fmt_command = " ".join(command)
    if user:
        fmt_command = f"su {user} -c '{fmt_command}'"
    with Popen(fmt_command, shell=True, stdout=PIPE, stderr=PIPE) as process:
        output, errors = process.communicate()
        log.debug("Output: (%s), Errors: (%s)", output, errors)
        return str(output).rstrip("\n"), str(errors).rstrip("\n"), process.returncode

from importlib.util import find_spec
from importlib import import_module
import json
from logging import Logger, getLogger
import socket
from subprocess import PIPE, Popen

import pysnooper  # type: ignore
from kaya_module_sdk.src.exceptions.kit_failure import KITFailureException
from kaya_module_sdk.src.exceptions.module_not_found import ModuleNotFoundException

log: Logger = getLogger(__name__)


class KITE:
    """[ KIT(E)xecuter ]: Responsibilities -

    * Imports specified module
    * Runs module with specified arguments
    * Validates the return values, errors, and other details specified in test metadata
    * Collects all test results in a easy to handle manner
    """

    test: dict
    context: dict

    def __init__(self, *tests: list, **kith_context: dict) -> None:
        self.context = kith_context
        self.test = {
            "definitions": list(tests),
            "results": {
                "ok": [],
                "nok": [],
            },
        }

    @pysnooper.snoop()
    def shell_cmd(self, command: str, user: str | None = None) -> tuple[str, str, int]:
        log.debug("Issuing system command: (%s)", command)
        if user:
            command = f"su {user} -c '{command}'"
        with Popen(command, shell=True, stdout=PIPE, stderr=PIPE) as process:
            output, errors = process.communicate()
            log.debug("Output: (%s), Errors: (%s)", output, errors)
            return (
                str(output.decode("utf-8")).rstrip("\n"),
                str(errors.decode("utf-8")).rstrip("\n"),
                process.returncode,
            )

    @pysnooper.snoop()
    def check_webserver_running(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(
                (self.context["_webserver_host"], self.context["_webserver_port"])
            )
            return result == 0

    @pysnooper.snoop()
    def check_package_installed(self, test: dict) -> bool:
        try:
            find_spec(test["package"])
        except ModuleNotFoundError as e:
            raise ModuleNotFoundException(
                f'Package {test["package"]} is not installed!'
            ) from e
        except ValueError as e:
            raise ModuleNotFoundException(
                f'Package {test["package"]} does not have a spec!'
            ) from e
        return True

    @pysnooper.snoop()
    def check_module_exists(self, test: dict) -> bool:
        try:
            module = import_module(test["package"] + ".module")
            return hasattr(module, test["module"])
        except ImportError:
            return False

    @pysnooper.snoop()
    def check_preconditions(self, *tests: dict) -> bool:
        check_results, preconditions = {}, {
            "general": {
                "webserver_running": self.check_webserver_running,
            },
            "module_specific": {
                "package_installed": self.check_package_installed,
                "module_exists": self.check_module_exists,
            },
        }
        for check in preconditions["general"]:
            check_results.update({check: preconditions["general"][check]()})
        for test in tests:
            for check in preconditions["module_specific"]:
                check_results.update(
                    {check: preconditions["module_specific"][check](test)}
                )
        if False in check_results.values():
            log.error("KIT(E) Preconditions not met -")
            for check, result in check_results.items():
                if result:
                    continue
                log.error("%s", check)
        return False not in check_results.values()

    @pysnooper.snoop()
    def module_request(self, test, request_type, request_body) -> dict:
        request_body = json.dumps(request_body)
        cmd = (
            f"curl -X {request_type} -H \"Content-Type: application/json\" -d '{request_body}' "
            f'http://{self.context["_webserver_host"]}:{self.context["_webserver_port"]}/{test["module"]}'
        )
        run_stdout, run_stderr, run_exit = self.shell_cmd(cmd)
        sanitized_out = run_stdout.replace("\\n", "").strip(" ")
        response = run_stdout + run_stderr if run_exit else sanitized_out
        errors = []
        try:
            json_out = dict(json.loads(sanitized_out))
            if json_out.get("errors"):
                errors += json_out["errors"]
            elif json_out.get("error"):
                errors.append(json_out["error"])
        except (TypeError, ValueError):
            pass
        if run_exit:
            errors.append(run_stderr)
        result = {
            "response": run_stdout if run_exit else json.loads(response),
            "errors": errors,
            "exit": run_exit,
        }
        return result

    @pysnooper.snoop()
    def module(self, test: dict, request_type: str = "GET") -> dict:
        if request_type not in ["GET", "POST"]:
            raise KITFailureException(f"Invalid request type! {request_type}")
        try:
            request_body = {arg: test["args"][arg]["value"] for arg in test["args"]}
        except KeyError as e:
            log.error("Invalid module test arg definition! Details", exc_info=e)
            raise KITFailureException("Invalid module test arg definition!") from e
        # [ NOTE ]: Make sure request body uses double quotes!!
        return self.module_request(test, request_type, request_body)

    # [ NOTE ]: Package and module names and version are declared directly in
    #           the JSON test definition.
    @pysnooper.snoop()
    def _execute(self, *tests: dict) -> dict:
        ok, nok = {}, {}
        for test in tests:
            result = self.module(test)
            test["return"] = result["response"]
            test_record = {test["name"]: {"definition": test, "result": result}}
            if result.get("errors"):
                if "any" in test["expected"].get("errors", []):
                    ok.update(test_record)
                    continue
                for error_msg in result["errors"]:
                    if error_msg in test["expected"].get("errors", []):
                        continue
                    nok.update(test_record)
                    break
                if test["name"] in nok:
                    continue
            if result.get("exit", 1) != 0:
                nok.update(test_record)
                continue
            for key in result["response"]:
                if key in ("error", "errors"):
                    continue
                expected_keys = list(test["expected"]["return"].keys())  # []
                # TODO: REFACTOR - check if values are typecast-able as
                # specified type
                if (
                    key not in expected_keys
                    or type(
                        None
                        if not len(result["response"][key])
                        else result["response"][key][0]
                    )
                    is not eval(test["expected"]["return"][key]["type"])
                    or result["response"][key]
                    != test["expected"]["return"][key]["value"]
                ):
                    nok.update(test_record)
                    break
            if test["name"] in nok:
                continue
            ok.update(test_record)
        for test_name in nok:
            nok[test_name]["definition"]["result"] = "NOK"
        for test_name in ok:
            ok[test_name]["definition"]["result"] = "OK"
        return {"ok": ok, "nok": nok}

    @pysnooper.snoop()
    def run(self, *tests: dict) -> dict:
        """
        [ INPUT ]: {
            'name': <test-id>,
            'package': '<name>',
            'package_version': '<M.m.p>',
            'module': '<name>',
            'module_version': '<M.m.p>',
            'args': {
                '<label>': {
                    'value': <arg-value>,
                    'type': <value-type>,
                    'meta': {}
                },
            },
            'expected': {
                'return': {
                    '<label>': <value>,
                    'type': <value-type>,
                    'mets': {},
                },
                'errors': []
            },
        }, {...}, {...}, ...

        [ RETURN ]: {
            'ok': {
                'test_name': {
                    'definition': {

                    },
                    'result': {

                    },
                }
            },
            'nok': {...},
        }
        """
        self.test["definitions"] = list(tests)
        check = self.check_preconditions(*tests)
        if not check:
            raise KITFailureException("Failed to verify preconditions")
        execute = self._execute(*tests)
        return execute


# CODE DUMP

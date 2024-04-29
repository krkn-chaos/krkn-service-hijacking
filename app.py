import logging
import re
import time

import yaml
from flask import Flask, request, Response

from models import HttpRequest
from utils import validate_step

app = Flask(__name__)
method_steps: dict[(str, str), list[dict[any]]] = dict[(str, str), list[dict[any]]]()
start_time = time.time()
requests: list[HttpRequest] = list[HttpRequest]()


def request_handler(params: str = None):
    splitted_url = re.search(r"^((/.*)+)/([^/]*)$", request.path)
    if splitted_url is None:
        return Response(
            f"[KRKN ERROR] url format currently not supported {request.path} "
            f"please report an issue with this log "
            f"on https://github.com/krkn-chaos/krkn-service-hijacking/issues",
            status=500,
        )
    path = splitted_url.group(1)
    steps = method_steps[(request.method, path)]
    for request_step in steps:
        if validate_step(request_step):
            return Response(
                f"[KRKN ERROR] invalid plan step for route {path}, method {request.method}. "
                f'The following parameters are missing : "{validate_step(request_step)}". Please '
                f"refer to the documentation on https://github.com/krkn-chaos/krkn-service-hijacking",
                status=500,
            )
        if time.time() - start_time <= request_step["duration"]:
            # append stats
            return Response(request_step["payload"], request_step["status"])
        # append stats
    return Response(steps[-1]["payload"], steps[-1]["status"])


with open("tests/testdata/plan.yaml") as stream:
    test_plan = yaml.safe_load(stream)

# TODO: reporting endpoint logic missing (to be loaded via env)

for step in test_plan:
    for i, method in enumerate(step["steps"]):
        app.add_url_rule(step["route"], view_func=request_handler, methods=[method])
        app.add_url_rule(
            f'{step["route"]}/<params>', view_func=request_handler, methods=[method]
        )
        method_steps[(method, step["route"])] = step["steps"][method]

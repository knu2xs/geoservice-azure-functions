import json
from typing import Any

import azure.functions as fns
import logging

app = fns.FunctionApp(http_auth_level=fns.AuthLevel.ANONYMOUS)


def get_parameter(req: fns.HttpRequest, param_name: str) -> Any:
    """Try to extract a parameter from a request, either from a URL parameter or the body."""
    # extract submitted parameters from request
    val = req.params.get(param_name)

    # if parameter not located in url parameters
    if not val:

        # try to get the response from the body
        try:
            req_body = req.get_json()

        # if no value provided, do not do anything
        except ValueError:
            pass

        # if parameter passed in POST payload
        else:
            val = req_body.get(param_name)

    # if nothing found value is none
    if not val:
        val = None

    return val


@app.route(route="info")
def info(req: fns.HttpRequest) -> fns.HttpResponse:
    """Root server info endpoint."""

    # assemble the dictionary payload for the response
    payload = {
        "currentVersion": "0.1",
        "fullVersion": "0.1.0",
        "owningSystemUrl": "https://azure.app.url",
    }

    # convert the payload to a string
    payload_str = json.dumps(payload)

    # assemble the response
    res = fns.HttpResponse(payload_str, status_code=200)


@app.route(route="query")
def query(req: fns.HttpRequest) -> fns.HttpResponse:

    # log function invocation
    logging.info('Python HTTP trigger function "info" invoked.')

    # try to retrieve name parameter
    where = get_parameter(req, "where")

    # report invocation success but missing parameter if no parameter passed
    if where is None:
        return fns.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200,
        )

    # report success if parameter value is able to be retrieved
    else:
        return fns.HttpResponse(
            f"This HTTP triggered function executed successfully.\nwhere clause: {where}"
        )

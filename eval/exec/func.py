import fdk
import json
import logging

log = logging.getLogger(__name__)


def handler(ctx, data=None, loop=None):
    # serialize the string and then pass it into the json object
    # should probably raise an error if name or code is not present
    body = json.loads(data)
    #if "code" in data and "name" in data else {"code": ""}
    # exec(body.pop("code"))
    c = """def func(a, b, c):\n return a+b+c"""
    exec(c)
    # name = body.pop("name")
    name = "func"
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(name)

    return method(**body)


if __name__ == "__main__":
    fdk.handle(handler)

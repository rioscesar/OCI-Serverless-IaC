import fdk
import json
import logging
import logging.handlers
import base64

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
log.addHandler(handler)

def handler(ctx, data=None, loop=None):
    # serialize the string and then pass it into the json object
    # should probably raise an error if name or code is not present
    body = json.loads(data) if "code" in data and "name" in data else {"code": ""}
    log.debug(body.get("code"))
    exec(body.pop("code"))

    name = body.pop("name")

    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(name)

    return method(**body)


if __name__ == "__main__":
    fdk.handle(handler)

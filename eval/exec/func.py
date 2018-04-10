import fdk
import json


def handler(ctx, data=None, loop=None):
    # serialize the string and then pass it into the json object
    # should probably raise an error if name or code is not present
    body = json.loads(data) if "code" in data and "name" in data else {"code": ""}
    exec(body.pop("code"))
    name = body.pop("name")

    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(name)

    return method(**body)


if __name__ == "__main__":
    fdk.handle(handler)

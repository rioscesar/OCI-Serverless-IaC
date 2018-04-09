import fdk
import json


def handler(ctx, data=None, loop=None):
    # serialize the string and then pass it into the json object
    # should probably raise an error if name or code is not present
    body = json.loads(data) if "code" in data and "name" in data else {"code": ""}
    code = body.pop("code")
    name = body.pop("name")
    exec(code)
    return func(**body)


if __name__ == "__main__":
    fdk.handle(handler)

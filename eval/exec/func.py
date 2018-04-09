import fdk
import json


def handler(ctx, data=None, loop=None):
    body = json.loads(data) if "code" in data else {"code": ""}
    return eval(body["code"])


if __name__ == "__main__":
    fdk.handle(handler)

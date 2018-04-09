import fdk
import json


def handler(ctx, data=None, loop=None):
    body = json.loads(data) if len(data) > 0 else {"name": "World"}
    return "Hello {0}".format(body.get("name"))


if __name__ == "__main__":
    fdk.handle(handler)

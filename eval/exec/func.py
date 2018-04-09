import fdk
import json


def handler(ctx, data=None, loop=None):
    body = json.loads(data)
    return eval(body)


if __name__ == "__main__":
    fdk.handle(handler)

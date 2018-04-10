code = """def func(a=1, b=2, c=3):\n print(a+b+c)"""

d = {
    "code": code,
    "name": "func",
    "a": 1,
    "b": 2,
    "c": 3
}

exec(d.pop("code"))
name = d.pop("name")

possibles = globals().copy()
possibles.update(locals())
method = possibles.get(name)

method(**d)

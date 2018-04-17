code = """def func(a=1, b=2, c=3):\n return a+b+c"""

d = {
    "code": code,
    "name": "func",
    "a": 1,
    "b": 2,
    "c": 3
}

def func(d): 
    exec(d.pop("code"))
    name = d.pop("name")

    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(name)

    return method(**d)
    
# print(func(d))

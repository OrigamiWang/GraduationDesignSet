d = {"a" : 1, "b": 2}
del d["a"]
if "c" in d:
    del d["c"]
print(d)

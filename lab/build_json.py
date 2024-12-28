import json

file_name = "lab/geetanjali.txt"

data = open(file_name, 'r').read()
data = data.split("\n")
find, replace = [], []

for line in data:
    if len(line.split())!=2: continue

    f, r = line.split()
    s = ""
    for ch in f:
        s += f'&#{ord(ch)};'
    find.append(s)

    t = ""
    for ch in r:
        t += f'&#{ord(ch)};'
    replace.append(t)

mapper = {
    "find": find,
    "replace": replace
}

with open('lab/geetanjali_mapper.json', 'w') as file:
    json.dump(mapper, file)
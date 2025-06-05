import json

data = {"name": "Alice", "age": 30, "city": "New York"}

with open('output.json', 'w') as f:
   json.dump(data, f)


with open('output.json', 'r') as f:
    data = json.load(f)

print(data)


#  Pretty-printing JSON   pretty-print json



data = {"name": "Alice", "age": 30, "city": "New York"}

# Print with indentation
print(json.dumps(data, indent=4))




import json

with open("recipes.json", "r") as file:
  data = json.load(file)
recipe_data = data.items()

longest_recipe = ""
length = 0

for k, v in recipe_data:
  if len(v) > length:
    longest_recipe = k
    length = len(v)

print(longest_recipe)
print(length)
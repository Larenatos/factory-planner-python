import json
with open("data.json", "r") as file:
  data = json.load(file)

# print(data["recipes"].keys())
# print(len(data["recipes"].keys()))

recipeSource = data["recipes"].items()
itemSource = data["items"]

items = {}
names = []
ing = []

# getting all the recipes
for k, v in recipeSource:
  if not v["forBuilding"] and v["inMachine"] and "package" not in k.lower():
    for product in v["products"]:
      name = itemSource[product["item"]]["name"]
      ingredients = []
      products = []
      if name not in items: 
        items[name] = []
      # getting actual names for ingredients
      for ingredient in v["ingredients"]:
        ingredients.append({
          "item": itemSource[ingredient["item"]]["name"],
          "amount": ingredient["amount"]
          })
      # getting ectual names for products
      for product in v["products"]:
        products.append({
          "item": itemSource[product["item"]]["name"],
          "amount": product["amount"]
        })
      # adding everything together
      items[name].append({
        "name":         v["name"],
        "time":         v["time"],
        "ingredients":  ingredients,
        "products":     products
      })

excluded_products = ["Coal", "Water", "Biomass"]
for product in excluded_products:
  del items[product]

# items = {k: v for k, v in sorted(list(items.items()))}

# puttin information into json files
with open("recipes.json", "w") as file:
  json.dump(items, file, indent=2, sort_keys=True)

# with open("items.json", "w") as file:
#   json.dump(items, file, indent=4)
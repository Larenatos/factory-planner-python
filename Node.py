from end_screen import end_screen_handler

# Node class
class Node:
  def __init__(self, parent, input, siblings, tree, recurse):
    self.parent = parent
    self.item = input["item"]
    self.amount = input["amount"]
    self.siblings = siblings
    self.input = []
    self.tree = tree
    self.recurse = recurse
    self.recipes = None
    self.resolved_inputs = []
  
  def find_product(self, products, product_name):
    for product in products:
      if product["item"] == product_name:
        return product

  def set_recipe(self, recipe):
    self.recipe_name = recipe["name"]

    product = self.find_product(recipe["products"], self.item)

    # how many crafts will that recipe make per minute
    rate_per_minute = product["amount"] / recipe["time"] * 60
    # how many crafts is needed to make to meet the amount user entered
    self.craft_per_minute_wanted = self.amount / product["amount"]
    # how many building are needed
    self.building_count = self.amount / rate_per_minute

    self.input = recipe["ingredients"]
    self.handle_relatives()

  def handle_relatives(self):
    if self.input:
      current_input = self.input.pop(0)
      current_input["amount"] *= self.craft_per_minute_wanted
      if self.is_ore(current_input): 
        self.resolved_inputs.append(current_input)
        return self.handle_relatives()
      self.tree.current = Node(self, current_input, self.input, self.tree, self.recurse)
      self.resolved_inputs.append(self.tree.current)
      self.recurse()
      return
    if self.parent:
      self.tree.current = self.parent
      self.parent.handle_relatives()
      return
    else:
      dict_tree = self.tree.to_dict()

      end_screen_handler(self.tree.t, dict_tree)

  def is_ore(self, input):
    ores = ["Limestone", "Copper Ore", "Iron Ore", "Coal", "Raw Quartz", "Crude Oil", "Water", "Bauxite", "Uranium", "Caterium Ore", "Sulfur", "Nitrogen Gas", "Uranium Waste"]
    ores = [ore.lower() for ore in ores]

    if input["item"].lower() in ores:
        return True
    return False

  # printing for easier debugging
  def __repr__(self):
    #try:
    resolved_inputs_text = []
    for input in self.resolved_inputs:
      if type(input) is dict:
        resolved_inputs_text.append(input["item"])
      else:
        resolved_inputs_text.append(input.item)
    siblings_text = []
    if self.siblings:
      siblings_text = [sibling["item"] for sibling in self.siblings]
    return f"""'Item: {self.item}, amount: {self.amount}, buildings: {self.building_count} 
recipe_name: {self.recipe_name} craft: {self.craft_per_minute_wanted}, siblings: {siblings_text}, 
inputs: {[input["item"] for input in self.input]},
resolved_inputs: {resolved_inputs_text}'"""
    #except (NameError, AttributeError) as e:
      # return f"'Name: {self.item}, amount: {self.amount}'"
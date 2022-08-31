from classes import Selection, Button, Tree, Position, Dimensions
from Node import Node
from copy import deepcopy

def draw(t):
  t.clear()
  t.goto(0, 400)
  t.write(f"There are more than 1 recipe to choose from. \nChoose which one you want to use for you factory. \nEnter your answer as the number infront of the recipe you want to use.", align="center", font=("arial", 15, "normal"))

def alternate_recipe_handler(t, recipe_data, final_product, final_amount):
  # submit
  position = Position(-60 ,-380)
  dimensions = Dimensions(120, 50)
  button_submit = Button(position, dimensions, "Submit", None, t)

  position = Position(-450, 370)
  alternate_recipe_selection = Selection(position, (900, 180), t)

  input = {
    "amount": final_amount,
    "item": final_product
  }

  root = Node(None, input, None, None, None)
  tree = Tree(root, t)
  # current is a node
  tree.current.tree = tree

  def redraw():
    draw(t)
    alternate_recipe_selection.draw()
    button_submit.draw()

  alternate_recipe_selection.set_redraw_screen(redraw)

  def recurse():
    node = tree.current
    recipes = deepcopy(recipe_data[node.item])
    if len(recipes) == 1:
      tree.current.set_recipe(recipes[0])
      return

    tree.current.recipes = recipes
    setup(recipes)

  tree.current.recurse = recurse

  def setup(recipes):
    recipe_options = []
    for i in range(len(recipes)):
      recipe_text = [f"{i+1:>2} {recipes[i]['name']:45} Products:"]

      for product in recipes[i]["products"]:
        recipe_text.append(f"\n{product['amount']:>52} {product['item']:27}") 
      
      recipe_text.append(f"\n{'Ingredients:':>61}") 

      for ingredient in recipes[i]["ingredients"]:
        recipe_text.append(f"\n{ingredient['amount']:>52} {ingredient['item']:27}") 

      recipe_options.append([recipe_text])  

    alternate_recipe_selection.set_content(recipe_options)
    redraw()

  def collect_recipe():
    index = alternate_recipe_selection.selected_row
    recipe = tree.current.recipes[index]
    tree.current.set_recipe(recipe)

  button_submit.clicked = collect_recipe
  
  t.onscreenclick(button_submit.check_click)
  t.onscreenclick(alternate_recipe_selection.onclick, add=True)
  recurse()
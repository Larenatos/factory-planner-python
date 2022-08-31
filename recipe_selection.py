import json
from alternate_recipe_selection import alternate_recipe_handler
from classes import Selection, Button, Input, Position, Dimensions

def draw_recipes(t):
  t.clear()
  t.pu()

  t.goto(-850, 450)
  t.write("Select by clicking on a recipe you want to use.", font=("arial", 25, "normal"))
  t.goto(-240, -300)
  t.write("Click the box to set a custom amount", font=("arial", 20, "normal"))

def prepare_recipes(t):
  with open("recipes.json", "r") as file:
    recipe_data = json.load(file)

  recipes = []

  row_data = []
  col = 0
  # looping trough the keys in the recipes.json
  for k in recipe_data:
    if col == 5:
      recipes.append(row_data)
      row_data = []
      col = 0
    row_data.append(k)
    col += 1
  if len(row_data):
    recipes.append(row_data)

  position = Position(-860, 440)

  recipe_selection = Selection(position, (340, 35), t)
  recipe_selection.set_content(recipes)

  # input
  position = Position(-100, -320)
  dimensions = Dimensions(200, 50)
  input = Input(position, dimensions, 0, "num", "Enter a number", t)
  
  # next
  position = Position(-55, -390)
  dimensions = Dimensions(110, 50)
  button_next = Button(position, dimensions, "Next", alternate_recipe_handler, t)

  interactions = (recipe_selection, input, button_next)

  return interactions, recipe_data

def recipe_handler(t):
  interactions, recipe_data = prepare_recipes(t)

  recipe_selection, input, button_next = interactions

  def redraw():
    draw_recipes(t)
    for interaction in interactions:
      interaction.draw()

  def onclick(x, y):
    input.check_click(x, y)
    button_next.check_click(x, y, t, recipe_data, recipe_selection.selected_item, input.content)
  
  for interaction in interactions:
    interaction.set_redraw_screen(redraw)

  redraw()
  t.onscreenclick(onclick)
  t.onscreenclick(recipe_selection.onclick, add=True)
import json

from classes import Button, Position, Dimensions
from draw_tree import draw_tree
import instructions
from utils import file_path

def draw(t):
  t.clear()
  t.goto(0, 200)
  t.write("You have succesfully made a tree. You can view it by pressing Draw. \nIf you are happy with the out put you can also hit save to save the tree for later use.", align="center", font=("arial", 20, "normal"))

def save_tree(t, tree, prompt):
  tree_name = t.textinput("Enter the name", prompt)
  abs_file_path = file_path(tree_name)
  try:
    with open(f"{abs_file_path}.json", "x") as file:
      json.dump(tree, file)
  except (FileExistsError) as e:
    save_tree(t, tree, "That name was taken. Enter another.")

def end_screen_handler(t, tree):
  # draw
  position = Position(-270, 0)
  dimensions = Dimensions(100, 50)
  button_draw = Button(position, dimensions, "Draw", None, t)

  # save
  position = Position(-150, 0)
  button_save = Button(position, dimensions, "Save", save_tree, t)

  # back to start
  position = Position(-30, 0)
  dimensions = Dimensions(300, 50)
  button_instructions = Button(position, dimensions, "Back to start", instructions.draw_instructions, t)

  interactions = [button_draw, button_save, button_instructions]

  def redraw():
    print("redrawn")
    draw(t)
    for interaction in interactions:
      interaction.draw()

  button_draw.set_redraw_screen(redraw)

  def draw_tree_func(tree):
    # t.clear()
    draw_tree(tree)
    # redraw()

  button_draw.set_clicked(draw_tree_func)

  def onclick(x, y):
    button_draw.check_click(x, y, tree)
    button_save.check_click(x, y, t, tree, "Enter a name for this save.")
    button_instructions.check_click(x, y, t)

  t.onscreenclick(onclick)
  redraw()
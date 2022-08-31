import os

from classes import Selection, Button, Position, Dimensions
from draw_tree import draw_saved_tree
from utils import file_path
import instructions

def draw(t):
  t.clear()
  t.pu()

  # instructions
  t.goto(-500, 420)
  t.write("If there are no saves displayed on the left then you need to go ahead and make one and then come back here.", font=("arial", 20, "normal"))
  t.goto(-500, 370)
  t.write("Now that you got a save made you can select them and draw, rename or delete them.", font=("arial", 20, "normal"))


def save_handler(t):
  position = Position(-850, 450)
  save_selection = Selection(position, (300, 35), t)

  def update_selection():
    saved_files = os.listdir("saved_trees")
    saved_files = [[file] for file in saved_files]
    save_selection.set_content(saved_files)

  update_selection()

  def rename_save(tree_name):
    abs_file_path = file_path(tree_name)

    new_name = t.textinput("", "Enter new name for the file")
    os.rename(abs_file_path, f"saved_trees\\{new_name}.json")
    t.clear()
    update_selection()
    redraw()

  def delete_save(tree_name):
    abs_file_path = file_path(tree_name)

    check = t.textinput("ARE YOU SURE YOU WANT TO DELETE THIS FILE?", f"{'Type Yes or No':100}")
    if check.lower() == "yes":
      os.remove(abs_file_path)
      t.clear()
      update_selection()
      redraw()

  # draw
  position = Position(-200, 0)
  dimensions = Dimensions(100, 50)
  button_draw = Button(position, dimensions, "Draw", draw_saved_tree, t)

  # rename
  position = Position(-70, 0)
  dimensions = Dimensions(140, 50)
  button_rename = Button(position, dimensions, "Rename", rename_save, t)

  # delete
  position = Position(100, 0)
  dimensions = Dimensions(140, 50)
  button_delete = Button(position, dimensions, "Delete", delete_save, t)
  
  # back
  position = Position(260, 0)
  dimensions = Dimensions(100, 50)
  button_back = Button(position, dimensions, "Back", instructions.draw_instructions, t)

  interactions = (button_draw, button_rename, button_delete, save_selection, button_back)

  def redraw():
    draw(t)
    for interaction in interactions:
      interaction.draw()

  def onclick(x, y):
    button_draw.check_click(x, y, save_selection.selected_item)
    button_rename.check_click(x, y, save_selection.selected_item)
    button_delete.check_click(x, y, save_selection.selected_item)
    button_back.check_click(x, y, t)

  save_selection.set_redraw_screen(redraw)

  redraw()
  t.onscreenclick(onclick)
  t.onscreenclick(save_selection.onclick, add=True)
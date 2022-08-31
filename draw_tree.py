import turtle
import tkinter
import json
from utils import file_path

# we use this as a library for the other file so everything needs to be in a function

def draw_saved_tree(tree_name):
  abs_file_path = file_path(tree_name)

  with open(abs_file_path, "r") as file:
    tree = json.load(file)
  draw_tree(tree)

def draw_tree(tree):
  # making the canvas scrollable with tkinter
  root = tkinter.Tk()

  # setting the canvas the user sees
  cv = turtle.ScrolledCanvas(root, width=1800, height=1000)
  cv.pack()

  # screen will be the canvas
  screen = turtle.TurtleScreen(cv)
  # the hole canvas size
  screen.screensize(4000, 13000)
  # background color
  screen.bgcolor("black")
  t = turtle.RawTurtle(screen)

  # defining the size of nodes in the tree
  unit_width = 275
  unit_height = 55

  # ores dictionary
  ores_total = {}

  # defining color speed and stuff
  t.hideturtle()
  t.pensize(3)
  # making the do the drawing instantly
  t._tracer(0, 0)

  t.color("white")
  t.penup()

  # function to get the x value for each node
  def get_x(width):
      return width * unit_width - 890 - unit_width

  # function to get the y value for each node
  def get_y(height):
      return -1 * height * unit_height + 490 + unit_height

  # recursive function that draws node and then children for that node (ingredients)
  def draw_node(width, height, node):
    # getting the x and y coordinates
    x, y = get_x(width), get_y(height)
    # part of making the line so everything links together
    t.goto(x, y-40)
    t.penup()
    # going a bit in so there is nice padding between the border and text
    t.goto(x + 10, y-5)

    # writing the data in the recipe
    t.write(f"{node['item']} {round(node['amount'], 5)}/min", font=('Arial', 10, 'normal'))
    t.goto(x + 10, y-20)
    if "input" in node:
      t.write(f"Recipe: {node['recipe_name']}", font=('Arial', 10, 'normal'))
      t.goto(x + 10, y-35)
      t.write(f"Building count: {node['building_count']}", font=('Arial', 10, 'normal'))

    # making the line below text
    t.penup()
    t.goto(x, y-40)
    t.pendown()
    t.goto(x+unit_width, y-40)

    # if there are any ingredients for the node / recipe
    if "input" in node:
      # increasing the width and height for children so they go down like staircase
      child_width = width + 1
      child_height = height + 1
      # looping trough the inputs for node
      for child in node["input"]:
        #calling the same function to draw next node
        # and getting the the hight of the last children(ore)
        child_height += draw_node(child_width, child_height, child)
        t.penup()
        # going to the bottom right corner of the current node
        t.goto(x + unit_width, y - unit_height)
        # part of the making the line for the next node
        t.pendown()
      # returning the height(length) of children
      return child_height - height
    # when drawn node was ore return 1

    # saving the ore info
    ores_listed_so_far = ores_total.keys()
    if node["item"] not in ores_listed_so_far:
      ores_total[node["item"]] = {
        "item": node["item"],
        "amount": node["amount"]
      }
    else: 
      ores_total[node["item"]]["amount"] += node["amount"]
    return 1
  
  # drawing the ore and total amount of that below the first element
  def draw_ores(height, ores):
    ores = ores.items()
    t.penup()
    x = get_x(1)
    y = get_y(height)
    for k, ore in ores:
      y -= 25
      t.goto(x, y)
      t.write(f"{ore['item']} {round(ore['amount'], 5)}", font=('Arial', 10, 'normal'))
      height += 1
    
  #calling the draw_node function with the tree that program got from the main.py
  draw_node(1, 1, tree)
  draw_ores(2, ores_total)
  # part of making the scrollable canvas
  root.mainloop()
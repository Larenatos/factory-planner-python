from collections import namedtuple
from math import floor


# named tuples
Position = namedtuple("Position", "x y")
Dimensions = namedtuple("Dimensions", "width height")


# Button class
class Button:
  def __init__(self, position, dimensions, content, clicked, t):
    self.position = position
    self.dimensions = dimensions
    self.content = content
    self.t = t
    self.x_range = (position.x, position.x + dimensions.width)
    self.y_range = (position.y - dimensions.height, position.y)
    self.clicked = clicked

  def set_redraw_screen(self, redraw_screen):
    self.redraw_screen = redraw_screen

  def set_clicked(self, clicked):
    self.clicked = clicked

  def draw(self):
    position = self.position
    t = self.t
    if type(self.content) is float:
      content = f"{self.content:g}"
    else:
      content = self.content
    dimensions = self.dimensions
  
    t.color("yellow")
    t.pu()
    t.goto(position)
    t.pd()
    t.goto(position.x, position.y - dimensions.height)
    t.goto(position.x + dimensions.width, position.y - dimensions.height)
    t.goto(position.x + dimensions.width, position.y)
    t.goto(position)
    t.pu()
    center = (position.x + (dimensions.width / 2), position.y - (dimensions.height / 2) - 16)
    t.goto(center)
    t.write(content, align="center", font=("Consolas", 23, "normal"))
    t.color("white")
  
  def check_click(self, x, y, *args):
    if x in range(*self.x_range) and y in range(*self.y_range):
      self.clicked(*args)


# input display button class
class Input(Button):
  def __init__(self, position, dimensions, content, type, custom_text, t):
    Button.__init__(self, position, dimensions, content, self.onclick, t)
    self.custom_text = custom_text
    self.type = type

  def onclick(self):
    t = self.t
    match self.type:
      case "num":
        self.content = t.numinput('', self.custom_text, 0, minval=0, maxval=99999)
      case "text":
        self.content = t.textinput("", self.custom_text)
    
    self.redraw_screen()


# Selection class
class Selection:
  def __init__(self, position, cell_dimensions, t):
    self.cell_width, self.cell_height = cell_dimensions
    self.position = position
    self.t = t

    self.reset_selected()
    
  def set_content(self, content):
    self.reset_selected()
    self.content = content
    self.width = len(content[0])
    self.height = len(content)
    self.x_range = (self.position.x, self.position.x + (self.cell_width * self.width))
    self.y_range = (self.position.y - (self.cell_height * self.height), self.position.y)

  def set_redraw_screen(self, redraw_screen):
    self.redraw_screen = redraw_screen

  def reset_selected(self):
    self.selected_row = None
    self.selected_col = None

    self.selected_item = ""

  def draw_grid(self):
    t = self.t
    t.pu()

    # horizontal
    x, y = self.position
    for _ in range(self.height + 1):
      t.goto(x, y)
      t.pd()
      t.goto(x + (self.width * self.cell_width), y)
      y -= self.cell_height
      t.pu()
    
    # vertical
    x, y = self.position
    for _ in range(self.width + 1):
      t.goto(x, y)
      t.pd()
      t.goto(x, y - self.cell_height * (self.height))
      x += self.cell_width
      t.pu()
  
  def write_text(self):
    t = self.t

    for row in range(self.height):
      row_len = len(self.content[row])
      for col in range(self.width):
        if col == row_len: break
        cell_content = self.content[row][col]
        x = self.position.x + 10 + (col * self.cell_width)

        if type(cell_content) is list:
          y = self.position.y - 30 - (row * self.cell_height)
          
          for line in cell_content:
            t.goto(x, y)
            t.write(line, font=("consolas", 15, "normal"))
            y -= 20

        else:
          y = self.position.y - (self.cell_height / 2) - 10 - (row * self.cell_height)
          t.goto(x, y)
          t.write(cell_content, font=("consolas", 15, "normal"))
  
  def highlight_selected(self):
    y = self.position.y - self.cell_height * self.selected_row
    x = self.position.x + self.cell_width * self.selected_col
    t = self.t
    t.color("green")
    t.pensize(4)
    t.goto(x + 3, y - 3)
    t.pd()
    t.goto(x + self.cell_width - 3, y - 3)
    t.goto(x + self.cell_width - 3, y - self.cell_height + 3)
    t.goto(x + 3, y - self.cell_height + 3)
    t.goto(x + 3, y - 3)
    t.pu()
    t.update()
    t.pensize(2)
    t.color("white")
  
  def draw(self):
    self.draw_grid()
    self.write_text()

    if self.selected_item:
      self.highlight_selected()

  def onclick(self, x, y):
    if not (x in range(*self.x_range) and y in range(*self.y_range)):
      return
    
    col = floor((x-self.position.x) / self.cell_width)
    row = floor((y-self.position.y) / -self.cell_height)

    row_len = len(self.content[row])
    if col >= row_len: return

    self.selected_item = self.content[row][col]
    self.selected_row = row
    self.selected_col = col

    self.redraw_screen()


# Tree class
class Tree:
  def __init__(self, root, t):
    self.root = root
    self.current = root
    self.t = t
  
  def to_dict(self):
    return self.parse_node(self.root)
    
  def parse_node(self, current_node):
    if type(current_node) is dict:
      return current_node
    output = {
      "item": current_node.item,
      "recipe_name": current_node.recipe_name,
      "building_count": round(current_node.building_count, 5),
      "amount": round(current_node.amount, 5),
      "input": []
    }

    for ingredient in current_node.resolved_inputs:
      output["input"].append(self.parse_node(ingredient))

    return output
from classes import Button, Position, Dimensions
from recipe_selection import recipe_handler
from saved_screen import save_handler

def draw_instructions(t):
  t.clear()
  t.color("#fff")

  x, y = -850, 450
  t.goto(x, y)
  t.write("Instruction for using Factoy Planner", font=('Arial', 30, 'normal'))
  t.goto(x - 5, y - 5)
  t.pendown()
  t.goto(x + 610, y - 5)
  t.penup()
  t.goto(x, y - 70)
  t.write("What is the idea behind Factory Planner?", font=('Arial', 20, 'normal'))
  t.goto(x, y - 100)
  t.write("How to use it?", font=('Arial', 20, 'normal'))
  t.goto(x, y - 130)
  t.write("What is Satisfactory?", font=('Arial', 20, 'normal'))
  # writing what satisfactory is
  t.goto(x, y - 200)
  t.write("Satisfactory is a game of factory management and planet exploitation. You are dropped onto an alien planet with a handful of tools and must harvest the planet's natural resources to construct ", font=('Arial', 15, 'normal'))
  t.goto(x, y - 225)
  t.write("increasingly complex factories for automating all your resource needs. After you are set up, it will be time to build the Space Elevator and begin Project Assembly,", font=('Arial', 15, 'normal'))
  t.goto(x, y - 250)
  t.write("supplying FICSIT with increasingly numerous and complex components for their unknown purposes.", font=('Arial', 15, 'normal'))
  # writing how this app works
  t.goto(x, y - 300)
  t.write("This app let's you select any item that can be processed in satisfactory example reinforced iron plate or circuit board.", font=('Arial', 15, 'normal'))
  t.goto(x, y - 325)
  t.write("First the app will ask you to select a item and how many you want to make per minute.", font=('Arial', 15, 'normal'))
  t.goto(x, y - 350)
  t.write("After you entered those values the app will start to ask you for alternate recipes to use. It will do so because there are only few items that can be made with only 1 recipe ", font=('Arial', 15, 'normal'))
  t.goto(x, y - 375)
  t.write("And others have multiple ways to create. Once it has made the tree from inputs user entered it will pass that tree into turtle program.", font=('Arial', 15, 'normal'))
  t.goto(x, y - 400)
  t.write("It will draw it for you in a nice staircase shape starting from top to bottom. I will mention my friend Alex for helping me to make this app!", font=('Arial', 15, 'normal'))
  t.goto(x, y - 425)
  t.write("You can click on saved to go and see all the saved trees you have made. There is no limit. You can also click on next to start making new tree.", font=('Arial', 15, 'normal'))

  position = Position(15, -200)
  dimensions = Dimensions(110, 50)
  # button next
  button_next = Button(position, dimensions, "Next", recipe_handler, t)
  # button saved
  position = Position(-125, -200)
  button_saved = Button(position, dimensions, "Saved", save_handler, t)

  button_next.draw()
  button_saved.draw()

  def onclick(x, y):
    button_next.check_click(x, y, t)
    button_saved.check_click(x, y, t)

  t.onscreenclick(onclick)
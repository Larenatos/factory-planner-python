import turtle as t

from instructions import draw_instructions

# setup
t.setup(1800, 1000)
t.bgcolor("#000")
t.speed(0)
t.tracer(0, 0)
t.pensize(2)
t.hideturtle()
t.pu()

draw_instructions(t)

t.mainloop()
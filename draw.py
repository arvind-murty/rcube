
import sys
from cube import Index
from cube import Cube
from solver import Solver
from pyglet.gl import *

width  = 40
x_pos  = 400
y_pos  = 300

cube   = Cube()
solver = Solver (cube)
window = pyglet.window.Window(1000, 600)

def color(c):
    if c == Index.B:
        return (0, 0, 255)
    if c == Index.G:
        return (0, 255, 0)
    if c == Index.O:
        return (255, 165, 0)
    if c == Index.R:
        return (255, 0, 0)
    if c == Index.W:
        return (255, 255, 255)
    if c == Index.Y:
        return (255, 255, 0)
        
    assert False
    

def draw_face (a, b, face, size):
    for i in range(0,3):
        for j in range(0,3):
            x = a + j * size
            y = b - i * size + 2 * size
            w = size - 3
            (n1, n2) = face.get_neighbors(i, j)
            c = color (face.get_color (n1, n2))
            c = c + c + c + c
            pyglet.graphics.draw (4, pyglet.gl.GL_POLYGON, ('v2i', (x, y, x + w, y, x + w, y + w, x, y + w)), ('c3B', c) )
 

def draw():
    global cube
    global width
    global x_pos
    global y_pos

    face = cube.get_face (cube.center)
    
    
    draw_face (x_pos, y_pos, face, width)
    draw_face (x_pos, y_pos + 3 * width, face.neighbors[0], width)
    draw_face (x_pos + 3 * width, y_pos, face.neighbors[1], width)
    draw_face (x_pos, y_pos - 3 * width, face.neighbors[2], width)
    draw_face (x_pos - 3 * width, y_pos, face.neighbors[3], width)
    draw_face (x_pos + 3 * width + 3 * width, y_pos, face.opposite, width)
    

def rotate(a,b):
    global cube
    global width
    global x_pos
    global y_pos

    
    f = cube.get_face (cube.center)
    n = (f, f.neighbors[0], f.neighbors[1], f.neighbors[2], f.neighbors[3], f.opposite)
    o = ((0,0), (0, 3 * width), (3 * width, 0), (0, -3 * width), (-3 * width, 0), (6 * width, 0))
    
    for i in range(0, len(n)):
        x = x_pos + o[i][0]
        y = y_pos + o[i][1]
        f = n[i]
        if a > x and a < x + 3 * width and b > y and b < y + 3 * width:
            cube.rotate (f.color)
            return True
            
    return False

def set_center(x,y):
    global width
    global cube

    if x < 10 or x > (7 + len(Index.COLORS) * width):
        return False
    if y < 10 or y > 10 + width:
        return False
    
    idx = (x - 10)//width
    
    return cube.set_center (Index.COLORS[idx])
 
def solve(x,y):
    global width
    global window
    global cube
    global solver

    if y < 10 or y > 10 + width:
        return False
        
    if x > window.width - 10 - 1 * width and x < window.width - 10:
        center = cube.center
        try:
            solver.solve()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            
        cube.set_center (center) 
        return True
        
    return False              


def undo(x,y):
    global width
    global window
    global cube

    if y < 10 or y > 10 + width:
        return False
        
    if x > window.width - 10 - 3 * width and x < window.width - 10 - 2 * width:
        cube.undo()
        return True
        
    return False              
    
def buttons():
    global width
    global window
    
    for i in range(0, len(Index.COLORS)):
        x = 10 + i * width
        y = 10
        w = width - 3
        c = color (Index.COLORS[i]) + color (Index.COLORS[i]) + color (Index.COLORS[i]) + color (Index.COLORS[i])
        pyglet.graphics.draw (4, pyglet.gl.GL_POLYGON, ('v2i', (x, y, x + w, y, x + w, y + w, x, y + w)), ('c3B', c) )
    
    c = (255, 255, 255)
    
    x = window.width - 10 - 3 * width
    y = 10 + width//2
    
    pyglet.graphics.draw (3, pyglet.gl.GL_POLYGON, ('v2i', (x, y, x + width, y + width//2, x + width, y - width//2)), ('c3B', c + c + c) )
    pyglet.graphics.draw (3, pyglet.gl.GL_POLYGON, ('v2i', (x + 3 * width, y, x + 2 * width, y + width//2, x + 2 * width, y - width//2)), ('c3B', c + c + c) )

@window.event
def on_mouse_press(x, y, button, modifiers):
    #print ('on mouse press at (' + str(x) + ' ' + str(y) + ')')
    if rotate(x,y) or solve (x,y) or undo (x,y) or set_center(x,y):
        return True
    
    

    
@window.event
def on_draw():
    buttons()
    draw()  
    
pyglet.app.run()

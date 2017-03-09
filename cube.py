


class Index:

    G = 'g'
    O = 'o'
    W = 'w'
    B = 'b'
    R = 'r'
    Y = 'y'
    
    COLORS = (G, O, W, B, R, Y)
    STARTS = (1, 5, 1, 2, 0, 3)

    def __init__ (self, list):
        colors = []
        for c in Index.COLORS:
            if c in list:
                colors.append (c)
        self.colors = tuple (colors)


    def __hash__ (self):
        return hash (self.colors)
 
    def __eq__ (self, other):
        return self.colors == other.colors
 
    def __str__ (self):
        return str(self.colors)

class Face:
    def __init__(self, idx, colors, faces):
        self.idx   = idx
        self.color = colors[idx]

        faces[self.color] = self

        self.neighbors = []
        self.opposite = None
        
        n = Index.STARTS[idx]
        while len(self.neighbors) != 4:
            if n != idx and n != ((idx + 3) % len(Index.COLORS)):
                if colors[n] in faces:
                    self.neighbors.append (faces.get (colors[n]))
                else:
                    self.neighbors.append (Face(n, colors, faces))
            n = (n + 1) % len(Index.COLORS)
        
            
            if n == ((idx + 3) % len(Index.COLORS)):
                if colors[n] in faces:
                    self.opposite = faces.get (colors[n])
                else:
                    self.opposite =  Face(n, colors, faces)
                    
        if self.idx % 2 == 1:
            self.neighbors.reverse()
        
        self.colors = {}
        for i in range(0,4):
            h = self.neighbors[i]
            p = self.neighbors[(i - 1) % len(self.neighbors)]
            n = self.neighbors[(i + 1) % len(self.neighbors)]
                               

            assert (len(self.colors) <= 9)
            
            self.colors[Index([])]                 = self.color
            self.colors[Index([h.color])]          = self.color
            self.colors[Index([h.color, p.color])] = self.color
            self.colors[Index([h.color, n.color])] = self.color

    def order (self):
        result = []
        for f in self.neighbors:
            result.append (f.color)
        return result
        
    def reset_order (self, face, idx):        
        curr = self.neighbors.index(face)
        
        assert curr >= 0 and curr < len(self.neighbors)
        
        while curr > idx:
            self.neighbors.append (self.neighbors.pop(0))
            curr = curr - 1
        while curr < idx:
            self.neighbors.insert (0, self.neighbors.pop())
            curr = curr + 1
        
        
    def reset_center(self):
        self.neighbors[0].reset_order (self, 2)
        self.neighbors[1].reset_order (self, 3)
        self.neighbors[2].reset_order (self, 0)
        self.neighbors[3].reset_order (self, 1)
        self.opposite.reset_order (self.neighbors[1], 3)
        
    
    def get_neighbors (self, i, j):
        n1 = None
        if i == 0:
            n1 = self.neighbors[0]
        if i == 2:
            n1 = self.neighbors[2]

        n2 = None
        if j == 0:
            n2 = self.neighbors[3]
        if j == 2:
            n2 = self.neighbors[1]
        return (n1, n2)
        
    def get_color (self, n1 = None, n2 = None):
        if type(n1) == type(self):
            n1 = n1.color
        if type(n2) == type(self):
            n2 = n2.color
        if n1 != None and n2 != None:
            return self.colors[Index([n1, n2])]
        if n1 != None:
            return self.colors[Index([n1])]
        if n2 != None:
            return self.colors[Index([n2])]
        return self.colors[Index([])]
    
    def adjust_colors (self, primary, right, opposite, left, neighbors):
    
        assert primary != right
        assert left    != right
        assert primary != left
        assert opposite != right
        assert opposite != left
        assert opposite != primary
        
        self.colors[Index ((primary, left))]   = neighbors[left][Index((primary, opposite))]
        self.colors[Index ((primary))]         = neighbors[left][Index((primary))]
        self.colors[Index ((primary, right))]  = neighbors[left][Index((primary, self.color))]

        assert (len(self.colors)) == 9
               
    def anticlockwise (self, faces):
        n = self.neighbors
        prev = self.colors[Index([n[0].color])]
                           
        for i in range(3,-1, -1):
            prev, self.colors[Index([n[i].color])] = self.colors[Index([n[i].color])], prev
                              
        prev = self.colors[Index([n[0].color, n[1].color])]
        for i in range(3,-1, -1):
            prev, self.colors[Index([n[i].color, n[(i+1)%4].color])] = self.colors[Index([n[i].color, n[(i+1)%4].color])], prev
                              
        neighbors = {}
        for i in self.neighbors:
            neighbors[i.color] = i.colors.copy()
        for i in range(0,4):
            n[i].adjust_colors (self.color, n[(i+3) % len(n)].color, n[(i+2)% len(n)].color, n[(i+1)%len(n)].color, neighbors)
                     
    def clockwise (self, faces):
        n = self.neighbors
        
        prev = self.colors[Index([n[3].color])]
        for i in range(0,4):
            prev, self.colors[Index([n[i].color])] = self.colors[Index([n[i].color])], prev

        prev = self.colors[Index([n[3].color, n[0].color])]
        for i in range(0,4):
            prev, self.colors[Index([n[i].color, n[(i+1)%4].color])] = self.colors[Index([n[i].color, n[(i+1)%4].color])], prev
                              
        neighbors = {}
        for i in self.neighbors:
            copy = {}
            for k in i.colors:
                copy[k] = i.colors[k]
            neighbors[i.color] = copy

        for i in range(0,4):
            n[i].adjust_colors (self.color, n[(i+1) % len(n)].color, n[(i+2)% len(n)].color, n[(i+3)%len(n)].color, neighbors)
    
                             
    def __str__(self):
        result = ''
        n = self.neighbors
        result = result + '\n  (' + n[0].color + ',' + n[1].color + ',' + n[2].color + ',' + n[3].color + ')\n'
        
        result = result + '\n    ' + self.get_color(n[-1], n[0]) + ' ' + self.get_color(n[0]) + ' ' + self.get_color(n[0], n[1])
        result = result + '\n    ' + self.get_color(n[-1])       + ' ' + self.get_color()     + ' ' + self.get_color(n[1])
        result = result + '\n    ' + self.get_color(n[-1], n[2]) + ' ' + self.get_color(n[2]) + ' ' + self.get_color(n[2], n[1])
        return result
        
class Cube (object):


    def __init__ (self):
        
        self.faces = {}
        self.undo_rotations = []
        self.redo_rotations = []
        

        for idx in range(0, len(Index.COLORS)):
            c = Index.COLORS[idx]
            if not c in self.faces:
                Face(idx, Index.COLORS, self.faces)
                
        self.center = Index.G
        
    def __str__ (self):
        result = ''
        for c in Index.COLORS:
            result = result + str(c) + '  ->  ' + str(self.faces[c]) + '\n'
        return result
        
    def set_center (self, c):
        if not c in Index.COLORS:
            return False
        if c == self.center:
            return False
        
        self.center = c
        self.faces[c].reset_center()
        return True
            
    def get_face (self, color):
        return self.faces[color]

    def get_faces (self):
        self.faces.items()
        
    def undo (self):
        if len(self.undo_rotations) == 0:
            return
            
        (color, dir) = self.undo_rotations.pop();
        self.redo_rotations.append((color, dir))
        
        if dir:
            self.faces[color].anticlockwise (self.faces)
        else:
            self.faces[color].clockwise (self.faces)

    def redo (self):
        if len(self.redo_rotations) == 0:
            return
            
        (color, dir) = self.redo_rotations.pop();
        self.undo_rotations.append((color, dir))
        if dir:
            self.faces[color].clockwise (self.faces)
        else:
            self.faces[color].anticlockwise (self.faces)

        
    def clockwise (self, color, track = True):
        if color in self.faces:

            self.redo_rotations = []
            self.undo_rotations.append ((color, True))
            self.faces[color].clockwise (self.faces)
            
            
    def anticlockwise (self, color, track = True):
        if color in self.faces:
            
            self.redo_rotations = []
            self.undo_rotations.append ((color, False))
            self.faces[color].anticlockwise (self.faces)
       
    def rotate(self, color, clockwise = True):
        if clockwise:
            self.clockwise(color)
        else:
            self.anticlockwise(color)
        
        



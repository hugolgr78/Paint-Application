import customtkinter as ctk
from settings import *
import sys
from tkinter import ALL
from CTkMessagebox import CTkMessagebox
from PIL import ImageGrab

class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, bgcolor, paintVars, optionVars):

        super().__init__(parent, bg = bgcolor, highlightthickness = 0) 
        self.grid(row = 0, column = 1, sticky = "nsew", pady = 10)
        self.initParameters()

        self.bind("<Button-1>", lambda event: self.startDraw(event, paintVars, optionVars))
        self.bind("<MouseWheel>", lambda event: self.zoom(event))

    def zoom(self, event):
        global totalFactor

        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.scale(ALL, x, y, factor, factor)

    def initParameters(self):
        global lastShapes, shape, ovalsList, eraserList, BGEraserList

        shape = None
        lastShapes = []
        ovalsList = []
        eraserList = []
        BGEraserList = []

    def draw(self, event, color, brushSize):

        x = event.x
        y = event.y

        oval = self.create_oval((x - brushSize / 2, y - brushSize / 2, x + brushSize / 2, y + brushSize / 2), fill = color, outline = color)
        ovalsList.append(oval)

        self.bind('<ButtonRelease-1>', lambda event: self.endDraw(event)) 

    def endDraw(self, event):
        global ovalsList

        lastShapes.append(ovalsList)
        ovalsList = []

    def erase(self, event, bgcolor, eraserSize):
        x = event.x
        y = event.y

        oval = self.create_oval((x - eraserSize / 2, y - eraserSize / 2, x + eraserSize / 2, y + eraserSize / 2), fill = bgcolor, outline = bgcolor)
        eraserList.append(oval)
        BGEraserList.append(oval)

        self.bind('<ButtonRelease-1>', lambda event: self.endErase(event)) 

    def endErase(self, event):
        global eraserList

        lastShapes.append(eraserList)
        eraserList = []
        
    def deleteEraser(self, bgcolor):

        for oval in BGEraserList:
            self.itemconfig(oval, fill = bgcolor, outline = bgcolor)

    def startDraw(self, event, paintVars, optionVars):
        global startX, startY

        startX = event.x
        startY = event.y

        color = paintVars["color"].get()
        for entry in COLORS:
            if color == entry:
                color = COLORS[color]["color"]
                break
            
        bgcolor = optionVars["color"].get()
        for entry in COLORS:
            if bgcolor == entry:
                bgcolor = COLORS[bgcolor]["color"]
                break

        brushSize = paintVars["brushSize"].get()
        eraserSize = paintVars["eraserSize"].get()

        if paintVars["tool"].get() == "brush":
            self.bind("<B1-Motion>", lambda event: self.draw(event, color, brushSize))

        if paintVars["tool"].get() == "eraser":
            self.bind("<B1-Motion>", lambda event: self.erase(event, bgcolor, eraserSize))

        if paintVars["tool"].get() == "line":
            self.bind("<B1-Motion>", lambda event: Line(self, event, color, brushSize, self.endShape, paintVars))

        for num, entry in enumerate(TOOLS):
            if num > 2 and paintVars["tool"].get() == entry:

                className = TOOLS[entry]["class"]
                Class = getattr(sys.modules[__name__], className)

                if "filled" in entry:
                    fill = color
                else:
                    fill = ""

                self.bind("<B1-Motion>", lambda event: Class(self, event, color, brushSize, self.endShape, fill, paintVars))

    def endShape(self, event):
        global startX, startY, lastShapes, shape

        lastShapes.append(shape)
        shape = None
        
        startX = None
        startY = None

    def undo(self):
        global lastShapes

        if len(lastShapes) > 0:
            if isinstance(lastShapes[-1], list):
                for oval in lastShapes[-1]:
                    self.delete(oval)

                    for entry in BGEraserList:
                        if entry == oval:
                            BGEraserList.remove(entry)
            else: 
                self.delete(lastShapes[-1])
        
            del lastShapes[-1]

    def reset(self, canvas):
        question = CTkMessagebox(width = 100, title = "Reset Canvas", message = "Are you sure you want to reset the canvas?", icon = "question", option_1 = "Yes", option_2 = "No")
        response = question.get()

        if response == "Yes":
            canvas.delete(ALL)

    def save(self, name, path):
        self.update()
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        x1 = x + self.winfo_width()
        y1 = y + self.winfo_height()

        ImageGrab.grab().crop((x, y, x1, y1)).save(path + "/" + name + ".png")

class Line():
    def __init__(self, canvas, event, color, brushSize, endShape, paintVars):
        global shape, startX, startY

        self.canvas = canvas

        if startX != None and startY != None:
            # delete the previous line
            canvas.delete(shape)
            shape = canvas.create_line((startX, startY, event.x, event.y), fill = color, width = brushSize)

        
        # event for when line is finished
        self.canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class Rectangle():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY

        self.canvas = canvas
        
        if startX != None and startY != None:
                self.canvas.delete(shape)
                shape = canvas.create_rectangle((startX, startY, event.x, event.y), fill = fill, width = brushSize, outline = color) 

        self.canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))   

class RoundedRectangle():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY
        r = 25

        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)

            if event.x < startX and event.y < startY:
                points = (startX-r, startY, startX-r, startY, event.x+r, startY, event.x+r, startY, event.x, startY, event.x, startY-r, event.x, startY-r, 
                        event.x, event.y+r, event.x, event.y+r, event.x, event.y, event.x+r, event.y, event.x+r, event.y, startX-r, event.y, startX-r, 
                        event.y, startX, event.y, startX, event.y+r, startX, event.y+r, startX, startY-r, startX, startY-r, startX, startY)
            
            elif event.x < startX:
                points = (startX-r, startY, startX-r, startY, event.x+r, startY, event.x+r, startY, event.x, startY, event.x, startY+r, event.x, startY+r, 
                        event.x, event.y-r, event.x, event.y-r, event.x, event.y, event.x+r, event.y, event.x+r, event.y, startX-r, event.y, startX-r, 
                        event.y, startX, event.y, startX, event.y-r, startX, event.y-r, startX, startY+r, startX, startY+r, startX, startY)
                
            elif event.y < startY:
                points = (startX+r, startY, startX+r, startY, event.x-r, startY, event.x-r, startY, event.x, startY, event.x, startY-r, event.x, startY-r, 
                        event.x, event.y+r, event.x, event.y+r, event.x, event.y, event.x-r, event.y, event.x-r, event.y, startX+r, event.y, startX+r, 
                        event.y, startX, event.y, startX, event.y+r, startX, event.y+r, startX, startY-r, startX, startY-r, startX, startY)
            

            else:
                points = (startX+r, startY, startX+r, startY, event.x-r, startY, event.x-r, startY, event.x, startY, event.x, startY+r, event.x, startY+r, 
                        event.x, event.y-r, event.x, event.y-r, event.x, event.y, event.x-r, event.y, event.x-r, event.y, startX+r, event.y, startX+r, 
                        event.y, startX, event.y, startX, event.y-r, startX, event.y-r, startX, startY+r, startX, startY+r, startX, startY)
            
            shape = canvas.create_polygon(points, smooth = True, width = brushSize, fill = fill, outline = color)
        
        self.canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class Circle():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY

        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)
            shape = canvas.create_oval((startX, startY, event.x, event.y), fill = fill, width = brushSize, outline = color)

        canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class RightAngle():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY

        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)
            shape = canvas.create_polygon((startX, startY, event.x, event.y, startX, event.y), fill = fill , width = brushSize, outline = color)
        
        canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class Triangle():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY
        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)
            shape = canvas.create_polygon((startX, startY, event.x, event.y, (2 * startX - event.x), event.y), fill = fill, width = brushSize, outline = color)
        
        canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class Diamond():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY

        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)

            halfDistanceY = abs(startY - event.y) / 2
            if event.y < startY:
                shape = canvas.create_polygon((event.x, startY, startX, startY - halfDistanceY, event.x, event.y, 2 * event.x - startX, startY - halfDistanceY), fill = fill, width = brushSize, outline = color)
            else:
                shape = canvas.create_polygon((event.x, startY, startX, startY + halfDistanceY, event.x, event.y, 2 * event.x - startX, startY + halfDistanceY), fill = fill, width = brushSize, outline = color)
        
        canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class Pentagon():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY

        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)
            shape = canvas.create_polygon((startX, startY, (2 * event.x - startX), (event.y + startY) / 2, event.x, event.y, (2 * startX - event.x), event.y, (((3 * startX) - (2 * event.x))), (event.y + startY) / 2), fill = fill, width = brushSize, outline = color)

        canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class Hexagon():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY

        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)

            halfDistanceY = abs(startY - event.y) / 2
            if event.y < startY:
                shape = canvas.create_polygon((event.x, startY, startX, startY - (halfDistanceY - (0.33 * halfDistanceY)), startX, startY - (halfDistanceY + (0.33 * halfDistanceY)), event.x, event.y, 2 * event.x - startX, startY - (halfDistanceY + (0.33 * halfDistanceY)), 2 * event.x - startX, startY - (halfDistanceY - (0.33 * halfDistanceY))), fill = fill, width = brushSize, outline = color)
            else:
                shape = canvas.create_polygon((event.x, startY, startX, startY + (halfDistanceY - (0.33 * halfDistanceY)), startX, startY + (halfDistanceY + (0.33 * halfDistanceY)), event.x, event.y, 2 * event.x - startX, startY + (halfDistanceY + (0.33 * halfDistanceY)), 2 * event.x - startX, startY + (halfDistanceY - (0.33 * halfDistanceY))), fill = fill, width = brushSize, outline = color)

        canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

class FlatHexagon():
    def __init__(self, canvas, event, color, brushSize, endShape, fill, paintVars):
        global shape, startX, startY

        self.canvas = canvas

        if startX != None and startY != None:
            canvas.delete(shape)
            
            halfDistanceY = abs(startY - event.y) / 2
        if event.y < startY:
            shape = canvas.create_polygon((startX, startY - halfDistanceY, startX + 0.33 * (event.x - startX), event.y, event.x, event.y, event.x + 0.33 * (event.x - startX), startY - halfDistanceY, event.x, startY, startX + 0.33 * (event.x - startX), startY), fill = fill, width = brushSize, outline = color)
        else:
            shape = canvas.create_polygon((startX, startY + halfDistanceY, startX + 0.33 * (event.x - startX), event.y, event.x, event.y, event.x + 0.33 * (event.x - startX), startY + halfDistanceY, event.x, startY, startX + 0.33 * (event.x - startX), startY), fill = fill, width = brushSize, outline = color)

        canvas.bind('<ButtonRelease-1>', lambda event: endShape(event))

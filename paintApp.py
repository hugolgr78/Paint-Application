import customtkinter as ctk 
from ctypes import windll
from settings import *
from menu import Menu
from canvas import Canvas

class PaintApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
        self.iconbitmap("appIcon.ico")
        self.title("Paint")
        ctk.set_appearance_mode("dark")
        self.geometry(str(APP_SIZE[0]) + "x" + str(APP_SIZE[1]))
        # self.resizable(False, False)
        self.minsize(int(APP_SIZE[0]), int(APP_SIZE[1]))

        # layout
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 2, uniform = "a")
        self.columnconfigure(1, weight = 6, uniform = "a")

        # parameters
        self.initParameters()

        # menu and canvas
        self.canvas = Canvas(self, CANVAS_COLOR_DEFAULT, self.paintVars, self.optionVars)
        self.menu = Menu(self, self.paintVars, self.optionVars, self.canvas)
        
        self.bind("<Control-z>", lambda event: self.canvas.undo())

        self.mainloop()

    def initParameters(self):
        self.paintVars = {
            "brushSize": ctk.IntVar(value = BRUSHSIZE_DEFAULT),
            "eraserSize": ctk.IntVar(value = ERASERSIZE_DEFAULT),
            "color": ctk.StringVar(value = BRUSH_COLOR_DEFAULT),
            "tool": ctk.StringVar(value = DEFAULT_TOOL)}
        
        self.optionVars = {
            "color": ctk.StringVar(value = CANVAS_COLOR_DEFAULT)}
        
        # trace changes to background color
        self.optionVars["color"].trace("w", self.changeCanvasColor)
    
    def changeCanvasColor(self, *args):
        bgcolor = self.optionVars["color"].get()

        for entry in COLORS:
            if bgcolor == entry:
                bgcolor = COLORS[entry]["color"]
                break

        Canvas.deleteEraser(self.canvas,bgcolor)
        self.canvas.configure(bg = bgcolor)
        
PaintApp()
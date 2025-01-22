import customtkinter as ctk
from panels import *
from canvas import Canvas

class Menu(ctk.CTkTabview):
    def __init__(self, parent, paintVars, optionVars, canvas):
        super().__init__(parent)
        self.grid(row = 0, column = 0, sticky = "nsew", pady = 10, padx = 10)

        self.add("Paint")
        self.add("Options")

        # widgets
        PaintFrame(self.tab("Paint"), paintVars, canvas)
        OptionsFrame(self.tab("Options"), optionVars, canvas)

class PaintFrame(ctk.CTkFrame):
    def __init__(self, parent, paintVars, canvas):
        super().__init__(parent, fg_color = "grey")
        self.pack(expand = True, fill = "both")

        SliderPanel(self, "Brush Size", paintVars["brushSize"], 1, 50)
        SliderPanel(self, "Eraser Size", paintVars["eraserSize"], 1, 80)

        self.colorPanel = ColorPanel(self, "Brush Color", paintVars, "black")
        ToolPanel(self, "Tools", paintVars)

        rVar = ctk.IntVar(value = 0)
        gVar = ctk.IntVar(value = 0)
        bVar = ctk.IntVar(value = 0)

        RBGPanel(self, "RGB", rVar, gVar, bVar, paintVars, self.colorPanel)
        undoButton = ctk.CTkButton(self, text = "Undo", fg_color = DARK_GREY, hover_color = CLOSE_RED, command = lambda: canvas.undo())
        undoButton.pack(fill = "x", padx = 5, pady = 5)

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, parent, optionVars, canvas):
        super().__init__(parent, fg_color = "grey")
        self.pack(expand = True, fill = "both")

        self.colorPanel = ColorPanel(self, "Canvas Color", optionVars, "white")

        rVar = ctk.IntVar(value = 0)
        gVar = ctk.IntVar(value = 0)
        bVar = ctk.IntVar(value = 0)

        RBGPanel(self, "RGB", rVar, gVar, bVar, optionVars, self.colorPanel)

        # entry widget for name of file
        self.name = ctk.StringVar()
        self.path = ctk.StringVar()

        FileNamePanel(self, self.name)
        FilePathPanel(self, self.path)

        saveButton = ctk.CTkButton(self, text = "Save File", fg_color = DARK_GREY, hover_color = CLOSE_RED, command = lambda: canvas.save(self.name.get(), self.path.get()))
        saveButton.pack(fill = "x", padx = 5, pady = 5)

        resetButton = ctk.CTkButton(self, text = "Reset Canvas", fg_color = DARK_GREY, hover_color = CLOSE_RED, command = lambda: canvas.reset(canvas))
        resetButton.pack(fill = "x", padx = 5, pady = 5)
import customtkinter as ctk
from settings import *
from PIL import Image
from CTkColorPicker import *
from tkinter import filedialog

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color = DARK_GREY)
        self.pack(fill = 'x', pady = 4, ipady = 8, padx = 5)

class SliderPanel(Panel):
    def __init__(self, parent, text, dataVar, minValue, maxValue):
        super().__init__(parent)

        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1), weight = 1)

        self.dataVar = dataVar
        self.dataVar.trace("w", self.updateText)

        ctk.CTkLabel(self, text = text).grid(row = 0, column = 0, sticky = 'w', padx = 8)
        self.numLabel = ctk.CTkLabel(self, text = dataVar.get())
        self.numLabel.grid(row = 0, column = 1, sticky = 'e', padx = 8)

        ctk.CTkSlider(
            self, 
            fg_color = SLIDER_BG, 
            variable = dataVar,
            from_ = minValue,
            to = maxValue).grid(row = 1, column = 0, columnspan = 2, sticky = 'ew', padx = 5, pady = 5)
        
    def updateText(self, *args):
        self.numLabel.configure(text = round(self.dataVar.get(), 2))

class ColorPanel(Panel):
    def __init__(self, parent, text, colorVars, startColor):
        super().__init__(parent)

        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight = 1)

        ctk.CTkLabel(self, text = text).grid(row = 0, column = 0, columnspan = 4, sticky = "w", padx = 8)
        ctk.CTkLabel(self, text = "", bg_color = startColor, width = 32, height = 32).grid(row = 0, column = 6, columnspan = 2, sticky = "e", padx = 8, pady = 5)

        col = 0
        row = 1
        for num, entry in enumerate(COLORS):
            if num % 8 == 0:
                row += 1
                col = 0

            image = ctk.CTkImage(Image.open(COLORS[entry]["image path"]))
            Button(self, col, row, image, entry, colorVars["color"], COLORS[entry]["color"], self.changeColorLabel)
            col += 1

    def changeColorLabel(self, colorVars, color):
        colorVars.set(color)

        for entry in COLORS:
            if color == entry:
                color = COLORS[color]["color"]
                break

        ctk.CTkLabel(self, text = "", bg_color = color, width = 32, height = 32).grid(row = 0, column = 6, columnspan = 2, sticky = "e", padx = 8, pady = 5)

class ToolPanel(Panel):
    def __init__(self, parent, text, optionVars):
        super().__init__(parent)

        self.rowconfigure((0, 1, 2, 3, 4, 5), weight = 1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight = 1)

        ctk.CTkLabel(self, text = text).grid(row = 0, column = 0, columnspan = 4, sticky = "w", padx = 8)
        ctk.CTkLabel(self, text = "", image = ctk.CTkImage(Image.open(TOOLS["brush"]["image path"]))).grid(row = 0, column = 5, columnspan = 2, sticky = "e", padx = 8, pady = 5)

        col = 0
        row = 1
        for num, entry in enumerate(TOOLS):
            if num % 7 == 0:
                row += 1
                col = 0

            image = ctk.CTkImage(Image.open(TOOLS[entry]["image path"]))
            Button(self, col, row, image, entry, optionVars["tool"], LIGHT_GREY, self.changeToolLabel)
            col += 1

    def changeToolLabel(self, toolVars, tool):
        toolVars.set(tool)
        ctk.CTkLabel(self, text = "", image = ctk.CTkImage(Image.open(TOOLS[tool]["image path"]))).grid(row = 0, column = 5, columnspan = 2, sticky = "e", padx = 8, pady = 5)

class Button(ctk.CTkButton):
    def __init__(self, parent, col, row, image, data, dataVar, hover_color, function, text = ""):
        super().__init__(
        master = parent, 
        text = text,
        command = lambda: function(dataVar, data),
        image = image,
        corner_radius = STYLING["corner-radius"],
        hover_color = hover_color,
        fg_color = "transparent")

        self.grid(column = col, row = row, sticky = "nsew", padx = STYLING["gap"], pady = STYLING["gap"])

class RBGPanel(Panel):
    def __init__(self, parent, text, rVar, bVar, gVar, paintVars, colorPanel):
        super().__init__(parent)

        self.rowconfigure((0, 1, 2, 3, 4), weight = 1)
        self.columnconfigure((0, 3), weight = 1)
        self.columnconfigure((1, 2), weight = 4)

        rSlider = ctk.CTkSlider(self, fg_color = SLIDER_BG, progress_color = "red", variable = rVar, from_ = 0, to = 255)
        rSlider.grid(row = 0, column = 1, columnspan = 3, padx = (0, 5), pady = 5)

        ctk.CTkLabel(self, textvariable = rVar).grid(row = 0, column = 0, sticky = "w", padx = 5)


        gSlider = ctk.CTkSlider(self, fg_color = SLIDER_BG, progress_color = "green", variable = gVar, from_ = 0, to = 255)
        gSlider.grid(row = 1, column = 1, columnspan = 3, padx = (0, 5), pady = 5)

        ctk.CTkLabel(self, textvariable = gVar).grid(row = 1, column = 0, sticky = "w", padx = 5)


        bSlider = ctk.CTkSlider(self, fg_color = SLIDER_BG, progress_color = "blue", variable = bVar, from_ = 0, to = 255)
        bSlider.grid(row = 2, column = 1, columnspan = 3, padx = (0, 5), pady = 5)

        ctk.CTkLabel(self, textvariable = bVar).grid(row = 2, column = 0, sticky = "w", padx = 5)


        selectButton = ctk.CTkButton(self, text = "Select", fg_color = DARKER_GREY, hover_color = GREY, command = lambda: self.selectColor(rVar, gVar, bVar, colorPanel, paintVars))
        selectButton.grid(row = 3, column = 0, columnspan = 2, sticky = "ew", padx = 5, pady = 5)

        colorWheelButton = ctk.CTkButton(self, text = "Color Wheel", fg_color = DARKER_GREY, hover_color = GREY, command = lambda: self.askColor(paintVars, colorPanel))
        colorWheelButton.grid(row = 3, column = 2, columnspan = 2, sticky = "ew", padx = 5, pady = 5)

    def selectColor(self, rVar, gVar, bVar, colorPanel, paintVars):
        colorPanel.changeColorLabel(paintVars["color"], "#%02x%02x%02x" % (rVar.get(), gVar.get(), bVar.get()))

    def askColor(self, paintVars, colorPanel):
        color = AskColor(title = "Color Wheel")
        color.protocol("WM_DELETE_WINDOW", lambda: self.closeWheel(paintVars, color, colorPanel))

        colorPanel.changeColorLabel(paintVars["color"], color.get())

    def closeWheel(self, paintVars, color, colorPanel):
        colorPanel.changeColorLabel(paintVars["color"], "white")
        color.destroy()

class FileNamePanel(Panel):
    def __init__(self, parent, name):
        super().__init__(parent)

        self.name = name
        self.name.trace("w", self.updateText)

        ctk.CTkLabel(self, text = "File Name").pack(pady = 5, padx = 20)
        ctk.CTkEntry(self, textvariable = self.name).pack(fill = "x", padx = 20, pady = 5)

        self.output = ctk.CTkLabel(self, text = "")
        self.output.pack()

    def click(self, value):
        self.fileType.set(value)
        self.updateText()

    def updateText(self, *args):
        if self.name.get():
            text = self.name.get().replace(" ", "_") + ".png"
            self.output.configure(text = text)
            self.name.set(self.name.get().replace(" ", "_"))
        
        if self.name.get() == "":
            self.output.configure(text = "")

class FilePathPanel(Panel):
    def __init__(self, parent, path):
        super().__init__(parent)
        
        self.path = path

        ctk.CTkLabel(self, text = "File Path").pack(pady = 5, padx = 20)
        ctk.CTkButton(self, text = "Open explorer", command = self.openfileDialog).pack(pady = 5)
        ctk.CTkEntry(self, textvariable = self.path).pack(expand = True, fill = "both", padx = 5, pady = 5)

    def openfileDialog(self):
        self.path.set(filedialog.askdirectory())
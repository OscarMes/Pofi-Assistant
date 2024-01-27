import tkinter as tk
from tkinter import DISABLED

class Cls_Burbuja:
    def __init__(self, ventana, column, row,bg):
        self.ventana = ventana
        self.column= column
        self.row= row
        self.bg = bg
        self.ventana.config(state=DISABLED)
        self.ventana.grid(column=self.column,row=self.row,)
        self.ventana.grid_propagate(0)
        self.frm = tk.Frame(self.ventana, bg="#e5ddd5")
    
    def fnt_mensaje(self,mensaje):
        self.lbl = tk.Label(self.frm, text=mensaje, bg=self.bg, padx=10, pady=5,wraplength=180,justify="left",font=("Arial", 12))
        self.lbl.pack()
        self.frm.pack()




  
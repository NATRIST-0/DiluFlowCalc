# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:26:19 2024

@author: GAYRARD
"""

import numpy as np
import tkinter as tk
from sys import exit
from PIL import Image, ImageTk
from tkinter.constants import BOTH, YES
from tkinter import ttk,Button, Text

def on_close():
    root.destroy()
    exit()

def dil_step(wdil_val, step_val, Range_val):
    wdil_array = np.arange(wdil_val - Range_val, wdil_val + (Range_val + 1), step_val)
    return wdil_array

def calculate():
    result.delete("1.0", tk.END)
    wdil_val = float(wdil.get("1.0", "end-1c"))
    wGAS_val = float(wGAS.get("1.0", "end-1c"))
    Vair_val = float(Vair.get("1.0", "end-1c"))
    Vcalmax_val = float(Vcalmax.get("1.0", "end-1c"))
    step_val = float(step.get("1.0", "end-1c"))
    Range_val = float(Range.get("1.0", "end-1c"))
    percent_val = float(percent.get("1.0", "end-1c"))
    slope_value = float(slope.get("1.0", "end-1c"))

    wdil_array = dil_step(wdil_val, step_val, Range_val)
    wdil_C_array = wdil_array * 10**-9  # From ppb to nothing

    wGAS_val = wGAS_val * 10**-6  # From ppm to nothing

    Vdil = Vair_val * wdil_C_array / (wGAS_val - (1 - wGAS_val) * wdil_C_array)
    Vdil = Vdil * 1000  # From SLPM to SCCM

    percent_val = percent_val / 100
    Vgas_max = (Vcalmax_val - Vcalmax_val * percent_val) * 1000  # From SLPM to SCCM
    Vgas_min = Vcalmax_val * percent_val

    Uflow = abs(1 - slope_value)
    Utolerence = percent_val 
    U = Uflow + Utolerence

    for w, V in zip(wdil_array, Vdil):
        if V > 0:  # Only proceed if V is non-negative
            if V <= Vgas_min or V >= Vgas_max:
                result.insert(tk.END, f"\nFor Cdil = {w} ± {w*U:.0f} ppb, Vcal = {V:.3f} SCCM, outside the\ninstrument's confidence zone")
            else:
                result.insert(tk.END, f"\nFor Cdil = {w} ± {w*U:.0f} ppb, Vcal = {V:.3f} SCCM")
            result.insert(tk.END, "\n")

root = tk.Tk()
root.title("Determination of the Volumetric Flow of the Cylinder of Air V3")
root.geometry('1152x648')

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo
    
image = Image.open("App_Dil_Bkr.png")
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = ttk.Label(root, image = photo)

# Create widgets
wGAS = Text(root, height=1, width=8, font=('Sans-serif', 18))
wGAS.place(relx=0.154, rely=0.85, relwidth=0.05, relheight=0.04)

wdil = Text(root, height=1, width=10, font=('Sans-serif', 18))
wdil.place(relx=0.49, rely=0.21, relwidth=0.05, relheight=0.05)

Vair = Text(root, height=1, width=7, font=('Sans-serif', 18))
Vair.place(relx=0.155, rely=0.056, relwidth=0.04, relheight=0.04)

Vcalmax = Text(root, height=1, width=7, font=('Sans-serif', 18))
Vcalmax.place(relx=0.23, rely=0.38, relwidth=0.04, relheight=0.04)

step = Text(root, height=1, width=6, font=('Sans-serif', 18))
step.place(relx=0.53, rely=0.765, relwidth=0.04, relheight=0.04)

Range = Text(root, height=1, width=6, font=('Sans-serif', 18))
Range.place(relx=0.65, rely=0.765, relwidth=0.04, relheight=0.04)

percent = Text(root, height=1, width=8, font=('Sans-serif', 18))
percent.place(relx=0.735, rely=0.765, relwidth=0.05, relheight=0.04)

slope = Text(root, height=1, width=7, font=('Sans-serif', 18))
slope.place(relx=0.87, rely=0.765, relwidth=0.05, relheight=0.04)

result = Text(root, height=12, width=55, font=('Sans-serif', 18))
result.place(relx=0.466, rely=0.375, relwidth=0.47, relheight=0.38)

button = Button(root, text='SEND', relief=tk.RAISED, font=('Sans-serif', 18), command=calculate)
button.place(relx=0.515, rely=0.9)


label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
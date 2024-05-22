#!/bin/etc python3
#author: Tristan Gayrard

"""
new_dilution_app
"""

import numpy as np
import tkinter as tk
from tkinter import Button, Text
from PIL import ImageTk, Image

def dil_step(wdil_val, step_val, Range_val):
    wdil_array = np.arange(wdil_val - Range_val, wdil_val + (Range_val+1) , step_val)
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

    wdil_array = dil_step(wdil_val,step_val,Range_val)
    wdil_C_array = wdil_array * 10**-9  # From ppb to nothing

    wGAS_val = wGAS_val * 10**-6  # From ppm to nothing

    Vdil = Vair_val * wdil_C_array / (wGAS_val - (1 - wGAS_val) * wdil_C_array)
    Vdil = Vdil * 1000  # From SLPM to SCCM

    percent_val = percent_val / 100
    Vgas_max = (Vcalmax_val - Vcalmax_val * percent_val) * 1000 # From SLPM to SCCM
    Vgas_min = Vcalmax_val * percent_val
    
    Uflow = (abs( 1 - slope_value )) 
    Utolerence = percent_val 
    U = Uflow + Utolerence
    

    for w, V in zip(wdil_array, Vdil):
        if V > 0:  # Only proceed if V is non-negative
            if V <= Vgas_min or V >= Vgas_max:
                result.insert(tk.END, f"\nFor Cdil = {w} ± {w*U:.0f} ppb, Vcal = {V:.3f} SCCM, outside the\ninstrument's confidence zone")
            else:
                result.insert(tk.END, f"\nFor Cdil = {w} ± {w*U:.0f} ppb, Vcal = {V:.3f} SCCM")
            result.insert(tk.END, "\n")
            

#GUI###########################################################################

ws = tk.Tk()
ws.title("Determination of the Volumetric Flow of the Cylinder of Air V2")

width = ws.winfo_screenwidth()
height = ws.winfo_screenheight()

ws.geometry("%dx%d" % (width, height))
ws.resizable(False, False)

imgTemp = Image.open("App_Dil_Bkr.png")
img2 = imgTemp.resize((width, height))
img = ImageTk.PhotoImage(img2)

label = tk.Label(ws, image=img)
label.place(x=0, y=0, relwidth=1, relheight=1)

wGAS = Text(ws,height=1,width=8,font=('Sans-sherif', 18))
wGAS.place(x=215, y=730)

wdil = Text(ws,height=1,width=10,font=('Sans-sherif', 18))
wdil.place(x=750, y=185)

Vair = Text(ws,height=1,width=7,font=('Sans-sherif', 18))
Vair.place(x=225, y=60)

Vcalmax = Text(ws,height=1,width=7,font=('Sans-sherif', 18))
Vcalmax.place(x=335, y=340)

step = Text(ws,height=1,width=6,font=('Sans-sherif', 18))
step.place(x=800, y=660)

Range = Text(ws,height=1,width=5,font=('Sans-sherif', 18))
Range.place(x=1000, y=660)

percent = Text(ws,height=1,width=8,font=('Sans-sherif', 18))
percent.place(x=1120,y=660)

slope = Text(ws,height=1,width=7,font=('Sans-sherif', 18))
slope.place(x=1326,y=660)

result = Text(ws,height=12,width=55,font=('Sans-sherif', 18))
result.place(x=713,y=320)

button = Button(ws,text='SEND',relief=tk.RAISED,font=('Sans-sherif', 18), command=calculate)
button.place(x=990, y=770)

ws.mainloop()

###############################################################################






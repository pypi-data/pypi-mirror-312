from KIB_LAP.Plattentragwerke import PlateBendingKirchhoffClass
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import time
import os


a = 4.5
b = 14

Plate = PlateBendingKirchhoffClass(
    35000, 0.35, a, b, 1, 0.5, 0.5, 0.5, 0.5, 0.0, 0, 0, 50, "Liste", "hhhh",8
)


# Daten als Liste von Listen
new_data = [
    ["No.","x0[m]","x1[m]","y0[m]","y1[m]","p0[MN/m**2]"],
    [1,4.5-0.2,4.5+0.2,0.5,1.9,12/1000],
    [2,0,4.5,0,3,12/1000]
]

# Konvertiere die Daten in ein DataFrame
df = pd.DataFrame(new_data[1:], columns=new_data[0])

# Dateipfad zur CSV-Datei
file_path = 'Loading/Constant_Loading.csv'

# Schreibe das DataFrame in eine CSV-Datei
df.to_csv(file_path, index=False)


Plate.CalculateAll()

Plate.SolutionPointDisp(0.5,0.5)
Plate.SolutionPointMomentx(0.5,0.5)
Plate.SolutionPointMomenty(0.5,0.5)


Plate.PlotLoad()
Plate.PlotMomentGrid()
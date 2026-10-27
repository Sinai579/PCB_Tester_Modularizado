"""Guardado local del resultado de cada prueba en CSV."""

import csv
import os
from datetime import datetime


def guardar_resultado(qr_data, resultado):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    archivo_csv = os.path.join(desktop, "PCB_TESTER_REGISTER.csv")

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archivo_existe = os.path.isfile(archivo_csv)

    with open(archivo_csv, mode="a", newline="") as archivo:
        writer = csv.writer(archivo)

        if not archivo_existe:
            writer.writerow(["QR", "Fecha", "Resultado"])

        writer.writerow([qr_data, fecha_hora, resultado])

    print("Guardado CSV correctamente")

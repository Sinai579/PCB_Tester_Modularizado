"""Punto de entrada del PCB Tester Husky Control."""

import threading
import cv2
import tkinter as tk

from state import AppState
from services.csv_service import guardar_resultado
from services.ftp_service import subir_csv_ftp
from services.power_supply import PowerSupplyService
from services.vision_service import VisionService
from ui.main_window import crear_ventana


class PCBTesterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.state = AppState()

        self.widgets = crear_ventana(self.root, self.ejecutar_go)

        self.power_supply = PowerSupplyService(
            self.state,
            self.root,
            self.widgets,
            guardar_resultado,
        )

        self.vision = VisionService(
            self.state,
            self.widgets["cambiar_status"],
            self.power_supply.rutina_go,
        )

        self.abrir_camaras()

    def abrir_camaras(self):
        dispositivos = [
            "/dev/video0",
            "/dev/video2",
            "/dev/video4",
            "/dev/video6",
        ]

        for dispositivo in dispositivos:
            camara = cv2.VideoCapture(dispositivo, cv2.CAP_V4L2)

            if camara.isOpened():
                camara.set(
                    cv2.CAP_PROP_FOURCC,
                    cv2.VideoWriter_fourcc(*"MJPG"),
                )
                camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                camara.set(cv2.CAP_PROP_EXPOSURE, -4)

                self.state.camaras.append(camara)
                print(f"{dispositivo}: camara abierta")
            else:
                print(f"{dispositivo}: error al abrir")
                camara.release()

    def ejecutar_go(self):
        for i, camara in enumerate(self.state.camaras, start=1):
            self.widgets["cambiar_status"](f"ESCANEANDO QR...{i}", "#ffcc00")
            self.root.update()
            self.vision.iniciar_vision(camara)

    def iniciar(self):
        self.power_supply.read()

        threading.Thread(
            target=self.power_supply.auto_connect,
            daemon=True,
        ).start()

        threading.Thread(
            target=subir_csv_ftp,
            daemon=True,
        ).start()

        self.root.mainloop()


if __name__ == "__main__":
    app = PCBTesterApp()
    app.iniciar()

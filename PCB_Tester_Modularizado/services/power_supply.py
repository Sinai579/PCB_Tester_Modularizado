"""Comunicación con la fuente mediante MinimalModbus."""

import time
import minimalmodbus
import serial.tools.list_ports


class PowerSupplyService:
    def __init__(self, state, root, widgets, guardar_resultado):
        self.state = state
        self.root = root
        self.widgets = widgets
        self.guardar_resultado = guardar_resultado

    def auto_connect(self):
        self.root.after(
            0,
            lambda: self.widgets["estado"].config(text="Buscando fuente..."),
        )

        while True:
            time.sleep(2)

            if self.state.instrument is not None:
                continue

            puertos = serial.tools.list_ports.comports()

            for puerto_info in puertos:
                puerto = puerto_info.device

                try:
                    temp = minimalmodbus.Instrument(puerto, 1)
                    temp.serial.baudrate = 9600
                    temp.serial.timeout = 1

                    # Prueba real de comunicación.
                    temp.read_register(0, 0)

                    self.state.instrument = temp

                    self.root.after(
                        0,
                        lambda puerto=puerto: self.widgets["estado"].config(
                            text=f"Conectado a fuente {puerto}"
                        ),
                    )
                    self.root.after(
                        0,
                        lambda: self.widgets["boton_go"].config(state="normal"),
                    )
                    break
                except Exception:
                    continue

    def rutina_go(self):
        if self.state.instrument is None:
            self.widgets["estado"]["text"] = "No conectado"
            return

        try:
            self.widgets["estado"]["text"] = "iniciando rutina..."

            # Set to 3.5 V.
            self.state.instrument.write_register(0, 350, functioncode=6)
            self.state.instrument.write_register(9, 1, functioncode=6)

            self.widgets["estado"]["text"] = "Salida en 23v"

            # Poner la fuente a 0 V después de 10 segundos.
            self.root.after(10000, self.paso_2)

        except Exception:
            self.state.instrument = None
            self.widgets["estado"]["text"] = "Error conexion"

    def paso_2(self):
        try:
            self.widgets["estado"]["text"] = "Fuente apagada"
            self.state.instrument.write_register(0, 0, functioncode=6)

            self.state.detener_camara = True
            self.guardar_resultado(
                self.state.qr_data_global,
                self.state.resultado_global,
            )

        except Exception as error:
            self.widgets["estado"]["text"] = "error en paso 2"
            print(error)

    def read(self):
        if self.state.instrument is None:
            self.widgets["lectura"]["text"] = "No conectado"
            self.root.after(1000, self.read)
            return

        try:
            voltaje = self.state.instrument.read_register(2, 2)
            corriente = self.state.instrument.read_register(3, 2)
            self.widgets["lectura"]["text"] = (
                f"voltaje: {voltaje} V Corriente: {corriente} A"
            )
        except Exception:
            self.widgets["lectura"]["text"] = "connected"

        self.root.after(1000, self.read)

"""Estado compartido de la aplicación PCB Tester."""


class AppState:
    def __init__(self):
        self.cap = None
        self.instrument = None
        self.detener_camara = False
        self.qr_data_global = ""
        self.resultado_global = ""
        self.camaras = []

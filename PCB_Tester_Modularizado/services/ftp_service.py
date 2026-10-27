"""Subida periódica del CSV al servidor FTP."""

import json
import os
import time
from ftplib import FTP


def subir_csv_ftp():
    while True:
        try:
            config_path = os.path.join(
                os.path.expanduser("~"),
                "Desktop",
                "config_ftp.json",
            )

            with open(config_path, "r") as archivo_config:
                config = json.load(archivo_config)

            servidor = config["FtpServerUrl"]
            usuario = config["Username"]
            password = config["Password"]

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            archivo_csv = os.path.join(desktop, "PCB_TESTER_REGISTER.csv")

            if os.path.isfile(archivo_csv):
                ftp = FTP(servidor)
                ftp.login(usuario, password)
                ftp.cwd("Testers")
                ftp.cwd("PCBTester")
                print("Directorio actual:", ftp.pwd())

                with open(archivo_csv, "rb") as archivo:
                    ftp.storbinary("STOR PCB_TESTER_REGISTER.csv", archivo)

                ftp.quit()
                print("CSV subido correctamente")

        except Exception as error:
            print("Error al subir:", error)

        time.sleep(60)

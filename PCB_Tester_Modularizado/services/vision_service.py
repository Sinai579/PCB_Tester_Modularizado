"""Lectura de QR y detección de LEDs mediante OpenCV."""

import time
import cv2
import numpy as np


class VisionService:
    def __init__(self, state, cambiar_status, rutina_go):
        self.state = state
        self.cambiar_status = cambiar_status
        self.rutina_go = rutina_go

    def iniciar_vision(self, camara):
        self.state.detener_camara = False
        self.cambiar_status("TESTING", "#ffcc00")
        self.state.cap = camara
        cap = self.state.cap

        # Ajuste para la exposición del QR.
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        cv2.waitKey(1000)
        cap.set(cv2.CAP_PROP_EXPOSURE, -4)

        qr = cv2.QRCodeDetector()
        qr_leido = False
        qr_data = ""

        print("ESC para salir")

        while True:
            if self.state.detener_camara:
                break

            ret, frame = cap.read()
            if not ret:
                break

            # DETECCIÓN QR
            if not qr_leido:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Región de búsqueda QR.
                x1, y1 = 80, 150
                x2, y2 = 350, 400
                roi = gray[y1:y2, x1:x2]

                data, bbox, _ = qr.detectAndDecode(roi)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                if bbox is not None:
                    bbox[:, :, 0] += x1
                    bbox[:, :, 1] += y1
                    pts = bbox.astype(int)
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

                if data:
                    qr_leido = True
                    qr_data = data
                    self.state.qr_data_global = qr_data

                    self.rutina_go()
                    print("QR leído:", qr_data)
                    cap.set(cv2.CAP_PROP_EXPOSURE, -13)
                    time.sleep(0.3)

            # DETECCIÓN LEDs: se conserva la condición original de entrar
            # aquí después de que el QR haya sido leído.
            else:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                gray = cv2.add(hsv[:, :, 2], frame[:, :, 2])

                UMBRAL_BRIGHTNESS = 190
                _, thresh = cv2.threshold(
                    gray,
                    UMBRAL_BRIGHTNESS,
                    255,
                    cv2.THRESH_BINARY,
                )

                kernel = np.ones((3, 3), np.uint8)
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                thresh = cv2.morphologyEx(
                    thresh,
                    cv2.MORPH_DILATE,
                    kernel,
                    iterations=1,
                )

                contours, _ = cv2.findContours(
                    thresh,
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE,
                )

                puntos = 0

                for contorno in contours:
                    area = cv2.contourArea(contorno)

                    if 60 < area < 400:
                        x, y, w, h = cv2.boundingRect(contorno)
                        puntos += 1
                        cv2.rectangle(
                            frame,
                            (x, y),
                            (x + w, y + h),
                            (255, 255, 255),
                            2,
                        )

                cv2.putText(
                    frame,
                    f"LEDs detectados: {puntos}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2,
                )

                # Se conserva el umbral original.
                if puntos >= 31:
                    self.cambiar_status("PASS", "#00cc00")
                    self.state.resultado_global = "PASS"
                else:
                    self.cambiar_status("NOT PASS", "#cc0000")
                    self.state.resultado_global = "FAIL"

            cv2.putText(
                frame,
                f"QR: {qr_data}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Vision", frame)

            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()

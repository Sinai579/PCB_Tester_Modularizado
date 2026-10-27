"""Construcción de la interfaz gráfica Tkinter."""

import tkinter as tk


def crear_ventana(root, ejecutar_go):
    root.title("PCB Tester")
    root.geometry("1000x2000")
    root.configure(bg="#e6e6e6")

    logo = tk.PhotoImage(file="zircon.png")
    logo = logo.subsample(4, 4)

    logo_label = tk.Label(root, image=logo, bg="#e6e6e6")
    logo_label.image = logo  # Mantener una referencia a la imagen.
    logo_label.place(x=20, y=-30)

    legend_frame = tk.Frame(root, bg="#e6e6e6")
    legend_frame.place(x=20, y=170)

    def crear_leyenda(texto, color):
        item = tk.Frame(legend_frame, bg="#e6e6e6")
        item.pack(anchor="w", pady=5)

        cuadro = tk.Label(
            item,
            width=2,
            height=1,
            bg=color,
        )
        cuadro.pack(side="left", padx=5)

        label = tk.Label(
            item,
            text=texto,
            font=("Arial", 11, "bold"),
            bg="#e6e6e6",
            fg="black",
        )
        label.pack(side="left")

    crear_leyenda("PASS", "#00cc00")
    crear_leyenda("TESTING", "#ffcc00")
    crear_leyenda("NOT PASS", "#cc0000")

    titulo = tk.Label(
        root,
        text="PCB TESTER",
        font=("Arial", 28, "bold"),
        bg="#e6e6e6",
        fg="black",
    )
    titulo.pack(pady=40)

    boton_go = tk.Button(
        root,
        text="GO",
        font=("Arial", 28, "bold"),
        bg="green",
        fg="white",
        width=10,
        height=2,
        command=ejecutar_go,
        state="disabled",
    )
    boton_go.pack(pady=20)

    frame_pcbs = tk.Frame(root, bg="#e6e6e6")
    frame_pcbs.pack(pady=40)

    for i in range(4):
        pcb = tk.Canvas(
            frame_pcbs,
            width=150,
            height=200,
            bg="#000000",
            highlightthickness=2,
            highlightbackground="black",
        )
        pcb.grid(row=0, column=i, padx=20)

        pcb.create_text(
            75,
            180,
            text=f"PCB {i + 1}",
            fill="white",
            font=("Arial", 12, "bold"),
        )

    estado = tk.Label(
        root,
        text="STATUS: READY",
        font=("Arial", 16),
        bg="#e6e6e6",
        fg="gray",
    )

    lectura = tk.Label(root, text="Lectura")
    lectura.pack()

    def cambiar_status(texto, color):
        estado.config(text=f"STATUS: {texto}", fg=color)
        root.update()

    estado.pack(pady=20)

    return {
        "estado": estado,
        "lectura": lectura,
        "boton_go": boton_go,
        "cambiar_status": cambiar_status,
    }

import os
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
from PIL import Image, ImageDraw
from tensorflow.keras.models import load_model

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MODELO = os.path.join(DIRECTORIO_ACTUAL, "red_digitos.keras")

ANCHO_LIENZO = 280
RADIO_TRAZO = 9


def adaptar_trazo(imagen_pil):
    limites = imagen_pil.getbbox()
    if not limites:
        return None

    recorte = imagen_pil.crop(limites)
    w, h = recorte.size
    factor = 20.0 / max(w, h)
    nuevo_w = max(1, int(w * factor))
    nuevo_h = max(1, int(h * factor))
    recorte = recorte.resize((nuevo_w, nuevo_h), Image.Resampling.LANCZOS)

    base = Image.new("L", (28, 28), 0)
    offset_x = (28 - nuevo_w) // 2
    offset_y = (28 - nuevo_h) // 2
    base.paste(recorte, (offset_x, offset_y))

    matriz = np.array(base, dtype="float32") / 255.0
    suma = matriz.sum()
    if suma == 0:
        return None

    filas, cols = np.indices((28, 28))
    cx = (cols * matriz).sum() / suma
    cy = (filas * matriz).sum() / suma

    matriz = np.roll(matriz, int(round(14 - cy)), axis=0)
    matriz = np.roll(matriz, int(round(14 - cx)), axis=1)
    return matriz


class AppClasificador:
    def __init__(self, raiz, modelo):
        self.raiz = raiz
        self.modelo = modelo
        self.raiz.title("Reconocimiento de Dígitos (MNIST)")
        self.raiz.resizable(False, False)

        self.img_memoria = Image.new("L", (ANCHO_LIENZO, ANCHO_LIENZO), 0)
        self.dibujante = ImageDraw.Draw(self.img_memoria)
        self.ultimo_x = None
        self.ultimo_y = None

        self._construir_ventana()

    def _construir_ventana(self):
        contenedor = ttk.Frame(self.raiz, padding=15)
        contenedor.pack()

        # Panel izquierdo: Predicción y probabilidades
        izq = ttk.Frame(contenedor)
        izq.pack(side="left", padx=(0, 20), fill="y")

        ttk.Label(izq, text="Número detectado:", font=("Segoe UI", 12)).pack()
        self.lbl_numero = ttk.Label(izq, text="?", font=("Segoe UI", 58, "bold"))
        self.lbl_numero.pack(pady=4)

        self.lbl_seguridad = ttk.Label(izq, text="Dibuja un dígito", font=("Segoe UI", 10))
        self.lbl_seguridad.pack(pady=(0, 10))

        self.medidores = []
        self.textos_prob = []
        for n in range(10):
            fila = ttk.Frame(izq)
            fila.pack(fill="x", pady=1)
            ttk.Label(fila, text=f"{n}:", width=3).pack(side="left")
            barra = ttk.Progressbar(fila, length=140, maximum=100)
            barra.pack(side="left", padx=4)
            lbl = ttk.Label(fila, text="0%", width=6)
            lbl.pack(side="left")
            self.medidores.append(barra)
            self.textos_prob.append(lbl)

        # Panel derecho: Pizarrón de dibujo
        der = ttk.Frame(contenedor)
        der.pack(side="right")

        ttk.Label(der, text="Área de dibujo (0 - 9):", font=("Segoe UI", 11)).pack()
        self.lienzo = tk.Canvas(
            der,
            width=ANCHO_LIENZO,
            height=ANCHO_LIENZO,
            bg="black",
            cursor="crosshair"
        )
        self.lienzo.pack(pady=8)
        self.lienzo.bind("<B1-Motion>", self._trazar)
        self.lienzo.bind("<ButtonRelease-1>", self._fin_trazo)

        ttk.Button(der, text="Limpiar pizarrón", command=self._reiniciar).pack(fill="x")

    def _trazar(self, evento):
        x, y = evento.x, evento.y
        grosor = RADIO_TRAZO * 2

        if self.ultimo_x is not None and self.ultimo_y is not None:
            self.lienzo.create_line(
                self.ultimo_x, self.ultimo_y, x, y,
                fill="white", width=grosor, capstyle=tk.ROUND, smooth=True
            )
            self.dibujante.line([self.ultimo_x, self.ultimo_y, x, y], fill=255, width=grosor)

        self.dibujante.ellipse([x - RADIO_TRAZO, y - RADIO_TRAZO, x + RADIO_TRAZO, y + RADIO_TRAZO], fill=255)
        self.ultimo_x = x
        self.ultimo_y = y

    def _fin_trazo(self, evento):
        self.ultimo_x = None
        self.ultimo_y = None
        self._clasificar()

    def _clasificar(self):
        datos = adaptar_trazo(self.img_memoria)
        if datos is None:
            return

        predicciones = self.modelo.predict(datos.reshape(1, 28, 28), verbose=0)[0]
        ganador = int(np.argmax(predicciones))

        self.lbl_numero.config(text=str(ganador))
        self.lbl_seguridad.config(text=f"Seguridad: {predicciones[ganador] * 100:.1f}%")

        for i in range(10):
            val = float(predicciones[i]) * 100
            self.medidores[i]["value"] = val
            self.textos_prob[i].config(text=f"{val:.0f}%")

    def _reiniciar(self):
        self.lienzo.delete("all")
        self.dibujante.rectangle([0, 0, ANCHO_LIENZO, ANCHO_LIENZO], fill=0)
        self.ultimo_x = None
        self.ultimo_y = None
        self.lbl_numero.config(text="?")
        self.lbl_seguridad.config(text="Dibuja un dígito")
        for i in range(10):
            self.medidores[i]["value"] = 0
            self.textos_prob[i].config(text="0%")


if __name__ == "__main__":
    ventana = tk.Tk()
    if not os.path.exists(ARCHIVO_MODELO):
        ventana.withdraw()
        messagebox.showerror(
            "Modelo no encontrado",
            "Primero debes ejecutar 'entrenar_mnist.py' para generar el modelo entrenado."
        )
    else:
        red = load_model(ARCHIVO_MODELO)
        AppClasificador(ventana, red)
        ventana.mainloop()
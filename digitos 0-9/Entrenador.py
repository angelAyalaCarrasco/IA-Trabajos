import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_MODELO = os.path.join(DIRECTORIO_ACTUAL, "red_digitos.keras")


def preparar_datos():
    (x_entrena, y_entrena), (x_prueba, y_prueba) = tf.keras.datasets.mnist.load_data()
    x_entrena = x_entrena.astype("float32") / 255.0
    x_prueba = x_prueba.astype("float32") / 255.0
    return (x_entrena, y_entrena), (x_prueba, y_prueba)


def crear_red():
    modelo = models.Sequential([
        layers.Input(shape=(28, 28)),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])
    modelo.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return modelo


def mostrar_graficas(historial):
    fig, ejes = plt.subplots(1, 2, figsize=(11, 4))

    ejes[0].plot(historial.history["accuracy"], label="Entrenamiento", color="navy")
    ejes[0].plot(historial.history["val_accuracy"], label="Validación", color="darkorange")
    ejes[0].set_title("Precisión por Época")
    ejes[0].set_xlabel("Época")
    ejes[0].set_ylabel("Precisión")
    ejes[0].legend()
    ejes[0].grid(True, alpha=0.4)

    ejes[1].plot(historial.history["loss"], label="Entrenamiento", color="navy")
    ejes[1].plot(historial.history["val_loss"], label="Validación", color="darkorange")
    ejes[1].set_title("Pérdida por Época")
    ejes[1].set_xlabel("Época")
    ejes[1].set_ylabel("Pérdida")
    ejes[1].legend()
    ejes[1].grid(True, alpha=0.4)

    plt.tight_layout()
    plt.show()


def ver_ejemplos(imagenes, etiquetas):
    fig, ejes = plt.subplots(4, 8, figsize=(9, 5))
    for i, ax in enumerate(ejes.flat):
        ax.imshow(imagenes[i], cmap="gray")
        ax.set_title(f"Etiqueta: {etiquetas[i]}", fontsize=8)
        ax.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    (x_train, y_train), (x_test, y_test) = preparar_datos()
    print(f"Imágenes de entrenamiento: {x_train.shape[0]} | Prueba: {x_test.shape[0]}")

    modelo = crear_red()
    historial = modelo.fit(
        x_train,
        y_train,
        epochs=8,
        batch_size=256,
        validation_split=0.15
    )

    loss, acc = modelo.evaluate(x_test, y_test, verbose=0)
    print(f"Evaluación final -> Pérdida: {loss:.4f} | Precisión: {acc * 100:.2f}%")

    modelo.save(ARCHIVO_MODELO)
    print(f"Modelo guardado en: {ARCHIVO_MODELO}")

    mostrar_graficas(historial)
    ver_ejemplos(x_test, y_test)


if __name__ == "__main__":
    main()
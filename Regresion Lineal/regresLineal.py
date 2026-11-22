import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing


def obtener_datos(n_muestras=60, semilla=42):
    datos = fetch_california_housing()
    rng = np.random.default_rng(semilla)
    indices = rng.choice(len(datos.target), size=n_muestras, replace=False)

    # Columna 0 corresponde a MedInc
    x = datos.data[indices, 0]
    y = datos.target[indices]
    return x, y


def entrenar_modelo(x, y, tasa_aprendizaje=0.01, epocas=4500):
    m_pendiente = 0.0
    b_interseccion = 0.0
    m = len(x)
    historial_error = []

    for _ in range(epocas):
        prediccion = m_pendiente * x + b_interseccion
        diferencia = prediccion - y

        error = np.sum(diferencia ** 2) / (2 * m)
        historial_error.append(error)

        grad_m = np.sum(diferencia * x) / m
        grad_b = np.sum(diferencia) / m

        m_pendiente -= tasa_aprendizaje * grad_m
        b_interseccion -= tasa_aprendizaje * grad_b

    return m_pendiente, b_interseccion, historial_error


def graficar_resultados(x, y, m, b, historial_error):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Gráfica 1: Ajuste lineal
    ax1.scatter(x, y, color="teal", alpha=0.8, label="Muestras reales")
    x_recta = np.linspace(x.min() - 0.3, x.max() + 0.3, 100)
    ax1.plot(
        x_recta,
        m * x_recta + b,
        color="darkorange",
        linewidth=2.2,
        label=f"Recta: y = {m:.2f}x + {b:.2f}"
    )
    ax1.set_title("Ajuste de Regresión Lineal (California Housing)")
    ax1.set_xlabel("Ingreso Medio (decenas de miles USD)")
    ax1.set_ylabel("Valor Medio de Vivienda (cientos de miles USD)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend()

    # Gráfica 2: Evolución del error
    ax2.plot(historial_error, color="crimson", linewidth=1.8)
    ax2.set_title("Disminución del Error Cuadrático Medio")
    ax2.set_xlabel("Épocas")
    ax2.set_ylabel("Costo (MSE)")
    ax2.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


def main():
    x, y = obtener_datos(n_muestras=60)
    print(f"Se cargaron {len(x)} registros del dataset.")

    pendiente, interseccion, errores = entrenar_modelo(x, y)
    print(f"Modelo entrenado -> y = {pendiente:.4f}x + {interseccion:.4f}")

    # Comparación con cálculo analítico
    m_ref, b_ref = np.polyfit(x, y, 1)
    print(f"Referencia analítica -> y = {m_ref:.4f}x + {b_ref:.4f}")

    graficar_resultados(x, y, pendiente, interseccion, errores)


if __name__ == "__main__":
    main()
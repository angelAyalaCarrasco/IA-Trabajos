import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler


def ejecutar_ejemplo():
    # Datos de entrenamiento: Kilómetros y su equivalencia en Millas
    km_entrenamiento = np.array([1, 5, 10, 21.1, 42.2, 60, 80, 100], dtype=float).reshape(-1, 1)
    millas_reales = km_entrenamiento.flatten() * 0.621371

    # Normalización de entradas
    escalador = StandardScaler()
    km_normalizados = escalador.fit_transform(km_entrenamiento)

    # Configuración y entrenamiento de la neurona lineal
    neurona = SGDRegressor(
        max_iter=1500,
        tol=1e-4,
        learning_rate="invscaling",
        eta0=0.02,
        random_state=10
    )
    neurona.fit(km_normalizados, millas_reales)

    # Evaluación con datos nuevos
    km_prueba = np.array([3, 15, 50], dtype=float).reshape(-1, 1)
    predicciones = neurona.predict(escalador.transform(km_prueba))

    print("Resultados de predicción (Km a Millas):")
    for km, pred in zip(km_prueba.flatten(), predicciones):
        esperado = km * 0.621371
        print(f"  {km:5.1f} km -> Estimado: {pred:.4f} mi | Exacto: {esperado:.4f} mi")

    # Extracción de pesos en escala normalizada
    w_norm = neurona.coef_[0]
    b_norm = neurona.intercept_[0]

    # Conversión de parámetros a la escala original
    media = escalador.mean_[0]
    desv_est = escalador.scale_[0]

    w_real = w_norm / desv_est
    b_real = b_norm - (w_norm * media / desv_est)

    print("\nParámetros del modelo:")
    print(f"  Escala normalizada -> W: {w_norm:.4f}, Bias: {b_norm:.4f}")
    print(f"  Escala original    -> W: {w_real:.4f}, Bias: {b_real:.4f}")
    print(f"  Ecuación resultante: Millas = {w_real:.4f} * Km + {b_real:.4f}")


if __name__ == "__main__":
    ejecutar_ejemplo()
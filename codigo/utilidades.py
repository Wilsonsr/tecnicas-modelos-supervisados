"""
Utilidades del curso · Técnicas de Análisis Estadístico de Modelos Supervisados

Funciones de apoyo para los cuadernillos y para el proyecto integrador.
Nada aquí es imprescindible: todo se puede escribir a mano con pandas y
scikit-learn. El objetivo es evitar repetir el mismo bloque diez veces.

Uso:
    import sys; sys.path.append("codigo")
    from utilidades import SEMILLA, radiografia, evaluar_regresion, ...
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
    root_mean_squared_error,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEMILLA = 42

# Paleta del sitio, para que los gráficos del curso se vean consistentes.
COLORES = {
    "azul": "#12304F",
    "teal": "#17808C",
    "terracota": "#B4543A",
    "verde": "#2E6B4F",
    "ambar": "#B07D12",
    "morado": "#6A4C93",
    "gris": "#6B7A8C",
}


# ──────────────────────────────────────────────────────────────────────────
# Exploración
# ──────────────────────────────────────────────────────────────────────────

def radiografia(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen estructural de un DataFrame: tipo, faltantes, únicos y ejemplo.

    Es lo primero que conviene mirar de cualquier tabla nueva: revela columnas
    numéricas leídas como texto, faltantes concentrados y variables de alta
    cardinalidad.
    """
    return pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "faltantes": df.isna().sum(),
        "% faltantes": (df.isna().mean() * 100).round(2),
        "únicos": df.nunique(),
        "ejemplo": [df[c].dropna().iloc[0] if df[c].notna().any() else None
                    for c in df.columns],
    })


def construir_preprocesador(cols_num: list[str],
                            cols_cat: list[str],
                            estandarizar: bool = True) -> ColumnTransformer:
    """Preprocesador estándar del curso.

    Numéricas: imputación por mediana y, opcionalmente, estandarización.
    Categóricas: imputación por moda y codificación one-hot.

    `estandarizar=False` es apropiado para modelos basados en árboles, donde
    la escala no aporta nada.
    """
    pasos_num = [("imputar", SimpleImputer(strategy="median"))]
    if estandarizar:
        pasos_num.append(("escalar", StandardScaler()))

    rama_cat = Pipeline([
        ("imputar", SimpleImputer(strategy="most_frequent")),
        ("codificar", OneHotEncoder(handle_unknown="ignore", drop="first",
                                    sparse_output=False)),
    ])

    return ColumnTransformer([
        ("num", Pipeline(pasos_num), cols_num),
        ("cat", rama_cat, cols_cat),
    ])


def agrupar_categorias_raras(serie: pd.Series,
                             minimo: int = 20,
                             etiqueta: str = "OTROS") -> pd.Series:
    """Agrupa en una sola categoría los niveles con menos de `minimo` casos.

    Evita matrices enormes al aplicar one-hot a variables de alta cardinalidad
    y reduce el sobreajuste en categorías con muy pocos casos.
    """
    frecuencias = serie.value_counts()
    frecuentes = frecuencias[frecuencias >= minimo].index
    return serie.where(serie.isin(frecuentes), etiqueta)


# ──────────────────────────────────────────────────────────────────────────
# Evaluación
# ──────────────────────────────────────────────────────────────────────────

def evaluar_regresion(nombre: str, modelo, X_train, y_train,
                      X_test, y_test) -> dict:
    """Ajusta un modelo de regresión y devuelve RMSE, MAE y R² en prueba."""
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)
    return {
        "Modelo": nombre,
        "RMSE": root_mean_squared_error(y_test, pred),
        "MAE": mean_absolute_error(y_test, pred),
        "R²": r2_score(y_test, pred),
    }


def evaluar_clasificacion(nombre: str, modelo, X_train, y_train,
                          X_test, y_test, umbral: float = 0.5) -> dict:
    """Ajusta un clasificador y devuelve las métricas de la matriz de confusión.

    El umbral es explícito y por defecto vale 0,5. En problemas desbalanceados
    ese valor casi nunca es el adecuado: ver el Cuadernillo 4.
    """
    modelo.fit(X_train, y_train)
    proba = modelo.predict_proba(X_test)[:, 1]
    pred = (proba >= umbral).astype(int)
    return {
        "Modelo": nombre,
        "Umbral": umbral,
        "Exactitud": accuracy_score(y_test, pred),
        "Sensibilidad": recall_score(y_test, pred, zero_division=0),
        "Especificidad": recall_score(y_test, pred, pos_label=0, zero_division=0),
        "Precisión": precision_score(y_test, pred, zero_division=0),
        "F1": f1_score(y_test, pred, zero_division=0),
        "AUC": roc_auc_score(y_test, proba),
    }


def barrido_umbral(y_verdadero, probabilidades,
                   umbrales=None,
                   costo_fp: float = 1.0,
                   costo_fn: float = 1.0) -> pd.DataFrame:
    """Tabla de métricas y costo total para una serie de umbrales.

    Los costos son relativos y los define el problema. El umbral recomendado
    es el de costo mínimo, no el de exactitud máxima.
    """
    if umbrales is None:
        umbrales = np.arange(0.05, 0.96, 0.05)

    filas = []
    for umbral in umbrales:
        pred = (np.asarray(probabilidades) >= umbral).astype(int)
        vn, fp, fn, vp = confusion_matrix(y_verdadero, pred,
                                          labels=[0, 1]).ravel()
        filas.append({
            "umbral": round(float(umbral), 3),
            "VP": int(vp), "FN": int(fn), "FP": int(fp), "VN": int(vn),
            "sensibilidad": vp / (vp + fn) if (vp + fn) else 0.0,
            "especificidad": vn / (vn + fp) if (vn + fp) else 0.0,
            "precision": vp / (vp + fp) if (vp + fp) else 0.0,
            "exactitud": (vp + vn) / len(y_verdadero),
            "costo_total": fp * costo_fp + fn * costo_fn,
        })
    return pd.DataFrame(filas)


def resumen_validacion(puntajes: np.ndarray, etiqueta: str = "") -> str:
    """Formatea el resultado de una validación cruzada con su dispersión.

    Reportar la media sin la dispersión es el error más común al comparar
    modelos: sin ella no se puede saber si una diferencia es real.
    """
    puntajes = np.asarray(puntajes)
    return (f"{etiqueta}media = {puntajes.mean():.3f} · "
            f"sd = {puntajes.std():.3f} · "
            f"rango = [{puntajes.min():.3f} ; {puntajes.max():.3f}]")


# ──────────────────────────────────────────────────────────────────────────
# Verificación de reproducibilidad
# ──────────────────────────────────────────────────────────────────────────

def verificar_fuga(columnas: list[str], objetivo: str) -> None:
    """Recordatorio de la pregunta que hay que hacerse por cada predictora.

    No detecta la fuga automáticamente —ninguna función puede hacerlo—, pero
    obliga a mirar la lista completa antes de modelar.
    """
    print(f"Variable objetivo: {objetivo}\n")
    print("Para CADA predictora, responde: en el momento de predecir, "
          "¿ya conozco este valor?\n")
    for i, col in enumerate(columnas, 1):
        print(f"  {i:>2}. {col}")
    print("\nSi alguna se calcula a partir del objetivo, o solo se conoce "
          "después, sácala.")

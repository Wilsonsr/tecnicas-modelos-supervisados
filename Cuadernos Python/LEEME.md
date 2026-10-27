# Cuadernos Python — material de referencia

Notebooks del curso anterior (*Métodos Estadísticos para Analítica de Datos*),
conservados como **fuente de ejemplos**. No forman parte del sitio del curso:
los cuadernillos vivos están en `00-inicio/` … `06-proyecto/`.

El nombre de cada archivo dice de qué trata: `regresion-`, `clasificacion-`,
`ambos-`, `nosupervisado-`, `teoria-` o `auxiliar-`. El sufijo `-v2` / `-v3`
marca versiones anteriores de un mismo cuaderno; **la versión sin sufijo es la
más completa**.

> **Aviso sobre los datos.** Varios de estos cuadernos leen de URL que ya
> cambiaron (UCI reorganizó sus rutas) o usan conjuntos retirados. Lo que se
> reutiliza de ellos es la **secuencia didáctica**, no el código tal cual.

---

## Regresión

| Archivo | Qué aporta | Datos | Celdas |
|---|---|---|---|
| `regresion-01-random-forest-boston.ipynb` | **La pieza más completa.** `n_estimators`, `max_features`, grid search por **OOB frente a validación cruzada**, importancia de predictores y SHAP | Boston (⚠️ retirado por motivos éticos) | 57 |
| `regresion-01-random-forest-boston-v2.ipynb` | Versión anterior, más corta | — | 48 |
| `regresion-02-xgboost-inmuebles.ipynb` | Boosting con ajuste de hiperparámetros y selección de variables | Real estate valuation (UCI, URL caducada) | 101 |
| `regresion-03-pronostico-precios-vivienda.ipynb` | EDA extenso, regresión lineal y una sección de logística | Inmuebles Bogotá | 50 |
| `regresion-04-inmobiliario-bogota.ipynb` | Lineal paso a paso (incluida la ecuación normal) y logística | Inmuebles Bogotá | 84 |

## Regresión y clasificación

| Archivo | Qué aporta | Datos | Celdas |
|---|---|---|---|
| `ambos-01-arbol-decision-carseats.ipynb` | **Poda por coste-complejidad (`ccp_alpha`)**, one-hot con `ColumnTransformer`, árbol de regresión y de clasificación | Carseats (ISLR) | 56 |
| `ambos-01-arbol-decision-carseats-v2.ipynb` | Versión anterior | Carseats | 55 |
| `ambos-01-arbol-decision-carseats-v3.ipynb` | Versión anterior | Carseats | 52 |
| `ambos-02-metricas-regresion-clasificacion.ipynb` | **El más limpio de la carpeta.** Métricas de ambos tipos, sin dependencias raras | — | 18 |

## Clasificación

| Archivo | Qué aporta | Datos | Celdas |
|---|---|---|---|
| `clasificacion-01-arbol-decision-iris.ipynb` | Árbol paso a paso | Iris (UCI) | 33 |
| `clasificacion-02-naive-bayes.ipynb` | Teorema de Bayes y supuesto de independencia | — | 12 |
| `clasificacion-03-naive-bayes-aplicado.ipynb` | Naive Bayes frente a logística | Google Drive (enlace personal) | 47 |
| `clasificacion-04-titanic-reglas-vs-ml.ipynb` | **Buena estructura pedagógica:** modelo de reglas contra modelo aprendido, con ejercicios puntuados | Titanic | 18 |
| `clasificacion-05-boosting-adult.ipynb` | Random Forest, XGBoost y LightGBM comparados | Adult (UCI, URL caducada) | 81 |
| `clasificacion-06-datos-desbalanceados.ipynb` | SMOTE, enlaces de Tomek, NearMiss y entrenamiento sensible al coste | Credit card fraud | 31 |

## Teoría (sin código ejecutable)

| Archivo | Qué aporta |
|---|---|
| `teoria-01-arboles-de-decision.ipynb` | Entropía, ganancia de información, índice de Gini, poda. 21 celdas de texto |
| `teoria-02-maquinas-soporte-vectorial.ipynb` | SVM y el truco del kernel. 17 celdas de texto, ninguna de código |

## Aprendizaje no supervisado

Fuera del alcance del curso actual, que es de modelos **supervisados**. Se
conservan por su valor para otras asignaturas.

| Archivo | Tema |
|---|---|
| `nosupervisado-01-agrupamiento-jerarquico.ipynb` | Dendrogramas y enlace |
| `nosupervisado-02-cluster-jerarquico.ipynb` · `-v2` | Clúster jerárquico aplicado (Mall Customers) |
| `nosupervisado-03-kmeans.ipynb` · `-v2` | k-means y selección de k |
| `nosupervisado-04-dbscan.ipynb` · `-v2` | DBSCAN frente a k-means |
| `nosupervisado-05-kmeans-samsung.ipynb` | k-means aplicado |
| `nosupervisado-06-pca-kmeans-airbnb.ipynb` | PCA seguido de k-means |
| `nosupervisado-07-delitos-colombia.ipynb` · `-v2` · `-v3` | Agrupamiento de delitos por departamento |

## Auxiliares

| Archivo | Tema |
|---|---|
| `auxiliar-01-codificacion-variables-categoricas.ipynb` | Label, ordinal, Helmert, binary, frequency, mean y WoE encoding |
| `auxiliar-02-visualizacion.ipynb` | Gráficos con series de COVID-19 |
| `auxiliar-03-actividad-delitos.ipynb` | Enunciado de actividad |

---

## Qué se reutilizó en el curso nuevo

| De aquí | Fue a |
|---|---|
| Secuencia de ajuste de Random Forest (OOB frente a CV) | Cuadernillo 3b · Torneo de modelos |
| Poda por coste-complejidad del árbol | Cuadernillo 3b |
| Métricas de regresión y clasificación | Cuadernillos 3a y 4a |
| Idea de contrastar reglas con modelo aprendido | El modelo base obligatorio de todos los cuadernillos |
| Codificación de variables categóricas | Cuadernillo 2 |

Lo demás quedó fuera por estar en aprendizaje no supervisado, por depender de
datos inaccesibles o por caer fuera del plan de contenidos.

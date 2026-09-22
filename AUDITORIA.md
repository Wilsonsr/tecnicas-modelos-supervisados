# Auditoría del repositorio `Wilsonsr/Metodos-Estadisticos`

**Fecha:** 22 de septiembre de 2026
**Alcance:** 134 archivos versionados (excluyendo `.git`)
**Propósito:** determinar qué material del repositorio original es reutilizable
para el nuevo espacio académico *Técnicas de Análisis Estadístico de Modelos
Supervisados*.

> El repositorio original **no fue modificado**. Se leyó en su estado actual y
> permanece intacto como archivo.

---

## 1. Hallazgo principal

El repositorio original corresponde a un curso **distinto**: *Métodos
Estadísticos para Analítica de Datos* (Universidad Central, maestría), centrado
en **estadística exploratoria multidimensional** y **aprendizaje no
supervisado**.

De las 17 lecturas que anuncia su README, **diez** tratan temas fuera del
alcance del nuevo curso:

| Tema del repositorio original | ¿Pertenece al nuevo curso? |
|---|---|
| Análisis de Componentes Principales (PCA) | No — no supervisado |
| Análisis de Correspondencias simple y múltiple | No — no supervisado |
| Análisis Factorial | No — no supervisado |
| Clúster jerárquico, k-means, DBSCAN | No — no supervisado |
| Naive Bayes, SVM, XGBoost, LightGBM | No — fuera del plan de contenidos |
| Regresión lineal y logística | **Sí** |
| Árboles de decisión y Random Forest | **Sí** |
| Validación cruzada | **Sí** |
| Métricas de regresión y clasificación | **Sí** |
| Codificación de variables y datos desbalanceados | **Sí** |

**Conclusión:** el repositorio original es una **fuente de materiales**, no una
estructura a conservar. Aproximadamente el **20 %** de su contenido tiene valor
directo para el nuevo curso.

### Lo que sí resultó valioso

1. **Las dos presentaciones de 2026** (`01 - Introducción a Machine Learning.pptx`
   y `Validación, Evaluación y Regularización.pptx`). Son el material más
   reciente, más pedagógico y más alineado con el nuevo curso de todo el
   repositorio. Contienen exactamente la secuencia conceptual que el nuevo plan
   exige, incluido un ejemplo excelente de *accuracy* engañoso con diagnóstico
   médico y una exposición clara del compromiso sesgo-varianza y de la
   regularización.
2. **Dos conjuntos de datos** de calidad y pertinencia notables, que se
   convirtieron en los datasets transversales del nuevo curso.
3. **Fragmentos de código** sobre métricas, codificación de categóricas y
   Random Forest, reutilizables tras actualización.

---

## 2. Tabla de diagnóstico

Códigos de acción: **A** conservar casi sin cambios · **B** conservar
actualizando · **C** reutilizar parcialmente · **D** reemplazar · **E**
eliminar o archivar · **F** material nuevo por crear.

### 2.1 Raíz del repositorio

| Recurso actual | Tema | Calidad | Vigencia | Acción | Nuevo destino |
|---|---|---|---|---|---|
| `README.md` | Índice del curso anterior | Media | **Obsoleta** — los enlaces apuntan a `CUADERNOS/` y `BASES/`, carpetas que ya no existen: **todos los enlaces internos están rotos** | **D** | `README.md` nuevo + `index.qmd` |
| `01 - Introducción a Machine Learning.pptx` (72 diapositivas, sep. 2026) | Introducción a ML, supervisado vs. no supervisado, componentes, proceso | **Alta** | Vigente | **C** | Base conceptual del **Cuadernillo 1** |
| `Validación, Evaluación y Regularización.pptx` (47 diapositivas, sep. 2026) | Métricas, matriz de confusión, ROC, AUC, sesgo-varianza, Ridge, Lasso, estandarización | **Alta** | Vigente | **C** | Base conceptual de los **Cuadernillos 1, 3, 4 y 5** |
| `Lectura_2_Analisis_Descriptivo_Multivariado.ipynb` (14 MB, 67 celdas) | EDA multivariado, covarianzas, dispersión, tablas de contingencia | Media-alta | Parcial | **C** | Ideas de EDA → **Cuadernillo 2**. Autoría de un tercero (Luis Andrés Campos Maldonado): no se reutiliza literalmente |
| `app_enfermeria_fgr.py`, `app_medicina_fgr.py`, `app_final.py`, `app_forestplot.py`, `menores.py` | Aplicaciones Streamlit del Ministerio de Salud | — | Vigente pero **ajena al curso** | **E** | Permanecen en el repositorio original |
| `arrem_app/` (incluye 10 `.pyc` versionados) | Aplicación Streamlit ARREM | — | Ajena al curso | **E** | Permanece. *Nota: los `.pyc` no deberían estar versionados* |
| `THS_FORMULARIO/DIVIPOLA_Municipios.xlsx` | Codificación territorial | — | Ajena al curso | **E** | Permanece |
| `data_enfermeria_graduado.csv`, `data_medicina_graduado.csv` | Datos de las apps | — | Ajenos al curso | **E** | Permanecen |
| `requirements.txt` | Dependencias de las apps Streamlit | Baja | **Obsoleto** para el curso — no incluye `scikit-learn` | **D** | `requirements.txt` nuevo |
| `.devcontainer/devcontainer.json` | Configuración de Codespaces que lanza `menores.py` | Baja | Ajena al curso | **E** | Permanece |

### 2.2 `Cuadernos Python/` (36 notebooks)

| Recurso actual | Tema | Calidad | Vigencia | Acción | Nuevo destino |
|---|---|---|---|---|---|
| `metricas regresion y clasificacion.ipynb` (23 KB, 29 celdas) | Métricas de ambos tipos | **Alta** — el más limpio del repositorio | Vigente | **B** | **Cuadernillos 1, 3 y 4**, con métricas contextualizadas |
| `Codificacion variables categoricas.ipynb` (49 celdas) | Label, ordinal, Helmert, binary, frequency, mean, WoE | **Alta** | Parcial — depende de `category_encoders`, no estándar | **C** | **Cuadernillo 2**, reducido a one-hot y ordinal, con `ColumnTransformer` |
| `Laboratorio_Titanic_v6…ipynb` (40 celdas) | Reglas frente a ML, con ejercicios puntuados | **Alta** estructura pedagógica | Parcial — dataset clásico; enlace a Google Drive frágil | **C** | Inspiración de las **microactividades**; el modelo base del Cuadernillo 1 recoge su idea central |
| `precios_en_el_sector_inmobiliario_en_Bogotá.ipynb` (117 celdas) | Regresión lineal y logística con vivienda en Bogotá | Media-alta | **Rota** — lee de `…/main/BASES/inmuebles_bogota_res.csv`, ruta inexistente; usa `ydata_profiling` | **C** | **Se rescata el dataset**, que pasa a ser el conjunto transversal de regresión |
| `04a_Pronóstico_de_precios_de_viviendas_20221 (1).ipynb` (83 celdas) | El mismo caso con más EDA | Media | **Rota** — misma URL; usa `sweetviz` | **C** | Ideas de EDA → **Cuadernillo 2** |
| `Random_Forest_1.ipynb` (89 celdas) | RF, hiperparámetros, grid search OOB y CV, importancia, SHAP | **Alta** contenido | Parcial — `sweetviz`, `shap`, sin `Pipeline` | **C** | **Cuadernillo 4**, reescrito con `Pipeline` e importancia por permutación |
| `arbol_decision_1.ipynb` (27 celdas, 21 de texto) | Teoría de árboles: entropía, Gini, poda | Media-alta | Vigente | **C** | Síntesis conceptual → **Cuadernillo 4** |
| `arbol_de_decision_2.ipynb` y sus 2 duplicados | Árboles aplicados con one-hot | Media | Parcial | **C** / **E** | Se conserva una versión; los duplicados se archivan |
| `Copia_de_Datos_desbalanceados.ipynb` (51 celdas) | SMOTE, Tomek, NearMiss, cost-sensitive | Media-alta | Parcial — `imblearn`; descarga externa desde GitHub de terceros | **C** | El **enfoque de umbral y costos** del Cuadernillo 4 sustituye al remuestreo, más adecuado al enfoque estadístico del curso |
| `Adult.ipynb` (102 celdas) | LightGBM, XGBoost | Media | Parcial — UCI cambió de estructura de URL | **E** | Fuera del plan de contenidos |
| `Xgboost (1).ipynb` (127 celdas) | XGBoost | Media | Parcial | **E** | Fuera del plan |
| `svmint.ipynb` (17 celdas, **0 de código**) | SVM, solo teoría | Baja | Vigente | **E** | Fuera del plan |
| `Naive_Bayes_1.ipynb`, `Naive_Bayes_2.ipynb` | Naive Bayes | Media | Vigente | **E** | Fuera del plan |
| `Visualizacion_(1).ipynb` | Gráficos | Media | Vigente | **C** | Criterios gráficos incorporados al nuevo material |
| `1_Agrupamiento_jerarquico.ipynb` (12,8 MB), `2_Cluster_jerarquico*.ipynb` ×2, `Aprendizaje_no_supervisado Kmeans*.ipynb` ×2, `DBSCAN*.ipynb` ×2, `kmeanssamsung.ipynb`, `pca_kmeans_airbnb.ipynb` | Aprendizaje no supervisado | Media-alta | Vigente | **E** | **Fuera del alcance.** Permanecen en el repositorio original |
| `Delitos Colombia*.ipynb` ×3 (hasta 21,9 MB), `Actividad Delitos.ipynb` (14,9 MB) | Clustering de delitos | Media | Vigente | **E** | No supervisado; además, archivos muy pesados |
| `rsconnect/` | Metadatos de publicación en RPubs | — | Residual | **E** | Archivo residual |
| `.RData`, `.Rhistory`, `.ipynb_checkpoints/` | Residuos de sesión | — | — | **E** | No deberían estar versionados |

### 2.3 `Cuadernos R/` (6 archivos `.Rmd`)

| Recurso actual | Tema | Calidad | Vigencia | Acción | Nuevo destino |
|---|---|---|---|---|---|
| `ACP.Rmd`, `Actividad_ACP.Rmd`, `homicidiosacp.Rmd` | Componentes principales | Media-alta | Vigente | **E** | No supervisado |
| `ANALISIS DE CORRESPONDENCIAS.Rmd`, `ANALISIS DE CORRESPONDENCIAS MULTIPLES .Rmd`, `acmunal.Rmd` | Correspondencias | Media-alta | Vigente | **E** | No supervisado |

> **Observación:** no existía **ningún** material en R sobre modelos
> supervisados. La ruta en R del nuevo curso es material completamente nuevo
> (acción **F**), construida con `tidymodels`.

### 2.4 `Data/` (56 archivos)

| Recurso actual | Filas | Calidad | Acción | Nuevo destino |
|---|---|---|---|---|
| `inmuebles_bogota_res.csv` | 10 000 | **Alta pertinencia**, calidad de datos deliberadamente imperfecta | **A** | **Dataset transversal de regresión** → `datos/crudos/vivienda_bogota.csv` |
| `Absenteeism_at_work.xls` | 740 | **Alta** — UCI, bien documentado, 9 % de casos positivos | **A** | **Dataset transversal de clasificación** → `datos/crudos/ausentismo_laboral.csv` |
| `boston_house_prices.csv` | 506 | Media | **E** | Dataset retirado de scikit-learn por problemas éticos documentados |
| `IRIS.csv` | 150 | Media | **E** | Excesivamente clásico |
| `Social_Network_Ads.csv` | 400 | Baja | **E** | Artificial |
| `weatherAUS.csv` | **0** | **Archivo vacío (1 línea)** | **E** | Archivo roto |
| `StudentsPerformance.csv`, `student-mat.csv`, `student-por.csv` | 1000 / 395 / 649 | Media-alta | **C** | Alternativas ofrecidas para el proyecto |
| `Diabetes.csv`, `Cancer.csv` | 520 / 569 | Media | **C** | Alternativas; requieren cuidado ético |
| `Computers.csv`, `airbnb.csv`, `datos.csv` | 6259 / 7210 / 4406 | Media | **C** | Alternativas de regresión |
| `Delitos_Colombia.csv`, `Departamentos.csv`, `depto.csv`, `DelitosC.xlsx` | 33–34 | Media | **E** | Pensados para clustering; muy pocas filas |
| `Mall_Customers (1).csv`, `segmentation data.csv`, `Whisky.csv`, `poison1.csv`, `admisiones.csv`, `basestronk.csv`, `trees.csv`, `Howell1.csv`, `athletes.csv`, `medals.csv`, `005930.KS (1).csv`, `series1 (2).xlsx`, `INFLACION.xlsx`, `IPC.xlsx`, `ML.xlsx`, `ObesityDataSet…csv` | varias | — | **E** | Para clustering, series temporales u otros cursos |
| `MGN_DPTO_POLITICO.zip`, `gadm36_COL_1_sp.rds` | — | — | **E** | Cartografía; fuera del alcance |
| 14 archivos `.png` (gráficos de clustering, cuantiles, transformaciones) | — | Media | **E** | Ilustran temas no supervisados |

---

## 3. Auditoría técnica: enlaces, código y dependencias

### 3.1 Enlaces rotos

| Problema | Detalle | Impacto |
|---|---|---|
| **Todos los enlaces del README** | Apuntan a `.../blob/main/CUADERNOS/...`; la carpeta se renombró a `Cuadernos Python` | **Crítico** — ningún enlace del índice funciona |
| **URL de datos en dos notebooks** | `https://raw.githubusercontent.com/Wilsonsr/Metodos-Estadisticos/main/BASES/inmuebles_bogota_res.csv`; la carpeta `BASES/` se renombró a `Data/` | **Crítico** — los notebooks de vivienda no se ejecutan |
| **UCI Adult** | `https://archive.ics.uci.edu/ml/machine-learning-databases/adult/…`; UCI migró su estructura de URL | Alto |
| **Google Drive (Titanic)** | `https://docs.google.com/uc?id=…` | Medio — depende de permisos de un archivo personal |
| **Repositorio de terceros (creditcard)** | `github.com/nsethi31/Kaggle-Data-Credit-Card-Fraud-Detection` | Medio — dependencia externa fuera de control |
| **Presentaciones en Google Slides** | Dos enlaces con `ouid` personal | Medio — no accesibles sin permisos |
| **RPubs** | Cinco enlaces a `rpubs.com/wilsonsr/…` | Bajo — vigentes, pero fuera del repositorio |

### 3.2 Dependencias obsoletas o frágiles

| Librería | Usada en | Problema |
|---|---|---|
| `sweetviz` | 5 notebooks | Mantenimiento irregular; frecuentes conflictos con versiones recientes de `pandas` |
| `ydata_profiling` | 1 notebook | Muy pesada; API inestable entre versiones |
| `category_encoders` | 1 notebook | No es estándar; la mayoría de sus codificadores requieren cuidado extremo con la fuga de información |
| `imblearn` | 1 notebook | Válida, pero su uso desplaza la discusión de umbral y costos, más apropiada para un curso estadístico |
| `shap` | 1 notebook | Pesada; API cambiante |
| `xgboost`, `lightgbm` | 3 notebooks | Fuera del plan de contenidos del nuevo curso |

**Decisión para el nuevo repositorio:** el entorno se reduce a
`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `plotly`,
`statsmodels` y `openpyxl`. Ocho librerías, todas estándar y estables.

### 3.3 Problemas de reproducibilidad detectados

| Problema | Frecuencia | Corrección en el nuevo repositorio |
|---|---|---|
| Ausencia de `random_state` en `train_test_split` y en modelos | Generalizada | `SEMILLA = 42` explícita en toda función con azar |
| Preprocesamiento aplicado antes de la partición | Frecuente | Todo dentro de `Pipeline` / `ColumnTransformer` |
| Ausencia de `Pipeline` | **Ningún notebook lo usa** | `Pipeline` en todos los cuadernillos, con justificación explícita |
| Notebooks con salidas de ejecuciones fuera de orden | Frecuente | Los `.qmd` se renderizan de principio a fin en cada publicación |
| Archivos de hasta 21,9 MB por salidas embebidas | 6 notebooks | Los `.qmd` no almacenan salidas; se generan al renderizar |
| Duplicados con sufijos `(1)`, `(2)` | 9 pares | Un archivo por tema |
| Archivos `.pyc`, `.RData`, `.Rhistory` versionados | 13 archivos | `.gitignore` completo |

---

## 4. Vacíos conceptuales frente al nuevo plan

Verificación de los problemas señalados en el encargo:

| Problema a verificar | ¿Presente en el repositorio original? | Tratamiento en el nuevo repositorio |
|---|---|---|
| Explicación insuficiente de train/test | **Sí** — se usa sin explicar su fundamento | Cuadernillo 1, sección propia con los dos errores contrastados |
| Confusión entre explicar y predecir | **Sí** — no se distinguen en ningún punto | Cuadernillo 1, «Dos culturas, una misma ecuación»; Cuadernillo 3, `statsmodels` frente a `scikit-learn` |
| Poca conexión entre estadística y ML | **Sí** — el enfoque es de ejecución de algoritmos | Supuestos, inferencia, VIF, Breusch-Pagan, Cook y calibración integrados |
| Métricas sin contexto | **Sí** | Toda métrica se justifica con el problema; función de costo explícita |
| Ausencia de validación cruzada | Parcial — aparece en un notebook de RF | Cuadernillos 3 y 5, incluida validación agrupada |
| Uso del test set para ajustar | **Sí** — prácticas ambiguas | Regla explícita y microactividad *Reto* de corrección (Cuadernillo 4) |
| Ausencia de pipelines | **Sí — total** | `Pipeline` en todos los cuadernillos |
| Data leakage | **Sí** — sin mencionar nunca el concepto | Sección central del Cuadernillo 2, con dos demostraciones cuantitativas |
| Poca interpretación estadística | **Sí** | Preguntas de interpretación tras cada resultado relevante |
| Ejemplos artificiales | Parcial — Iris, Social Network Ads, Titanic | Dos datasets reales y transversales |
| Código obsoleto | **Sí** | Código nuevo, ejecutado y verificado en cada publicación |
| Paquetes desactualizados | **Sí** | Ocho librerías estándar |
| Gráficos poco claros | Parcial | Paleta única, gráficos con pregunta asociada |
| Exceso de teoría / poca práctica | Parcial — `arbol_decision_1` y `svmint` son casi solo texto | Conceptos breves; el peso está en la interpretación |
| Ausencia de Ridge/Lasso | **Sí en código** (solo en presentación) | Cuadernillo 3, con ruta de coeficientes y experimento de tamaño muestral |
| Ausencia de Random Forest | No — sí está | Cuadernillo 4, reescrito con `Pipeline` |
| Ausencia de k-NN | **Sí — no existe** | Cuadernillo 4, con demostración de la necesidad de estandarizar |
| Ausencia de comparación entre modelos | **Sí** | Cuadernillos 3, 4 y 5, con dispersión y análisis de estabilidad |
| ROC/AUC superficial | Parcial — bien en la presentación, ausente en el código | Cuadernillo 4: ROC interactiva con umbral, curva PR y su justificación |
| Ausencia de ética o análisis de sesgos | **Sí — total** | Cuadernillo 5, parte 4, con medición empírica del aporte de las variables sensibles |

**Vacíos adicionales detectados durante la auditoría**, no previstos en el
encargo:

1. **Sin modelo base en ningún notebook.** Los resultados se reportan sin punto
   de comparación. → Requisito obligatorio en el nuevo material.
2. **Sin tratamiento de la estructura de grupos.** Con datos de medidas
   repetidas, la validación cruzada estándar es optimista. → Cuadernillo 5.
3. **Sin discusión del umbral de clasificación.** Se usa `predict()` con 0,5
   implícito. → Eje central del Cuadernillo 4.
4. **Sin calibración de probabilidades.** → Cuadernillo 5.
5. **Sin diccionarios de datos.** Ningún dataset está documentado. → Página
   «Datos del curso» con diccionario completo y advertencias de calidad.
6. **Sin guía de uso de IA**, pertinente en 2026. → Página propia.

---

## 5. Resumen cuantitativo

| Acción | Archivos | Proporción |
|---|---|---|
| **A** · Conservar casi sin cambios | 2 | 1,5 % |
| **B** · Conservar actualizando | 1 | 0,7 % |
| **C** · Reutilizar parcialmente | 16 | 11,9 % |
| **D** · Reemplazar | 2 | 1,5 % |
| **E** · Archivar (permanecen en el repositorio original) | 113 | 84,3 % |
| **Total auditado** | **134** | **100 %** |

| **F** · Material nuevo creado | Cantidad |
|---|---|
| Cuadernillos completos con código ejecutable | 7 |
| Páginas de recursos (mapa curricular, errores, glosario, equivalencias, IA) | 5 |
| Páginas de inicio (portada, instalación, datos) | 3 |
| Bibliografía verificada | 1 |
| Ruta completa en R con `tidymodels` | 1 |
| Módulo de utilidades en Python | 1 |
| Infraestructura (Quarto, tema, flujo de publicación) | 6 |

---

## 6. Recomendaciones sobre el repositorio original

No requieren acción inmediata, pero conviene registrarlas:

1. **Corregir los enlaces del README**: `CUADERNOS/` → `Cuadernos%20Python/`.
   Es un cambio de cinco minutos que devuelve la utilidad al índice.
2. **Corregir la URL de datos** en los notebooks de vivienda:
   `BASES/` → `Data/`.
3. **Añadir un `.gitignore`** que excluya `.pyc`, `.RData`, `.Rhistory` y
   `.ipynb_checkpoints/`.
4. **Limpiar las salidas** de los notebooks más pesados antes de versionarlos:
   cuatro archivos superan los 12 MB solo por imágenes embebidas.
5. **Separar las aplicaciones del Ministerio** (`arrem_app/`, `app_*.py`,
   `menores.py`) en su propio repositorio: no tienen relación con el curso y
   dificultan la navegación.
6. **Añadir un aviso en el README** indicando que el curso de modelos
   supervisados continúa en el nuevo repositorio.

---

## 7. Decisiones de diseño del nuevo repositorio

| Decisión | Justificación |
|---|---|
| **Quarto + GitHub Pages** en lugar de notebooks sueltos | El código se ejecuta en cada publicación: un cuadernillo roto no llega al sitio. Además da navegación, buscador, modo oscuro y pestañas R/Python |
| **Dos datasets transversales** en lugar de uno por técnica | Permite ver cómo evoluciona una misma decisión conforme crecen las herramientas |
| **Datos entregados crudos** | Aprender a limpiar con datos limpios es imposible. Los 951 inmuebles de 0 m² y el precio de 870 mil millones son material didáctico |
| **Python principal, R en pestañas** | El 95 % del material aprovechable estaba en Python; duplicarlo todo multiplicaría el mantenimiento sin ganancia pedagógica |
| **Sin XGBoost, LightGBM, SVM ni Naive Bayes** | No están en el plan de contenidos. Menos temas, mejor tratados |
| **Umbral y costos en lugar de SMOTE** | El enfoque de teoría de la decisión es más estadístico y más honesto que el remuestreo sintético para el desbalance de este problema |
| **Ética con medición, no con declaración** | Se mide el aporte real de las variables sensibles (+0,008 de AUC, dentro del ruido) y se decide con evidencia |
| **Ocho librerías estándar** | Un entorno que se instala con un comando y no se rompe en seis meses |

---

*Auditoría realizada sobre el estado del repositorio al 22 de septiembre de 2026.
El repositorio original no fue modificado en ningún punto del proceso.*

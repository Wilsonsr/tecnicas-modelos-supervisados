# ═══════════════════════════════════════════════════════════════════════════
# Flujo completo en R con tidymodels
# Técnicas de Análisis Estadístico de Modelos Supervisados
#
# Equivalente en R de lo que los cuadernillos hacen en Python.
# Requiere: tidymodels, glmnet, ranger, kknn, vip, car, lmtest
#
# Este archivo NO se ejecuta al construir el sitio. Es material de referencia
# para quienes trabajen el curso en R.
# ═══════════════════════════════════════════════════════════════════════════

library(tidymodels)
library(readr)
library(dplyr)

tidymodels_prefer()
set.seed(42)


# ───────────────────────────────────────────────────────────────────────────
# PARTE 1 · REGRESIÓN — vivienda en Bogotá  (Cuadernillo 3)
# ───────────────────────────────────────────────────────────────────────────

vivienda <- read_csv("datos/procesados/vivienda_modelado.csv") |>
  mutate(
    precio_mm     = valor_venta / 1e6,
    tipo_inmueble = factor(tipo_inmueble),
    zona          = factor(zona)
  ) |>
  select(-valor_venta, -barrio_comun)

# --- Partición -------------------------------------------------------------
particion_v   <- initial_split(vivienda, prop = 0.80)
entrenamiento <- training(particion_v)
prueba        <- testing(particion_v)

pliegues <- vfold_cv(entrenamiento, v = 5)

# --- Receta (≈ ColumnTransformer + Pipeline) -------------------------------
receta_v <- recipe(precio_mm ~ ., data = entrenamiento) |>
  step_impute_median(all_numeric_predictors()) |>
  step_impute_mode(all_nominal_predictors()) |>
  step_novel(all_nominal_predictors()) |>
  step_dummy(all_nominal_predictors()) |>
  step_zv(all_predictors()) |>
  step_normalize(all_numeric_predictors())

# --- Modelo base -----------------------------------------------------------
base_v <- null_model() |>
  set_engine("parsnip") |>
  set_mode("regression")

flujo_base <- workflow() |>
  add_recipe(receta_v) |>
  add_model(base_v)

# --- Regresión lineal ------------------------------------------------------
lineal <- linear_reg() |> set_engine("lm")

flujo_lineal <- workflow() |>
  add_recipe(receta_v) |>
  add_model(lineal)

metricas_reg <- metric_set(rmse, mae, rsq)

res_lineal <- fit_resamples(flujo_lineal, resamples = pliegues,
                            metrics = metricas_reg)
collect_metrics(res_lineal)

# --- Ridge (mixture = 0) y Lasso (mixture = 1) -----------------------------
ridge <- linear_reg(penalty = tune(), mixture = 0) |> set_engine("glmnet")
lasso <- linear_reg(penalty = tune(), mixture = 1) |> set_engine("glmnet")

rejilla <- grid_regular(penalty(range = c(-2, 4)), levels = 40)

flujo_ridge <- workflow() |> add_recipe(receta_v) |> add_model(ridge)

ajuste_ridge <- tune_grid(flujo_ridge, resamples = pliegues,
                          grid = rejilla, metrics = metricas_reg)

autoplot(ajuste_ridge)
mejor_ridge <- select_best(ajuste_ridge, metric = "rmse")

# --- Ajuste final y evaluación en prueba (UNA sola vez) --------------------
final_ridge <- finalize_workflow(flujo_ridge, mejor_ridge) |>
  last_fit(particion_v, metrics = metricas_reg)

collect_metrics(final_ridge)

# --- Diagnóstico de supuestos (con lm directo) -----------------------------
modelo_lm <- lm(precio_mm ~ area_m2 + n_cuartos + n_banos + n_garajes,
                data = entrenamiento)

summary(modelo_lm)

par(mfrow = c(2, 2)); plot(modelo_lm); par(mfrow = c(1, 1))

car::vif(modelo_lm)          # multicolinealidad
lmtest::bptest(modelo_lm)    # Breusch-Pagan (homocedasticidad)
cooks.distance(modelo_lm)    # observaciones influyentes


# ───────────────────────────────────────────────────────────────────────────
# PARTE 2 · CLASIFICACIÓN — ausentismo laboral  (Cuadernillos 4 y 5)
# ───────────────────────────────────────────────────────────────────────────

ausentismo <- read_csv("datos/crudos/ausentismo_laboral.csv")

eventos <- ausentismo |>
  filter(horas_ausencia > 0) |>
  mutate(
    # El nivel de interés va PRIMERO para que yardstick lo tome como evento.
    ausencia_prolongada = factor(if_else(horas_ausencia > 8, "si", "no"),
                                 levels = c("si", "no")),
    motivo     = factor(motivo_cod),
    dia_semana = factor(dia_semana),
    estacion   = factor(estacion),
    educacion  = factor(educacion)
  ) |>
  select(ausencia_prolongada, motivo, dia_semana, estacion, educacion,
         gasto_transporte, distancia_km, antiguedad_anios, edad,
         carga_trabajo_dia, cumplimiento_meta, n_hijos, n_mascotas,
         id_empleado)

# --- Partición estratificada ----------------------------------------------
particion_a <- initial_split(eventos, prop = 0.70,
                             strata = ausencia_prolongada)
entren_a <- training(particion_a)
prueba_a <- testing(particion_a)

# --- Receta ---------------------------------------------------------------
receta_a <- recipe(ausencia_prolongada ~ ., data = entren_a) |>
  update_role(id_empleado, new_role = "id") |>   # identificador, no predictor
  step_other(motivo, threshold = 0.03) |>        # agrupa motivos raros
  step_impute_median(all_numeric_predictors()) |>
  step_novel(all_nominal_predictors()) |>
  step_dummy(all_nominal_predictors()) |>
  step_zv(all_predictors()) |>
  step_normalize(all_numeric_predictors())

# --- Modelos --------------------------------------------------------------
logistica <- logistic_reg() |> set_engine("glm")

bosque <- rand_forest(trees = 500, min_n = 2) |>
  set_engine("ranger", importance = "permutation") |>
  set_mode("classification")

vecinos <- nearest_neighbor(neighbors = 15) |>
  set_engine("kknn") |>
  set_mode("classification")

metricas_clas <- metric_set(roc_auc, accuracy, sens, spec, precision, f_meas)

# --- Validación cruzada AGRUPADA por empleado (Cuadernillo 5) -------------
# Equivale a StratifiedGroupKFold en scikit-learn.
pliegues_grupo <- group_vfold_cv(entren_a, group = id_empleado, v = 5)

flujo_log <- workflow() |> add_recipe(receta_a) |> add_model(logistica)

res_log <- fit_resamples(flujo_log, resamples = pliegues_grupo,
                         metrics = metricas_clas,
                         control = control_resamples(save_pred = TRUE))

collect_metrics(res_log)

# --- Curva ROC ------------------------------------------------------------
ajuste_log   <- fit(flujo_log, data = entren_a)
predicciones <- augment(ajuste_log, prueba_a)

conf_mat(predicciones, truth = ausencia_prolongada, estimate = .pred_class)

roc_auc(predicciones, truth = ausencia_prolongada, .pred_si)

roc_curve(predicciones, truth = ausencia_prolongada, .pred_si) |>
  autoplot()

pr_curve(predicciones, truth = ausencia_prolongada, .pred_si) |>
  autoplot()

# --- Umbral distinto de 0,5 (Cuadernillo 4) -------------------------------
# El paquete probably permite mover el punto de corte.
library(probably)

predicciones |>
  mutate(.pred_umbral = make_two_class_pred(
    .pred_si, levels(ausencia_prolongada), threshold = 0.15)) |>
  conf_mat(truth = ausencia_prolongada, estimate = .pred_umbral)

# Barrido de umbrales
predicciones |>
  threshold_perf(truth = ausencia_prolongada, estimate = .pred_si,
                 thresholds = seq(0.05, 0.95, by = 0.05)) |>
  filter(.metric %in% c("sens", "spec", "j_index"))

# --- Importancia de variables ---------------------------------------------
library(vip)

workflow() |>
  add_recipe(receta_a) |>
  add_model(bosque) |>
  fit(data = entren_a) |>
  extract_fit_parsnip() |>
  vip(num_features = 15)

# --- Calibración ----------------------------------------------------------
cal_plot_breaks(predicciones, truth = ausencia_prolongada,
                estimate = .pred_si)


# ───────────────────────────────────────────────────────────────────────────
# NOTAS
# ───────────────────────────────────────────────────────────────────────────
#
# 1. event_level: yardstick toma como evento el PRIMER nivel del factor.
#    Por eso arriba se define levels = c("si", "no"). Si se usa el orden
#    inverso, hay que pasar event_level = "second" a cada métrica.
#
# 2. En glmnet, `mixture` es la mezcla L1/L2 (0 = Ridge, 1 = Lasso) y
#    `penalty` es la fuerza. En scikit-learn, `alpha` es la fuerza y
#    `l1_ratio` es la mezcla. Los nombres no se corresponden.
#
# 3. last_fit() ajusta con todo el entrenamiento y evalúa en prueba una sola
#    vez. Es la forma correcta de cerrar el flujo: no se debe usar antes de
#    haber elegido el modelo final.
#
# 4. group_vfold_cv() es el equivalente de GroupKFold. En datos con varias
#    filas por individuo, es obligatorio: ver Cuadernillo 5.

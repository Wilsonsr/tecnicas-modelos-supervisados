# Técnicas de Análisis Estadístico de Modelos Supervisados

Sitio docente del espacio académico, construido con [Quarto](https://quarto.org)
y publicado con GitHub Pages.

**Sitio:** <https://wilsonsr.github.io/tecnicas-modelos-supervisados/>

---

## Qué es esto

Material de apoyo a los cinco encuentros virtuales del curso y de consulta
posterior. **No reemplaza** las actividades institucionales del aula virtual: las
prepara.

Siete cuadernillos siguen la misma secuencia —problema → datos → exploración →
pregunta → modelo → evaluación → interpretación → decisión— sobre dos conjuntos
de datos que recorren todo el semestre.

| Cuadernillo | Encuentro | Semana | Unidad |
|---|---|---|---|
| 0 · Cómo usar este repositorio | — | Previa | Transversal |
| 1 · Pensar estadísticamente un problema predictivo | Virtual 1 | 1 | 1 |
| 2 · Antes de modelar: conocer y preparar los datos | Virtual 2 | 2 | 1 |
| 3 · De explicar a predecir: modelos de regresión | Virtual 3 | 4 | 2 |
| 4 · Clasificar para tomar decisiones | Virtual 4 | 5 | 2 |
| 5 · ¿Podemos confiar en nuestro modelo? | Virtual 5 | 7 | 3 |
| 6 · Proyecto integrador | — | 1–9 | Transversal |

## Los datos del curso

| | Regresión | Clasificación |
|---|---|---|
| **Archivo** | `datos/crudos/vivienda_bogota.csv` | `datos/crudos/ausentismo_laboral.csv` |
| **Pregunta** | ¿Cuánto vale un inmueble residencial en Bogotá? | ¿Esta ausencia laboral será prolongada? |
| **Observaciones** | 10 000 inmuebles | 740 eventos · 36 empleados |
| **Particularidad** | Datos reales sin depurar: obliga a limpiar antes de modelar | 9 % de casos positivos: obliga a mirar más allá del *accuracy* |

Ambos se entregan **crudos**, con sus problemas de origen. Limpiarlos es parte
del trabajo (Cuadernillo 2). El archivo `datos/procesados/vivienda_modelado.csv`
lo genera ese cuadernillo al ejecutarse.

## Estructura

```
tecnicas-modelos-supervisados/
├── _quarto.yml              # configuración del sitio
├── index.qmd                # página inicial
├── requirements.txt         # entorno de Python
│
├── 00-inicio/               # Cuadernillo 0, instalación, datos del curso
├── 01-fundamentos/          # Cuadernillo 1
├── 02-preprocesamiento/     # Cuadernillo 2
├── 03-regresion/            # Cuadernillo 3
├── 04-clasificacion/        # Cuadernillo 4
├── 05-validacion/           # Cuadernillo 5
├── 06-proyecto/             # Cuadernillo 6
│
├── recursos/                # mapa curricular, errores frecuentes, glosario,
│                            # equivalencias R↔Python, uso de IA
├── referencias/             # bibliografía y referencias.bib
│
├── datos/
│   ├── crudos/              # los dos datasets, sin depurar
│   └── procesados/          # generados por el Cuadernillo 2
├── codigo/                  # utilidades y equivalencias en R
├── estilos/                 # tema SCSS y CSS de componentes
├── imagenes/
└── .github/workflows/       # publicación automática
```

## Trabajar con el repositorio

### Requisitos

- [Quarto](https://quarto.org/docs/get-started/) 1.4 o superior
- Python 3.10 o superior

### Puesta en marcha

```bash
git clone https://github.com/Wilsonsr/tecnicas-modelos-supervisados.git
cd tecnicas-modelos-supervisados

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

quarto preview                   # vista previa con recarga automática
quarto render                    # construir el sitio completo en _site/
```

### Renderizar un solo cuadernillo

```bash
quarto render 03-regresion/cuadernillo-03.qmd
```

### Publicar

El sitio se publica automáticamente en GitHub Pages con cada `push` a `main`,
mediante el flujo de trabajo `.github/workflows/publicar.yml`.

Para activarlo la primera vez: **Settings → Pages → Source: GitHub Actions**.

## Convenciones del material

- **Semilla fija** (`SEMILLA = 42`) en toda función que use azar.
- **Rutas relativas**; nunca rutas absolutas.
- **Todo el preprocesamiento dentro de un `Pipeline`**, sin excepción.
- **Modelo base obligatorio** en toda tabla de resultados.
- Cada cuadernillo cierra con: lo que debes recordar · errores frecuentes ·
  conexión con la actividad institucional · recursos adicionales.

## Ruta de lenguaje

Python (`pandas` + `scikit-learn`) es la ruta principal. En los puntos donde la
decisión metodológica es la misma pero la sintaxis cambia, se incluye la
equivalencia en R con `tidymodels`, en pestañas. La tabla completa está en
`recursos/equivalencias-r-python.qmd`.

Los bloques de R son material de referencia y no se ejecutan al construir el
sitio.

## Créditos y licencia

Material docente de **Wilson Sandoval Rodríguez**.

El conjunto *Absenteeism at work* procede del UCI Machine Learning Repository
(Martiniano, Ferreira, Sassi y Affonso, 2012); los nombres de sus variables
fueron traducidos al español, sin modificar el contenido.

Contenido bajo licencia
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es).
Código de ejemplo bajo licencia MIT.

---

Este repositorio sucede a
[Metodos-Estadisticos](https://github.com/Wilsonsr/Metodos-Estadisticos), del
cual reutiliza material seleccionado. Aquel repositorio no se modifica y
permanece como archivo.

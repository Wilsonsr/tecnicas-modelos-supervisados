#!/usr/bin/env python3
"""
Genera los cuadernos Jupyter (.ipynb) a partir de los cuadernillos .qmd.

Los .qmd son la fuente de verdad: el sitio web y los cuadernos salen de ellos,
así que nunca se desincronizan. Este script se ejecuta automáticamente al
publicar (ver .github/workflows/publicar.yml) y también se puede correr a mano:

    python codigo/generar_cuadernos.py

Qué hace, además de llamar a `quarto convert`:

1.  Sustituye el encabezado YAML por una portada legible con enlace a la
    versión web del cuadernillo.
2.  Inserta una celda de arranque que descarga los datos si no están, de modo
    que el cuaderno funcione igual en Google Colab que en el repositorio
    clonado.
3.  Traduce a Markdown corriente los elementos propios de Quarto que en Jupyter
    aparecerían como texto crudo: callouts (`::: {.callout-note}`), pestañas,
    rejillas, y los bloques HTML de las microactividades y las fichas.
4.  Limpia los comentarios de configuración de celda (`#| label:` y demás).

Requiere Quarto en el PATH. No requiere ninguna librería externa.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "cuadernos"

BASE_URL = ("https://raw.githubusercontent.com/Wilsonsr/"
            "tecnicas-modelos-supervisados/main/")
SITIO_URL = "https://wilsonsr.github.io/tecnicas-modelos-supervisados/"

# (ruta del .qmd, nombre del .ipynb, ruta de la página en el sitio)
CUADERNILLOS = [
    ("00-inicio/como-usar.qmd",                 "cuadernillo-00-como-usar.ipynb",      "00-inicio/como-usar.html"),
    ("00-inicio/datos-del-curso.qmd",           "cuadernillo-00-datos.ipynb",          "00-inicio/datos-del-curso.html"),
    ("01-fundamentos/cuadernillo-01.qmd",       "cuadernillo-01-fundamentos.ipynb",    "01-fundamentos/cuadernillo-01.html"),
    ("02-preprocesamiento/cuadernillo-02.qmd",  "cuadernillo-02-preparacion.ipynb",    "02-preprocesamiento/cuadernillo-02.html"),
    ("03-regresion/cuadernillo-03.qmd",         "cuadernillo-03-regresion.ipynb",      "03-regresion/cuadernillo-03.html"),
    ("04-clasificacion/cuadernillo-04.qmd",     "cuadernillo-04-clasificacion.ipynb",  "04-clasificacion/cuadernillo-04.html"),
    ("05-validacion/cuadernillo-05.qmd",        "cuadernillo-05-validacion.ipynb",     "05-validacion/cuadernillo-05.html"),
]

DATOS = [
    "datos/crudos/vivienda_bogota.csv",
    "datos/crudos/ausentismo_laboral.csv",
    "datos/procesados/vivienda_modelado.csv",
]

NOMBRES_CALLOUT = {
    "note": "NOTA", "tip": "SUGERENCIA", "important": "IMPORTANTE",
    "warning": "ADVERTENCIA", "caution": "ATENCIÓN",
}


# ── Conversión de HTML a Markdown ────────────────────────────────────────────

def html_a_markdown(fragmento: str) -> str:
    """Traduce a Markdown el HTML que usan las microactividades y las fichas."""
    t = fragmento

    # Listas. Las numeradas conservan su numeración: varias microactividades
    # se refieren a sus elementos por número ("la pregunta 4").
    def numerar(m):
        elementos = re.findall(r"<li>(.*?)</li>", m.group(1), flags=re.S)
        return "\n" + "\n".join(f"{i}. {e.strip()}"
                                for i, e in enumerate(elementos, 1)) + "\n"

    t = re.sub(r"<ol>(.*?)</ol>", numerar, t, flags=re.S)
    t = re.sub(r"<li>(.*?)</li>", r"\n- \1", t, flags=re.S)
    t = re.sub(r"</?(ol|ul)>", "\n", t)

    # Énfasis y código.
    t = re.sub(r"<(b|strong)>(.*?)</\1>", r"**\2**", t, flags=re.S)
    t = re.sub(r"<(i|em)>(.*?)</\1>", r"*\2*", t, flags=re.S)
    t = re.sub(r"<code>(.*?)</code>", r"`\1`", t, flags=re.S)

    # Párrafos y citas.
    t = re.sub(r"<blockquote>(.*?)</blockquote>", r"\n> \1\n", t, flags=re.S)
    t = re.sub(r"</p>", "\n\n", t)
    t = re.sub(r"<p>", "", t)
    t = re.sub(r"<br\s*/?>", "\n", t)

    # Lo que quede de etiquetas se descarta.
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def convertir_microactividad(bloque: str) -> str:
    """Un <div class="micro ..."> pasa a un recuadro de Markdown."""
    tipo = re.search(r'<span class="tipo">(.*?)</span>', bloque, re.S)
    titulo = re.search(r'<span class="titulo">(.*?)</span>', bloque, re.S)
    tiempo = re.search(r'<span class="tiempo">(.*?)</span>', bloque, re.S)

    cuerpo = re.sub(r'<div class="micro-cab">.*?</div>', "", bloque, flags=re.S)
    cuerpo = html_a_markdown(cuerpo)

    encabezado = f"**{tipo.group(1).strip().upper()}"
    if titulo:
        encabezado += f" · {titulo.group(1).strip()}"
    encabezado += "**"
    if tiempo:
        encabezado += f"  ·  *{tiempo.group(1).strip()}*"

    return f"---\n\n{encabezado}\n\n{cuerpo}\n\n---"


def convertir_ficha(bloque: str) -> str:
    """La ficha de portada pasa a una lista de metadatos."""
    lineas = []
    for et, vl in re.findall(
            r'<span class="et">(.*?)</span><span class="vl">(.*?)</span>',
            bloque, re.S):
        lineas.append(f"- **{html_a_markdown(et)}:** {html_a_markdown(vl)}")

    previos = re.search(r'<div class="previos">(.*?)</div>', bloque, re.S)
    texto = "\n".join(lineas)
    if previos:
        texto += "\n\n" + html_a_markdown(previos.group(1))
    return texto


def convertir_recordar(bloque: str) -> str:
    return html_a_markdown(bloque)


def procesar_bloques_html(texto: str) -> str:
    """Sustituye cada bloque ```{=html} por su equivalente en Markdown."""
    def reemplazo(m):
        contenido = m.group(1)
        if 'class="acciones"' in contenido:
            return ""   # la barra de descarga no tiene sentido dentro del cuaderno
        if 'class="micro' in contenido:
            partes = re.findall(r'<div class="micro [^"]*">.*?</div>\s*</div>|'
                                r'<div class="micro [^"]*">.*?(?=<div class="micro |\Z)',
                                contenido, re.S)
            if partes:
                return "\n\n".join(convertir_microactividad(p) for p in partes)
            return convertir_microactividad(contenido)
        if 'class="ficha"' in contenido:
            return convertir_ficha(contenido)
        if 'class="recordar"' in contenido:
            return convertir_recordar(contenido)
        if 'class="ruta"' in contenido or 'class="tarjetas"' in contenido:
            return html_a_markdown(contenido)
        return html_a_markdown(contenido)

    return re.sub(r"```\{=html\}\n(.*?)\n```", reemplazo, texto, flags=re.S)


# ── Conversión de la sintaxis propia de Quarto ───────────────────────────────

def procesar_divs_quarto(texto: str) -> str:
    """Callouts, pestañas y rejillas pasan a Markdown corriente."""
    lineas = texto.split("\n")
    salida, pila = [], []

    for linea in lineas:
        abre = re.match(r"^:::+\s*\{([^}]*)\}\s*$", linea)
        cierra = re.match(r"^:::+\s*$", linea)

        if abre:
            atributos = abre.group(1)
            callout = re.search(r"\.callout-(\w+)", atributos)
            if callout:
                etiqueta = NOMBRES_CALLOUT.get(callout.group(1), callout.group(1).upper())
                salida.append(f"> **{etiqueta}**")
                pila.append("callout")
            elif ".panel-tabset" in atributos or ".grid" in atributos \
                    or ".g-col" in atributos or ".column" in atributos:
                pila.append("mudo")
            else:
                pila.append("mudo")
            continue

        if cierra and pila:
            if pila.pop() == "callout":
                salida.append("")
            continue

        if pila and pila[-1] == "callout":
            if not linea.strip():
                salida.append(">")
                continue
            # Un encabezado dentro de un callout sería un H2 dentro de una
            # cita: queda desproporcionado en Jupyter. Pasa a negrita.
            titulo = re.match(r"^#{1,6}\s+(.*)$", linea)
            salida.append(f"> **{titulo.group(1)}**" if titulo else f"> {linea}")
        else:
            salida.append(linea)

    return "\n".join(salida)


def limpiar_markdown(texto: str) -> str:
    texto = procesar_bloques_html(texto)
    texto = procesar_divs_quarto(texto)

    # Expresiones inline de Quarto: el sitio las evalúa al renderizar, pero en
    # un cuaderno no hay dónde hacerlo. Se muestran como código, que además
    # deja ver al estudiante de dónde sale cada cifra del texto.
    def expresion(m):
        codigo = m.group(1).strip()
        codigo = re.sub(r'^f"|"$', "", codigo)
        codigo = re.sub(r'\.replace\(["\']\.["\'],\s*["\'],["\']\)$', "", codigo)
        return f"`{codigo}`"

    texto = re.sub(r"`\{python\}\s*([^`]*)`", expresion, texto)

    # Atributos de tabla y de figura.
    texto = re.sub(r"^:\s*(.+?)\s*\{[^}]*\}\s*$", r"*\1*", texto, flags=re.M)
    texto = re.sub(r"\{\.[^}]*\}", "", texto)

    # Enlaces internos del sitio: se apuntan a la versión publicada.
    texto = re.sub(r"\]\(\.\./([\w\-/]+)\.qmd\)", rf"]({SITIO_URL}\1.html)", texto)
    texto = re.sub(r"\]\(([\w\-]+)\.qmd\)", rf"]({SITIO_URL}\1.html)", texto)
    texto = re.sub(r"\]\(\.\./([\w\-/]+)\.html\)", rf"]({SITIO_URL}\1.html)", texto)

    # Citas bibliográficas.
    texto = re.sub(r"\[@([\w\-]+)(?:;\s*@[\w\-]+)*\]", r"(\1)", texto)
    texto = re.sub(r"(?<![\w`])@([\w\-]+\d{4}\w?)", r"\1", texto)

    texto = re.sub(r"\n{4,}", "\n\n\n", texto)
    return texto.strip()


def limpiar_codigo(texto: str) -> str:
    lineas = []
    for linea in texto.split("\n"):
        if re.match(r"^#\|\s*(label|code-summary|echo|include|warning|message|"
                    r"code-fold|output|fig-align|fig-width|fig-height)\s*:", linea):
            continue
        cap = re.match(r"^#\|\s*fig-cap\s*:\s*[\"']?(.*?)[\"']?\s*$", linea)
        if cap:
            lineas.append(f"# Figura: {cap.group(1)}")
            continue
        if linea.startswith("#|"):
            continue
        lineas.append(linea)
    return "\n".join(lineas).strip()


# ── Celdas que se añaden al cuaderno ─────────────────────────────────────────

def celda_portada(titulo: str, subtitulo: str, url_pagina: str) -> dict:
    fuente = [
        f"# {titulo}\n",
        "\n",
    ]
    if subtitulo:
        fuente += [f"*{subtitulo}*\n", "\n"]
    fuente += [
        "---\n",
        "\n",
        "**Técnicas de Análisis Estadístico de Modelos Supervisados**\n",
        "\n",
        f"Este cuaderno se genera automáticamente a partir del cuadernillo del sitio "
        f"del curso. La versión web, con los gráficos interactivos y el formato "
        f"completo, está en [{url_pagina}]({url_pagina}).\n",
        "\n",
        "Ejecuta las celdas en orden, de principio a fin. Si te saltas alguna, "
        "las siguientes fallarán: es la misma disciplina que se exige en las "
        "actividades del curso.\n",
    ]
    return {"cell_type": "markdown", "metadata": {}, "source": fuente}


def celda_arranque() -> dict:
    archivos = ",\n        ".join(f'"{d}"' for d in DATOS)
    codigo = f'''# Celda añadida automáticamente al generar este cuaderno.
# Descarga los datos del curso si no están disponibles, de modo que el cuaderno
# funcione igual en Google Colab que en el repositorio clonado. Si ya tienes el
# repositorio, no descarga nada.

import os
import urllib.request

BASE_URL = "{BASE_URL}"
ARCHIVOS = [
        {archivos},
]

if not os.path.exists("../datos/crudos/vivienda_bogota.csv"):
    # Sin repositorio: se crea la estructura y se descargan los datos.
    os.makedirs("curso/cuadernos", exist_ok=True)
    os.chdir("curso/cuadernos")
    for archivo in ARCHIVOS:
        destino = os.path.join("..", archivo)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        if not os.path.exists(destino):
            urllib.request.urlretrieve(BASE_URL + archivo, destino)
    print("Datos del curso descargados.")
else:
    print("Datos del curso encontrados en el repositorio.")
'''
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": codigo.splitlines(keepends=True),
    }


# ── Proceso principal ────────────────────────────────────────────────────────

def extraer_titulo(ruta_qmd: Path) -> tuple[str, str]:
    texto = ruta_qmd.read_text(encoding="utf-8")
    m = re.search(r"^---\n(.*?)\n---", texto, re.S)
    if not m:
        return ruta_qmd.stem, ""
    cabecera = m.group(1)
    t = re.search(r'^title:\s*"(.*?)"\s*$', cabecera, re.M)
    s = re.search(r'^subtitle:\s*"(.*?)"\s*$', cabecera, re.M)
    return (t.group(1) if t else ruta_qmd.stem), (s.group(1) if s else "")


def generar(qmd: str, salida: str, pagina: str) -> None:
    ruta_qmd = RAIZ / qmd
    ruta_ipynb = DESTINO / salida

    subprocess.run(
        ["quarto", "convert", str(ruta_qmd), "--output", str(ruta_ipynb)],
        check=True, capture_output=True, text=True)

    nb = json.loads(ruta_ipynb.read_text(encoding="utf-8"))
    titulo, subtitulo = extraer_titulo(ruta_qmd)

    celdas = []
    for i, celda in enumerate(nb["cells"]):
        fuente = "".join(celda["source"])

        # La primera celda es el encabezado YAML: se reemplaza por la portada.
        if i == 0 and fuente.lstrip().startswith("---"):
            continue

        if celda["cell_type"] == "markdown":
            limpio = limpiar_markdown(fuente)
            if not limpio:
                continue
            celda["source"] = [l + "\n" for l in limpio.split("\n")]
        else:
            limpio = limpiar_codigo(fuente)
            if not limpio:
                continue
            celda["source"] = [l + "\n" for l in limpio.split("\n")]
            celda["outputs"] = []
            celda["execution_count"] = None

        celdas.append(celda)

    nb["cells"] = [celda_portada(titulo, subtitulo, SITIO_URL + pagina),
                   celda_arranque()] + celdas

    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3", "language": "python", "name": "python3"}
    nb["metadata"]["language_info"] = {"name": "python"}

    ruta_ipynb.write_text(
        json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    n_cod = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
    print(f"  {salida:<38} {len(nb['cells']):>3} celdas ({n_cod} de código)")


def main() -> int:
    if shutil.which("quarto") is None:
        print("ERROR: no se encontró 'quarto' en el PATH.", file=sys.stderr)
        return 1

    DESTINO.mkdir(exist_ok=True)
    print(f"Generando cuadernos en {DESTINO.relative_to(RAIZ)}/\n")
    for qmd, salida, pagina in CUADERNILLOS:
        if not (RAIZ / qmd).exists():
            print(f"  AVISO: no existe {qmd}, se omite.", file=sys.stderr)
            continue
        generar(qmd, salida, pagina)
    print(f"\n{len(CUADERNILLOS)} cuadernos generados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

import sys
import json
from PIL import Image
import math

def mostrar_ayuda():
    ayuda = """
🛠️  MODO DE EMPLEO - ELLEN FULL FIXER 🛠️

Este script repara la transparencia de Ellen en Harvest Moon 64, parcheando 
simultáneamente la textura (.ci), la paleta binaria (.pal) y el índice (.json).

Uso:
  python3 ellen_full_fixer.py <ci_ref> <png_ref> <png_edit> <ci_out> <pal_bin> <pal_json>

Argumentos:
  1. ci_ref:   Archivo .ci original (ej. 000_sit.ci) para aprender índices.
  2. png_ref:  Imagen original (ej. 000_sit.png) para aprender colores.
  3. png_edit: Tu nueva imagen editada (002.png).
  4. ci_out:   Nombre del archivo de salida (002.ci).
  5. pal_bin:  Ruta al archivo 00.pal del juego.
  6. pal_json: Ruta al archivo 00.json del juego.

Ejemplo listo para usar:
  python3 tools/modding/sprites/ellen_full_fixer.py \\
  assets/sprites/entitySprites/npc/Ellen/textures/000_sit.ci \\
  assets/sprites/entitySprites/npc/Ellen/textures/000_sit.png \\
  assets/sprites/entitySprites/npc/Ellen/textures/002.png \\
  assets/sprites/entitySprites/npc/Ellen/textures/002.ci \\
  assets/sprites/entitySprites/npc/Ellen/textures/00.pal \\
  assets/sprites/entitySprites/npc/Ellen/textures/00.json
    """
    print(ayuda)

def distancia_color(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def corregir_paleta_binaria(pal_path):
    try:
        with open(pal_path, "rb") as f:
            data = bytearray(f.read())
        data[0] = 0x00
        data[1] = 0x00
        with open(pal_path, "wb") as f:
            f.write(data)
        print(f"✔️  Binario {pal_path} corregido (Color 0 = Transparente).")
    except Exception as e:
        print(f"⚠️  Error parcheando .pal: {e}")

def corregir_paleta_json(json_path):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        if "colors" in data and len(data["colors"]) > 0:
            data["colors"][0]["alpha"] = 0
            data["colors"][0]["rgba"][3] = 0
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✔️  JSON {json_path} corregido (Alpha 0 en Index 0).")
    except Exception as e:
        print(f"⚠️  Error parcheando JSON: {e}")

def crear_diccionario_paleta(png_ref, ci_ref):
    img_ref = Image.open(png_ref).convert("RGB")
    pix_ref = list(img_ref.getdata())
    with open(ci_ref, "rb") as f:
        idx_ref = list(f.read())
    
    diccionario = {}
    for i in range(min(len(pix_ref), len(idx_ref))):
        color = pix_ref[i]
        indice = idx_ref[i]
        if indice != 0x00 and color not in diccionario:
            diccionario[color] = indice
    return diccionario

def procesar(ci_ref, png_ref, png_edit, ci_out, pal_bin, pal_json):
    corregir_paleta_binaria(pal_bin)
    corregir_paleta_json(pal_json)

    print("🎨 Aprendiendo paleta...")
    paleta = crear_diccionario_paleta(png_ref, ci_ref)
    colores_conocidos = list(paleta.keys())

    img_edit = Image.open(png_edit).convert("RGBA")
    pix_edit = list(img_edit.getdata())
    color_fondo_png = pix_edit[0][:3]
    
    nuevo_ci = bytearray()
    print(f"🛠️  Generando {ci_out}...")
    for p in pix_edit:
        rgb = p[:3]
        alpha = p[3]

        if alpha < 128 or rgb == color_fondo_png:
            nuevo_ci.append(0x00)
        elif rgb in paleta:
            nuevo_ci.append(paleta[rgb])
        else:
            mas_cercano = min(colores_conocidos, key=lambda c: distancia_color(rgb, c))
            nuevo_ci.append(paleta[mas_cercano])

    with open(ci_out, "wb") as f:
        f.write(nuevo_ci)
    print(f"✅ Proceso completado.")

if __name__ == "__main__":
    if len(sys.argv) == 1 or "--help" in sys.argv:
        mostrar_ayuda()
    elif len(sys.argv) < 7:
        print("❌ Error: Faltan argumentos. Usa --help para ver el manual.")
    else:
        procesar(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
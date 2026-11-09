import sys
import os
from PIL import Image

def procesar_todo(target_name, reference_name):
    # Definimos rutas basadas en el nombre (ej. 000)
    target_png = f"{target_name}.png"
    target_ci = f"{target_name}.ci"
    ref_png = f"{reference_name}.png"
    
    try:
        if not os.path.exists(ref_png):
            print(f"Error: No se encuentra la referencia {ref_png}")
            return

        # 1. Cargar referencia para obtener la PALETA real
        ref_img = Image.open(ref_png).convert("P")
        paleta_original = ref_img.getpalette()

        # 2. Cargar tu imagen y convertirla a la paleta de la referencia
        nueva_img = Image.open(target_png).convert("RGBA")
        
        # Crear imagen temporal indexada
        img_temp = Image.new("P", nueva_img.size)
        img_temp.putpalette(paleta_original)

        pixeles = nueva_img.getdata()
        indices_finales = []

        for p in pixeles:
            # Si es transparente o muy blanco/claro -> Indice 0 (Transparente)
            if p[3] < 128 or (p[0] > 240 and p[1] > 240 and p[2] > 240):
                indices_finales.append(0)
            else:
                # Buscar color más cercano en la paleta, evitando el 0
                temp_rgb = Image.new("RGB", (1,1), (p[0], p[1], p[2]))
                idx = temp_rgb.quantize(palette=ref_img).getdata()[0]
                indices_finales.append(idx if idx != 0 else 1)

        # 3. Guardar el PNG corregido (por si el make lo usa luego)
        img_temp.putdata(indices_finales)
        img_temp.save(target_png, transparency=0)
        
        # 4. GENERAR EL ARCHIVO .CI (Binario puro)
        # Cada pixel es exactamente un byte con su indice
        with open(target_ci, "wb") as f:
            f.write(bytearray(indices_finales))

        print(f"✅ Éxito total:")
        print(f"   - {target_png}: Actualizado e indexado.")
        print(f"   - {target_ci}: Generado manualmente ({len(indices_finales)} bytes).")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    # Uso: python3 script.py 000 000_sit
    if len(sys.argv) < 3:
        print("Uso: python3 script.py nombre_objetivo nombre_referencia (sin extensiones)")
    else:
        procesar_todo(sys.argv[1], sys.argv[2])
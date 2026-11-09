from PIL import Image

# Ruta de tus archivos
path_000 = "assets/sprites/entitySprites/npc/Ellen/Textures/000.png"
path_ref = "assets/sprites/entitySprites/npc/Ellen/Textures/000_sit.png"

# 1. Abrir tu imagen actual y la de referencia (que tiene la paleta buena)
img = Image.open(path_000).convert("RGBA")
ref = Image.open(path_ref).convert("P")

# 2. Crear una nueva imagen paletizada
# Todo lo que sea blanco puro (255,255,255) lo mandaremos al índice 0
new_img = Image.new("P", img.size)
new_img.putpalette(ref.getpalette())

pixels = img.getdata()
new_pixels = []

for p in pixels:
    # Si el pixel es blanco o transparente, índice 0
    if (p[0] > 240 and p[1] > 240 and p[2] > 240) or p[3] < 128:
        new_pixels.append(0)
    else:
        # Si no, buscamos el color más cercano en la paleta de referencia
        # Convertimos el pixel a una imagen minúscula para usar quantize
        temp = Image.new("RGB", (1,1), (p[0], p[1], p[2]))
        p_idx = temp.quantize(palette=ref).getdata()[0]
        # Si el color mapeado es 0 pero no es el fondo, lo movemos al 1 
        # para que no se vuelva transparente por error
        new_pixels.append(p_idx if p_idx != 0 else 1)

new_img.putdata(new_pixels)
# 3. Guardar con el flag de transparencia en el índice 0
new_img.save(path_000, transparency=0)
print("¡Limpieza completada! El fondo ahora es el índice 0 transparente.")
import sys
from PIL import Image

def reparar_png(path):
    # 1. Abrir la imagen original en RGBA para leer la transparencia
    img = Image.open(path).convert("RGBA")
    
    # 2. Crear una versión indexada (Modo P)
    # Esto genera automáticamente una paleta de 256 colores
    img_p = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    
    # 3. Guardar la imagen
    # Al guardarla así, PIL se encarga de que los metadatos sean Modo P real
    img_p.save(path)
    print(f"PNG Reparado: {path} ahora es Modo P (Indexado)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        reparar_png(sys.argv[1])
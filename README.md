# PixelForge MathEngine 2D - Grupo F

Programa de consola en Python para representar y transformar figuras mediante matrices de algebra lineal, sin NumPy.

## Funciones

- Jugador (cuadrado), enemigo (triangulo) y obstaculo (rectangulo).
- Traslacion, rotacion, escalamiento y reflexion respecto a los ejes X o Y.
- Vertices numerados en el grafico ASCII para comparar su posicion antes y despues.
- Transformaciones consecutivas, matrices, calculos, coordenadas y grafico ASCII.

## Ejecutar

Requiere Python 3.10 o posterior y no tiene dependencias externas.

```powershell
python main.py
```

Cada punto se representa como `[x, y]`. La rotacion, el escalamiento y la reflexion usan matrices 2x2. La traslacion se calcula sumando el vector `[dx, dy]`, ya que una matriz 2x2 no puede trasladar puntos. Los angulos positivos giran en sentido antihorario y las transformaciones se realizan respecto al origen.

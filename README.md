# PixelForge MathEngine 2D - Grupo F

Programa de consola en Python para representar y transformar figuras mediante matrices de algebra lineal, sin NumPy.

## Funciones

- Jugador (cuadrado), enemigo (triangulo) y obstaculo (rectangulo).
- Traslacion, rotacion, escalamiento uniforme y reflexion respecto a los ejes X o Y.
- Vertices numerados en el grafico ASCII para comparar su posicion antes y despues.
- Opcion para configurar y ejecutar varias transformaciones en secuencia.
- Matrices, calculos, coordenadas y grafico ASCII para cada paso.
- Comparacion grafica entre el estado inicial y el resultado final de la secuencia.

## Ejecutar

Requiere Python 3.10 o posterior y no tiene dependencias externas.

```powershell
python main.py
```

Cada punto se representa como `[x, y]`. La rotacion, el escalamiento y la reflexion usan matrices 2x2 y se aplican alrededor del centro actual de la figura. El escalamiento usa el mismo factor en X y Y para conservar la forma. La traslacion se calcula sumando el vector `[dx, dy]`.

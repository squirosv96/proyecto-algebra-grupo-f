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

## Matrices de transformacion

Un vertice se representa mediante el vector:

$$
p =
\begin{bmatrix}
x \\
y
\end{bmatrix}
$$

### Rotacion

Para rotar un angulo $\theta$ en sentido antihorario se utiliza:

$$
R(\theta) =
\begin{bmatrix}
\cos(\theta) & -\sin(\theta) \\
\sin(\theta) & \cos(\theta)
\end{bmatrix}
$$

Por ejemplo, para una rotacion de $90^\circ$:

$$
R(90^\circ) =
\begin{bmatrix}
0 & -1 \\
1 & 0
\end{bmatrix}
$$

### Escalamiento uniforme

El mismo factor $k$ se aplica en X y Y para cambiar el tamaño sin alterar las
proporciones:

$$
S(k) =
\begin{bmatrix}
k & 0 \\
0 & k
\end{bmatrix}
$$

- Si $k > 1$, la figura aumenta de tamaño.
- Si $0 < k < 1$, la figura se reduce.
- Si $k = 1$, la figura conserva su tamaño.
- El programa no permite $k = 0$.

### Reflexion

Reflexion respecto al eje X:

$$
F_x =
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
$$

Reflexion respecto al eje Y:

$$
F_y =
\begin{bmatrix}
-1 & 0 \\
0 & 1
\end{bmatrix}
$$

Como el programa aplica estas matrices respecto al centro de la figura, los
ejes de reflexion son lineas paralelas a X o Y que atraviesan dicho centro.

### Transformacion respecto al centro

El centro se calcula promediando las coordenadas de los $n$ vertices:

$$
c =
\frac{1}{n}
\sum_{i=1}^{n} p_i
$$

Para aplicar una matriz $M$ sin desplazar el centro se utiliza:

$$
p' = c + M(p-c)
$$

El procedimiento es:

1. Restar el centro: $p-c$.
2. Aplicar la matriz: $M(p-c)$.
3. Sumar nuevamente el centro: $c+M(p-c)$.

### Traslacion

La traslacion no puede representarse con una matriz 2x2. Se suma el vector de
desplazamiento:

$$
d =
\begin{bmatrix}
d_x \\
d_y
\end{bmatrix}
\qquad
p' = p+d
$$

## Ejemplo: rotacion del cuadrado

Para el cuadrado con vertices:

$$
P_1=(0,0),\quad P_2=(2,0),\quad P_3=(2,2),\quad P_4=(0,2)
$$

su centro es:

$$
c=(1,1)
$$

Al rotar $P_1=(0,0)$ un angulo de $90^\circ$ alrededor del centro:

$$
P_1-c =
\begin{bmatrix}
0 \\
0
\end{bmatrix}
-
\begin{bmatrix}
1 \\
1
\end{bmatrix}
=
\begin{bmatrix}
-1 \\
-1
\end{bmatrix}
$$

$$
R(90^\circ)(P_1-c) =
\begin{bmatrix}
0 & -1 \\
1 & 0
\end{bmatrix}
\begin{bmatrix}
-1 \\
-1
\end{bmatrix}
=
\begin{bmatrix}
1 \\
-1
\end{bmatrix}
$$

Finalmente se suma el centro:

$$
P_1' =
\begin{bmatrix}
1 \\
1
\end{bmatrix}
+
\begin{bmatrix}
1 \\
-1
\end{bmatrix}
=
\begin{bmatrix}
2 \\
0
\end{bmatrix}
$$

Despues de rotar todos los vertices:

$$
P_1'=(2,0),\quad P_2'=(2,2),\quad P_3'=(0,2),\quad P_4'=(0,0)
$$

El centro sigue siendo $(1,1)$; por eso la figura rota sin cambiar de posicion.

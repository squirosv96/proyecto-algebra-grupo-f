# PixelForge MathEngine 2D - Grupo F

Programa de consola en Python para representar y transformar figuras mediante matrices de álgebra lineal, sin NumPy.

## Funciones

- Jugador (cuadrado), enemigo (triángulo) y obstáculo (rectángulo).
- Traslación, rotación, escalamiento uniforme y reflexión respecto a los ejes X o Y.
- Vértices numerados en el gráfico ASCII para comparar su posición antes y después.
- Opción para configurar y ejecutar varias transformaciones en secuencia.
- Matrices, cálculos, coordenadas y gráfico ASCII para cada paso.
- Comparación gráfica entre el estado inicial y el resultado final de la secuencia.
- Análisis de independencia lineal, bases, dimensión y redundancia.
- Verificación de restricciones que pueden formar subespacios vectoriales.
- Historial de transformaciones, reinicio y cambio de figura.

## Ejecutar

Requiere Python 3.10 o posterior y no tiene dependencias externas.

```powershell
python main.py
```

Cada punto se representa como `[x, y]`. La rotación, el escalamiento y la reflexión usan matrices 2x2 y se aplican alrededor del centro actual de la figura. El escalamiento usa el mismo factor en X y Y para conservar la forma. La traslación se calcula sumando el vector `[dx, dy]`.

## Figuras disponibles

Al iniciar, el programa solicita una de estas figuras:

| Opción | Objeto | Figura | Vértices iniciales |
|---|---|---|---|
| 1 | Jugador | Cuadrado | $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$ |
| 2 | Enemigo | Triángulo | $(0,0)$, $(2,0)$, $(1,2)$ |
| 3 | Obstáculo | Rectángulo | $(0,0)$, $(4,0)$, $(4,2)$, $(0,2)$ |

Las coordenadas actuales cambian al aplicar transformaciones. Las coordenadas
iniciales se conservan para poder restablecer la figura.

## Guía del menú principal

```text
1. Aplicar una transformación
2. Aplicar secuencia de transformaciones
3. Analizar matemáticamente el escenario
4. Ver historial de transformaciones
5. Restablecer figura
6. Escoger otra figura
7. Salir
```

### 1. Aplicar una transformación

Permite escoger una sola operación:

```text
1. Trasladar
2. Rotar
3. Escalar
4. Reflejar
```

Después de aplicarla, el programa muestra:

- coordenadas anteriores;
- matriz 2x2 o vector utilizado;
- cálculo realizado para cada vértice;
- coordenadas resultantes;
- gráfico ASCII comparativo.

#### Operaciones con respecto al centro

La rotación, el escalamiento y la reflexión se aplican alrededor del centro
actual de la figura. Esto evita que la figura cambie de posición solamente
porque se está rotando, escalando o reflejando.

Para una figura con $n$ vértices, el centro se calcula promediando sus
coordenadas:

$$
c =
\frac{1}{n}
\sum_{i=1}^{n}P_i
$$

Después, cada vértice se transforma mediante:

$$
P_i'=c+M(P_i-c)
$$

donde $M$ es la matriz de rotación, escalamiento o reflexión. La operación se
divide en tres pasos:

1. Llevar el vértice al origen restando el centro:

   $$
   P_{\text{relativo}}=P_i-c
   $$

2. Aplicar la matriz a las coordenadas relativas:

   $$
   P_{\text{transformado}}=M P_{\text{relativo}}
   $$

3. Devolver el vértice a la posición del objeto:

   $$
   P_i'=P_{\text{transformado}}+c
   $$

Por ejemplo, para el cuadrado:

$$
P_1=(0,0),\quad P_2=(2,0),\quad P_3=(2,2),\quad P_4=(0,2)
$$

el centro es:

$$
c=
\left(
\frac{0+2+2+0}{4},
\frac{0+0+2+2}{4}
\right)
=(1,1)
$$

Antes de aplicar cualquier matriz, $P_1$ se expresa respecto al centro:

$$
P_1-c=(0,0)-(1,1)=(-1,-1)
$$

La matriz se aplica a $(-1,-1)$, no directamente a $(0,0)$. Finalmente, al
resultado se le suma $(1,1)$. El mismo procedimiento se repite para todos los
vértices usando el mismo centro.

La traslación es la excepción: no necesita calcular el centro porque suma el
mismo vector de desplazamiento a todos los vértices.

#### Ejemplo de traslación

Si se ingresa el desplazamiento:

$$
d=(3,-1)
$$

entonces:

$$
p'=p+d
$$

Para $P_1=(0,0)$:

$$
P_1'=(0,0)+(3,-1)=(3,-1)
$$

La traslación cambia la posición, pero no el tamaño ni la orientación de la
figura.

#### Ejemplo de rotación

Para rotar el cuadrado $90^\circ$ en sentido antihorario se utiliza:

$$
R(90^\circ)=
\begin{bmatrix}
0 & -1 \\
1 & 0
\end{bmatrix}
$$

Si $P_1=(0,0)$ y el centro es $c=(1,1)$:

$$
P_1'=c+R(90^\circ)(P_1-c)
$$

$$
P_1'=
\begin{bmatrix}
1 \\
1
\end{bmatrix}
+
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
2 \\
0
\end{bmatrix}
$$

Después de aplicar la misma operación a todos los vértices:

$$
P_1'=(2,0),\quad P_2'=(2,2),\quad P_3'=(0,2),\quad P_4'=(0,0)
$$

El centro permanece en $(1,1)$ y la figura cambia su orientación sin
desplazarse.

#### Ejemplo de escalamiento

Para reducir el cuadrado a la mitad sin mover su centro se utiliza $k=0.5$:

$$
S(0.5)=
\begin{bmatrix}
0.5 & 0 \\
0 & 0.5
\end{bmatrix}
$$

Si $P_1=(0,0)$ y el centro es $c=(1,1)$:

$$
P_1'=c+S(0.5)(P_1-c)
$$

$$
P_1'=
\begin{bmatrix}
1 \\
1
\end{bmatrix}
+
\begin{bmatrix}
0.5 & 0 \\
0 & 0.5
\end{bmatrix}
\begin{bmatrix}
-1 \\
-1
\end{bmatrix}
=
\begin{bmatrix}
0.5 \\
0.5
\end{bmatrix}
$$

El centro permanece en $(1,1)$ y la forma conserva sus proporciones.

#### Ejemplo de reflexión

Para reflejar el cuadrado respecto a una línea horizontal que atraviesa su
centro se usa $F_x$. Con $P_1=(0,0)$ y $c=(1,1)$:

$$
P_1'=c+F_x(P_1-c)
$$

$$
P_1'=
\begin{bmatrix}
1 \\
1
\end{bmatrix}
+
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
\begin{bmatrix}
-1 \\
-1
\end{bmatrix}
=
\begin{bmatrix}
0 \\
2
\end{bmatrix}
$$

La opción de reflexión Y realiza el mismo procedimiento con una línea vertical
que atraviesa el centro.

### 2. Aplicar secuencia de transformaciones

Esta opción solicita la cantidad de operaciones y luego permite configurarlas
una por una. Cada transformación recibe las coordenadas producidas por la
anterior:

$$
p_0 \xrightarrow{T_1} p_1
\xrightarrow{T_2} p_2
\xrightarrow{T_3} p_3
$$

Ejemplo:

1. Rotar $90^\circ$.
2. Escalar uniformemente por $0.5$.
3. Trasladar por $(3,-1)$.

Para el cuadrado inicial, las coordenadas finales son:

$$
P_1=(4.5,-0.5),\quad
P_2=(4.5,0.5),\quad
P_3=(3.5,0.5),\quad
P_4=(3.5,-0.5)
$$

El programa muestra el resultado de cada paso y, al final, un gráfico que
compara el estado anterior a toda la secuencia con el resultado final.

### 3. Analizar matemáticamente el escenario

Contiene dos opciones de álgebra lineal.

#### 3.1 Independencia lineal, base y dimensión

Los vértices actuales se interpretan como vectores de $\mathbb{R}^2$. Dos
vectores:

$$
v_1=(x_1,y_1),\qquad v_2=(x_2,y_2)
$$

son linealmente independientes cuando:

$$
\det(v_1,v_2)=x_1y_2-y_1x_2\neq0
$$

En $\mathbb{R}^2$ una base puede contener como máximo dos vectores. Los demás
son combinaciones lineales y se reportan como redundantes para generar el
espacio vectorial.

Ejemplo con el cuadrado:

$$
P_1=(0,0),\quad P_2=(2,0),\quad P_3=(2,2),\quad P_4=(0,2)
$$

- $P_1$ es el vector cero y es dependiente.
- $P_2$ y $P_3$ son independientes porque:

$$
\det(P_2,P_3)=
\begin{vmatrix}
2 & 2 \\
0 & 2
\end{vmatrix}
=2(2)-0(2)=4\neq0
$$

- $P_4$ es combinación lineal:

$$
P_4=-P_2+P_3
$$

Una base encontrada es:

$$
\mathcal{B}=\{(2,0),(2,2)\}
$$

y la dimensión del espacio generado es:

$$
\dim(\operatorname{span}\mathcal{B})=2
$$

> Un vértice redundante para generar el espacio vectorial no necesariamente
> puede eliminarse del dibujo: puede seguir siendo necesario para conservar la
> forma geométrica.

#### 3.2 Restricción de espacio o subespacio

El usuario ingresa una ecuación:

$$
ax+by=c
$$

El programa comprueba:

1. pertenencia del vector cero;
2. cierre bajo la suma;
3. cierre bajo multiplicación escalar.

Si $c\neq0$, el origen no pertenece al conjunto:

$$
a(0)+b(0)=0\neq c
$$

por lo tanto, no es un subespacio.

Si $c=0$, para $u,v$ que cumplen la ecuación:

$$
a(u_x+v_x)+b(u_y+v_y)
=(au_x+bu_y)+(av_x+bv_y)=0
$$

También, para cualquier escalar $k$:

$$
a(ku_x)+b(ku_y)=k(au_x+bu_y)=0
$$

Por ejemplo:

- $2x+3y=0$ sí es un subespacio: es una recta por el origen.
- $2x+3y=5$ no es un subespacio: no contiene el origen.
- $0x+0y=0$ representa todo $\mathbb{R}^2$.

### 4. Ver historial de transformaciones

Muestra en orden cada operación aplicada a la figura actual, junto con:

- descripción de la transformación;
- coordenadas antes de aplicarla;
- coordenadas obtenidas.

El historial pertenece a la figura actual y se vacía al restablecerla.

### 5. Restablecer figura

Recupera las coordenadas iniciales de la figura seleccionada y elimina su
historial.

### 6. Escoger otra figura

Regresa al catálogo de cuadrado, triángulo y rectángulo. La nueva figura
comienza en sus coordenadas iniciales y con historial vacío.

### 7. Salir

Finaliza el ciclo del menú y cierra el programa.

## Lectura del gráfico ASCII

El gráfico ajusta automáticamente su escala para incluir las coordenadas antes
y después de la transformación:

- `O1`, `O2`, ... representan vértices originales.
- `T1`, `T2`, ... representan vértices transformados.
- `X1`, `X2`, ... indican que el vértice conserva la misma posición.
- `O4/T2` indica que dos vértices diferentes aparecen en la misma celda.
- `-` representa el eje X, `|` representa el eje Y y `+` representa el origen.

## Matrices de transformación

Un vértice se representa mediante el vector:

$$
p =
\begin{bmatrix}
x \\
y
\end{bmatrix}
$$

### Rotación

Para rotar un ángulo $\theta$ en sentido antihorario se utiliza:

$$
R(\theta) =
\begin{bmatrix}
\cos(\theta) & -\sin(\theta) \\
\sin(\theta) & \cos(\theta)
\end{bmatrix}
$$

Por ejemplo, para una rotación de $90^\circ$:

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
- Si $k < 0$, además de escalar, la figura invierte su orientación respecto al centro.
- El programa no permite $k = 0$.

### Reflexión

Reflexión respecto al eje X:

$$
F_x =
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
$$

Reflexión respecto al eje Y:

$$
F_y =
\begin{bmatrix}
-1 & 0 \\
0 & 1
\end{bmatrix}
$$

Como el programa aplica estas matrices respecto al centro de la figura, los
ejes de reflexión son líneas paralelas a X o Y que atraviesan dicho centro.

### Traslación

La traslación no puede representarse con una matriz 2x2. Se suma el vector de
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

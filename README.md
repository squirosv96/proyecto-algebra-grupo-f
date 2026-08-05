# PixelForge MathEngine 2D - Grupo F

Programa de consola en Python para representar y transformar figuras mediante
operaciones de álgebra lineal, sin utilizar NumPy.

## Funciones

- Jugador (cuadrado), enemigo (triángulo) y obstáculo (rectángulo).
- Traslación, rotación, escalamiento uniforme y reflexión.
- Transformaciones matriciales respecto al centro actual de la figura.
- Vértices numerados en un gráfico ASCII.
- Ejecución de varias transformaciones en secuencia.
- Comparación entre el estado inicial y el resultado final.
- Análisis de independencia lineal, bases, dimensión y redundancia.
- Verificación de restricciones que pueden formar subespacios vectoriales.
- Historial de transformaciones, reinicio y cambio de figura.

## Ejecutar

Se requiere Python 3.10 o posterior. El proyecto no tiene dependencias externas.

```powershell
python main.py
```

## Figuras disponibles

| Opción | Objeto | Figura | Vértices iniciales |
|---|---|---|---|
| 1 | Jugador | Cuadrado | `(0,0)`, `(2,0)`, `(2,2)`, `(0,2)` |
| 2 | Enemigo | Triángulo | `(0,0)`, `(2,0)`, `(1,2)` |
| 3 | Obstáculo | Rectángulo | `(0,0)`, `(4,0)`, `(4,2)`, `(0,2)` |

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

## 1. Aplicar una transformación

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

### Operaciones respecto al centro

La rotación, el escalamiento y la reflexión se aplican alrededor del centro
actual de la figura. La fórmula general es:

```text
P' = centro + M × (P - centro)
```

El centro de una figura con `n` vértices se obtiene promediando sus
coordenadas:

```text
centro_x = (x1 + x2 + ... + xn) / n
centro_y = (y1 + y2 + ... + yn) / n

centro = (centro_x, centro_y)
```

Cada vértice se transforma en tres pasos:

```text
1. Punto relativo:       P_relativo = P - centro
2. Aplicar la matriz:    P_transformado = M × P_relativo
3. Regresar al centro:   P' = P_transformado + centro
```

Para el cuadrado:

```text
P1=(0,0)  P2=(2,0)  P3=(2,2)  P4=(0,2)

centro_x = (0 + 2 + 2 + 0) / 4 = 1
centro_y = (0 + 0 + 2 + 2) / 4 = 1

centro = (1,1)
```

Antes de aplicar una matriz a `P1`:

```text
P1 - centro = (0,0) - (1,1) = (-1,-1)
```

La matriz actúa sobre `(-1,-1)`. Después se suma `(1,1)` al resultado. Este
procedimiento se repite para todos los vértices usando el mismo centro.

La traslación es la excepción: no necesita calcular el centro porque suma el
mismo vector de desplazamiento a todos los vértices.

### Ejemplo de traslación

Si el desplazamiento es:

```text
d = (3,-1)
```

la operación es:

```text
P' = P + d
```

Para `P1=(0,0)`:

```text
P1' = (0,0) + (3,-1) = (3,-1)
```

La traslación cambia la posición, pero no el tamaño ni la orientación.

### Ejemplo de rotación

Para rotar el cuadrado 90 grados en sentido antihorario:

```text
           [ 0  -1 ]
R(90°)  =  [ 1   0 ]
```

Con `P1=(0,0)` y `centro=(1,1)`:

```text
P1 - centro = (-1,-1)

R(90°) × P_relativo:

[ 0  -1 ] [ -1 ]   [  1 ]
[ 1   0 ] [ -1 ] = [ -1 ]

P1' = (1,1) + (1,-1) = (2,0)
```

Después de transformar todos los vértices:

```text
P1'=(2,0)  P2'=(2,2)  P3'=(0,2)  P4'=(0,0)
```

El centro permanece en `(1,1)`, por lo que la figura rota sin desplazarse.

### Ejemplo de escalamiento uniforme

El mismo factor se aplica en X y Y para conservar las proporciones. Para
reducir el cuadrado a la mitad se utiliza `k=0.5`:

```text
         [ 0.5   0  ]
S(0.5) = [  0   0.5 ]
```

Con `P1=(0,0)` y `centro=(1,1)`:

```text
P1 - centro = (-1,-1)

S(0.5) × P_relativo:

[ 0.5   0  ] [ -1 ]   [ -0.5 ]
[  0   0.5 ] [ -1 ] = [ -0.5 ]

P1' = (1,1) + (-0.5,-0.5) = (0.5,0.5)
```

El centro permanece en `(1,1)` y la figura conserva su forma.

Comportamiento del factor:

- `k > 1`: aumenta el tamaño.
- `0 < k < 1`: reduce el tamaño.
- `k = 1`: conserva el tamaño.
- `k < 0`: escala e invierte la orientación respecto al centro.
- `k = 0`: no está permitido.

### Ejemplo de reflexión

Para reflejar respecto a una línea horizontal que atraviesa el centro se usa:

```text
       [ 1   0 ]
Fx  =  [ 0  -1 ]
```

Con `P1=(0,0)` y `centro=(1,1)`:

```text
P1 - centro = (-1,-1)

Fx × P_relativo:

[ 1   0 ] [ -1 ]   [ -1 ]
[ 0  -1 ] [ -1 ] = [  1 ]

P1' = (1,1) + (-1,1) = (0,2)
```

La reflexión Y usa una línea vertical que atraviesa el centro.

## 2. Aplicar una secuencia de transformaciones

Esta opción solicita la cantidad de operaciones y permite configurarlas una
por una. Cada transformación recibe las coordenadas producidas por la anterior:

```text
P0 --T1--> P1 --T2--> P2 --T3--> P3
```

Ejemplo:

```text
1. Rotar 90 grados.
2. Escalar uniformemente por 0.5.
3. Trasladar por (3,-1).
```

Para el cuadrado inicial, las coordenadas finales son:

```text
P1=(4.5,-0.5)
P2=(4.5, 0.5)
P3=(3.5, 0.5)
P4=(3.5,-0.5)
```

El programa muestra el resultado de cada paso y finalmente compara el estado
anterior a toda la secuencia con el resultado final.

## 3. Analizar matemáticamente el escenario

Esta opción contiene dos análisis de álgebra lineal.

### 3.1 Independencia lineal, base y dimensión

Los vértices actuales se interpretan como vectores de `R²`. Dos vectores:

```text
v1 = (x1,y1)
v2 = (x2,y2)
```

son linealmente independientes cuando su determinante no es cero:

```text
det(v1,v2) = x1×y2 - y1×x2

det(v1,v2) ≠ 0  =>  independientes
det(v1,v2) = 0  =>  dependientes
```

En `R²`, el espacio generado puede tener dimensión máxima 2. Si los vértices
generan todo `R²`, cualquier base contiene exactamente dos vectores. Los demás
son combinaciones lineales y se reportan como redundantes para generar el
espacio vectorial.

Ejemplo con el cuadrado:

```text
P1=(0,0)  P2=(2,0)  P3=(2,2)  P4=(0,2)
```

`P1` es el vector cero y es dependiente. Para `P2` y `P3`:

```text
              | 2  2 |
det(P2,P3) = | 0  2 | = 2×2 - 0×2 = 4
```

Como el determinante no es cero, son independientes. El cuarto vector es una
combinación lineal:

```text
P4 = -P2 + P3
(0,2) = -(2,0) + (2,2)
```

Una base encontrada es:

```text
B = {(2,0), (2,2)}
dimensión = 2
```

Un vértice redundante para generar el espacio vectorial no necesariamente puede
eliminarse del dibujo: puede ser necesario para conservar la forma geométrica.

### 3.2 Restricción de espacio o subespacio

El usuario ingresa una ecuación:

```text
a×x + b×y = c
```

El programa comprueba:

1. pertenencia del vector cero;
2. cierre bajo la suma;
3. cierre bajo multiplicación escalar.

Si `c ≠ 0`, el origen no pertenece al conjunto:

```text
a×0 + b×0 = 0 ≠ c
```

Por lo tanto, no es un subespacio.

Si `c = 0` y `u`, `v` cumplen la ecuación:

```text
a(ux + vx) + b(uy + vy)
= (a×ux + b×uy) + (a×vx + b×vy)
= 0 + 0
= 0
```

Esto demuestra el cierre bajo la suma. Para cualquier escalar `k`:

```text
a(k×ux) + b(k×uy)
= k(a×ux + b×uy)
= k×0
= 0
```

Esto demuestra el cierre bajo multiplicación escalar.

Ejemplos:

- `2x + 3y = 0`: sí es un subespacio; es una recta por el origen.
- `2x + 3y = 5`: no es un subespacio; no contiene el origen.
- `0x + 0y = 0`: representa todo `R²`.

## 4. Ver el historial de transformaciones

Muestra en orden cada operación aplicada a la figura actual:

- descripción de la transformación;
- coordenadas antes de aplicarla;
- coordenadas obtenidas.

El historial pertenece a la figura actual y se vacía al restablecerla.

## 5. Restablecer la figura

Recupera las coordenadas iniciales de la figura seleccionada y elimina su
historial.

## 6. Escoger otra figura

Regresa al catálogo de cuadrado, triángulo y rectángulo. La nueva figura
comienza en sus coordenadas iniciales y con un historial vacío.

## 7. Salir

Finaliza el ciclo del menú y cierra el programa.

## Lectura del gráfico ASCII

El gráfico ajusta automáticamente su escala para incluir las coordenadas antes
y después de la transformación:

- `O1`, `O2`, etc.: vértices originales.
- `T1`, `T2`, etc.: vértices transformados.
- `X1`, `X2`, etc.: el vértice conserva la misma posición.
- `O4/T2`: dos vértices diferentes aparecen en la misma celda.
- `-`: eje X.
- `|`: eje Y.
- `+`: origen.

## Referencia de matrices

Un vértice se representa como un vector columna:

```text
    [ x ]
P = [ y ]
```

### Rotación

```text
         [ cos(θ)  -sin(θ) ]
R(θ)  =  [ sin(θ)   cos(θ) ]
```

Los ángulos positivos producen rotaciones en sentido antihorario.

### Escalamiento uniforme

```text
        [ k  0 ]
S(k) = [ 0  k ]
```

### Reflexión

Respecto al eje horizontal que atraviesa el centro:

```text
       [ 1   0 ]
Fx  =  [ 0  -1 ]
```

Respecto al eje vertical que atraviesa el centro:

```text
       [ -1  0 ]
Fy  =  [  0  1 ]
```

### Traslación

La traslación no se representa con una matriz 2x2. Se suma un vector:

```text
d  = (dx,dy)
P' = P + d
```

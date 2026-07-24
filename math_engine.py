"""Nucleo matematico 2D implementado sin bibliotecas de algebra lineal."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import cos, radians, sin
from typing import Sequence

# Alias de tipos: una matriz 2x2 y un punto/vector del plano R2.
Matrix = tuple[tuple[float, float], tuple[float, float]]
Point = tuple[float, float]

# Figuras iniciales. Cada vertice se almacena como una tupla (x, y).
FIGURES: dict[str, tuple[str, tuple[Point, ...]]] = {
    "1": ("Jugador - cuadrado", ((0, 0), (2, 0), (2, 2), (0, 2))),
    "2": ("Enemigo - triangulo", ((0, 0), (2, 0), (1, 2))),
    "3": ("Obstaculo - rectangulo", ((0, 0), (4, 0), (4, 2), (0, 2))),
}


def rotation_matrix(angle_degrees: float) -> Matrix:
    """Construye la matriz 2x2 de rotacion para el angulo indicado."""
    # Las funciones trigonometricas de Python trabajan con radianes.
    angle = radians(angle_degrees)
    c, s = cos(angle), sin(angle)
    return ((c, -s), (s, c))


def scaling_matrix(scale: float) -> Matrix:
    """Construye una escala uniforme que conserva la forma de la figura."""
    return ((scale, 0.0), (0.0, scale))


def reflection_matrix(axis: str) -> Matrix:
    """Devuelve la matriz de reflexion correspondiente al eje X o Y."""
    if axis == "x":
        return ((1.0, 0.0), (0.0, -1.0))
    if axis == "y":
        return ((-1.0, 0.0), (0.0, 1.0))
    raise ValueError("El eje de reflexion debe ser 'x' o 'y'.")


def multiply_matrix_vector(matrix: Matrix, point: Point) -> Point:
    """Calcula M[x,y] mediante una implementacion propia."""
    return (
        matrix[0][0] * point[0] + matrix[0][1] * point[1],
        matrix[1][0] * point[0] + matrix[1][1] * point[1],
    )


def translate_point(point: Point, displacement: Point) -> Point:
    """Traslada un punto sumando el vector de desplazamiento (dx, dy)."""
    return (point[0] + displacement[0], point[1] + displacement[1])


def format_matrix(matrix: Matrix) -> str:
    """Convierte una matriz en texto alineado para mostrarla en consola."""
    return "\n".join("| " + "  ".join(f"{value:8.3f}" for value in row) + " |" for row in matrix)


def format_points(points: Sequence[Point]) -> str:
    """Enumera y formatea una coleccion de vertices como P1, P2, etc."""
    return "  ".join(f"P{i}=({x:.2f}, {y:.2f})" for i, (x, y) in enumerate(points, 1))


def calculation_text(matrix: Matrix, point: Point, result: Point) -> str:
    """Explica las operaciones de la multiplicacion matriz-vector."""
    x, y = point
    first = f"({matrix[0][0]:.3f}*{x:.2f}) + ({matrix[0][1]:.3f}*{y:.2f})"
    second = f"({matrix[1][0]:.3f}*{x:.2f}) + ({matrix[1][1]:.3f}*{y:.2f})"
    return f"x' = {first} = {result[0]:.2f}; y' = {second} = {result[1]:.2f}"


def translation_calculation_text(displacement: Point, point: Point, result: Point) -> str:
    """Explica la suma utilizada para trasladar un vertice."""
    return (f"x' = {point[0]:.2f} + {displacement[0]:.2f} = {result[0]:.2f}; "
            f"y' = {point[1]:.2f} + {displacement[1]:.2f} = {result[1]:.2f}")


@dataclass(frozen=True)
class TransformationResult:
    """Datos necesarios para explicar y registrar una transformacion."""

    description: str
    matrix: Matrix | None
    displacement: Point | None
    center: Point | None
    before: tuple[Point, ...]
    after: tuple[Point, ...]


@dataclass
class Figure:
    """Representa una figura y administra sus coordenadas actuales."""

    name: str
    original_points: tuple[Point, ...]
    points: tuple[Point, ...] = field(init=False)
    # Almacena cada transformacion para reconstruir el recorrido de la figura.
    history: list[TransformationResult] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """Inicia la figura con sus puntos originales y un historial vacio."""
        self.points = self.original_points
        self.history = []

    def apply(self, description: str, matrix: Matrix) -> TransformationResult:
        """Aplica una matriz respecto al centro actual de la figura."""
        points_before = self.points
        number_of_points = len(points_before)

        # El centro se obtiene promediando por separado las x y las y.
        sum_x = sum(point[0] for point in points_before)
        sum_y = sum(point[1] for point in points_before)
        center_x = sum_x / number_of_points
        center_y = sum_y / number_of_points
        center = (center_x, center_y)

        # Formula por vertice: p' = centro + M * (p - centro).
        # Se lleva el punto al origen, se transforma y se devuelve al centro.
        transformed_points: list[Point] = []
        for point in points_before:
            point_x, point_y = point

            relative_x = point_x - center_x
            relative_y = point_y - center_y
            point_relative_to_center = (relative_x, relative_y)

            transformed_relative_point = multiply_matrix_vector(
                matrix,
                point_relative_to_center,
            )

            final_point = translate_point(
                transformed_relative_point,
                center,
            )
            transformed_points.append(final_point)

        points_after = tuple(transformed_points)
        result = TransformationResult(
            description,
            matrix,
            None,
            center,
            points_before,
            points_after,
        )

        # El resultado pasa a ser el estado actual y se registra.
        self.points = points_after
        self.history.append(result)
        return result

    def translate(self, description: str, displacement: Point) -> TransformationResult:
        """Suma el mismo desplazamiento a todos los vertices."""
        before = self.points
        after = tuple(translate_point(point, displacement) for point in before)
        result = TransformationResult(description, None, displacement, None, before, after)
        self.points = after
        self.history.append(result)

        return result

    def reset(self) -> None:
        """Recupera la figura original y elimina su historial."""
        self.points = self.original_points
        #Cuando el usuario limpie la figura, el histrial se vacía
        self.history.clear()


def ascii_plot(original: Sequence[Point], transformed: Sequence[Point], width: int = 61, height: int = 21) -> str:
    """Dibuja vertices numerados: O original, T transformado, X coincidencia."""
    # Se incluye el origen para que los ejes siempre tengan una referencia.
    all_points = list(original) + list(transformed) + [(0.0, 0.0)]
    min_x, max_x = min(p[0] for p in all_points), max(p[0] for p in all_points)
    min_y, max_y = min(p[1] for p in all_points), max(p[1] for p in all_points)
    # El margen evita que las etiquetas queden pegadas al borde.
    px, py = max(1.0, (max_x - min_x) * 0.1), max(1.0, (max_y - min_y) * 0.1)
    min_x, max_x, min_y, max_y = min_x - px, max_x + px, min_y - py, max_y + py
    grid = [[" " for _ in range(width)] for _ in range(height)]

    def cell(point: Point) -> tuple[int, int]:
        """Convierte coordenadas cartesianas en fila y columna del texto."""
        column = round((point[0] - min_x) / (max_x - min_x) * (width - 1))
        row = round((max_y - point[1]) / (max_y - min_y) * (height - 1))
        return row, column

    # Los ejes se dibujan solo si el cero pertenece al rango visible.
    if min_x <= 0 <= max_x:
        axis_column = cell((0, 0))[1]
        for row in range(height):
            grid[row][axis_column] = "|"
    if min_y <= 0 <= max_y:
        axis_row = cell((0, 0))[0]
        for column in range(width):
            grid[axis_row][column] = "-"
    origin_row, origin_column = cell((0, 0))
    grid[origin_row][origin_column] = "+"
    def put_label(point: Point, label: str) -> None:
        """Escribe una etiqueta sin sobrepasar el borde derecho."""
        row, column = cell(point)
        # Desplaza la etiqueta si esta cerca del borde derecho.
        start = min(column, width - len(label))
        for offset, character in enumerate(label):
            grid[row][start + offset] = character

    # Agrupa etiquetas cuando varios vertices ocupan la misma celda.
    transformed_cells = {cell(point): index for index, point in enumerate(transformed, 1)}
    labels_by_cell: dict[tuple[int, int], list[str]] = {}
    for index, point in enumerate(original, 1):
        label = f"X{index}" if transformed_cells.get(cell(point)) == index else f"O{index}"
        labels_by_cell.setdefault(cell(point), []).append(label)
    for index, point in enumerate(transformed, 1):
        if cell(point) != cell(original[index - 1]):
            labels_by_cell.setdefault(cell(point), []).append(f"T{index}")
    for position, labels in labels_by_cell.items():
        row, column = position
        put_label((min_x + column / (width - 1) * (max_x - min_x),
                   max_y - row / (height - 1) * (max_y - min_y)), "/".join(labels))
    legend = "O#=vertice original  T#=vertice transformado  X#=coinciden"
    return "\n".join("".join(row) for row in grid) + "\n" + legend


# =====================================================================
# ACTIVIDAD 3: ANÁLISIS MATEMÁTICO DEL ESCENARIO
# =====================================================================

def check_subspace_restriction(a: float, b: float, c: float) -> str:
    """
    Verifica si una restricción lineal ax + by = c forma un subespacio en R2.
    Decisión: Un subespacio requiere contener al vector nulo (0,0).
    Por ende, 'c' DEBE ser 0 para que sea un subespacio válido.
    """
    report = [f"Analizando la restricción de movimiento: {a:g}x + {b:g}y = {c:g}"]

    # 1. Verificación del vector nulo (0,0)
    contains_zero = (a * 0 + b * 0 == c)
    report.append(f"1. Contiene al origen (0,0): {contains_zero} (Evaluación: {a:g}(0) + {b:g}(0) = {c:g})")

    if not contains_zero:
        report.append("RESULTADO: NO es un subespacio vectorial porque no incluye la posición (0,0).")
        return "\n".join(report)

    # 2. Demostración de Cierre por Suma
    report.append("2. Cierre bajo la suma: VÁLIDO. Si u=(x1,y1) y v=(x2,y2) cumplen la ecuación, u+v también.")
    # 3. Demostración de Cierre por Escalar
    report.append("3. Cierre bajo multiplicación por escalar: VÁLIDO. Si u=(x1,y1) cumple, k*u también.")
    report.append("RESULTADO: SÍ es un subespacio vectorial de R2 (representa una línea que pasa por el origen).")

    return "\n".join(report)


def are_linearly_independent(v1: Point, v2: Point) -> bool:
    """
    Determina si dos vectores en R2 son linealmente independientes.
    Decisión: En R2, 2 vectores son LI si su determinante es diferente de cero (no son colineales/paralelos).
    det([v1, v2]) = v1[0]*v2[1] - v1[1]*v2[0]
    """
    det = v1[0] * v2[1] - v1[1] * v2[0]
    return abs(det) > 1e-9 # Evita errores de precisión flotante


def analyze_figure_vectors(points: tuple[Point, ...]) -> str:
    """
    Analiza la independencia lineal, redundancia, bases y dimensión de los vértices de una figura.
    """
    report = ["\n--- ANÁLISIS DE INDEPENDENCIA LINEAL Y BASES ---"]
    report.append(f"Puntos analizados: {format_points(points)}")

    # Filtrar el origen (0,0) ya que siempre es linealmente dependiente
    non_zero_points = [p for p in points if abs(p[0]) > 1e-9 or abs(p[1]) > 1e-9]

    if not non_zero_points:
        report.append("Todos los puntos están en el origen (0,0). Dimensión = 0.")
        return "\n".join(report)

    basis: list[Point] = [non_zero_points[0]]
    redundant: list[Point] = []

    for p in non_zero_points[1:]:
        # Verificar si 'p' es independiente respecto al primer vector de la base encontrada
        if len(basis) < 2 and are_linearly_independent(basis[0], p):
            basis.append(p)
        else:
            redundant.append(p)

    # Redundancia original (si había ceros)
    zeros = [p for p in points if abs(p[0]) <= 1e-9 and abs(p[1]) <= 1e-9]
    redundant.extend(zeros)

    report.append(f"\n1. Vectores Base encontrados ({len(basis)}): {basis}")
    report.append(f"2. Vectores Redundantes/Dependientes ({len(redundant)}): {redundant}")
    report.append(f"3. Dimensión del espacio generado: {len(basis)}")

    # Interpretación geométrica
    report.append("\n--- INTERPRETACIÓN GEOMÉTRICA ---")
    if len(basis) == 2:
        report.append("• Los puntos de la figura generan todo el espacio 2D (R2).")
        report.append("• Toda la escena/figura se puede representar usando únicamente los 2 vectores de la base.")
    elif len(basis) == 1:
        report.append("• Todos los puntos son colineales (están sobre una misma línea que pasa por el origen).")
        report.append("• La figura está colapsada en una dimensión (Dimensión = 1).")

    if redundant:
        report.append(f"• ¡Optimización posible! Hay {len(redundant)} punto(s) redundante(s) que son combinación lineal.")
    else:
        report.append("• Representación óptima: No existen puntos redundantes.")

    return "\n".join(report)

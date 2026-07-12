"""Nucleo matematico 2D implementado sin bibliotecas de algebra lineal."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import cos, radians, sin
from typing import Sequence

Matrix = tuple[tuple[float, float], tuple[float, float]]
Point = tuple[float, float]

FIGURES: dict[str, tuple[str, tuple[Point, ...]]] = {
    "1": ("Jugador - cuadrado", ((0, 0), (2, 0), (2, 2), (0, 2))),
    "2": ("Enemigo - triangulo", ((0, 0), (2, 0), (1, 2))),
    "3": ("Obstaculo - rectangulo", ((0, 0), (4, 0), (4, 2), (0, 2))),
}


def rotation_matrix(angle_degrees: float) -> Matrix:
    angle = radians(angle_degrees)
    c, s = cos(angle), sin(angle)
    return ((c, -s), (s, c))


def scaling_matrix(scale_x: float, scale_y: float) -> Matrix:
    return ((scale_x, 0.0), (0.0, scale_y))


def reflection_matrix(axis: str) -> Matrix:
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
    return (point[0] + displacement[0], point[1] + displacement[1])


def format_matrix(matrix: Matrix) -> str:
    return "\n".join("| " + "  ".join(f"{value:8.3f}" for value in row) + " |" for row in matrix)


def format_points(points: Sequence[Point]) -> str:
    return "  ".join(f"P{i}=({x:.2f}, {y:.2f})" for i, (x, y) in enumerate(points, 1))


def calculation_text(matrix: Matrix, point: Point, result: Point) -> str:
    x, y = point
    first = f"({matrix[0][0]:.3f}*{x:.2f}) + ({matrix[0][1]:.3f}*{y:.2f})"
    second = f"({matrix[1][0]:.3f}*{x:.2f}) + ({matrix[1][1]:.3f}*{y:.2f})"
    return f"x' = {first} = {result[0]:.2f}; y' = {second} = {result[1]:.2f}"


def translation_calculation_text(displacement: Point, point: Point, result: Point) -> str:
    return (f"x' = {point[0]:.2f} + {displacement[0]:.2f} = {result[0]:.2f}; "
            f"y' = {point[1]:.2f} + {displacement[1]:.2f} = {result[1]:.2f}")


@dataclass(frozen=True)
class TransformationResult:
    description: str
    matrix: Matrix | None
    displacement: Point | None
    before: tuple[Point, ...]
    after: tuple[Point, ...]


@dataclass
class Figure:
    name: str
    original_points: tuple[Point, ...]
    points: tuple[Point, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.points = self.original_points

    def apply(self, description: str, matrix: Matrix) -> TransformationResult:
        before = self.points
        after = tuple(multiply_matrix_vector(matrix, point) for point in before)
        entry = TransformationResult(description, matrix, None, before, after)
        self.points = after
        return entry

    def translate(self, description: str, displacement: Point) -> TransformationResult:
        before = self.points
        after = tuple(translate_point(point, displacement) for point in before)
        result = TransformationResult(description, None, displacement, before, after)
        self.points = after
        return result

    def reset(self) -> None:
        self.points = self.original_points


def ascii_plot(original: Sequence[Point], transformed: Sequence[Point], width: int = 61, height: int = 21) -> str:
    """Dibuja vertices numerados: O original, T transformado, X coincidencia."""
    all_points = list(original) + list(transformed) + [(0.0, 0.0)]
    min_x, max_x = min(p[0] for p in all_points), max(p[0] for p in all_points)
    min_y, max_y = min(p[1] for p in all_points), max(p[1] for p in all_points)
    px, py = max(1.0, (max_x - min_x) * 0.1), max(1.0, (max_y - min_y) * 0.1)
    min_x, max_x, min_y, max_y = min_x - px, max_x + px, min_y - py, max_y + py
    grid = [[" " for _ in range(width)] for _ in range(height)]

    def cell(point: Point) -> tuple[int, int]:
        column = round((point[0] - min_x) / (max_x - min_x) * (width - 1))
        row = round((max_y - point[1]) / (max_y - min_y) * (height - 1))
        return row, column

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
        row, column = cell(point)
        # Desplaza la etiqueta si esta cerca del borde derecho.
        start = min(column, width - len(label))
        for offset, character in enumerate(label):
            grid[row][start + offset] = character

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

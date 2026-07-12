"""Interfaz de consola de PixelForge MathEngine 2D."""

from math_engine import (FIGURES, Figure, ascii_plot,
    calculation_text, format_matrix, format_points, rotation_matrix,
    scaling_matrix, reflection_matrix, translation_calculation_text)


def read_option(prompt: str, valid: set[str]) -> str:
    while True:
        option = input(prompt).strip()
        if option in valid:
            return option
        print("Opcion invalida. Intente de nuevo.")


def read_number(prompt: str, nonzero: bool = False) -> float:
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if nonzero and value == 0:
                print("El valor no puede ser cero.")
                continue
            return value
        except ValueError:
            print("Ingrese un numero valido, por ejemplo 2 o 1.5.")


def choose_figure() -> Figure:
    print("\nFIGURAS DISPONIBLES")
    for key, (name, points) in FIGURES.items():
        print(f"  {key}. {name}: {format_points(points)}")
    option = read_option("Seleccione una figura: ", set(FIGURES))
    name, points = FIGURES[option]
    return Figure(name, points)


def choose_transformation():
    print("\n1. Trasladar\n2. Rotar\n3. Escalar\n4. Reflejar")
    option = read_option("Seleccione una transformacion: ", {"1", "2", "3", "4"})
    if option == "1":
        dx, dy = read_number("Desplazamiento en x: "), read_number("Desplazamiento en y: ")
        return f"Traslacion ({dx:g}, {dy:g})", None, (dx, dy)
    if option == "2":
        angle = read_number("Angulo en grados (positivo = antihorario): ")
        return f"Rotacion {angle:g} grados", rotation_matrix(angle), None
    if option == "3":
        scale = read_number("Factor de escala para x e y: ", True)
        return f"Escalamiento uniforme ({scale:g})", scaling_matrix(scale), None
    print("1. Respecto al eje X\n2. Respecto al eje Y")
    reflection = read_option("Seleccione el tipo de reflexion: ", {"1", "2"})
    description, axis = {
        "1": ("Reflexion respecto al eje X", "x"),
        "2": ("Reflexion respecto al eje Y", "y"),
    }[reflection]
    return description, reflection_matrix(axis), None


def show_result(figure: Figure, entry) -> None:
    print(f"\n{'=' * 72}\n{entry.description}\nFigura: {figure.name}")
    print(f"Coordenadas antes:   {format_points(entry.before)}")
    if entry.matrix is not None:
        print("\nMatriz 2x2 utilizada:\n" + format_matrix(entry.matrix))
        print("\nCalculos realizados (M * [x, y]):")
        calculation, operator = calculation_text, entry.matrix
    else:
        print(f"\nVector de traslacion: ({entry.displacement[0]:.2f}, {entry.displacement[1]:.2f})")
        print("\nCalculos realizados ([x, y] + [dx, dy]):")
        calculation, operator = translation_calculation_text, entry.displacement
    for index, (before, after) in enumerate(zip(entry.before, entry.after), 1):
        print(f"  P{index}: {calculation(operator, before, after)}")
    print(f"\nCoordenadas despues: {format_points(entry.after)}")
    print("\nRepresentacion grafica:\n" + ascii_plot(entry.before, entry.after))


def main() -> None:
    print("=" * 72)
    print("PIXELFORGE MATHENGINE 2D v1.0 - TRANSFORMACIONES GEOMETRICAS")
    print("=" * 72)
    figure = choose_figure()
    while True:
        print(f"\nFigura actual: {figure.name}\nCoordenadas: {format_points(figure.points)}")
        print("\n1. Aplicar transformacion\n2. Restablecer figura\n3. Escoger otra figura\n4. Salir")
        option = read_option("Seleccione una opcion: ", {"1", "2", "3", "4"})
        if option == "1":
            description, matrix, displacement = choose_transformation()
            result = (figure.apply(description, matrix) if matrix is not None
                      else figure.translate(description, displacement))
            show_result(figure, result)
        elif option == "2":
            figure.reset()
            print("Figura restablecida.")
        elif option == "3":
            figure = choose_figure()
        else:
            print("Gracias por usar PixelForge MathEngine 2D.")
            break


if __name__ == "__main__":
    main()

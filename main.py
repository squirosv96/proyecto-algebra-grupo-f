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


def read_positive_integer(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Ingrese un numero entero mayor que cero.")


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
        if entry.center is not None:
            print(f"Centro fijo de la figura: ({entry.center[0]:.2f}, {entry.center[1]:.2f})")
            print("Calculo: centro + M * (punto - centro)")
        else:
            print("\nCalculos realizados (M * [x, y]):")
        calculation, operator = calculation_text, entry.matrix
    else:
        print(f"\nVector de traslacion: ({entry.displacement[0]:.2f}, {entry.displacement[1]:.2f})")
        print("\nCalculos realizados ([x, y] + [dx, dy]):")
        calculation, operator = translation_calculation_text, entry.displacement
    for index, (before, after) in enumerate(zip(entry.before, entry.after), 1):
        if entry.center is not None:
            relative = (before[0] - entry.center[0], before[1] - entry.center[1])
            transformed_relative = (after[0] - entry.center[0], after[1] - entry.center[1])
            detail = calculation(operator, relative, transformed_relative)
            print(f"  P{index}: relativo al centro {relative} -> {detail}; final = ({after[0]:.2f}, {after[1]:.2f})")
        else:
            print(f"  P{index}: {calculation(operator, before, after)}")
    print(f"\nCoordenadas despues: {format_points(entry.after)}")
    print("\nRepresentacion grafica:\n" + ascii_plot(entry.before, entry.after))


def apply_transformation(figure: Figure) -> None:
    description, matrix, displacement = choose_transformation()
    result = (figure.apply(description, matrix) if matrix is not None
              else figure.translate(description, displacement))
    show_result(figure, result)


def apply_sequence(figure: Figure) -> None:
    amount = read_positive_integer("Cantidad de transformaciones en la secuencia: ")
    initial_points = figure.points
    for step in range(1, amount + 1):
        print(f"\n--- Transformacion {step} de {amount} ---")
        apply_transformation(figure)
    print(f"\nSecuencia completada. Coordenadas finales: {format_points(figure.points)}")
    print("\nCOMPARACION DE LA SECUENCIA COMPLETA")
    print(f"Antes:   {format_points(initial_points)}")
    print(f"Despues: {format_points(figure.points)}")
    print("\nGrafico antes y despues de toda la secuencia:\n"
          + ascii_plot(initial_points, figure.points))


def show_history(figure: Figure) -> None:
    print(f"\n{'=' * 72}")
    print(f"HISTORIAL DE TRANSFORMACIONES - {figure.name.upper()}")
    print(f"{'=' * 72}")

    if not figure.history:
        print("El historial está vacío. Aún no se han aplicado transformaciones.")
        return

    for index, entry in enumerate(figure.history, 1):
        print(f"\n🔹 Paso {index}: {entry.description}")
        print(f"   Coordenadas antes:  {format_points(entry.before)}")
        print(f"   Coordenadas después: {format_points(entry.after)}")

    print(f"\n{'=' * 72}")
    print("Fin del historial.")


def main() -> None:
    print("=" * 72)
    print("PIXELFORGE MATHENGINE 2D v1.0 - TRANSFORMACIONES GEOMETRICAS")
    print("=" * 72)
    figure = choose_figure()
    while True:
        print(f"\nFigura actual: {figure.name}\nCoordenadas: {format_points(figure.points)}")
        print("\n1. Aplicar una transformación\n2. Aplicar secuencia de transformaciones"
              "\n3. Ver historial de transformaciones"
              "\n4. Restablecer figura\n5. Escoger otra figura\n6. Salir")
        option = read_option("Seleccione una opcion: ", {"1", "2", "3", "4", "5"})
        if option == "1":
            apply_transformation(figure)
        elif option == "2":
            apply_sequence(figure)
        elif option == "3":
            show_history(figure)
        elif option == "4":
            figure.reset()
            print("Figura restablecida.")
        elif option == "5":
            figure = choose_figure()
        else:
            print("Gracias por usar PixelForge MathEngine 2D.")
            break


if __name__ == "__main__":
    main()

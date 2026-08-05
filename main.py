"""Interfaz de consola de PixelForge MathEngine 2D."""

from math_engine import (FIGURES, Figure, ascii_plot,
                         calculation_text, format_matrix, format_points, rotation_matrix,
                         scaling_matrix, reflection_matrix, translation_calculation_text,
                         check_subspace_restriction, analyze_figure_vectors)


def read_option(prompt: str, valid: set[str]) -> str:
    """Solicita una opcion hasta que pertenezca al conjunto permitido."""
    while True:
        option = input(prompt).strip()
        if option in valid:
            return option
        print("Opcion invalida. Intente de nuevo.")


def read_number(
    prompt: str,
    nonzero: bool = False,
    positive_integer: bool = False,
) -> float:
    """Lee un numero y aplica las validaciones solicitadas."""
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if nonzero and value == 0:
                print("El valor no puede ser cero.")
                continue
            if positive_integer and (value <= 0 or not value.is_integer()):
                print("Ingrese un numero entero mayor que cero.")
                continue
            return value
        except ValueError:
            print("Ingrese un numero valido, por ejemplo 2 o 1.5.")


def choose_figure() -> Figure:
    """Muestra el catalogo y crea la figura seleccionada."""
    print("\nFIGURAS DISPONIBLES")
    for key, (name, points) in FIGURES.items():
        print(f"  {key}. {name}: {format_points(points)}")
    option = read_option("Seleccione una figura: ", set(FIGURES))
    name, points = FIGURES[option]
    return Figure(name, points)


def choose_transformation():
    """Recopila los parametros de la transformacion elegida."""
    print("\n1. Trasladar\n2. Rotar\n3. Escalar\n4. Reflejar")
    option = read_option("Seleccione una transformacion: ", {"1", "2", "3", "4"})
    # La traslacion usa un vector; las demas operaciones usan matrices 2x2.
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
    """Presenta operador, calculos, coordenadas y grafico comparativo."""
    print(f"\n{'=' * 72}\n{entry.description}\nFigura: {figure.name}")
    print(f"Coordenadas antes:   {format_points(entry.before)}")
    # Una matriz indica rotacion, escalamiento o reflexion.
    if entry.matrix is not None:
        print("\nMatriz 2x2 utilizada:\n" + format_matrix(entry.matrix))
        if entry.center is not None:
            print(f"Centro fijo de la figura: ({entry.center[0]:.2f}, {entry.center[1]:.2f})")
            print("Calculo: centro + M * (punto - centro)")
        else:
            print("\nCalculos realizados (M * [x, y]):")
        calculation, operator = calculation_text, entry.matrix
    else:
        # La ausencia de matriz indica una traslacion vectorial.
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
    """Ejecuta una transformacion y muestra inmediatamente su resultado."""
    description, matrix, displacement = choose_transformation()
    result = (figure.apply(description, matrix) if matrix is not None
              else figure.translate(description, displacement))
    show_result(figure, result)


def apply_sequence(figure: Figure) -> None:
    """Aplica varias operaciones en orden sobre el resultado anterior."""
    amount = int(read_number(
        "Cantidad de transformaciones en la secuencia: ",
        positive_integer=True,
    ))
    # Se conserva el inicio para compararlo con el resultado completo.
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
    """Lista cronologicamente las transformaciones registradas."""
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

def analyze_scene_menu(figure: Figure) -> None:
    """Permite escoger entre los analisis matematicos disponibles."""
    print(f"\n{'=' * 72}")
    print("ACTIVIDAD 3: ANÁLISIS MATEMÁTICO DEL ESCENARIO")
    print(f"{'=' * 72}")
    print("1. Analizar vectores de la figura actual (Independencia, Base y Dimensión)")
    print("2. Evaluar restricción de espacio/subespacio vectorial de movimiento")

    sub_option = read_option("Seleccione una opción de análisis: ", {"1", "2"})

    if sub_option == "1":
        # Se analizan las coordenadas actuales, no solo las originales.
        print(analyze_figure_vectors(figure.points))
    else:
        # El usuario define una ecuacion lineal de la forma ax + by = c.
        print("\n--- EVALUACIÓN DE SUBESPACIOS VECTORIALES ---")
        print("Ingrese la restricción de movimiento de la forma: a*x + b*y = c")
        a = read_number("Ingrese la constante 'a': ")
        b = read_number("Ingrese la constante 'b': ")
        c = read_number("Ingrese la constante 'c': ")
        print("\n" + check_subspace_restriction(a, b, c))


def main() -> None:
    """Punto de entrada y ciclo principal del programa."""
    print("=" * 72)
    print("PIXELFORGE MATHENGINE 2D v1.0 - TRANSFORMACIONES GEOMETRICAS")
    print("=" * 72)
    figure = choose_figure()
    # El ciclo termina cuando el usuario selecciona la opcion Salir.
    while True:
        print(f"\nFigura actual: {figure.name}\nCoordenadas: {format_points(figure.points)}")
        print("\n1. Aplicar una transformacion"
              "\n2. Aplicar secuencia de transformaciones"
              "\n3. Analizar matematicamente el escenario"
              "\n4. Ver historial de transformaciones"
              "\n5. Restablecer figura"
              "\n6. Escoger otra figura"
              "\n7. Salir")

        option = read_option("Seleccione una opcion: ", {"1", "2", "3", "4", "5", "6", "7"})

        # Cada opcion delega el trabajo a una funcion especializada.
        if option == "1":
            apply_transformation(figure)
        elif option == "2":
            apply_sequence(figure)
        elif option == "3":
            analyze_scene_menu(figure) # <-- Llama a nuestra nueva funcionalidad
        elif option == "4":
            show_history(figure)
        elif option == "5":
            figure.reset()
            print("Figura restablecida y su historial ha sido limpiado.")
        elif option == "6":
            figure = choose_figure()
        else:
            print("Gracias por usar PixelForge MathEngine 2D.")
            break


if __name__ == "__main__":
    main()

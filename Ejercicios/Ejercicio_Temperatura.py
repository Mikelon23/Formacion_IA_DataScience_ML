def pedir_temperaturas():
    """Solicita las temperaturas de 5 días y devuelve una lista."""
    temperaturas = []
    for i in range(1, 6):
        temp = float(input(f"Ingrese la temperatura del día {i}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_estadisticas(temperaturas):
    """Calcula promedio, máxima, mínima y cantidad de días > 25°C."""
    suma = 0
    maxima = temperaturas[0]
    minima = temperaturas[0]
    dias_calidos = 0

    for t in temperaturas:
        suma += t
        if t > maxima:
            maxima = t
        if t < minima:
            minima = t
        if t > 25:
            dias_calidos += 1

    promedio = suma / len(temperaturas)
    return promedio, maxima, minima, dias_calidos

def mostrar_resumen(temperaturas, promedio, maxima, minima, dias_calidos):
    """Muestra el resumen completo de las temperaturas."""
    print("\n=== Resumen de la semana ===")
    for i in range(len(temperaturas)):
        print(f"Día {i+1}: {temperaturas[i]}°C")

    print(f"\nTemperatura promedio: {promedio:.2f}°C")
    print(f"Temperatura máxima: {maxima}°C")
    print(f"Temperatura mínima: {minima}°C")
    print(f"Días con temperatura alta (>25°C): {dias_calidos}")

def main():
    temperaturas = pedir_temperaturas()
    promedio, maxima, minima, dias_calidos = calcular_estadisticas(temperaturas)
    mostrar_resumen(temperaturas, promedio, maxima, minima, dias_calidos)

# Ejecutar
if __name__ == "__main__":
    main()

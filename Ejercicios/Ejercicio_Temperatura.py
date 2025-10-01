#-solicitar la temperatura de 5 dias consecutivos
#-mostrar la temperatura promedio, maxima y minima de la semana
#-contar con cuantos dias tuvieron temperatura alta (mayor de 25 grados)
#-mostrar un resumen completo de los datos registrados

def pedir_temperaturas():
    """Solicita las temperaturas de 5 días y devuelve una lista."""
    temperaturas = []
    for i in range(1, 6):
        temp = float(input(f"Ingrese la temperatura del día {i}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_estadisticas(temperaturas):
    """Calcula promedio, máxima y mínima."""
    suma = 0
    maxima = temperaturas[0]
    minima = temperaturas[0]

    for t in temperaturas:
        suma += t
        if t > maxima:
            maxima = t
        if t < minima:
            minima = t

    promedio = suma / len(temperaturas)
    return promedio, maxima, minima

def mostrar_resumen(temperaturas, promedio, maxima, minima):
    """Muestra el resumen completo de las temperaturas."""
    print("\n=== Resumen de la semana ===")
    for i in range(len(temperaturas)):
        print(f"Día {i+1}: {temperaturas[i]}°C")

    print(f"\nTemperatura promedio: {promedio:.2f}°C")
    print(f"Temperatura máxima: {maxima}°C")
    print(f"Temperatura mínima: {minima}°C")

def main():
    temperaturas = pedir_temperaturas()
    promedio, maxima, minima = calcular_estadisticas(temperaturas)
    mostrar_resumen(temperaturas, promedio, maxima, minima)

# Ejecutar
if __name__ == "__main__":
    main()

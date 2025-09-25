# Programa: Lista de compras

# Paso 1: Crear una lista vacía para guardar productos
productos = []

# Paso 2: Pedir al usuario nombre y precio de 3 productos
for i in range(3):
    nombre = input(f"Ingrese el nombre del producto {i+1}: ")
    precio = float(input(f"Ingrese el precio de {nombre}: "))
    productos.append({"nombre": nombre, "precio": precio})

# Paso 3: Calcular el total
total = sum(p["precio"] for p in productos)

# Paso 4: Mostrar resultados
print("\n--- Lista de productos ---")
for p in productos:
    print(f"{p['nombre']} - ${p['precio']:.2f}")

print(f"\nTotal a pagar: ${total:.2f}")

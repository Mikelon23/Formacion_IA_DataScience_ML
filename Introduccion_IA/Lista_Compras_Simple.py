# Lista de compras sencilla

# Pedir al usuario nombre y precio de 3 productos
producto1 = input("Ingrese el nombre del producto 1: ")
precio1 = float(input("Ingrese el precio de " + producto1 + ": "))

producto2 = input("Ingrese el nombre del producto 2: ")
precio2 = float(input("Ingrese el precio de " + producto2 + ": "))

producto3 = input("Ingrese el nombre del producto 3: ")
precio3 = float(input("Ingrese el precio de " + producto3 + ": "))

# Calcular total
total = precio1 + precio2 + precio3

# Mostrar lista y total
print("\n--- Lista de productos ---")
print(producto1, "-", precio1)
print(producto2, "-", precio2)
print(producto3, "-", precio3)

print("\nTotal a pagar:", total)

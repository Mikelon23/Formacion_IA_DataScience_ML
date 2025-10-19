import pandas as pd
import numpy as np
from datetime import datetime
import os

class AnalizadorVentas:
    def __init__(self):
        self.ventas = None
        self.productos = None
        self.detalle_ventas = None
        self.clientes = None
        self.datos_cargados = False
    
    def cargar_datos(self):
        """Carga y prepara los datos desde los archivos Excel"""
        try:
            # Cargar datos desde archivos
            self.ventas = pd.read_excel('ventas.xlsx')
            self.productos = pd.read_excel('productos.xlsx')
            self.detalle_ventas = pd.read_excel('detalle_ventas.xlsx')
            self.clientes = pd.read_excel('clientes.xlsx')
            
            # Limpieza y preparación de datos
            self._preparar_datos()
            self.datos_cargados = True
            print("✓ Datos cargados exitosamente")
            return True
            
        except Exception as e:
            print(f"✗ Error al cargar datos: {e}")
            return False
    
    def _preparar_datos(self):
        """Prepara y limpia los datos cargados"""
        # Convertir fechas
        self.ventas['fecha'] = pd.to_datetime(self.ventas['fecha'])
        self.clientes['fecha_alta'] = pd.to_datetime(self.clientes['fecha_alta'])
        
        # Unir datos para análisis
        self.ventas_completas = pd.merge(
            self.detalle_ventas, 
            self.ventas, 
            on='id_venta', 
            how='left'
        )
        
        self.ventas_completas = pd.merge(
            self.ventas_completas,
            self.clientes,
            on='id_cliente',
            how='left',
            suffixes=('', '_cliente')
        )
    
    def resumen_general(self):
        """Muestra un resumen general del dataset"""
        if not self.datos_cargados:
            print("Primero debe cargar los datos (Opción 1)")
            return
        
        print("\n" + "="*50)
        print("         RESUMEN GENERAL DE VENTAS")
        print("="*50)
        
        # Métricas básicas
        total_ventas = len(self.ventas)
        total_clientes = len(self.clientes)
        total_productos = len(self.productos)
        monto_total = self.detalle_ventas['importe'].sum()
        
        print(f"• Total de ventas registradas: {total_ventas}")
        print(f"• Total de clientes: {total_clientes}")
        print(f"• Total de productos: {total_productos}")
        print(f"• Monto total vendido: ${monto_total:,.2f}")
        
        # Período de análisis
        fecha_min = self.ventas['fecha'].min().strftime('%d/%m/%Y')
        fecha_max = self.ventas['fecha'].max().strftime('%d/%m/%Y')
        print(f"• Período analizado: {fecha_min} - {fecha_max}")
        
        # Ventas por mes
        ventas_mes = self.ventas.groupby(self.ventas['fecha'].dt.month).size()
        print(f"• Ventas por mes: {dict(ventas_mes)}")
    
    def productos_mas_vendidos(self, top_n=10):
        """Muestra los productos más vendidos"""
        if not self.datos_cargados:
            print("Primero debe cargar los datos (Opción 1)")
            return
        
        print(f"\n{'='*50}")
        print(f"      TOP {top_n} PRODUCTOS MÁS VENDIDOS")
        print(f"{'='*50}")
        
        productos_vendidos = self.detalle_ventas.groupby('nombre_producto').agg({
            'cantidad': 'sum',
            'importe': 'sum'
        }).sort_values('cantidad', ascending=False).head(top_n)
        
        for i, (producto, datos) in enumerate(productos_vendidos.iterrows(), 1):
            print(f"{i:2d}. {producto:<30} | Cantidad: {datos['cantidad']:>4.0f} | Total: ${datos['importe']:>10,.2f}")
    
    def ventas_por_categoria(self):
        """Analiza ventas por categoría de productos"""
        if not self.datos_cargados:
            print("Primero debe cargar los datos (Opción 1)")
            return
        
        # Unir detalle_ventas con productos para obtener categorías
        ventas_categoria = pd.merge(
            self.detalle_ventas,
            self.productos[['id_producto', 'categoria']],
            on='id_producto',
            how='left'
        )
        
        resumen_categoria = ventas_categoria.groupby('categoria').agg({
            'cantidad': 'sum',
            'importe': 'sum',
            'id_venta': 'nunique'
        }).round(2)
        
        print(f"\n{'='*50}")
        print("       VENTAS POR CATEGORÍA")
        print(f"{'='*50}")
        
        for categoria, datos in resumen_categoria.iterrows():
            print(f"• {categoria}:")
            print(f"  - Ventas: {datos['id_venta']}")
            print(f"  - Unidades: {datos['cantidad']}")
            print(f"  - Monto: ${datos['importe']:,.2f}")
            print()
    
    def clientes_activos(self, top_n=10):
        """Identifica los clientes más activos"""
        if not self.datos_cargados:
            print("Primero debe cargar los datos (Opción 1)")
            return
        
        clientes_activos = self.ventas_completas.groupby(['id_cliente', 'nombre_cliente']).agg({
            'id_venta': 'nunique',
            'importe': 'sum'
        }).sort_values('importe', ascending=False).head(top_n)
        
        print(f"\n{'='*50}")
        print(f"      TOP {top_n} CLIENTES MÁS ACTIVOS")
        print(f"{'='*50}")
        
        for i, ((cliente_id, nombre), datos) in enumerate(clientes_activos.iterrows(), 1):
            print(f"{i:2d}. {nombre:<25} | Compras: {datos['id_venta']:>2} | Total: ${datos['importe']:>10,.2f}")
    
    def metodos_pago_populares(self):
        """Analiza los métodos de pago más utilizados"""
        if not self.datos_cargados:
            print("Primero debe cargar los datos (Opción 1)")
            return
        
        metodos_pago = self.ventas.groupby('medio_pago').agg({
            'id_venta': 'count',
            'id_cliente': 'nunique'
        }).sort_values('id_venta', ascending=False)
        
        print(f"\n{'='*50}")
        print("       MÉTODOS DE PGO MÁS POPULARES")
        print(f"{'='*50}")
        
        total_ventas = metodos_pago['id_venta'].sum()
        
        for metodo, datos in metodos_pago.iterrows():
            porcentaje = (datos['id_venta'] / total_ventas) * 100
            print(f"• {metodo:<15}: {datos['id_venta']:>3} ventas ({porcentaje:.1f}%) | {datos['id_cliente']} clientes únicos")
    
    def ventas_por_mes(self):
        """Muestra la evolución de ventas por mes"""
        if not self.datos_cargados:
            print("Primero debe cargar los datos (Opción 1)")
            return
        
        ventas_mes = self.ventas_completas.groupby(
            self.ventas_completas['fecha'].dt.month
        ).agg({
            'importe': 'sum',
            'id_venta': 'nunique',
            'cantidad': 'sum'
        })
        
        meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 
            4: 'Abril', 5: 'Mayo', 6: 'Junio'
        }
        
        print(f"\n{'='*50}")
        print("         VENTAS POR MES")
        print(f"{'='*50}")
        
        for mes, datos in ventas_mes.iterrows():
            nombre_mes = meses.get(mes, f'Mes {mes}')
            print(f"• {nombre_mes:<10}: {datos['id_venta']:>2} ventas | ${datos['importe']:>10,.2f} | {datos['cantidad']:>3} unidades")
    
    def ejecutar_analisis_completo(self):
        """Ejecuta todos los análisis disponibles"""
        if not self.datos_cargados:
            if not self.cargar_datos():
                return
        
        self.resumen_general()
        self.ventas_por_mes()
        self.productos_mas_vendidos()
        self.ventas_por_categoria()
        self.clientes_activos()
        self.metodos_pago_populares()

def main():
    analizador = AnalizadorVentas()
    
    while True:
        print("\n" + "="*60)
        print("       SISTEMA DE ANÁLISIS DE VENTAS")
        print("="*60)
        print("1. Cargar datos de ventas")
        print("2. Resumen general")
        print("3. Productos más vendidos")
        print("4. Ventas por categoría")
        print("5. Clientes más activos")
        print("6. Métodos de pago populares")
        print("7. Ventas por mes")
        print("8. Análisis completo")
        print("9. Salir")
        print("-"*60)
        
        opcion = input("Seleccione una opción (1-9): ").strip()
        
        if opcion == '1':
            analizador.cargar_datos()
        elif opcion == '2':
            analizador.resumen_general()
        elif opcion == '3':
            try:
                top = int(input("¿Cuántos productos mostrar? (default 10): ") or "10")
                analizador.productos_mas_vendidos(top)
            except ValueError:
                analizador.productos_mas_vendidos()
        elif opcion == '4':
            analizador.ventas_por_categoria()
        elif opcion == '5':
            try:
                top = int(input("¿Cuántos clientes mostrar? (default 10): ") or "10")
                analizador.clientes_activos(top)
            except ValueError:
                analizador.clientes_activos()
        elif opcion == '6':
            analizador.metodos_pago_populares()
        elif opcion == '7':
            analizador.ventas_por_mes()
        elif opcion == '8':
            analizador.ejecutar_analisis_completo()
        elif opcion == '9':
            print("¡Gracias por usar el sistema de análisis!")
            break
        else:
            print("Opción no válida. Por favor, seleccione 1-9.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
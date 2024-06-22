from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Cargar datos desde los archivos Excel
venta = pd.read_excel("data/VENTA.xlsx")
tiempo = pd.read_excel("data/TIEMPO.xlsx")
producto = pd.read_excel("data/PRODUCTO.xlsx")

# Convertir FE_REGISTRO a tipo datetime y unir tablas
ventas_tiempo = pd.merge(venta, tiempo, on='COD_TIEMPO')
ventas_productos = pd.merge(ventas_tiempo, producto, on='COD_PRODUCTO')

# Agrupar ventas por mes y producto
ventas_agrupadas = ventas_productos.groupby(['NOMBRE MES', 'PRODUCTO'])['CANTIDAD'].sum().reset_index()

# Añadir opción de 'Todos' los meses
opciones_meses = list(ventas_agrupadas['NOMBRE MES'].unique())
opciones_meses.insert(0, 'Todos')

def mostrar_grafico_barras(NOMBRE_MES):
    if NOMBRE_MES == 'Todos':
        datos = ventas_agrupadas.groupby('PRODUCTO')['CANTIDAD'].sum().reset_index().nlargest(10, 'CANTIDAD')
        titulo = 'Top 10 Productos más Vendidos - Todos los Meses'
    else:
        datos = ventas_agrupadas[ventas_agrupadas['NOMBRE MES'] == NOMBRE_MES].nlargest(10, 'CANTIDAD')
        titulo = f'Top 10 Productos más Vendidos - {NOMBRE_MES}'

    if not datos.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(datos['PRODUCTO'], datos['CANTIDAD'], color='skyblue')
        ax.set_xlabel('Producto')
        ax.set_ylabel('Cantidad Vendida')
        ax.set_title(titulo)
        plt.xticks(rotation=90)

        # Convertir el gráfico a un HTML/JavaScript interactivo
        buf = BytesIO()
        plt.savefig(buf, format='png')
        data = base64.b64encode(buf.getbuffer()).decode('ascii')
        plt.close(fig)
        return data
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html', meses=opciones_meses)

@app.route('/show_top_products_chart', methods=['POST'])
def show_top_products_chart():
    NOMBRE_MES = request.form['NOMBRE_MES']
    chart_data = mostrar_grafico_barras(NOMBRE_MES)
    return render_template('index.html', chart_data=chart_data, meses=opciones_meses)

if __name__ == '__main__':
    app.run(debug=True)

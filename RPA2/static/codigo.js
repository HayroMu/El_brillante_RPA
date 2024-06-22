// Obtener referencia al elemento HTML donde se mostrará el gráfico
var topProductsChartContainer = document.getElementById('top_products_chart');

// Función para actualizar el gráfico de Top 10 Productos
function updateTopProductsChart(selectedMonth) {
  // Llama a la función Python 'mostrar_grafico_barras' y obtén la imagen del gráfico
  $.ajax({
    url: '/show_top_products_chart',
    data: { NOMBRE_MES: selectedMonth },
    type: 'POST',
    success: function(data) {
      // Actualiza el contenido del elemento HTML con la imagen del gráfico
      topProductsChartContainer.innerHTML = data;
    },
    error: function(xhr, status, error) {
      console.error('Error al cargar el gráfico:', error);
    }
  });
}

// Agrega un event listener al widget de selección de mes
var monthSelect = document.getElementById('mes_seleccionado');
monthSelect.addEventListener('change', function() {
  var selectedMonth = this.value;
  updateTopProductsChart(selectedMonth);
});

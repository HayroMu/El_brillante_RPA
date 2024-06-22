document.addEventListener('DOMContentLoaded', function() {
  // Obtener referencia al elemento HTML donde se mostrará el gráfico dinámico
  var dynamicChartContainer = document.getElementById('dynamicChartContainer');

  // Función para actualizar el gráfico dinámico
  function updateDynamicChart(selectedMonth) {
    // Llama a la función Python 'mostrar_grafico_barras' y obtén la imagen del gráfico
    $.ajax({
      url: '/show_dynamic_chart', // Ruta en tu aplicación Flask para obtener el gráfico dinámico
      data: { NOMBRE_MES: selectedMonth },
      type: 'POST',
      success: function(data) {
        // Crea un nuevo elemento <img> y actualiza su src con la imagen del gráfico
        var img = new Image();
        img.src = 'data:image/png;base64,' + data; // data es la imagen codificada en base64 recibida desde Flask
        img.alt = 'Gráfico dinámico';
        
        // Limpia el contenido anterior y agrega el nuevo <img> al contenedor
        dynamicChartContainer.innerHTML = '';
        dynamicChartContainer.appendChild(img);
      },
      error: function(xhr, status, error) {
        console.error('Error al cargar el gráfico dinámico:', error);
      }
    });
  }

  // Agrega un event listener al widget de selección de mes
  var monthSelect = document.getElementById('opcionesMeses'); // Asegúrate de que coincida con el id en tu HTML
  monthSelect.addEventListener('change', function() {
    var selectedMonth = this.value;
    updateDynamicChart(selectedMonth);
  });
});

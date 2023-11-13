Highcharts.chart('container_hinchas', {
  chart: {
    type: 'bar',
    width: 800,  // Ajusta según sea necesario
    height: 1000  // Ajusta según sea necesario
  },
  title: {
    text: 'Frecuencia de Deportes',
    style: {
      fontSize: '30px'
    }
  },
  xAxis: {
    type: 'linear',
    categories: [],
    labels: {
        formatter: function () {
            // Muestra todas las etiquetas
            return this.value;
        },
        style: {
            fontSize: '10px'
        }
    }
  },
  yAxis: {
    title: {
      text: 'Frecuencia'
    },
    type: 'linear'
  },
  series: [{
    name: 'Frecuencias',
    data: []
  }]
});



fetch("http://localhost:5000/get_stats_data_hinchas")
.then((response) => response.json())
.then((data) => {

  // tomamos los nombres
  let names = data.map((item) => item[0])
  console.log(data)

  // tomamos las frecuencias
  let frequencies = data.map((item) => item[1])


  // Actualizar el gráfico con los nuevos datos names y frequencies

  // Get the chart by ID
  const chart = Highcharts.charts.find(
    (chart) => chart && chart.renderTo.id === "container_hinchas"
  );

  chart.update({
      xAxis: {
          categories: names
      },
      series: [{
          data: frequencies
      }]
  });

})
.catch((error) => console.error("Error:", error));
Highcharts.chart('container_artesanias', {
    chart: {
      type: 'bar',
      width: 800,  // Ajusta según sea necesario
      height: 500  // Ajusta según sea necesario
    },
    title: {
      text: 'Frecuencia de Artesanías',
      style: {
        fontSize: '30px'
      }
    },
    xAxis: {
      categories: []
    },
    yAxis: {
      title: {
        text: 'Frecuencia'
      }
    },
    series: [{
      name: 'Frecuencia',
      data: []
    }]
  });

  

  fetch("http://localhost:5000/get_stats_data_artesanos")
  .then((response) => response.json())
  .then((data) => {

    // tomamos los nombres
    let names = data.map((item) => item[0])


    // tomamos las frecuencias
    let frequencies = data.map((item) => item[1])


    // Actualizar el gráfico con los nuevos datos names y frequencies

    // Get the chart by ID
    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "container_artesanias"
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
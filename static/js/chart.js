// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

var ctx = document.getElementById("filterusagechart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"],
    datasets: [{
      label: "Filter Usage",
      lineTension: 0.3,
      backgroundColor: "rgba(78, 115, 223, 0.05)",
      borderColor: "rgba(78, 115, 223, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: ['0', '0', '0', '0', '20', '60', '60', '60', '60', '10', '0', '0', '0', '0', '0', '0', '0', '1', '60', '50', '0'],
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'hour'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + tooltipItem.yLabel + ' mins';
        }
      }
    }
  }
});

var ctx = document.getElementById("temperaturecharttt");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"],
    datasets: [
    {
      label: "Air Temperature",
      lineTension: 0.3,
      backgroundColor: "rgba(133, 135, 150, 0.05)",
      borderColor: "rgba(133, 135, 150, 1)",
      pointRadius: 3,
      pointBackgroundColor: "rgba(133, 135, 150, 1)",
      pointBorderColor: "rgba(133, 135, 150, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(133, 135, 150, 1)",
      pointHoverBorderColor: "rgba(133, 135, 150, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
      data: ['12', '12', '10', '10', '10', '9', '9', '7', '9', '9', '10', '12', '12', '16', '16', '16', '16', '16', '14', '12', '10'],
    },
    {
        label: "Pool Temperature",
        lineTension: 0.3,
        backgroundColor: "rgba(28, 200, 138, 0.05)",
        borderColor: "rgba(28, 200, 138, 1)",
        pointRadius: 3,
        pointBackgroundColor: "rgba(28, 200, 138, 1)",
        pointBorderColor: "rgba(28, 200, 138, 1)",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(28, 200, 138, 1)",
        pointHoverBorderColor: "rgba(28, 200, 138, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: ['40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '41', '41', '41', '41', '41', '41', '41', '41'],
      }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 0,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'hour'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          maxTicksLimit: 5,
          padding: 10
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: true
    },
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + tooltipItem.yLabel + 'º F';
        }
      }
    }
  }
});

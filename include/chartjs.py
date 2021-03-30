from pychartjs import BaseChart, ChartType, Color, Options                                

class LineGraph(BaseChart):

    type = ChartType.Line

    class labels:
        grouped = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]

    class data:
        class AirTemperature:
            label = 'Air Temperature'
            lineTension = 0.3
            backgroundColor = "rgba(133, 135, 150, 0.05)"
            borderColor = "rgba(133, 135, 150, 1)"
            pointRadius = 3
            pointBackgroundColor = "rgba(133, 135, 150, 1)"
            pointBorderColor = "rgba(133, 135, 150, 1)"
            pointHoverRadius = 3
            pointHoverBackgroundColor = "rgba(133, 135, 150, 1)"
            pointHoverBorderColor = "rgba(133, 135, 150, 1)"
            pointHitRadius = 10
            pointBorderWidth = 2
            data = []
        
    class options:
        maintainAspectRatio = False
        
        layout = {
            'padding': {
                'left': 10,
                'right': 25,
                'top': 0,
                'bottom': 0
            }
        }

        scales = {
            'xAxes': [{
                'time': {
                'unit': 'hour'
                },
                'gridLines': {
                'display': False,
                'drawBorder': False
                },
                'ticks': {
                'maxTicksLimit': 7
                }
            }],
            'yAxes': [{
                'ticks': {
                'maxTicksLimit': 5,
                'padding': 10
                },
                'gridLines': {
                'color': "rgb(234, 236, 244)",
                'zeroLineColor': "rgb(234, 236, 244)",
                'drawBorder': False,
                'borderDash': [2],
                'zeroLineBorderDash': [2]
                }
            }],
        }

        legend = { 'display': True }

        tooltips = {
            'backgroundColor': "rgb(255,255,255)",
            'bodyFontColor': "#858796",
            'titleMarginBottom': 10,
            'titleFontColor': '#6e707e',
            'titleFontSize': 14,
            'borderColor': '#dddfeb',
            'borderWidth': 1,
            'xPadding': 15,
            'yPadding': 15,
            'displayColors': False,
            'intersect': False,
            'mode': 'index',
            'caretPadding': 10,
        }

    class pluginOptions:
        pass
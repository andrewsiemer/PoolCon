from pychartjs import BaseChart, ChartType, Color, Options                                

class PumpGraph(BaseChart):

    type = ChartType.Line

    class labels:
        grouped = []

    class data:
        class PumpUsage:
            label = 'Pump Usage'
            lineTension = 0.3
            backgroundColor = "rgba(78, 115, 223, 0.05)"
            borderColor = "rgba(78, 115, 223, 1)"
            pointRadius = 3
            pointBackgroundColor = "rgba(78, 115, 223, 1)"
            pointBorderColor = "rgba(78, 115, 223, 1)"
            pointHoverRadius = 3
            pointHoverBackgroundColor = "rgba(78, 115, 223, 1)"
            pointHoverBorderColor = "rgba(78, 115, 223, 1)"
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

class TempGraph(BaseChart):

    type = ChartType.Line

    class labels:
        grouped = []

    class data:
        class PoolTemperature:
            label = 'Pool Temperature'
            lineTension = 0.3
            backgroundColor = "rgba(28, 200, 138, 0.05)"
            borderColor = "rgba(28, 200, 138, 1)"
            pointRadius = 3
            pointBackgroundColor = "rgba(28, 200, 138, 1)"
            pointBorderColor = "rgba(28, 200, 138, 1)"
            pointHoverRadius = 3
            pointHoverBackgroundColor = "rgba(28, 200, 138, 1)"
            pointHoverBorderColor = "rgba(28, 200, 138, 1)"
            pointHitRadius = 10
            pointBorderWidth = 2
            data = []

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
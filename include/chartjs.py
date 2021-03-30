from pychartjs import BaseChart, ChartType, Color                                     

class LineGraph(BaseChart):

    type = ChartType.Line

    class labels:
        grouped = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]

    class data:
        label = "Numbers"
        data = ['12', '12', '10', '10', '10', '9', '9', '7', '9', '9', '10', '12', '12', '16', '16', '16', '16', '16', '14', '12', '10']
    
    class options:
        pass

    class pluginOptions:
        pass
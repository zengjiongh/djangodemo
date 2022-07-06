from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    return render(request, "chart_list.html")


def chart_Bar(request):
    legend_data = ['花桥', "曾继榕"]
    x_axis = ['一月', '二月', '三月', '四月', "五月", '六月']

    series_list = [
        {
            "name": '花桥',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '曾继榕',
            "type": 'bar',
            "data": [15, 40, 66, 40, 50, 40],
        }
    ]

    restult = {
        "status": True,
        "data": {
            "legend": legend_data,
            "x_axis": x_axis,
            "series_list": series_list
        }
    }

    return JsonResponse(restult)


def chart_Pie(request):
    db_data_list = [
        {"value": 1048, "name": 'IT'},
        {"value": 735, "name": '运营'},
        {"value": 580, "name": '新媒体'},
        {"value": 484, "name": '运维'},
        {"value": 300, "name": "测试"}
    ]
    result = {
        "status": True,
        "data": db_data_list
    }

    return JsonResponse(result)


def chart_Line(request):
    series_list = [
        {
            "name": "本季度",
            "data": [10, 22, 28, 43, 49],
            "type": 'line',
            "stack": 'x',
            "smooth": "true"
        },
        {
            "name": "上季度",
            "data": [5, 4, 3, 5, 10],
            "type": 'line',
            "stack": 'x',
            "smooth": "true"
        }
    ]
    legend_data = ["本季度", "上季度"]
    x_axis = ['话费', '宽带', '彩信', '流量', '基站']

    result = {
        "status": True,
        "data": {
            "legend_data": legend_data,
            "series_list": series_list,
            "x_axis": x_axis
        },
    }
    return JsonResponse(result)

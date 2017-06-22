# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string

from django.shortcuts import render


def get(req, key, default):
    try:
        return req.GET[key]
    except:
        return default


def view_current(req):
    return render(req, "view_current.html")


def view_history_cpu(req):
    return render(req, "view_history_info.html", context={
        "title": "CPU用量查看",
        "div_name": "cpu_usage",
        "chart_title": "CPU用量",
        "data_legend": "CPU(%)",
        "api_name": "/api/history/cpu/sum",
    })


def view_history_memory_virtual(req):
    return render(req, "view_history_info.html", context={
        "title": "内存用量查看",
        "div_name": "ram_usage",
        "chart_title": "内存用量",
        "data_legend": "RAM(%)",
        "api_name": "/api/history/memory/virtual",
    })


def view_history_memory_swap(req):
    return render(req, "view_history_info.html", context={
        "title": "交换内存用量查看",
        "div_name": "swap_ram_usage",
        "chart_title": "交换内存用量",
        "data_legend": "RAM(%)",
        "api_name": "/api/history/memory/swap",
    })


def view_history_cpu_single(req):
    index = string.atoi(get(req, "cpuid", "0"))
    return render(req, "view_history_info.html", context={
        "title": "CPU [%d] 用量查看" % index,
        "div_name": "swap_ram_usage",
        "chart_title": "CPU[%d]" % index,
        "data_legend": "Usage(%)",
        "api_name": "/api/history/cpu/single?cpuid=%d" % index,
    })


def view_main(req):
    return render(req, "index_page.html")


def view_current_lite(req):
    return render(req, "view_current_table.html")


def view_current_disk(req):
    return render(req, "view_current_disk.html")

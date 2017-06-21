# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import psutil
import string
import json
import psycopg2
from DBUtils.PooledDB import PooledDB
from django.http import HttpResponse

dbPool = PooledDB(psycopg2, 5,
                  host="192.168.1.103",
                  port=5432,
                  database="monitor",
                  user="postgres",
                  password="979323")


def get(req, key, default):
    try:
        return req.GET[key]
    except:
        return default


def current_cpu_sum(request):
    interval = string.atof(get(request, "interval", "4"))
    return HttpResponse("%f" % psutil.cpu_percent(interval))


def current_cpu_single(request):
    interval = string.atof(get(request, "interval", "4"))
    return HttpResponse(json.dumps(psutil.cpu_percent(interval, percpu=True)))


def current_memory(request):
    meminfo = psutil.virtual_memory()
    swap_meminfo = psutil.swap_memory()
    response_info = {
        "total_memory": meminfo.total,
        "used_memory": meminfo.used,
        "total_swap": swap_meminfo.total,
        "used_swap": swap_meminfo.used
    }
    return HttpResponse(json.dumps(response_info))


def current_list_disk(request):
    response_info = dict()
    disk_parts = [d.device for d in filter(lambda x: x.opts != 'cdrom', psutil.disk_partitions())]
    return HttpResponse(json.dumps(disk_parts))


def current_all_disk(request):
    response_info = dict()
    disk_parts = filter(lambda x: x.opts != 'cdrom', psutil.disk_partitions())
    for disk in disk_parts:
        disk_use = psutil.disk_usage(disk.mountpoint)
        response_info[disk.device] = {
            "total": disk_use.total,
            "used": disk_use.used,
        }
    return HttpResponse(json.dumps(response_info))


def current_query_disk(request):
    try:
        disk_name = request.GET["device"]
        disks = filter(lambda x: x.device == disk_name, psutil.disk_partitions())
        disk_use = psutil.disk_usage(disks[0].device)
        return HttpResponse(json.dumps({
            "total": disk_use.total,
            "used": disk_use.used,
        }))
    except Exception as ex:
        return HttpResponse(json.dumps({
            "status": "error",
            "error_info": ex.message
        }))


def history_cpu_sum(request):
    conn = dbPool.connection()
    try:
        default_start = datetime.datetime.now() - datetime.timedelta(days=1)
        query_start = get(request, "start", default_start.strftime("%Y-%m-%d %H:%M:%S"))
        sql_cmd = "SELECT tick, usage FROM public.cpu WHERE tick>='%s' ORDER BY tick" % query_start
        cur = conn.cursor()
        cur.execute(sql_cmd)
        query_result = cur.fetchall()
        cur.close()
        return HttpResponse(json.dumps({
            "tick": [row[0].strftime("%Y-%m-%d %H:%M:%S") for row in query_result],
            "data": [row[1] for row in query_result]
        }))
    except Exception as ex:
        return HttpResponse(json.dumps({
            "status": "error",
            "error_info": ex.message
        }))
    finally:
        conn.close()


def history_memory_virtual(request):
    conn = dbPool.connection()
    try:
        default_start = datetime.datetime.now() - datetime.timedelta(days=1)
        query_start = get(request, "start", default_start.strftime("%Y-%m-%d %H:%M:%S"))
        sql_cmd = "SELECT tick, precent FROM public.memory_view WHERE tick>='%s' ORDER BY tick" % query_start
        cur = conn.cursor()
        cur.execute(sql_cmd)
        query_result = cur.fetchall()
        cur.close()
        return HttpResponse(json.dumps({
            "tick": [row[0].strftime("%Y-%m-%d %H:%M:%S") for row in query_result],
            "data": [row[1] for row in query_result]
        }))
    except Exception as ex:
        return HttpResponse(json.dumps({
            "status": "error",
            "error_info": ex.message
        }))
    finally:
        conn.close()


def history_memory_swap(request):
    conn = dbPool.connection()
    try:
        default_start = datetime.datetime.now() - datetime.timedelta(days=1)
        query_start = get(request, "start", default_start.strftime("%Y-%m-%d %H:%M:%S"))
        sql_cmd = "SELECT tick, swap_precent FROM public.memory_view WHERE tick>='%s' ORDER BY tick" % query_start
        cur = conn.cursor()
        cur.execute(sql_cmd)
        query_result = cur.fetchall()
        cur.close()
        return HttpResponse(json.dumps({
            "tick": [row[0].strftime("%Y-%m-%d %H:%M:%S") for row in query_result],
            "data": [row[1] for row in query_result]
        }))
    except Exception as ex:
        return HttpResponse(json.dumps({
            "status": "error",
            "error_info": ex.message
        }))
    finally:
        conn.close()


def history_cpu_single(request):
    conn = dbPool.connection()
    try:
        default_start = datetime.datetime.now() - datetime.timedelta(days=1)
        query_start = get(request, "start", default_start.strftime("%Y-%m-%d %H:%M:%S"))
        index = string.atoi(get(request, "cpuid", "0"))
        sql_cmd = "SELECT tick, usage_detail[%d] FROM public.cpu WHERE tick>='%s' ORDER BY tick" % (index, query_start)
        cur = conn.cursor()
        cur.execute(sql_cmd)
        query_result = cur.fetchall()
        cur.close()
        return HttpResponse(json.dumps({
            "tick": [row[0].strftime("%Y-%m-%d %H:%M:%S") for row in query_result],
            "data": [row[1] for row in query_result]
        }))
    except Exception as ex:
        return HttpResponse(json.dumps({
            "status": "error",
            "error_info": ex.message
        }))
    finally:
        conn.close()

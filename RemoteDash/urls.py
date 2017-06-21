"""RemoteDash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from apis.views import *
from frontend_render.views import *

urlpatterns = [
    url(r'^api/current/cpu/sum', current_cpu_sum),
    url(r'^api/current/cpu/single', current_cpu_single),

    url(r'^api/current/memory', current_memory),

    url(r'^api/current/disk/all', current_all_disk),
    url(r'^api/current/disk/list', current_list_disk),
    url(r'^api/current/disk/query', current_query_disk),

    url(r'^api/history/cpu/single', history_cpu_single),
    url(r'^api/history/cpu/sum', history_cpu_sum),

    url(r'^api/history/memory/virtual', history_memory_virtual),
    url(r'^api/history/memory/swap', history_memory_swap),

    url(r'^view/current', view_current),

    url(r'^view/history/cpu/single', view_history_cpu_single),
    url(r'^view/history/cpu', view_history_cpu),

    url(r'^view/history/memory/virtual', view_history_memory_virtual),
    url(r'^view/history/memory/swap', view_history_memory_swap),

    url(r'^admin/', admin.site.urls),
    url(r'^', view_main),
]

"""
url(r'^api/history/cpu/single', history_cpu_single),
url(r'^api/history/disk/query', history_query_disk),
"""
from django.conf.urls import url

from . import views

app_name = 'db'

urlpatterns = [

    url(r'^print', views.print_query),
    url(r'^get', views.query_db),
    url(r'^set', views.upd),
]
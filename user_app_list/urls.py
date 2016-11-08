from django.conf.urls import url

from user_app_list.views import index

urlpatterns = [
    url(r'^', index, name="index")
]
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.UploadJSONView.as_view(), name="upload"),
    path("list/", views.RecordListView.as_view(), name="list"),
]

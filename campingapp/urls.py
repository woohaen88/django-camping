from django.urls import path
from .views import CampingListView, CampingDetailView

app_name = "campingapp"
urlpatterns = [
    path("", CampingListView.as_view(), name="index"),
    path("detail/<int:pk>/", CampingDetailView.as_view(), name="detail"),
]

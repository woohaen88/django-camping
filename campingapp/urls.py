from django.urls import path
from .views import (
    CampingListView,
    CampingDetailView,
    CampingPostCreateView,
    CampingUpdateView,
    category_page,
    tag_page,
    new_comment,
    CommentUpdateView,
    delete_comment,
    CampingSearch,
)

app_name = "campingapp"
urlpatterns = [
    path("", CampingListView.as_view(), name="index"),
    path("detail/<int:pk>/", CampingDetailView.as_view(), name="detail"),
    path("create/", CampingPostCreateView.as_view(), name="create"),
    path("update/<int:pk>/", CampingUpdateView.as_view(), name="update"),
    path("category/<str:slug>/", category_page, name="slug"),
    path("tag/<str:slug>/", tag_page, name="tag_page"),
    path("<int:pk>/new_comment/", new_comment, name="new_comment"),
    path(
        "updated_comment/<int:pk>/", CommentUpdateView.as_view(), name="update_comment"
    ),
    path("delete_comment/<int:pk>/", delete_comment, name="delete_comment"),
]

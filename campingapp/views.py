from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class CampingListView(ListView):
    template_name = "index.html"
    model = Post
    context_object_name = "post_list"
    ordering = "-updated_at"


class CampingDetailView(DetailView):
    template_name = "detail.html"
    model = Post
    context_object_name = "post"

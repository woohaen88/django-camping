from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
)
from .models import (
    Post,
    Category,
    Tag,
    Comment,
)
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin


class CampingListView(ListView):
    template_name = "index.html"
    model = Post
    context_object_name = "post_list"
    ordering = "-updated_at"

    def get_context_data(self, **kwargs):
        context = super(CampingListView, self).get_context_data()
        context["categories"] = Category.objects.all()
        return context


class CampingDetailView(DetailView):
    template_name = "detail.html"
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super(CampingDetailView, self).get_context_data()
        context["categories"] = Category.objects.all()
        # context["no_category_post_count"] = Post.objects.filter(category=None).count()
        context["comment_form"] = CommentForm
        return context


class CampingPostCreateView(LoginRequiredMixin, CreateView):
    template_name = "create.html"
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("campingapp:index")

    def form_valid(self, form):
        user = self.request.user
        if user.is_authenticated:
            form.instance.author = user
            return super(CampingPostCreateView, self).form_valid(form)
        else:
            return redirect("campingapp:create")


class CampingUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "update.html"

    def get_success_url(self):
        post_pk = self.kwargs["pk"]
        # success_url = reverse("campingapp:detail", kwargs={"pk": post_pk})
        success_url = reverse("campingapp:index")
        return success_url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CampingUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category)

    context = {
        "post_list": post_list,
        "categories": Category.objects.all(),
        "category": category,
    }

    return render(request, "index.html", context=context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        "post_list": post_list,
        "tag": tag,
        "categories": Category.objects.all(),
    }
    return render(request, "index.html", context=context)


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(reverse("campingapp:detail", kwargs={"pk": pk}))
        else:
            return redirect(reverse("campingapp:detail", kwargs={"pk": pk}))
    else:
        raise PermissionDenied


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment_update.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(reverse("campingapp:detail", kwargs={"pk": pk}))
    else:
        raise PermissionDenied


class CampingSearch(CampingListView):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs["q"]
        camping_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return camping_list

    def get_context_data(self, **kwargs):
        context = super(CampingSearch, self).get_context_data()
        q = self.kwargs["q"]
        context["search_info"] = f"Search: {q} ({self.get_queryset().count()})"

        return context

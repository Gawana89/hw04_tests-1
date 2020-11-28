from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "index.html", {"page": page, "paginator": paginator}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {"group": group, "page": page, "paginator": paginator}
    return render(request, "group.html", context)


@login_required
def new_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("index")

    context = {
        "form": form,
        "is_new_post": True,
    }
    return render(request, "new.html", context)


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    post = user_profile.posts.all()
    paginator = Paginator(post, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    is_author = request.user == user_profile
    return render(
        request,
        "profile.html",
        {
            "page": page,
            "paginator": paginator,
            "is_author": is_author,
        },
    )


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_author = request.user == post.author
    return render(
        request,
        "post.html",
        {
            "post": post,
            "is_author": is_author,
        },
    )


@login_required
def post_edit(request, username, post_id):
    obj = get_object_or_404(Post, id=post_id)

    if obj.author != request.user:
        return redirect("post", username, post_id)

    form = PostForm(request.POST or None, instance=obj)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect("post", username, post_id)

    context = {
        "form": form,
        "post": obj,
    }
    return render(request, "new.html", context)

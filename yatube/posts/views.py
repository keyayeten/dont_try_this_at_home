from django.shortcuts import render
from .models import Post, Group
from django.shortcuts import get_object_or_404

# Create your views here.


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    num_of_posts = 10
    group = get_object_or_404(Group, slug=slug)
    related_name = group
    posts = Post.objects.filter(group=related_name).order_by('-pub_date')[:num_of_posts]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)

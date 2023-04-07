from django.shortcuts import render
from .models import Post, Group
from django.shortcuts import get_object_or_404


# Create your views here.
NUM_OF_POSTS = 10


def index(request):
    posts = Post.objects.order_by('-pub_date')[:NUM_OF_POSTS]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    posts = posts.order_by('-pub_date')[:NUM_OF_POSTS]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)

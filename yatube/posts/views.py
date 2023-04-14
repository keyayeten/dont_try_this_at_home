from django.shortcuts import render
from .models import Post, Group
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# Create your views here.
NUM_OF_POSTS = 10


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, NUM_OF_POSTS)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.all()
    posts = posts.order_by('-pub_date')

    paginator = Paginator(posts, NUM_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)

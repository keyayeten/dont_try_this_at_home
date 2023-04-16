from django.shortcuts import render
from .models import Post, Group, User
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


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    user_id = User.objects.get(username=username).id
    user_posts = Post.objects.all().filter(author=user_id)

    paginator = Paginator(user_posts, NUM_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'name': username,
        'page_obj': page_obj,
        'post_count': len(user_posts),
        'id': user_id,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = Post.objects.get(pk=post_id)
    user_id = User.objects.get(username=post.author).id
    user_posts = Post.objects.all().filter(author=user_id)

    context = {
        'post': post,
        'count': len(user_posts)
    }
    return render(request, 'posts/post_detail.html', context)

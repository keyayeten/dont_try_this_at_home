from django.shortcuts import render, redirect
from .models import Post, Group, User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .forms import PostForm
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


def post_create(request):
    username = User.objects.get(pk=request.user.id)
    author_id = request.user.id

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{username}/')
    else:
        initial_data = {'author': username}
        form = PostForm(initial=initial_data)
    return render(request, 'posts/create_post.html', {'form': form,
                                                      'author': username,
                                                      'is_edit': False
                                                      })


def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.id != post.author.id:
        return redirect(f'/posts/{post_id}/')

    author_id = request.user.id
    username = post.author.get_full_name
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{username}/')
    else:
        initial_data = {'author': post.author, 'text': post.text, 'group': post.group}
        form = PostForm(initial=initial_data)

    return render(request, 'posts/create_post.html', {'form': form,
                                                      'author': username,
                                                      'is_edit': True
                                                      })
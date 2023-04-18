# posts/urls.py
from django.urls import path

from . import views
app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='create_post'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='edit_post')
]

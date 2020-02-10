from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog', views.blog_list, name='blog_list'),
    path('my-post', views.user_post, name='user_post'),
    path('post-create', views.post_create, name='post_create'),
    path('post-detail/<slug:slug>/', views.post_detail, name='post_detail'),
    #path('post-detail/<int:id>/', views.post_detail, name='post_detail'),
    path('post-update/<slug:slug>/', views.post_update, name='post_update'),
    path('post-delete/<slug:slug>/', views.post_delete, name='post_delete'),
    path('post-search', views.post_search, name='post_search'),
    path('tinymce/', include('tinymce.urls')),
]

# -------------------class base view--------------------------
""""
    path('', IndexView.as_view(), name='home'),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('search/', search, name='search'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete')
"""

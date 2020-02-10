from blog.api.views import(
    api_detail_blog_view,
    api_update_blog_view,
    api_delete_blog_view,
    api_create_blog_view,
    PostListApiView,
    # api_is_author_of_blogpost,
    # ApiBlogListView
)
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('detail/<id>', api_detail_blog_view, name="detail"),
    path('update/<id>', api_update_blog_view, name="update"),
    path('delete/<id>', api_delete_blog_view, name="delete"),
    path('create', api_create_blog_view, name="create"),
    path('blog-list', PostListApiView.as_view(), name="blog_list"),
    #path('list', ApiBlogListView.as_view(), name="list"),
    #path('<slug>/is_author', api_is_author_of_blogpost, name="is_author"),
]

from django.contrib import admin

#from .models import Author, Category, Post, Comment
from .models import Author, Category, Post, Comment, PostView


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'overview', 'timestamp', 'status', 'author')
    prepopulated_fields = {'slug': ('title',)}  # new


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostView)

from tinymce.models import HTMLField
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from autoslug import AutoSlugField

User = get_user_model()


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class PostView(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    profile_picture = models.ImageField(
        upload_to='blog/', blank=True, null=True)
    about_author = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    #slug = AutoSlugField(populate_from='title', blank=True)
    slug = models.SlugField(blank=True, null=True)
    overview = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    #updated_on = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(choices=STATUS, default=0)

    #timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    #comment_count = models.IntegerField(default=0)
    #view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='blog/', blank=True, null=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('blog:post_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('blog:post_delete', kwargs={'slug': self.slug})

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()


""" SIGN UP MODEL FOR EMAILSUBSCRIBTION"""


class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

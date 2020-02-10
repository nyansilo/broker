import sweetify
from .models import Signup
from .models import Post, Author
from django.shortcuts import render
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.conf import settings
# from django.contrib.sessions.middleware import SessionMiddleware

from datetime import datetime
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Post, Author, PostView
# from marketing.forms import EmailSignupForm

# form = EmailSignupForm()

from easy_timezones.utils import get_ip_address_from_request, is_valid_ip, is_local_ip


""" /////////BLOG FUNCTION BASED IMPLEMENTATION ////////"""

#----------------------------SUPPORTING FUNCTIONS-------------------------------#


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

#----------------------------POST SEARCH-------------------------------#


def post_search(request):
    title = 'Search Post'
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(categories__title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    paginator = Paginator(queryset, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    postlatest = Post.objects.order_by('-timestamp')[0:3]

    context = {
        'title': title,
        'post_search': queryset,
        'post_latest': postlatest,
        'page_request_var': page_request_var,
    }

    template = 'blog/post-search.html'
    return render(request, template, context)

#----------------------------USER POST-------------------------------#


def user_post(request):
    title = 'My Posts'
    # featured = Post.objects.filter(featured=True)
    category_count = get_category_count()
    postlist = Post.objects.all()
    paginator = Paginator(postlist, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        postlist = paginator.page(page)
    except PageNotAnInteger:
        postlist = paginator.page(1)
    except EmptyPage:
        postlist = paginator.page(paginator.num_pages)

    template = 'blog/my-post.html'
    context = {
        'title': title,
        'post_list': postlist,
        'page_request_var': page_request_var,
        'category_count': category_count

    }
    return render(request, template, context)


#----------------------------BLOG LIST-------------------------------#
def blog_list(request):
    title = 'Blog Post'
    # featured = Post.objects.filter(featured=True)
    category_count = get_category_count()
    postlist = Post.objects.all()
    postlatest = Post.objects.order_by('-timestamp')[0:3]
    paginator = Paginator(postlist, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        postlist = paginator.page(page)
    except PageNotAnInteger:
        postlist = paginator.page(1)
    except EmptyPage:
        postlist = paginator.page(paginator.num_pages)

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    template = 'blog/post.html'
    context = {
        'title': title,
        'post_list': postlist,
        'post_latest': postlatest,
        'page_request_var': page_request_var,
        'category_count': category_count
        # 'form': form
    }

    return render(request, template, context)

#----------------------------POST DETAILS-------------------------------#


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ip_address_from_request(request):
    """ Makes the best attempt to get the client's real IP or return the loopback """
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = '127.0.0.1'
    return ip_address


def post_detail(request, slug):
    title = 'Post Detail'
    category_count = get_category_count()
    postlatest = Post.objects.order_by('-timestamp')[0:3]
    postrelated = Post.objects.order_by('-categories')[0:2]
    postdetail = get_object_or_404(Post, slug=slug)

    # if request.user.is_authenticated:
    # PostView.objects.get_or_create(user=request.user, post=postdetail)

    # if not request.session.exists(request.session.session_key):
    #    request.session.create()

    # ip = get_client_ip(request)
    ip = get_ip_address_from_request(request)
    PostView.objects.get_or_create(post=postdetail, ip=ip, created=datetime.now(
    ), session=request.session.session_key)

    # PostView.objects.get_or_create(post=postdetail, ip=request.META['REMOTE_ADDR'], created=datetime.now(
    # ), session=request.session.session_key)

    # PostView.objects.get_or_create(post=postdetail, ip=request.ip, user=request.user)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = postdetail
            form.save()
            return redirect(reverse("blog:post_detail", kwargs={
                'slug': postdetail.slug
            }))
    context = {
        'title': title,
        'form': form,
        'post_detail': postdetail,
        'post_latest': postlatest,
        'post_related': postrelated,
        'category_count': category_count
    }

    template = 'blog/post-detail.html'
    return render(request, template, context)

#----------------------------CREATE POST-------------------------------#


def post_create(request):
    title = 'Create Post'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            # return redirect(reverse("blog:post_detail", kwargs={'id': form.instance.id}))
            return redirect(reverse("blog:user_post"))
    context = {
        'title': title,
        'form': form
    }

    template = 'blog/post_create.html'
    return render(request, template, context)

#----------------------------UPDATE POST-------------------------------#


def post_update(request, slug):
    title = 'Update Post'
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            sweetify.warning(
                request,
                icon='warning',
                title='Post Sucessfully Updated',
                showCancelButton='true',
                confirmButtonColor='#3085d6',
                cancelButtonColor='#d33',
                confirmButtonText='Yes, delete it!',
                showConfirmButton='False',
                timer=6000
            )
            # return redirect(reverse("blog:post_detail", kwargs={'id': form.instance.id}))
            return redirect(reverse("blog:user_post"))
    context = {
        'title': title,
        'form': form
    }
    template = 'blog/post_create.html'
    return render(request, template, context)


def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect(reverse("blog:user_post"))


""" /////////BLOG CLASS BASED VIEW IMPLEMENTATION ////////"""


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
        }
        return render(request, 'search_results.html', context)


class IndexView(View):
    #form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        context = {
            'object_list': featured,
            'latest': latest,
            'form': self.form
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")


class PostListView(ListView):
    #form = EmailSignupForm()
    model = Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'

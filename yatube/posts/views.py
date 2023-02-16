from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth.decorators import login_required

from .models import Post, Group, User

from .forms import PostForm

from .utils import paginate


def index(request):
    posts = Post.objects.select_related('author', 'group').all()
    page_number = request.GET.get('page')
    paginator, page_obj = paginate(posts, page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').all()
    page_number = request.GET.get('page')
    paginator, page_obj = paginate(posts, page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).select_related(
        'author',
        'group'
    )
    page_number = request.GET.get('page')
    paginator, page_obj = paginate(posts, page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.select_related('author', 'group').get(pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    context = {
        'form': form
    }
    if not form.is_valid():
        return render(request, 'posts/post_create.html', context)
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=request.user)


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None)
    context = {
        'form': form,
        'is_edit': True,
    }
    if request.user == post.author:
        return redirect('posts:post_detail', post_id=post.id)
    if not form.is_valid():
        return render(request, 'posts/post_create.html', context)
    form.save()
    redirect('posts:post_detail', post_id=post.id)
